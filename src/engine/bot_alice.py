import discord
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import re
import yaml
import random
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

# Setting import
file_path = 'conf/bot_conf.yml'
with open(file_path, 'r') as f:
    settings = yaml.load(f, Loader=yaml.SafeLoader)
QUIT_PROMPT = settings['settings']['quit_prompt']
CONV_TIMEOUT = settings['settings']['conversation_timeout']
MAX_NUM_OF_CONVERSATION = settings['settings']['max_num_of_conversation']
START_MSG = settings['conversation']['start_msg']
TIMEOUT_MSG = settings['conversation']['timeout_msg']
BYE_MSG = settings['conversation']['bye_msg']
QUIT_MSG = settings['conversation']['quit_msg']
APP_START_LOG_MSG = settings['log_msg']['app_start']
CONV_START_LOG_MSG = settings['log_msg']['conv_start']
CONV_TIMEOUT_LOG_MSG = settings['log_msg']['conv_timeout']
CONV_END_LOG_MSG = settings['log_msg']['conv_end']
FILLER_WORDS = settings['filler']
SYS_CONV = settings['system_conv']
AI_EER = settings['error_msg']['ai_err']
AI_EER_MSG = settings['conversation']['ai_err_msg']
DISCORD_ERR = settings['error_msg']['discord_err']
DISCORD_EER_MSG = settings['conversation']['discord_err_msg']


# Discord Bot
@client.event
async def on_ready():
    """ Discord bot起動
    Discord botを起動しリスンにする。
    """
    logger.info(APP_START_LOG_MSG)


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

    # Create initial conversation.
    now = datetime.now(ZoneInfo('Asia/Tokyo'))
    today = now.strftime('%c')
    today_info = {'role': 'system', 'content': 'It is now ' + today}
    conversation = []
    conversation.extend(SYS_CONV)
    conversation.append(today_info)

    # # 開始コマンドを使用しない場合はこちらを使用
    is_active_user = (message.author in active_users)
    if message.content != QUIT_PROMPT and is_active_user == False:
        active_users[message.author] = now
        logger.info(f'{message.author}: {CONV_START_LOG_MSG}')
        logger.info(f'{message.author} say: {message.content}')
        await message.channel.send(START_MSG)

        start_conv_msg = {'role': 'user', 'content': message.content}
        conversation.append(start_conv_msg)
        async with message.channel.typing():
            first_res = ask_chatgpt.ai_call(conversation)
        # Error handling from ChatGPT
        if first_res[0] == 1:
            del active_users[message.author]
            await message.channel.send(AI_EER_MSG)
            logger.info(f'{AI_EER}')
            logger.error(f'{AI_EER}: {first_res[1]}')
            return
        first_ai_res = {'role': 'assistant', 'content': first_res[1]}
        conversation.append(first_ai_res)
        try:
            await message.channel.send(first_res[1])
        except Exception as e:
            del active_users[message.author]
            logger.info(f'{DISCORD_ERR}')
            logger.error(f'{DISCORD_ERR}: {e}')
            await message.channel.send(f'{DISCORD_EER_MSG}')
            return

        # Start with command
        # 開始コマンドを使用する場合はこちらを使用（インデントに注意！）
        # if re.search('/bi', message.content):
        #     await message.channel.send('何をしてほしい？')
        #     logger.info(f'{message.author}: {CONV_START_LOG_MSG}')

        for i in range(MAX_NUM_OF_CONVERSATION):
            try:
                receive_msg = await client.wait_for('message', check=check, timeout=CONV_TIMEOUT)
            except asyncio.TimeoutError:
                del active_users[message.author]
                logger.info(f'{message.author}: {CONV_TIMEOUT_LOG_MSG}')
                await message.channel.send(f'{message.author.mention}、{TIMEOUT_MSG}')
                return
            else:
                logger.info(f'{message.author} say: {receive_msg.content}')
                if re.match(QUIT_PROMPT, receive_msg.content):
                    del active_users[message.author]
                    logger.info(f'{message.author}: {CONV_END_LOG_MSG}')
                    await message.channel.send(QUIT_MSG)
                    return
                await message.channel.send(random.choice(FILLER_WORDS))
                # 会話の配列に追加
                new_msg = {'role': 'user', 'content': receive_msg.content}
                conversation.append(new_msg)
                # Send ChatGPT
                async with message.channel.typing():
                    res = ask_chatgpt.ai_call(conversation)
                # Error handling from ChatGPT
                if res[0] == 1:
                    del active_users[message.author]
                    logger.info(f'{AI_EER}')
                    logger.error(f'{AI_EER}: {res[1]}')
                    await message.channel.send(AI_EER_MSG)
                    return
                # 回答を配列に追加
                new_res = {'role': 'assistant', 'content': res[1]}
                conversation.append(new_res)
                try:
                    await message.channel.send(res[1])
                except Exception as e:
                    del active_users[message.author]
                    logger.info(f'{DISCORD_ERR}')
                    logger.error(f'{AI_EER}: {e}')
                    await message.channel.send(f'{DISCORD_EER_MSG}')
                    return
                    # Last conversation message
                if i == MAX_NUM_OF_CONVERSATION - 1:
                    del active_users[message.author]
                    logger.info(f'{message.author}: {CONV_END_LOG_MSG}')
                    await message.channel.send(BYE_MSG)
                    return

                    # Debug
                # logger.debug(i)
                # logger.debug(f'A CONVERSATION\n{conversation}')
        return
    else:
        return


# todo ソフトコーディング
# Discord token key
client.run('MTA5NjcyMDUxMDE4MTcyNDIzMQ.GSvjYt.lFLb9jwYohiA5A5o4s12dzt3PdO_aSLZk3M0qI')
