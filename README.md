# floodgateの更新をslackに送るツール

対局終了時に、以下のようなメッセージをslackに送る。

```
New game entry added: 2024-06-08 04:00:03, (csa), KifuwarabeWCSC34R, 3, v.s., npthao_ryzen5700x*, 129, 22, toryo
```

# 環境構築

python 3.9

```
poetry install
```

## 設定ファイル

`.env`に書き込む。

```
SLACK_WEBHOOK_URL=
FLOODGATE_URL=
```

SlackでWebhook URLを取得する。 <https://api.slack.com/messaging/webhooks>

FloodgateのプレイヤーページURLを取得する。Player Statisticsというタイトルのページ。例: <http://wdoor.c.u-tokyo.ac.jp/shogi/view/show-player.cgi?event=LATEST&filter=floodgate&show_self_play=1&user=gikou2_1c>

# 実行

```
poetry run python check.py
```

60秒ごとに更新チェックがされ、更新があれば送信される。

`--url` オプションを使うと、`.env`のURL設定を無視して指定したURLを監視する。
