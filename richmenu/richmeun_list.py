from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('ASWKfQvAGiXrAOCMcRoc0+vUMYY8hFUFOFFbIgOhBF4v6MIWjr9aHvsdkKrIXdN8MO4vduONxiuFu84dDTcGzGpy6u8umCW0ifDavs3yiPoVdZ94Kk5uKkL25553eygfgdkgCqAcZninEIk5n06J9gdB04t89/1O/w1cDnyilFU=')

rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)