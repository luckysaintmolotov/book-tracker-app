from datetime import datetime
def update_log(message):
    """Function to update the log file with a message"""
    with open('logs/book_logs.txt', 'a') as log_file:
        log_file.write(f"{message}-{datetime.now()}\n")
    print(f"Log updated: {message}")
    
    
