import llmApi

def get_response(message: str) -> str:

    # low_message = message.lower()
    # if low_message == '!help':
    #     return 'Right now I can write you a youtube video script about a topic\ntry it with: !yt (topic)'

    # if low_message.startswith('!yt '):
    #     low_message = low_message[4:]
    #     return low_message

    response = str(llmApi.llm_respond(message))
    if len(response) >=1:
        return response
    
    return 'no response'