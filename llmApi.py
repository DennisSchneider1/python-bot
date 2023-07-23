import json

import requests

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/chat'
CHARACTER_NAME = 'Shion'
TIMEOUT_SECONDS = 120

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/chat'

def run(user_name:str, user_input:str, preset:str):
    request = {
        'user_input': user_input,
        'max_new_tokens': 500,
        'mode': 'chat',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        'character': CHARACTER_NAME,
        'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
        # 'context_instruct': '',  # Optional
        'your_name': user_name,

        'regenerate': False,
        '_continue': False,
        'stop_at_newline': False,
        'chat_generation_attempts': 1,
        'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': preset,
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    print('wait for api response ...')
    response = requests.post(URI, json=request, timeout=TIMEOUT_SECONDS)

    if response.status_code == 200:
        result = response.json()['results'][0]['history']
        # print(response.json()['results'])
        # print(json.dumps(result, indent=4))
        # print(result['visible'][-1][1])
        return str(result['visible'][-1][1])
    
    return 'no response'


def llm_respond_user(user_name:str, user_input:str) -> str:
    return run(user_name, user_input + CHARACTER_NAME + ': ', 'Yara')

def llm_respond_creative_user(user_name:str, user_input:str) -> str:
    return run(user_name, user_input + CHARACTER_NAME + ': ', 'simple-1')

def llm_respond_creative(user_input:str) -> str:
    return run('USER', user_input, 'simple-1')