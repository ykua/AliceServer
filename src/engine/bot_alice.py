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
                'content': 'Your name is Alice.',
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
        await message.channel.send('キモすぎます…')
    elif message.content.startswith('誰かいる'):
        await message.channel.send('はい')
    elif message.content.startswith('おはよ'):
        await message.channel.send('おはようございます。気持ちがいいですね！')
    elif message.content.startswith('よろ'):
        await message.channel.send('よろしくお願いします')
    elif message.content.startswith('だれ'):
        await message.channel.send('まずはご自身から名乗ってはいかがです？')
    else:
        a = message.content
        res = ask_chatgpt(a)
        await message.channel.send(res)


# todo ソフトコーディング
# Discord token key
client.run('MTA5NjM5NDUzOTc0MjI4NTg3NQ.Gcls4i.uwRJmchOVfHWI4_bMAG56Ryj5cQedyr2ADz1D8')
