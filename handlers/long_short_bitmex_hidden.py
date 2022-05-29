import logging
import re
import sys

sys.path.append('handlers/trade_signal_handler_telethon-0.101-py3.8.egg')
from signal_handler.handler import ParsedSignal


def format_message(parsed: ParsedSignal, event):
    return handler7_format(parsed)


def format_message_ftx(parsed: ParsedSignal, event):
    return handler7_format(parsed, True)


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
    if '125' in parsed.get_leverage():
        parsed.set_leverage(parsed.get_leverage().replace("125","100"))
    for i in lines[2].replace('-', ' ').split()[-3:]:
        parsed.add_entry(int(round(float(i), -1)))
    count = 1
    for i in re.findall("[0-9.].*\).([0-9.]*)", signal)[1:]:
        target_int = int(round(float(i), -1))
        target = 0
        if count == 2:
            if is_long:
                target += 30
            else:
                target -= 30
        count = count + 1
        parsed.add_take_profit(target_int + target)
    parsed.add_stop_loss(int(round(float(lines[-2].split()[-1]), -1)))
    return parsed


def handler7_format(parsed, FTX=False):
    name = parsed.get_name()
    entries = parsed.get_entries()
    take_profit_targets = parsed.get_take_profit_targets()
    stop_lossses = parsed.get_stop_losses()
    exchanges = "ByBit USDT, Binance Futures"
    leverage = parsed.get_leverage()
    output = ""
    color = ""
    is_long = True
    if 'long' in parsed.get_type().lower():
        color = "🟢🟢"
    elif 'short' in parsed.get_type().lower():
        color = "🔴🔴"
    if FTX:
        name = name.replace("USDT", "USD")
    output += color + "#" + name + color
    if FTX:
        exchanges = "FTX Futures"
    output += "\nExchanges: {}".format(exchanges)
    output += "\nSignal Type: Regular {}".format(parsed.get_type())
    if FTX:
        leverage = "Cross (20.0X)"
    output += "\nLeverage: {}".format(leverage)
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
    output += "\n\n👉 Published By: @Prince_dw 👈\nAutomated [BTC] Scalping Signals, Risk should be managed\n"
    return output