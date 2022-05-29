import logging
import re
import sys

sys.path.append('handlers/trade_signal_handler_telethon-0.101-py3.8.egg')
from signal_handler.handler import ParsedSignal


def trigger_func(message: str, event):
    channel_name = event.chat.title
    logger = logging.getLogger()
    if ("All entry targets achieved" in message):
        logger.info(f"Ignoring {event.text[:15]} :: {channel_name}")
        return False

    if ("Period:" in message):
        logger.info(f"Ignoring {event.text[:15]} :: {channel_name}")
        return False

    if ("Loss:" in message):
        logger.info(f"Ignoring {event.text[:15]} :: {channel_name}")
        return False

    if ("Average Entry Price:" in message):
        logger.info(f"Ignoring {event.text[:15]} :: {channel_name}")
        return False

    if ("Target achieved before entering" in message):
        logger.info(f"Ignoring {event.text[:15]} :: {channel_name}")
        return False
    if ("Closed at trailing stoploss" in message):
        logger.info(f"Ignoring {event.text[:15]} :: {channel_name}")
        return False
    if ("Breakout" in message):
        logger.info(f"Ignoring {event.text[:15]} :: {channel_name}")
        return False
    if ("close" in message or "Close" in message):
        logger.info(f"Ignoring {event.text[:15]} :: {channel_name}")
        return False
    if ("✅" in message):
        logger.info(f"Ignoring {event.text[:15]} :: {channel_name}")
        return False
    logger.info("Handling message with: " + message.split('\n')[0])
    return True


def parse_message(message: str, event):
    logger = logging.getLogger()
    channel_name = event.chat.title
    parsed = ParsedSignal()
    signal = message.replace('–', '-')
    input_lines = signal.split('\n')
    lines = []
    for i in input_lines:
        if i.strip() != '':
            lines.append(i)
    is_long = True
    if 'long' in lines[2].lower():
        is_long = True
    elif 'short' in lines[2].lower():
        is_long = False
    parsed.set_name(lines[0][:3] + "/" + lines[0][3:])
    parsed.add_exchange(lines[1])
    parsed.set_type(lines[2].split()[0].capitalize())
    try:
        parsed.set_leverage("{} ({}x)".format(re.findall("everage.*=>(.*[A-z]).*\(", lines[-1])[0].strip(), float(re.findall("everage.*ross.*\(([0-9.]*).*", lines[-1])[0].strip())))
    except Exception as e:
        logger.error(f"Couldn't find leverage. Channel {channel_name}. Error: {e} :: [{signal[:15]}]")
    for i in lines[2].replace('-', ' ').split()[-3:]:
        parsed.add_entry(int(round(float(i), -1)))
    for i in re.findall("[0-9.].*\).([0-9.]*)", signal)[:6]:
        target_int = int(round(float(i), -1))
        parsed.add_take_profit(target_int)
    parsed.add_stop_loss(int(round(float(lines[-2].split()[-1]), -1)))
    return parsed


def format_message(parsed: ParsedSignal, event):
    entries = parsed.get_entries()
    take_profit_targets = parsed.get_take_profit_targets()
    stop_lossses = parsed.get_stop_losses()
    exchanges = parsed.get_exchanges()
    output = ""
    output += "#" + parsed.get_name()
    print(exchanges)
    output += "\nExchanges: " + exchanges[0]
    output += "\nSignal Type: Regular {}".format(parsed.get_type())
    output += "\nLeverage: Cross ({})".format(parsed.get_leverage())
    output += "\nAmount: 1.0%"
    output += "\n"
    output += "\nEntry Targets:"
    count = 1
    for i in entries:
        output += "\n{}) {}".format(count, i)
        count += 1
    output += "\n"
    output += "\nTake-Profit Targets:"
    count = 1
    for i in take_profit_targets[:6]:
        output += "\n{}) {}".format(count, i)
        count += 1
    output += "\n"
    output += "\nStop Targets:"
    output += "\n1) {}".format(stop_lossses[0])
    return output