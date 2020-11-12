import sqlite3
import time
from typing import Tuple, List

from telethon import TelegramClient
from telethon.tl.functions.bots import SetBotCommandsRequest, SendCustomRequestRequest
from telethon.tl.functions.messages import GetInlineBotResultsRequest, GetBotCallbackAnswerRequest, GetOnlinesRequest
from telethon.tl.types import InputUser, InputPeerUser, ReplyKeyboardMarkup, ReplyKeyboardForceReply, DataJSON, \
    PeerChannel



conn = sqlite3.connect('Message_data.db')
cur = conn.cursor()



async def click_bottom(message: object, button_name = None, check = None):
    """
    Return index of button_name
    '⇱ Main Menu'
    Import
    :type message: object
    :type button_name: str
    :return Tuple
    """
    if check == None:
        for button in message[0].buttons:
            for button_next in button:
                if button_name == button_next.text:
                    row = message[0].buttons.index(button)
                    column = button.index(button_next)
                    return await message[0].click(row, column)
    else:
        for button in message[0].buttons:
            for button_next in button:
                if button_name in button_next.text:
                    row = message[0].buttons.index(button)
                    column = button.index(button_next)
                    return await message[0].click(row, column)

def read_from_data_base():
    cur.execute(f'SELECT * FROM "MESSAGES"')
    wiadomosci = cur.fetchall()
    result = [x[1] for x in wiadomosci]
    result_msg = [x[2] for x in wiadomosci]
    return [result,result_msg]


def save_data_to_base(data):
    sprawdzic = read_from_data_base()
    for i in data:
        if i[1] not in sprawdzic[0]:
            cur.execute(f'''INSERT INTO 'MESSAGES' VALUES (?,?,?)''', (None, i[1],i[0]))
            conn.commit()


async def get_message_from_bot(entity):
    """

    :param entity:
    :return: First message from treading bot
    """
    time.sleep(2)
    message = await client.get_messages(
        entity=entity,
        limit=1,
        wait_time=5,
        offset_id=0,
        offset_date=None,
        add_offset=0,
        max_id=0,
        min_id=0,
    )

    return message


async def get_message_from_channels() -> List:
    """

    :return: messages from list of channels
    """
    channels = [1250232772,
                1141692661,
                1410247888,
                1474777826,
                1475063825,
                1436257183,
                ]

    messages = []

    for channel in channels:
        channel_entity = await client.get_entity(PeerChannel(channel))
        message = await client.get_messages(
            entity=channel_entity,
            limit=5,
            wait_time=5,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            max_id=0,
            min_id=0,
        )
        for msg in message:
            messages.append([msg.message, msg.id])
    return messages


def save_message_if_send_to_bot():
    pass


def change_to_BTCUSDT(mesagge):
    for word in mesagge[0].split():
        if word == "XBTUSD":
            mesagge[0] = mesagge[0].replace(word, 'BTCUSDT')



def check_message_is_signal(message):
    KEY_WORDS = ['Entry', 'Zone', 'Take', 'Profit', 'Targets', 'Stop', 'ENTRY', 'STOP', 'Target', 'AROUND', 'SEL', 'BUY', 'SHORT', 'FUTURES CALL', 'LONG']
    message = message
    quantity = 0
    if not 'Profit:' in message or not'Period' in message:
        for word in KEY_WORDS:
            if word in message:
                quantity += 1
    if quantity >= 2:
        return True
    else:
        return False

def check_message_is_close_signal(message):
    KEY_WORDS = ['Close', 'CLOSE', 'Closed', 'CLOSED']

async def send_signal(entity, message):
    from_bot = await get_message_from_bot(entity)
    if not 'Main Menu:' in from_bot[0].message:
        await click_bottom(message=from_bot, button_name='⇱ Main Menu')
    time.sleep(2)
    if 'Main Menu' in from_bot[0].message:
        from_bot = await get_message_from_bot(entity)
        await click_bottom(message=from_bot, button_name='Signals')
    time.sleep(2)
    from_bot = await get_message_from_bot(entity)
    if 'Choose an option below.' in from_bot[0].message:
        await click_bottom(message=from_bot, button_name='Import')

    time.sleep(1)

    from_bot = await get_message_from_bot(entity)
    if 'Either forward or copy-paste an external signal' in from_bot[0].message:
        await client.send_message(entity= entity, message= message)

    from_bot = await get_message_from_bot(entity)
    if 'Choose client' in from_bot[0].message:
        await click_bottom(message=from_bot, button_name='My-Binance Futures')

    from_bot = await get_message_from_bot(entity)
    if 'Current Price' in from_bot[0].message:
        await click_bottom(message=from_bot, button_name='Confirm')

    from_bot = await get_message_from_bot(entity)
    if 'Choose new_amount from' in from_bot[0].message:
        await click_bottom(message=from_bot, button_name='20', check='x')

    from_bot = await get_message_from_bot(entity)
    if 'Do you want to cancel the trade when the' in from_bot[0].message:
        await click_bottom(message=from_bot, button_name='Yes')
    time.sleep(2)






async def main():
    entity = await client.get_entity('cornix_trading_bot')
    while True:
        time.sleep(20)
        signals = []
        close = []
        mesagges = await get_message_from_channels()

        for msg in mesagges:
            if check_message_is_signal(message=msg[0]):
                change_to_BTCUSDT(msg)
                signals.append(msg)
        check = read_from_data_base()
        print(signals)
        for signal in signals:
            if signal[1] not in check[0] and signal[0] not in check[1]:
                await send_signal(entity,signal[0])
                save_data_to_base([signal])




#     mess = '''VİTE USDT 7X
#
# BUY 1700-1795
#
# SEL-2100-2300-
#
# 2X TO 3X'''
#     print(check_message_is_signal(message=mess))

    # channel_entity = await client.get_entity('cornix_trading_bot')
    # await send_signal(channel_entity, message=message)

    # x= await get_message_from_channels()
    # for i in x:
    #     print(i)
    # print()
    # print()




    # for message in message_from_get_channel:
    #     print(message)
    # row, column = find_button_index(message_from_get_channel, 'Signals')
    # await click_button(message_from_get_channel, row, column)


with TelegramClient(phone, api_id, api_hash) as client:
    if not  client.is_user_authorized():
         client.send_code_request(phone)
         client.sign_in(phone, input('Enter the code: '))

    client.loop.run_until_complete(main())


