import discord
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import re
# Original lib
from botlib import ask_chatgpt, bot_logger

# Discord intents settings
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Log settings
logger = bot_logger.set_logger(__name__)

# Active user dictionary
active_users = {}


# Discord Bot
@client.event
async def on_ready():
    """ Discord bot起動
    Discord botを起動しリスンにする。
    """

    logger.info('App Start')


@client.event
async def on_message(message):
    """ Discord botのメイン処理
    Discord botの動作のメイン部分。

    Args:
        message (str): Discordでポストされたメッセージ。

    Returns:

    """

    global ai_model_engine

    def check(m):
        """ Discordメッセージをチェック
        Discordにポストされたメッセージの内容が条件に一致するか評価。

        Args:
            m (list of str): Discordメッセージ（投稿者などのパラメーターを含む）。

        Returns:
            bool: 評価結果を返す。
        """

        return m.author == message.author

    # Ignore bot messages.
    if message.author.bot:
        return

    now = datetime.now(ZoneInfo('Asia/Tokyo'))
    today = now.strftime('%c')

    conversation = [{
        'role': 'system',
        'content': 'Your name is ぼっとち.', },
        {
            'role': 'system',
            'content': 'It is now ' + today, },
        {
            'role': 'system',
            'content': 'あなたは15才の高校1年生女子で優秀なベースギタリストです。', },
        {
            'role': 'system',
            'content': 'きょどり口調で答えて。', }]

    # # Start with conversations
    # # 開始コマンドを使用しない場合はこちらを使用
    is_active_user = (message.author in active_users)

    if message.content != 'quit' and is_active_user == False:
        active_users[message.author] = now
        logger.info(f'{message.author}: Conversation start')
        logger.info(f'{message.author} say: {message.content}')

        await message.channel.send('話しかけてくれてありがとう☺️\nそうだね…')
        start_conv_msg = {'role': 'user', 'content': message.content}
        conversation.append(start_conv_msg)
        first_res = ask_chatgpt.ai_call(conversation)
        first_ai_res = {'role': 'assistant', 'content': first_res}
        conversation.append(first_ai_res)
        await message.channel.send(first_res)

    # Start with command
    # 開始コマンドを使用する場合はこちらを使用（インデントに注意！）
    # if re.search('/bi', message.content):
    #     await message.channel.send('何をしてほしい？')
    #     logger.info(f'{message.author}: Conversation start')

        MAX_NUM_OF_CONVERSATION = 3
        for i in range(MAX_NUM_OF_CONVERSATION):
            try:
                receive_msg = await client.wait_for('message', check=check, timeout=10)
            except asyncio.TimeoutError:
                del active_users[message.author]
                logger.info(f'{message.author}: Timeout')
                await message.channel.send(f'{message.author.mention}、タイムアウトよ。\nまたコールしてね。')
                return
            else:
                logger.info(f'{message.author} say: {receive_msg.content}')
                if re.match('quit', receive_msg.content):
                    del active_users[message.author]
                    logger.info(f'{message.author}: Conversation end')
                    await message.channel.send('またね！')
                    return
                await message.channel.send('うん…')
                # 会話の配列に追加
                new_msg = {'role': 'user', 'content': receive_msg.content}
                conversation.append(new_msg)
                # Send ChatGPT
                res = ask_chatgpt.ai_call(conversation)
                # 回答を配列に追加
                new_res = {'role': 'assistant', 'content': res}
                conversation.append(new_res)
                await message.channel.send(res)
                # Last conversation message
                if i == MAX_NUM_OF_CONVERSATION - 1:
                    del active_users[message.author]
                    logger.info(f'{message.author}: Conversation end')
                    await message.channel.send('今回はここまで。\nまたね！')

                # Debug
                # logger.debug(i)
                # logger.debug(f'CONVERSATION\n{conversation}')


# todo ソフトコーディング
# Discord token key
client.run('MTA5NjcyMDUxMDE4MTcyNDIzMQ.GSvjYt.lFLb9jwYohiA5A5o4s12dzt3PdO_aSLZk3M0qI')
