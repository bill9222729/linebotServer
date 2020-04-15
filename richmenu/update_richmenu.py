from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('r3Vd2DMVe4ZRSPsC4/zQVzJlfBM6d4oayYSFtwAU5VuRgnfJDrl4HevnSNcW5O6NO1ryrqJJ6cVMvm4j1PNHQ2NBocWCdz9ZEXtUg3cGAAr5+MUZ3kzrfcveN81ZP+pTXRdSyE47DQZS4POJT4eG3QdB04t89/1O/w1cDnyilFU=')

with open("D:\\Restaurant_Server_Linebot\\richmenu_resized.jpeg",'rb') as f:
    print(f)
    line_bot_api.set_rich_menu_image("richmenu-69cecea7e4ae9c4295f15e328586b9a1", "image/jpeg", f)