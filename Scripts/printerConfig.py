import cups

class PrinterManagerUnix:
    @staticmethod
    def get_connected_printers():
        # Create a connection to the CUPS server
        printers = cups.Connection().getPrinters()
        
        # Return the list of printer names
        return list(printers.keys())

    @staticmethod
    def print_file(file_name, printer_name):
        # Create a connection to the CUPS server
        conn = cups.Connection()
        
        # Check if the printer exists
        printers = conn.getPrinters()
        if printer_name not in printers:
            print(f"Error: Printer '{printer_name}' not found.")
            return
        
        # Print the file
        try:
            # Send the print job to the specified printer
            print_job_id = conn.printFile(printer_name, file_name, "Print Job", {})
            print(f"File sent to printer '{printer_name}' with Job ID: {print_job_id}")
        except Exception as e:
            print(f"Error printing file: {e}")


# Get the list of connected printers (optional)
#connected_printers = PrinterManagerUnix.get_connected_printers()
#print("Connected printers:", connected_printers)

# Define the file name and printer
#file_name = "refrenceMaterial/1.pdf"  # Replace with your file path
#printer_name = connected_printers[0] # Replace with your printer name

# Print the file on the specified printer
#PrinterManagerUnix.print_file(file_name, printer_name)
