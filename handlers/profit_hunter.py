from telethon import events
import config
import logging

logger = logging.getLogger(__name__)


def parse_message(message):
    parsed = {"entry_targets": [], "take_profit_targets": []}
    key = None

    for line in message.split("\n"):
        if "Long" in line:
            parsed["type"] = "Long"
        elif "Short" in line:
            parsed["type"] = "Short"
        elif "/USDT" in line:
            parsed["title"] = line.split("$")[1]
        elif "Entry" in line:
            key = "entry_targets"
        elif "Profit" in line:
            key = "take_profit_targets"
        elif "Stop-loss" in line:
            key = "stop_loss"
        else:
            if line:
                if key == "entry_targets":
                    entries = line.split(" - ")
                    for entry in entries:
                        parsed["entry_targets"].append(entry)
                elif key == "take_profit_targets":
                    profits = line.split(" - ")
                    for profit in profits:
                        parsed["take_profit_targets"].append(profit)
                elif key == "stop_loss":
                    parsed["stop_loss"] = line
                    key = ""

    return parsed


def parse_message1(message):
    parsed = {"entry_targets": [], "take_profit_targets": []}
    key = None

    for line in message.split("\n"):
        if "LONG" in line:
            parsed["type"] = "Long"
        elif "SHORT" in line:
            parsed["type"] = "Short"
        elif "/USDT" in line:
            parsed["title"] = line.split("$")[1]
        elif "ENTRY" in line:
            entries = line.split(": ")[1].split(" - ")
            for entry in entries:
                parsed["entry_targets"].append(entry)
        elif "TARGET" in line:
            parsed["take_profit_targets"].append(line.split(": ")[1])
        elif "STOP" in line:
            parsed["stop_loss"] = line.split(": ")[1]

    return parsed


def get_title(parsed):
    return parsed["title"]


def get_signal_type(parsed):
    return f"Signal Type: Regular ({parsed['type']})"


def get_entry_targets(parsed):
    s = "Entry Targets:"
    index = 1
    for target in parsed["entry_targets"]:
        s += f"\n{index}) {target}"
        index += 1

    return s


def get_take_profit_targets(parsed):
    s = "Take-Profit Targets:"
    index = 1
    for i in range(0, 4):
        target = parsed["take_profit_targets"][i]
        s += f"\n{index}) {target}"
        index += 1

    return s


def get_stop_targets(parsed):
    return f"Stop Targets: \n1) {parsed['stop_loss']}"


@events.register(events.NewMessage(chats=config.SOURCE_CHANNEL_PROFIT_HUNTER))
async def profit_hunter_handler(event):
    message = event.message.message
    source_channel = None
    try:
        source_channel = await event.client.get_entity(config.SOURCE_CHANNEL_PROFIT_HUNTER)
    except Exception as e:
        logger.info(f"Error getting source channel {str(e)} [{config.SOURCE_CHANNEL_PROFIT_HUNTER}]\n")

    if event.message.reply_markup is not None:
        try:
            if "KEEP" in message:
                parsed = parse_message(message)
                message_out = f"⚡️⚡️#{get_title(parsed)}⚡️⚡️\nExchanges: Binance Futures,Bybit USDT\n{get_signal_type(parsed)}\nLeverage: Cross (25.0x)\n\n{get_entry_targets(parsed)}\n\n{get_take_profit_targets(parsed)}\n\n{get_stop_targets(parsed)}\n\n🌱 Published by: @Prince_dw 🌱"
            else:
                parsed = parse_message1(message)
                message_out = f"⚡️⚡️#{get_title(parsed)}⚡️⚡️\nExchanges: Binance Futures,Bybit USDT\n{get_signal_type(parsed)}\nLeverage: Cross (20.0x)\n\n{get_entry_targets(parsed)}\n\n{get_take_profit_targets(parsed)}\n\n{get_stop_targets(parsed)}\n\n🌱 Published by: @Prince_dw 🌱"

            await event.client.send_message(entity=config.DESTINATION_CHANNELS_PROFIT_HUNTER, message=message_out)

            logger.info(
                f"message forwarded successfully - [{source_channel.title}]"
            )
        except Exception as e:
            print(ass)
            logger.info("{0} - Error parsing message {1} -[{2}]\n".format(str(message[:30]).replace("\n", ""), e,
                                                                          source_channel.title))
    else:
        logger.info("{0} - Cornix Duplicate message - [{1}]\n".format(str(message[:30]).replace("\n", ""),
                                                                      source_channel.title))
