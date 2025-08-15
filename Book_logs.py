from datetime import datetime
def update_log(message):
    """Function to update the log file with a message"""
    with open('logs/book_logs', 'a') as log_file:
        log_file.write(f"{message}-{datetime.now()}\n")

# This function appends a message to the log file with a timestamp.
# It can be used to track events or errors in the application.
# The log file is named 'book_logs' and is stored in the 'logs' directory.
# Each log entry is appended with the current date and time for reference.
    
    
