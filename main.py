
import os

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage,
                            TextSendMessage, TemplateSendMessage,
                            CarouselColumn, CarouselTemplate, URIAction)

from foodstuff import Foodstuff
from recipe import Recipe

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


@app.route("/push_sample")
def push_sample():
    """プッシュメッセージを送る"""
    user_id = os.environ["USER_ID"]
    line_bot_api.push_message(user_id, TextSendMessage(text="Hello World!"))

    return "OK"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body:" + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    food = Foodstuff().get_food()
    recipes = Recipe().get_recipes(food)

    notes = [CarouselColumn(thumbnail_image_url=recipes[0]["image"],
                            title=recipes[0]["recipe"],
                            text=f"{food}のレシピ",
                            actions=[
                                URIAction(
                                    label='Go!!',
                                    uri=recipes[0]["link"]
                                )
                            ]),

             CarouselColumn(thumbnail_image_url=recipes[1]["image"],
                            title=f"{food}のレシピ",
                            text=recipes[1]["recipe"],
                            actions=[
                                {"type": "message",
                                 "label": "サイトURL",
                                 "text": recipes[1]["link"]}]),

             CarouselColumn(thumbnail_image_url=recipes[2]["image"],
                            title=f"{food}のレシピ",
                            text=recipes[2]["recipe"],
                            actions=[
                                {"type": "message", "label": "サイトURL", "text": recipes[2]["link"]}])]

    messages = TemplateSendMessage(alt_text='template',
                                   template=CarouselTemplate(columns=notes), )

    line_bot_api.reply_message(event.reply_token, messages=messages)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
