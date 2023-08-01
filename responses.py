import llmApiStream
import llmApi

def get_response_stream(character_name:str, user_name:str, message:str):
    return llmApiStream.llm_respond_creative_user(character_name=character_name, user_name=user_name, user_input=message)

def get_response(character_name:str, message:str) -> str:
    response = str(llmApi.llm_respond_creative(character_name=character_name, user_input=message))
    if len(response) >=1:
        return response
    return '...'