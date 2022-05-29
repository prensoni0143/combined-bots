# import os
import logging
import re

import telethon
from binance.client import Client as bicl
from telethon import events

import config

# Enable logging

logger = logging.getLogger(__name__)

api_key = 'fjGEyf1lLEZVyffXS3i7ZWWvNpiQZW3Pf8D36vzHZ9G0Pf2g1LgpSl5uTxsrNIYT'
api_secret = 'QAJmYwc3v7xFAIJJdx5Bd94O1JdKwQACkV11Q5PXaEnOnF15YYyZ0NpFxd3vabGT'
binance_client_api = bicl(api_key, api_secret)

# API_ID = 5911805
# API_HASH = 'baf59bae0d7caba308cdada2079670c2'
# CRYPTO_DESTINATION_CHANNEL_FUTURE = '-1001477534408, -1001475561637'
# CRYPTO_DESTINATION_CHANNEL_SPOT = '-1001251063725, -1001475561637'


def get_channel_a_output_format__second_destination_channel(text):
    final_output = ''
    bottom_line = "Published By: @Prince_dw"
    # To find the stock
    symbol_search = re.search(r"(#)(\w+)[/|_](\w+)", text)
    # To search find price of Entry Point
    for i in text.split('\n'):
        if 'entry' in i.lower():
            buying_range = re.findall(r"[\d\.\d]+", i)
        if 'sell' in i.lower():
            selling_range = re.findall(r"[\d\.\d]+", i)
        if 'stop' in i.lower():
            stoploss = re.findall(r"[\d\.\d]+", i)
            stoploss[0] = stoploss[-1]
    try:
        scalp = re.search(r'(long|short)', text.lower())
        if scalp.group(0) == 'long':
            b = 'Long'
        elif scalp.group(0) == 'short':
            b = 'Short'
    except:
        print("error happened")

    symbol_to_check = symbol_search.group(2).upper() + symbol_search.group(
        3).upper()

    # To find the price of stock
    info = binance_client_api.get_symbol_ticker(symbol=symbol_to_check.upper())
    price_len = len(str(int(float(info['price']) // 1)))
    # To find the number before decimal point

    for count, i in enumerate(buying_range):
        if len(i) != price_len and i[price_len] != '.':
            if info['price'][0] != '0':
                i = i[:price_len] + '.' + i[price_len:]
            else:
                i = '0.' + i
            buying_range[count] = i
    for count, i in enumerate(selling_range):
        if len(i) != price_len and i[price_len] != '.':
            if info['price'][0] != '0':
                i = i[:price_len] + '.' + i[price_len:]
            else:
                i = '0.' + i
            selling_range[count] = i

    for count, i in enumerate(stoploss):
        if len(i) != price_len and i[price_len] != '.':
            if info['price'][0] != '0':
                i = i[:price_len] + '.' + i[price_len:]
            else:
                i = '0.' + i
            stoploss[count] = i

    final_output += f'#{symbol_search.group(2).upper()}/{symbol_search.group(3).upper()}\n'
    final_output += 'Exchange : FTX Futures\n'
    final_output += f'Signal Type: Regular ({b})\n'
    final_output += 'Leverage: Cross (20.0X)\n'
    final_output += 'Amount: 2.0%\n\n'
    final_output += 'Entry Targets:\n'
    for count, i in enumerate(buying_range):
        final_output += f'{count+1}) {i}\n'

    final_output += f'\n'
    final_output += 'Take-Profit Targets:\n'
    final_output += f'1) {selling_range[0]}\n'
    final_output += f'2) {selling_range[1]}\n'
    final_output += f'3) {selling_range[2]}\n'
    final_output += f'4) {selling_range[3]}\n\n'
    final_output += 'Stop Targets:\n'
    final_output += f'1) {stoploss[0]}'
    return final_output.replace('USDT', 'USD') + f"\n\n{bottom_line}"


def change_text_channel_1(text, destination_channel):
    final_output = ''
    # To find the stock
    symbol_search = re.search(r"(#)(\w+)[/|_](\w+)", text)
    # To search find price of Entry Point
    for i in text.split('\n'):
        if 'entry' in i.lower():
            buying_range = re.findall(r"[\d\.\d]+", i)
        if 'sell' in i.lower():
            selling_range = re.findall(r"[\d\.\d]+", i)
        if 'stop' in i.lower():
            stoploss = re.findall(r"[\d\.\d]+", i)
            stoploss[0] = stoploss[-1]
    try:
        scalp = re.search(r'(long|short)', text.lower())
        if scalp.group(0) == 'long':
            b = 'Long'
        elif scalp.group(0) == 'short':
            b = 'Short'
    except:
        logger.error(
            f"Couldn't find symbol 'long' or 'short' for message: {text[:20]}-[{destination_channel.title}]"
        )
        print(
            f"Couldn't find symbol 'long' or 'short' for message: {text[:20]}-[{destination_channel.title}]"
        )

    symbol_to_check = symbol_search.group(2).upper() + symbol_search.group(
        3).upper()
    logger.info(symbol_to_check)

    # To find the price of stock
    info = binance_client_api.get_symbol_ticker(symbol=symbol_to_check.upper())
    price_len = len(str(int(float(info['price']) // 1)))
    # To find the number before decimal point
    logger.info(f'price_len, {info["price"][0]}')
    for count, i in enumerate(buying_range):
        if len(i) != price_len and i[price_len] != '.':
            if info['price'][0] != '0':
                i = i[:price_len] + '.' + i[price_len:]
            else:
                i = '0.' + i
            buying_range[count] = i
    for count, i in enumerate(selling_range):
        if len(i) != price_len and i[price_len] != '.':
            if info['price'][0] != '0':
                i = i[:price_len] + '.' + i[price_len:]
            else:
                i = '0.' + i
            selling_range[count] = i
    logger.info(stoploss)
    print(stoploss)
    for count, i in enumerate(stoploss):
        if len(i) != price_len and i[price_len] != '.':
            if info['price'][0] != '0':
                i = i[:price_len] + '.' + i[price_len:]
            else:
                i = '0.' + i
            stoploss[count] = i

    final_output += f'#{symbol_search.group(2).upper()}/{symbol_search.group(3).upper()}\n'
    final_output += 'Exchange : Binance Futures\n'
    final_output += f'Signal Type: Regular ({b})\n'
    final_output += 'Leverage: Cross (20.0X)\n'
    final_output += 'Amount: 2.0%\n\n'
    final_output += 'Entry Targets:\n'
    for count, i in enumerate(buying_range):
        final_output += f'{count+1}) {i}\n'

    final_output += f'\n'
    final_output += 'Take-Profit Targets:\n'
    final_output += f'1) {selling_range[0]}\n'
    final_output += f'2) {selling_range[1]}\n'
    final_output += f'3) {selling_range[2]}\n'
    final_output += f'4) {selling_range[3]}\n\n'
    final_output += 'Stop Targets:\n'
    final_output += f'1) {stoploss[0]}'

    return final_output


def change_text_for_channel_2(text):
    entry_limit = False
    final_output = ''

    # To find the stock
    symbol_search = re.search(r"(#)(\w+)/(\w+)", text)

    a = text.split('\n\n')[0]
    if '#long' in a.lower():
        output_client = 'Binance Futures'
        Trade_type = 'Long'
    elif '#sell' in a.lower() or '#profit' in a.lower() or '#short' in a.lower(
    ):
        output_client = 'Binance Futures'
        Trade_type = 'Short'
    elif 'spot' in a.lower():
        output_client = 'Binance'
        Trade_type = 'Long'
    elif '#limit' in a.lower():
        entry_limit = True

    for i in text.split('\n\n'):
        if 'buy' in i.lower() or 'entry' in i.lower():
            buying_range = re.findall(r"[\d\.\d]+", i)
        if 'sell' in i.lower() or 'profit' in i.lower():
            selling_range = re.findall(r"[\d\.\d]+", i)
        if 'stop' in i.lower():
            stoploss = re.findall(r"[\d\.\d]+", i)

    symbol_to_check = symbol_search.group(2).upper() + symbol_search.group(
        3).upper()

    # To find the price of stock
    info = binance_client_api.get_symbol_ticker(symbol=symbol_to_check)
    # To find the number before decimal point
    price_len = len(str(int(float(info['price']) // 1)))
    logger.info(f'price_len, {price_len}')
    for count, i in enumerate(buying_range):
        if len(i) != price_len and i[price_len] != '.':
            if info['price'][0] != '0':
                i = i[:price_len] + '.' + i[price_len:]
            else:
                i = '0.' + i
            buying_range[count] = i
    for count, i in enumerate(selling_range):
        if len(i) != price_len and i[price_len] != '.':
            if info['price'][0] != '0':
                i = i[:price_len] + '.' + i[price_len:]
            else:
                i = '0.' + i
            selling_range[count] = i
    logger.info(stoploss)
    print(stoploss)
    for count, i in enumerate(stoploss):
        logger.info(count, i)
        if len(i) != price_len and i[price_len] != '.':
            if info['price'][0] != '0':
                i = i[:price_len] + '.' + i[price_len:]
            else:
                i = '0.' + i
            stoploss[count] = i

    final_output += f'⚡️⚡️#{symbol_search.group(2)}/{symbol_search.group(3)}⚡️⚡️\n'
    final_output += f'Client: {output_client}\n'
    final_output += f'Trade Type: Regular ({Trade_type.upper()})\n'
    if output_client == 'Binance Futures':
        final_output += 'Leverage: Cross (10.0X)\n\n'
    else:
        final_output += '\n'
    final_output += 'Entry Targets:\n'
    for count, i in enumerate(buying_range):
        if entry_limit:
            final_output += f'{count+1}) {i} [Wait for Entry Price]\n'
        else:
            final_output += f'{count+1}) {i}\n'

    final_output += '\n'
    final_output += 'Take-Profit Targets:\n'
    for count, i in enumerate(selling_range):
        if count <= 3:
            final_output += f'{count+1}) {i}\n'
    final_output += '\n'
    final_output += 'Stop Targets:\n'
    for count, i in enumerate(stoploss):
        final_output += f'{count+1}) {i}\n'

    return final_output


#production
channel_a = -1001433774445
channel_b = -1001250899036
channel_c = -1001183431565
channel_d = -1001183431565
channel_e = -1001412809065
first_channel_list = [1433774445, 1250899036]

mapping = {
    channel_a: [channel_c, channel_e],
    channel_b: channel_d,
}


@events.register(events.NewMessage(chats=first_channel_list))
async def special_lev_handler(event: telethon.events.newmessage.NewMessage.Event):
    logger.info(f'New message. {event.text[:20]}')
    chat = event.chat_id
    # to check if event contains event

    chat_info = await event.client.get_entity(chat)
    text = event.text
    print(chat, channel_a)
    if chat == channel_a:
        destination_channel = await  event.client.get_entity(int(mapping[chat][0]))
        chat_link = f'Forward : [{chat_info.title}](t.me/{chat_info.username})\n'
        output_text = change_text_channel_1(text, destination_channel)
        output_text = chat_link + output_text
        # link_preview=False,

        # forward to the second destination channel
        allow = [
            coin for coin in config.SPECIAL_LEV_COIN_LIST.split(',')
            if coin in text
        ]
        if (allow):
            destination_channel = await event.client.get_entity(int(mapping[chat][1])
                                                          )

            output_text = get_channel_a_output_format__second_destination_channel(
                text)
            await event.client.send_message(entity=mapping[chat][1],
                                      message=output_text)
            logger.info(
                f"message forwarded successffully - {text[:20]} -[{destination_channel.title}]"
            )
        else:
            logger.info(
                f"message not forwarded successffully - {text[:20]} -[{destination_channel.title}]"
            )
    elif chat == channel_b:
        destination_channel = await event.client.get_entity(int(mapping[chat]))
        chat_link = f'Channel : ♻️[{chat_info.title}](t.me/{chat_info.username})♻️\n\n'
        text = event.text
        text = change_text_for_channel_2(text)
        text = chat_link + text
        # link_preview=False,
        await event.client.send_message(entity=mapping[chat], message=text)
        logger.info(
            f"message forwarded successffully - {event.text[:20]} -[{destination_channel.title}]"
        )
        print(
            f"message forwarded successffully - {event.text[:20]} -[{destination_channel.title}]"
        )