import discord

import os
import re

from urllib.request import urlopen

def find_cid(card_number: str) -> str:
  search_url = f'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&keyword={card_number}&stype=4&ctype=&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2&request_locale=ja'
  print(search_url)
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
      print(f'{message} cannot find')
    return_url = f'https://www.db.yugioh-card.com/yugiohdb/faq_search.action?ope=4&cid={cid}&request_locale=ja'
    print(f'Q&A URL: {return_url}')
    return return_url


def main():
  # client是跟discord連接，intents是要求機器人的權限
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents = intents)

  # 調用event函式庫
  @client.event
  # 當機器人完成啟動
  async def on_ready():
    print(f'目前登入身份 --> {client.user}')

  @client.event
  # 當頻道有新訊息
  async def on_message(message):
    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
      return
    # 關鍵字回覆
    return_message = message_handler(message.content)
    await message.channel.send(return_message)

  token = os.environ['DISCORD_BOT_TOKEN']
  client.run(token)


if __name__ == '__main__':
  main()