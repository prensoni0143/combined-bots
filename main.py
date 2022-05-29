import log
from handlers.special_lev import *
from handlers.levissignals import *
from handlers.profit_hunter import *
from telethon import TelegramClient
import sys

sys.path.append('handlers/trade_signal_handler_telethon-0.101-py3.8.egg')

from signal_handler.handler import SignalHandler
from handlers import long_short_bitmex_hidden

def main():
    log.setup()

    logger = logging.getLogger(__name__)

    client = TelegramClient('session', config.API_ID, config.API_HASH)
    client.start()

    client.add_event_handler(special_lev_handler)
    client.add_event_handler(levissignals_handler)
    client.add_event_handler(profit_hunter_handler)

    handler_long_short_bitmex_hidden = SignalHandler(src_channels=config.SOURCE_CHANNEL_LONG_SHORT_BITMEX_HIDDEN,
                                                     dst_channels=config.DESTINATION_CHANNEL_LONG_SHORT_BITMEX_HIDDEN,
                                                     parse_function=long_short_bitmex_hidden.parse_message,
                                                     trigger_function=lambda x, y: 'btc' in x.lower(),
                                                     format_function=long_short_bitmex_hidden.format_message,
                                                     logger=logger, find_entity=False, check_markup=True,
                                                     check_last=True)
    handler_long_short_bitmex_hidden_2 = SignalHandler(src_channels=config.SOURCE_CHANNEL_LONG_SHORT_BITMEX_HIDDEN,
                                                       dst_channels=config.DESTINATION_CHANNEL_LONG_SHORT_BITMEX_HIDDEN_FTX,
                                                       parse_function=long_short_bitmex_hidden.parse_message,
                                                       trigger_function=lambda x, y: 'btc' in x.lower(),
                                                       format_function=long_short_bitmex_hidden.format_message_ftx,
                                                       logger=logger, find_entity=False, check_markup=True,
                                                       check_last=True)

    handler_long_short_bitmex_hidden.telethon_add(client)
    handler_long_short_bitmex_hidden_2.telethon_add(client)

    logger.info('Bot-5 is ON')

    client.run_until_disconnected()


if __name__ == "__main__":
    main()

