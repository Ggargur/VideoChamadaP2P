LOG_LEVEL = 0


def log(message: str, message_log_level=0):
    global LOG_LEVEL
    if message_log_level <= LOG_LEVEL:
        print(message)
