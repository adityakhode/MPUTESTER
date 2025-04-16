import serial
import serial.tools.list_ports
import time
from PySide6.QtCore import QThread, Signal, QObject, QMutex, QWaitCondition


class ESPCommunicationThread(QThread):
    resistance_signal = Signal(float)
    frequency_signal = Signal(float)
    voltage_signal = Signal(float)
    error_signal = Signal(str)
    connection_signal = Signal(bool, str)

    def __init__(self, port=None, baud_rate=9600):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self._is_running = False
        self._serial_connection = None
        self.command_queue = []
        self.emergency_stop_flag = False

        # For thread synchronization
        self.mutex = QMutex()
        self.condition = QWaitCondition()

    def run(self):
        try:
            if not self.port:
                self.error_signal.emit("No port specified")
                return

            self._serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Wait for ESP to initialize
            self._is_running = True
            self.connection_signal.emit(True, self.port)

            while self._is_running and not self.emergency_stop_flag:
                self.mutex.lock()
                if not self.command_queue:
                    # Wait for commands or stop signal
                    self.condition.wait(self.mutex, 100)  # Wait up to 100ms

                # Get command if available
                command = None
                if self.command_queue:
                    command = self.command_queue.pop(0)
                self.mutex.unlock()

                # Process command if we have one
                if command:
                    self._send_command(command)

                # Small sleep to prevent CPU overuse
                time.sleep(0.01)

        except Exception as e:
            self.error_signal.emit(f"Thread error: {str(e)}")
            self.connection_signal.emit(False, self.port)
        finally:
            self._is_running = False
            if self._serial_connection and self._serial_connection.is_open:
                self._serial_connection.close()

    def _send_command(self, command):
        try:
            if not self._serial_connection or not self._serial_connection.is_open:
                self.error_signal.emit("Serial connection not established")
                return

            # Clear any pending data
            self._serial_connection.reset_input_buffer()

            # Send command
            print(f"Sending command: {command}")
            self._serial_connection.write(f"{command}\n".encode())

            # Wait for response with timeout
            timeout = time.time() + 2.0  # 2 second timeout
            while time.time() < timeout:
                if self._serial_connection.in_waiting:
                    response = self._serial_connection.readline().decode().strip()
                    print(f"Received response: {response}")
                    self._process_response(command, response)
                    return
                time.sleep(0.1)

            # If we get here, we timed out waiting for response
            self.error_signal.emit(f"Timeout waiting for response to {command}")

        except Exception as e:
            self.error_signal.emit(f"Command error: {str(e)}")

    def _process_response(self, command, response):
        try:
            if "ERROR" in response:
                self.error_signal.emit(response)
                return

            if command == "GET_RESISTANCE":
                resistance = float(response)
                self.resistance_signal.emit(resistance)
            elif command == "GET_FREQUENCY":
                frequency = float(response)
                self.frequency_signal.emit(frequency)
            elif command == "GET_VOLTAGE":
                voltage = float(response)
                self.voltage_signal.emit(voltage)
        except ValueError as e:
            self.error_signal.emit(f"Invalid response format: {response} - {str(e)}")

    def add_command(self, command):
        if not self.emergency_stop_flag:
            self.mutex.lock()
            self.command_queue.append(command)
            self.condition.wakeAll()
            self.mutex.unlock()

    def stop(self):
        self.mutex.lock()
        self._is_running = False
        self.condition.wakeAll()
        self.mutex.unlock()


