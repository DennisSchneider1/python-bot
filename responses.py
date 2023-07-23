import llmApi

def get_response_for_user_input(user_name:str, message: str) -> str:
    if message.endswith('!debug'):
        return message

    response = str(llmApi.llm_respond_creative_user(user_name=user_name, user_input=message))
    if len(response) >=1:
        return response
    
    return 'no response'

def get_response(message: str) -> str:
    response = str(llmApi.llm_respond_creative(user_input=message))
    if len(response) >=1:
        return response
    
    return 'no response'