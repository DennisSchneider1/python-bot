import discord
import responses
import memory

CHARACTER_NAME = 'Shion'
chat_history = memory.Memory(CHARACTER_NAME)
processing_message = False

async def send_message(message, user_message):
    #mutex to only process one message and discard all others while processing
    global processing_message
    if processing_message:
        await message.channel.send('I\'m currently busy, I\'m sorry.')
        return
    else:
        processing_message = True

    try:
        prompt = str(chat_history.get_memory()) + str(message.author) + ': ' + str(user_message) + '\n'
        cur_len_response = 0
        cur_len_discord_msg = 0
        response_message = ''
        response_discord_msg = ''
        response_message_obj = None
        start_of_message_sent = False
        # stream response from llm
        async for new_history in responses.get_response_stream(CHARACTER_NAME, str(message.author), prompt):
            cur_response_message = new_history[cur_len_response:]
            cur_len_response += len(cur_response_message)
            response_message += cur_response_message
            cur_len_discord_msg += len(cur_response_message)
            response_discord_msg += cur_response_message

            # send and update message im real time
            if not start_of_message_sent and str(cur_response_message).endswith('.') and len(response_discord_msg) > 100:
                response_message_obj = await message.channel.send(response_discord_msg)
                cur_len_discord_msg = len(response_discord_msg)
                start_of_message_sent = True
            elif start_of_message_sent and str(cur_response_message).endswith('.'):
                if cur_len_discord_msg < 1900:
                    await response_message_obj.edit(content=response_discord_msg)
                    cur_len_discord_msg = len(response_discord_msg)
                else:
                    response_discord_msg = response_discord_msg[cur_len_discord_msg:]
                    response_message_obj = await message.channel.send(response_discord_msg)
                    cur_len_discord_msg = len(response_message)

        #finish message response
        if not start_of_message_sent or len(response_discord_msg) > 1900:
            if len(response_discord_msg) < 1:
                response_discord_msg = ':heart:'
            await message.channel.send(response_discord_msg)
        else:
            await response_message_obj.edit(content=response_discord_msg)

        # save full history
        chat_history.add_memory(str(message.author) + ': ' + str(user_message), str(CHARACTER_NAME) + ': ' + str(response_message))
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
        response = responses.get_response(CHARACTER_NAME, generate_status_prompt)
        print(response)
        status_message = response.split('"')[1]
        game_status = discord.Game(status_message)
        await client.change_presence(status=discord.Status.idle, activity=game_status)
        print('bot status is set')

    @client.event
    async def on_message(message):
        #filter and prepare messages
        if message.author == client.user:
            return
        if not client.user.mentioned_in(message) and not isinstance(message.channel, discord.DMChannel):
            return
        if client.user.mentioned_in(message):
            user_message = CHARACTER_NAME + str(message.content).split('>', 1)[1]
        else:
            user_message = str(message.content)
        username = str(message.author)
        channel = str(message.channel)
        print(f'{username} said: "{user_message}" in ({channel})')

        #respond to message
        async with message.channel.typing():
            await send_message(message, user_message)

    client.run(TOKEN)