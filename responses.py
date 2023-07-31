import llmApiStream
import llmApi

def get_response_stream(user_name:str, message: str) -> str:
    return llmApiStream.llm_respond_creative_user(user_name=user_name, user_input=message)

def get_response(message: str) -> str:
    response = str(llmApi.llm_respond_creative(user_input=message))
    if len(response) >=1:
        return response
    
    return '...'