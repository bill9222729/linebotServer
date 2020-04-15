import requests
import json

from linebot import (
    LineBotApi, WebhookHandler
)
line_bot_api = LineBotApi('r3Vd2DMVe4ZRSPsC4/zQVzJlfBM6d4oayYSFtwAU5VuRgnfJDrl4HevnSNcW5O6NO1ryrqJJ6cVMvm4j1PNHQ2NBocWCdz9ZEXtUg3cGAAr5+MUZ3kzrfcveN81ZP+pTXRdSyE47DQZS4POJT4eG3QdB04t89/1O/w1cDnyilFU=')
headers = {"Authorization":"Bearer r3Vd2DMVe4ZRSPsC4/zQVzJlfBM6d4oayYSFtwAU5VuRgnfJDrl4HevnSNcW5O6NO1ryrqJJ6cVMvm4j1PNHQ2NBocWCdz9ZEXtUg3cGAAr5+MUZ3kzrfcveN81ZP+pTXRdSyE47DQZS4POJT4eG3QdB04t89/1O/w1cDnyilFU=",
    "Content-Type":"application/json"}

body = {
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": 'true',
  "name": "richmenu 2",
  "chatBarText": "查看更多資訊",
  "areas": [
    {
      "bounds": {
        "x": 0,
        "y": 0,
        "width": 835,
        "height": 839
      },
      "action": {
        "type": "message",
        "text": "目前訂位"
      }
    },
    {
      "bounds": {
        "x": 839,
        "y": 0,
        "width": 813,
        "height": 839
      },
      "action": {
        "type": "message",
        "text": "發送公告"
      }
    },
    {
      "bounds": {
        "x": 1661,
        "y": 0,
        "width": 839,
        "height": 839
      },
      "action": {
        "type": "message",
        "text": "取消訂位"
      }
    }
  ]
}
# step1 設定好按鈕json,POST取得richmenu Id
#req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/', headers=headers,data=json.dumps(body).encode('utf-8'))
#print(req.text)

# step2 設定richmenu的圖片, 無回傳東西代表成功
#with open('./menu/server_icon/rm_0112.jpg', 'rb') as rm:
#    line_bot_api.set_rich_menu_image('richmenu-0e6b67a28840b8b78fd936da6a3e2e2a', 'image/jpeg', rm)

# step3 啟用richmenu, 成功的話會回傳{}, 之後看 https://medium.com/front-end-augustus-study-notes/line-bot-rich-menu-aa5fa67ac6ae, 用postman正式啟用
# 客戶端: 077b16ffb71de810d9d50d02bfd03a8b
# 控制端: 80ce4a9e3fc8b765424e3b7bed97c84a
#req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-0e6b67a28840b8b78fd936da6a3e2e2a', headers=headers)
#print(req.text)

# check全部的richmenu, 一個token最多1000個
#rich_menu_list = line_bot_api.get_rich_menu_list()

#for rich_menu in rich_menu_list:
#    print(rich_menu.rich_menu_id)

# 刪除不要的richmenu
#line_bot_api.delete_rich_menu('richmenu-0a0b16e7a24a3c7539da647a56105eb9')