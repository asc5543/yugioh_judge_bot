import discord

import logging
import os
import re

import web_server
from urllib.request import urlopen

def find_cid(card_number: str) -> str:
    search_url = f'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&keyword={card_number}&stype=4&ctype=&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2&request_locale=ja'
    logging.info(f'Connect to {search_url}')
    card_search_page = urlopen(search_url)

    # value="/yugiohdb/card_search.action?ope=2&cid=15470"
    cid_pattern = re.compile('ope=2&cid=([^"]*)')
    if card_search_page.getcode() == 200:
        page_raw_data = card_search_page.read().decode('utf-8')
        cid_match = cid_pattern.search(page_raw_data)
        if cid_match:
            return cid_match.group(1)
    return ""


def message_handler(message: str) -> str:
    if message == '叫裁判啦':
        return '自己查啦幹：https://reurl.cc/mL6eEG'
    if message.find('-') in [2, 3, 4]:
        cid = find_cid(message)
        if not cid:
            logging.info(f'{message} cannot find')
            return ""
        return_url = f'https://www.db.yugioh-card.com/yugiohdb/faq_search.action?ope=4&cid={cid}&request_locale=ja'
        logging.info(f'Q&A URL: {return_url}')
        return return_url


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents, reconnect=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

    @client.event
    async def on_ready():
        logging.info(f'目前登入身份 --> {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        return_message = message_handler(message.content)
        if return_message:
            await message.channel.send(return_message)

    token = os.environ['DISCORD_BOT_TOKEN']
    web_server.run(os.environ['SERVER_TYPE'])
    client.run(token)


if __name__ == '__main__':
    main()
