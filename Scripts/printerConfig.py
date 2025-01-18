import cups

class PrinterManagerUnix:
    _instance = None  # This will hold the single instance of PrinterManagerUnix

    def __new__(cls):
        # Create the instance only once; otherwise, return the existing one
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = None  # Initialize connection as None initially
        return cls._instance

    def _get_connection(self):
        """Initialize connection lazily when needed."""
        if self._conn is None:
            self._conn = cups.Connection()  # Create connection only when needed
        return self._conn

    def get_connected_printers(self):
        """Get the list of connected printers."""
        conn = self._get_connection()  # Lazily initialize connection if necessary
        return list(conn.getPrinters().keys())

    def print_file(self, file_name, printer_name):
        """Send a file to the specified printer."""
        conn = self._get_connection()  # Lazily initialize connection if necessary
        printers = conn.getPrinters()

        if printer_name not in printers:
            print(f"Error: Printer '{printer_name}' not found.")
            return

        try:
            print_job_id = conn.printFile(printer_name, file_name, "Print Job", {})
            print(f"File sent to printer '{printer_name}' with Job ID: {print_job_id}")
        except Exception as e:
            print(f"Error printing file: {e}")


# Example Usage
#if __name__ == "__main__":
#    # Create an instance of the PrinterManagerUnix class
#    printer_manager = PrinterManagerUnix()
#
#    # Get the list of connected printers (lazily initialized)
#    connected_printers = printer_manager.get_connected_printers()
#    print("Connected printers:", connected_printers)
#
#    # Check if there are any printers available before attempting to print
#    if connected_printers:
#        file_name = "referenceMaterial/1.pdf"  # Replace with your file path
#        printer_name = connected_printers[0]  # Choose the first available printer
#        printer_manager.print_file(file_name, printer_name)
#    else:
#        print("No printers available.")