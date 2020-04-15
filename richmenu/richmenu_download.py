from linebot import (
    LineBotApi, WebhookHandler
)
linebotapi = LineBotApi('ASWKfQvAGiXrAOCMcRoc0+vUMYY8hFUFOFFbIgOhBF4v6MIWjr9aHvsdkKrIXdN8MO4vduONxiuFu84dDTcGzGpy6u8umCW0ifDavs3yiPoVdZ94Kk5uKkL25553eygfgdkgCqAcZninEIk5n06J9gdB04t89/1O/w1cDnyilFU=')

content = linebotapi.get_rich_menu_image(rich_menu_id='richmenu-aec048bea3ff9cebcc45f85f0a01ca1f',timeout=None)
with open('D:\\Restaurant_Client_Linebot\\richmenu', 'wb') as fd:
    for chunk in content.iter_content():
        fd.write(chunk)