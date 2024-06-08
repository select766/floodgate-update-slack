import os
import requests
from bs4 import BeautifulSoup
import time
import re
from dotenv import load_dotenv
import argparse

load_dotenv()

def send_slack_message(message):
    print(message)
    response = requests.post(
        os.environ["SLACK_WEBHOOK_URL"],
        json={"text": message},
    )

def clean_html_tags(raw_html):
    cleantext = re.sub('<.*?>', '', raw_html)
    return cleantext

def format_row(row_soup):
    columns = row_soup.find_all('td')
    return ', '.join(clean_html_tags(str(col)) for col in columns)


def get_rows():
    # ページ内容を取得
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # <h2>Game History</h2> の後にあるテーブルを取得
    game_history_header = soup.find('h2', string='Game History')
    game_table = game_history_header.find_next('table')
    # 偶数行と奇数行で色を変えるために、行の内容が同じでもタグの属性が違うため、行の内容を比較するために文字列に変換
    rows = set([format_row(row) for row in game_table.find_all('tr')])
    return rows

def check_for_updates():
    global initial_rows
    current_rows = get_rows()
    
    new_rows = current_rows - initial_rows
    if new_rows:
        initial_rows = current_rows
        for new_row in new_rows:
            send_slack_message("New game entry added: " + new_row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="floodgate URL to monitor")
    parser.add_argument("--interval", help="check interval in seconds (default 60)", type=int, default=60)
    args = parser.parse_args()

    if args.url:
        url = args.url
    else:
        url = os.environ["FLOODGATE_URL"]
    print(url)

    initial_rows = get_rows()
    while True:
        time.sleep(args.interval)  # 60秒ごとにチェック
        check_for_updates()