class ESPHardware(QObject):
    def __init__(self):
        super().__init__()
        self.comm_thread = None
        self.available_ports = []
        self.connected_port = None
        self.esp_serial = None

        # For synchronous access to measurement values
        self.resistance_value = None
        self.frequency_value = None
        self.voltage_value = None

        # Mutex for measurement data protection
        self.data_mutex = QMutex()
        self.data_received = QWaitCondition()

        # Auto-connect on initialization
        self.auto_connect()

    def find_esp_device(self):
        """Find the ESP device connected via USB."""
        # Common ESP8266/ESP32 USB-to-Serial adapter identifiers
        esp_identifiers = ['CP210x', 'CH340', 'FTDI', 'Silicon Labs', 'Espressif', 'USB-SERIAL']

        available_ports = list(serial.tools.list_ports.comports())
        self.available_ports = []

        # Filter out ttyS ports which are usually system serial ports, not ESP devices
        filtered_ports = [port for port in available_ports if not (
                port.device.startswith('/dev/ttyS') or
                (port.description == 'n/a' and 'ttyS' in port.device)
        )]

        if not filtered_ports:
            filtered_ports = available_ports  # Fallback to all ports if we filtered everything

        for port in filtered_ports:
            port_info = f"{port.device} - {port.description}"
            print(f"Found port: {port_info}")

            # Check if any of the ESP identifiers is in the port description
            for identifier in esp_identifiers:
                if (identifier.lower() in port.description.lower() or
                        (port.manufacturer and identifier.lower() in port.manufacturer.lower())):
                    print(f"ESP device found on port: {port.device}")
                    self.available_ports.append(port.device)
                    break  # Break the inner loop once we've identified a port

        # If no specific ESP identifier found, try to find any likely candidates
        if not self.available_ports and filtered_ports:
            for port in filtered_ports:
                # For Linux systems, ttyUSB and ttyACM are common for ESP devices
                if 'ttyUSB' in port.device or 'ttyACM' in port.device:
                    print(f"Possible ESP device found on port: {port.device}")
                    self.available_ports.append(port.device)
                # For Windows, look for COM ports
                elif 'COM' in port.device:
                    print(f"Possible ESP device found on port: {port.device}")
                    self.available_ports.append(port.device)

        if not self.available_ports:
            print("No ESP device found")
            return None

        return self.available_ports[0]  # Return the first found ESP device

    def connect_to_esp(self, port):
        """Connect to the ESP device."""
        if port:
            try:
                # Close existing connection if any
                if self.esp_serial and self.esp_serial.is_open:
                    self.esp_serial.close()
                    self.esp_serial = None
                    time.sleep(0.5)  # Brief pause before reconnecting

                # Note: Your ESP code uses 9600 baud rate
                self.esp_serial = serial.Serial(
                    port=port,
                    baudrate=9600,
                    timeout=2
                )
                print(f"Connected to ESP on port {port}")

                # Give the ESP more time to stabilize after connection
                time.sleep(2)  # Increased from 1 to 2 seconds

                # Clear any pending data more thoroughly
                self.esp_serial.reset_input_buffer()
                self.esp_serial.reset_output_buffer()

                # Send a dummy command to initialize communication
                self.esp_serial.write(b"\n")
                time.sleep(0.5)  # Wait for ESP to process
                self.esp_serial.reset_input_buffer()  # Clear the response

                return True
            except Exception as e:
                print(f"Error connecting to ESP: {e}")
                self.esp_serial = None
                return False
        else:
            print("No ESP device found to connect")
            return False

    def auto_connect(self):
        """Automatically connect to the first available ESP port"""
        esp_port = self.find_esp_device()

        if not esp_port:
            print("No ESP devices found")
            return False

        # Try to establish initial connection
        if not self.connect_to_esp(esp_port):
            # Try other ports if available
            for port in self.available_ports[1:]:
                if self.connect_to_esp(port):
                    esp_port = port
                    break
            else:
                print("Failed to connect to any ESP device")
                return False

        # Now create the communication thread with the established connection
        self._start_communication_thread(esp_port)
        return True

    def _start_communication_thread(self, port):
        """Start the communication thread with the ESP"""
        # Clean up existing thread properly
        if self.comm_thread:
            if self.comm_thread.isRunning():
                self.comm_thread.stop()
                self.comm_thread.wait(2000)  # Wait up to 2 seconds

        # Create new thread
        self.comm_thread = ESPCommunicationThread(port, 9600)

        # Set up callbacks
        self.comm_thread.resistance_signal.connect(self._update_resistance)
        self.comm_thread.frequency_signal.connect(self._update_frequency)
        self.comm_thread.voltage_signal.connect(self._update_voltage)
        self.comm_thread.error_signal.connect(self._handle_error)
        self.comm_thread.connection_signal.connect(self._handle_connection)

        # Start thread
        self.comm_thread.start()
        self.connected_port = port

        print(f"Successfully established communication thread with ESP on port {self.connected_port}")

    def get_resistance(self):
        """Get resistance measurement from ESP"""
        if not self._check_connection():
            return None

        # Reset the value before requesting new data
        self.data_mutex.lock()
        self.resistance_value = None
        self.data_mutex.unlock()

        # Send command to ESP
        self.comm_thread.add_command("GET_RESISTANCE")

        # Wait for response with timeout
        start_time = time.time()
        timeout = 3.0  # 3 seconds timeout

        while time.time() - start_time < timeout:
            self.data_mutex.lock()
            if self.resistance_value is not None:
                result = self.resistance_value
                self.resistance_value = None  # Reset for next measurement
                self.data_mutex.unlock()
                return result
            self.data_mutex.unlock()
            time.sleep(0.1)

        print("Timeout waiting for resistance value")
        return None

    def get_frequency(self):
        """Get frequency measurement from ESP"""
        if not self._check_connection():
            return None

        # Reset the value before requesting new data
        self.data_mutex.lock()
        self.frequency_value = None
        self.data_mutex.unlock()

        # Send command to ESP
        self.comm_thread.add_command("GET_FREQUENCY")

        # Wait for response with timeout
        start_time = time.time()
        timeout = 3.0  # 3 seconds timeout

        while time.time() - start_time < timeout:
            self.data_mutex.lock()
            if self.frequency_value is not None:
                result = self.frequency_value
                self.frequency_value = None  # Reset for next measurement
                self.data_mutex.unlock()
                return result
            self.data_mutex.unlock()
            time.sleep(0.1)

        print("Timeout waiting for frequency value")
        return None

    def get_voltage(self):
        """Get voltage measurement from ESP"""
        if not self._check_connection():
            return None

        # Reset the value before requesting new data
        self.data_mutex.lock()
        self.voltage_value = None
        self.data_mutex.unlock()

        # Send command to ESP
        self.comm_thread.add_command("GET_VOLTAGE")

        # Wait for response with timeout
        start_time = time.time()
        timeout = 3.0  # 3 seconds timeout

        while time.time() - start_time < timeout:
            self.data_mutex.lock()
            if self.voltage_value is not None:
                result = self.voltage_value
                self.voltage_value = None  # Reset for next measurement
                self.data_mutex.unlock()
                return result
            self.data_mutex.unlock()
            time.sleep(0.1)

        print("Timeout waiting for voltage value")
        return None

    def emergency_stop(self):
        """Emergency stop all operations"""
        if not self.comm_thread:
            return False

        try:
            # Send emergency stop command to ESP
            if self.esp_serial and self.esp_serial.is_open:
                self.esp_serial.write("EMERGENCY_STOP\n".encode())
                time.sleep(0.5)

            # Stop thread properly
            if self.comm_thread.isRunning():
                self.comm_thread.stop()
                # Wait briefly for thread to finish, but don't block indefinitely
                self.comm_thread.wait(1000)  # Wait up to 1 second

            self.connected_port = None
            return True
        except Exception as e:
            print(f"Error during emergency stop: {e}")
            return False

    def _check_connection(self):
        """Check if ESP is connected, try to reconnect if not"""
        if not self.comm_thread or not self.comm_thread.isRunning() or not self.connected_port:
            # Try to reconnect
            print("Connection lost, attempting to reconnect...")
            return self.auto_connect()
        return True

    def _update_resistance(self, value):
        """Update the stored resistance value"""
        self.data_mutex.lock()
        self.resistance_value = value
        self.data_mutex.unlock()

    def _update_frequency(self, value):
        """Update the stored frequency value"""
        self.data_mutex.lock()
        self.frequency_value = value
        self.data_mutex.unlock()

    def _update_voltage(self, value):
        """Update the stored voltage value"""
        self.data_mutex.lock()
        self.voltage_value = value
        self.data_mutex.unlock()

    def _handle_error(self, error_message):
        """Handle error messages from ESP"""
        print(f"ESP Error: {error_message}")

    def _handle_connection(self, connected, port):
        """Handle connection status changes"""
        if connected:
            self.connected_port = port
        else:
            self.connected_port = None
            # Try to connect to another port
            if not self.auto_connect():
                print("No ESP devices available")

    def __del__(self):
        """Clean up resources when object is destroyed"""
        self.emergency_stop()
        if self.comm_thread and self.comm_thread.isRunning():
            self.comm_thread.stop()
            self.comm_thread.wait(2000)  # Wait up to 2 seconds for thread to stop