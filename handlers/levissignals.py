from telethon import events
import config
import logging
import re

logger = logging.getLogger(__name__)

forwarding_keywords = ['exchanges:binancespot']
forwarding_keywords_ftx = ['exchanges:ftxfutures']
forwarding_keywords_binance = ['exchanges:binancefutures,bybitusdt']


def extract_number_string(s):
    p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
    if re.search(p, s) is not None:
        l = []
        for catch in re.finditer(p, s):
            l.append(catch[0])
        return l


def clean_signal(signal):
    signal = signal.replace(" ", "").lower().split("\n")
    for i in signal:
        if (i == ""):
            signal.remove(i)
    return signal

def check_forwarding_conditions(signal):
    for i in signal:
        if ([kw for kw in forwarding_keywords if kw == i]):
            return 1

    return


def check_forwarding_conditions_ftx(signal):
    for i in signal:
        if ([kw for kw in forwarding_keywords_ftx if kw == i]):
            return 1

    return


def check_forwarding_conditions_binance(signal):
    for i in signal:
        if [kw for kw in forwarding_keywords_binance if kw == i]:
            return True
    return False


def get_destination_channel(signal):
    if check_forwarding_conditions(signal):
        return config.LEVISSIGNALS_DESTINATION_CHANNEL
    if check_forwarding_conditions_ftx(signal):
        return config.LEVISSIGNALS_DESTINATION_CHANNEL_FTX
    if check_forwarding_conditions_binance(signal):
        return config.LEVISSIGNALS_DESTINATION_CHANNEL_BINANCE


@events.register(events.NewMessage(chats=int(config.LEVISSIGNALS_SOURCE_CHANNEL)))
async def levissignals_handler(event):
    try:
        if event.message.reply_markup:
            text = clean_signal(event.text)
            if check_forwarding_conditions(text):
                forward_message = event.text
                DES = []
                for destination_channel in config.LEVISSIGNALS_DESTINATION_CHANNEL:
                    response = await event.client.send_message(entity=destination_channel, message=forward_message)
                    if response:
                        destination_channel_detail = await event.client.get_entity(destination_channel)
                        DES.append(destination_channel_detail.title)

                if len(DES):
                    log_msg = f"{event.text[:30]} - Successfully forwarded to Channel(s)-" + str([k for k in DES])
                    logger.info(log_msg)
            elif check_forwarding_conditions_ftx(text):
                forward_message = event.text
                response = await event.client.send_message(entity=int(config.LEVISSIGNALS_DESTINATION_CHANNEL_FTX), message=forward_message)
                if response:
                    destination_channel_detail = await event.client.get_entity(int(config.LEVISSIGNALS_DESTINATION_CHANNEL_FTX))
                    log_msg = f"{event.text[:30]} - Successfully forwarded to Channel(s)-" + destination_channel_detail.title
                    logger.info(log_msg)
            elif check_forwarding_conditions_binance(text):
                forward_message = event.text
                response = await event.client.send_message(entity=int(config.LEVISSIGNALS_DESTINATION_CHANNEL_BINANCE), message=forward_message)
                if response:
                    destination_channel_detail = await event.client.get_entity(int(config.LEVISSIGNALS_DESTINATION_CHANNEL_BINANCE))
                    log_msg = f"{event.text[:30]} - Successfully forwarded to Channel(s)-" + destination_channel_detail.title
                    logger.info(log_msg)
            else:
                logger.info(f"{event.text[:30]} - Not forwarded successfully due to not containg the key word{forwarding_keywords + forwarding_keywords_binance + forwarding_keywords_ftx}")

    except Exception as e:
        raise e