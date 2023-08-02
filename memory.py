import llmApi

HISTORY_BUFFER_LENGTH = 2500
SUMMARY_BUFFER_LENGTH = 1500
SUMMARIZE_PROMPT_INIT = 'USER: Please provide me with a summary of the current conversation we had. Make sure not to miss any important details.\nASSISTANT: '
# HISTORY_PROMPT_INIT = '\n### START OF CONVERSATION: \n'

class Memory:
    def __init__(self):
        self.history = [] #init history from file here
        self.summarized_history = ''
        self.status = ''

    def get_memory(self) -> str:
        return self.summarized_history + self.historyToString() + '\n'

    def summarize_summary(self):
        # request reponse from llm
        response_message = llmApi.llm_respond_creative('Shion', self.summarized_history + SUMMARIZE_PROMPT_INIT)
        self.summarized_history = response_message
        print(f'Summarized. Current summary is: {self.summarized_history}')

    def generate_status(self):
        self.status = ''

    def add_memory(self, message_user:str, message_bot: str):
        self.history.append([message_user, message_bot])
        #manage history length
        while len(self.historyToString()) > HISTORY_BUFFER_LENGTH:
            old_history = self.history.pop(0)
            self.summarized_history += '\n'.join(map(str,old_history))
        #manage summary length
        if len(self.summarized_history) > SUMMARY_BUFFER_LENGTH:
            self.summarize_summary()

        #save history to file here

    def historyToString(self):
        flat_list = [item for sublist in self.history for item in sublist]
        return '\n'.join(map(str,flat_list))