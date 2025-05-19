# from PySide6.QtWidgets import QApplication
# import sys
# import time
# from Scripts.hardware import ESPHardware
#
#
# def main():
#     # Create QApplication instance (required for QThread)
#     app = QApplication(sys.argv)
#
#     # Create hardware interface - this will automatically try to connect
#     print("Initializing ESP hardware...")
#     esp = ESPHardware()
#
#     # Wait a moment for connection
#     time.sleep(2)
#
#     # Test all functions
#     print("\n--- Testing ESP Functions ---")
#
#     # Get resistance
#     print("\nGetting resistance measurement...")
#     resistance = esp.get_resistance()
#     print(f"Resistance: {resistance} ohms")
#
#     # Get frequency
#     print("\nGetting frequency measurement...")
#     frequency = esp.get_frequency()
#     print(f"Frequency: {frequency} Hz")
#
#     # Get voltage
#     print("\nGetting voltage measurement...")
#     voltage = esp.get_voltage()
#     print(f"Voltage: {voltage} V")
#
#     # Test emergency stop
#     print("\nTesting emergency stop...")
#     esp.emergency_stop()
#     print("Emergency stop activated")
#
#     # Try reconnecting
#     print("\nReconnecting...")
#     esp.auto_connect()
#
#     print("\nAll tests completed")
#
#     # Need to explicitly wait for thread completion before exiting
#     if esp.comm_thread and esp.comm_thread.isRunning():
#         print("Waiting for communication thread to finish...")
#         esp.comm_thread.stop()
#         esp.comm_thread.wait()
#
#     # Clean up and exit
#     del esp
#     sys.exit(0)
#
#
# if __name__ == "__main__":
#     main()
from Scripts.resultMaster import ResultMaster
x = (int(f"{(ResultMaster.getlastTCno("1235-Twintech") + 1):07d}"))
print((x))