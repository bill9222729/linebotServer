import requests

headers = {"Authorization":"Bearer r3Vd2DMVe4ZRSPsC4/zQVzJlfBM6d4oayYSFtwAU5VuRgnfJDrl4HevnSNcW5O6NO1ryrqJJ6cVMvm4j1PNHQ2NBocWCdz9ZEXtUg3cGAAr5+MUZ3kzrfcveN81ZP+pTXRdSyE47DQZS4POJT4eG3QdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{richmenu_id}'.format(richmenu_id='richmenu-69cecea7e4ae9c4295f15e328586b9a1'),
                       headers=headers)
print(req.text)