from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('5r3O9irAOQ1sO6UWklhlqQK48JgVe4LHTS7xdKmmsrVZWLv86sGFB4DbyRWdTaZJUbIVthCl7OH5Ic604V/GlbleKJv6y0YPTHl4J/KdAKLEW0TOb2E14AWzOfhlkPSWVjRBFnmyPROucJL44be5FgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4312ba4e017fe31417dd5f8b5f12dab6')

@app.route("/")
def test():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "世話かけるな":
        reply_message = "いいよ"
    elif event.message.text == "勉強開始":
        reply_message = "計測を開始しました"
        start = 今の時間
    elif event.message.text == "勉強終了":
        reply_message = "ただいまの勉強時間は０時間０分１０秒です。お疲れ様でした！"
    else:
        reply_message = f"あなたは{event.message.text}と言いましたね？"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()