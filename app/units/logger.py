from datetime import datetime

LOG_DATA = []

def log_event(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log = f"[{timestamp}] {message}"
    LOG_DATA.append(log)

    # keep the buffer bounded
    if len(LOG_DATA) > 200:
        LOG_DATA.pop(0)
