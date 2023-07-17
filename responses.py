
def get_response(message: str) -> str:
    low_message = message.lower()

    if low_message == 'ping':
        return 'pong'