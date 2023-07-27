import discord
import responses

chat_history = '' # replace with dict
processing_message = False
CHARACTER_NAME = 'Shion'

async def send_message(message, user_message):
    global processing_message
    if processing_message:
        await message.channel.send('I\'m currently busy, sorry')
        return
    else:
        processing_message = True

    try:
        #only read and append to history
        global chat_history
        chat_history += str(message.author) + ': ' + user_message + '\n'

        cur_len = 0
        response_message = ''
        response_message_obj = None
        start_of_message_sent = False
        async for new_history in responses.get_response_stream(str(message.author), chat_history):
            cur_response_message = new_history[cur_len:]
            cur_len += len(cur_response_message)
            response_message += cur_response_message

            if not start_of_message_sent and str(cur_response_message).endswith('.') and len(response_message) > 100:
                response_message_obj = await message.channel.send(response_message)
                start_of_message_sent = True
            elif start_of_message_sent and str(cur_response_message).endswith('.'):
                await response_message_obj.edit(content=response_message)

        if not start_of_message_sent:
            response_message_obj = await message.channel.send(response_message)
        else:
            await response_message_obj.edit(content=response_message)

        # save full history
        chat_history += CHARACTER_NAME + ': ' + response_message + '\n'

    except Exception as e:
        print(e)     

    processing_message = False

def run_discord_bot():
    # get API Token
    token_file = open("token.txt", "r")
    TOKEN = token_file.read()
    token_file.close()

    # set intent permissions to allow reading messages
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

        # set bot status with llm
        generate_status_prompt = 'I\'m Shion. I\'ve been thinking of a funny discord status and I think i\'ll set it to: '
        status_message = responses.get_response(generate_status_prompt)
        game_status = discord.Game(status_message)
        await client.change_presence(status=discord.Status.idle, activity=game_status)
        print('bot status is set')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f'{username} said: "{user_message}" in ({channel})')

        async with message.channel.typing():
            await send_message(message, user_message)

    client.run(TOKEN)