#搖桿的
import requests
import json

headers = {"Authorization":"Bearer r3Vd2DMVe4ZRSPsC4/zQVzJlfBM6d4oayYSFtwAU5VuRgnfJDrl4HevnSNcW5O6NO1ryrqJJ6cVMvm4j1PNHQ2NBocWCdz9ZEXtUg3cGAAr5+MUZ3kzrfcveN81ZP+pTXRdSyE47DQZS4POJT4eG3QdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

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

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)