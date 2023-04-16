import openai
import discord

# todo 本番運用ではソフトコーディングする
# OpenAI API Settings
openai.api_key = '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'
openai.organization = 'org-fgWaYosTeNaXwPemvIQvJdq4'
ai_model_engine = 'gpt-3.5-turbo'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


# OpenAI ChatGPT
def ask_chatgpt(msg):
    completion = openai.ChatCompletion.create(
        model=ai_model_engine,
        messages=[
            {
                'role': 'system',
                'content': 'Your name is ボットち.',
            },
            {
                'role': 'user',
                'content': msg,
            },
        ],
    )
    response = completion.choices[0].message.content
    return response


# Discord Bot
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    global ai_model_engine
    if message.author.bot:
        return

    if message.content.startswith('好き'):
        # ここに処理を書く
        await message.channel.send('きもっ! キモすぎます！！')
    elif message.content.startswith('こんにち'):
        await message.channel.send('ちは')
    elif message.content.startswith('よろ'):
        await message.channel.send('よっよろしくお願いします！')
    elif message.content.startswith('だれ'):
        await message.channel.send('あー、後藤ボットちです')
    else:
        a = message.content
        res = ask_chatgpt(a)
        await message.channel.send(res)


# todo ソフトコーディング
# Discord token key
client.run('MTA5NjcyMDUxMDE4MTcyNDIzMQ.GSvjYt.lFLb9jwYohiA5A5o4s12dzt3PdO_aSLZk3M0qI')
