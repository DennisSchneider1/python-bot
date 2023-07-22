import llmApi

def get_response(message: str) -> str:
    response = str(llmApi.llm_respond(message))
    if len(response) >=1:
        return response
    
    return 'no response'