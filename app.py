''' 此為控制端 '''
''' 透過額外另一支程式，不斷監控database(JSON or firebase)的情況，一但有紀錄有update的情況就push message給server端 '''

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, FollowEvent, UnfollowEvent,
    TextMessage, TextSendMessage, ImageSendMessage, 
    FlexSendMessage, StickerSendMessage, TemplateSendMessage,
    ButtonsTemplate, ConfirmTemplate, 
    PostbackAction, PostbackTemplateAction
)

app = Flask(__name__)

from App_Config import (
    serverId, Firebase_JsonPath, 
    LineBot_Token, LineBot_Secret, Client_LineBot_Token,
    Richmenu_Server_Id
)
line_bot_api = LineBotApi(LineBot_Token)
line_bot_api_client = LineBotApi(Client_LineBot_Token)
handler = WebhookHandler(LineBot_Secret)

''' firebase setting'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(Firebase_JsonPath)
firebase_admin.initialize_app(cred)
firedb = firestore.client()
''' firebase setting end '''

from datetime import datetime

# import Message template from ./model/message.py(for use reply message)
from model.message import AllMessage

@app.route("/")
def hello():
    return "Hello World!終於成功了。我擦!!!"

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


@handler.add(PostbackEvent)
def handle_postback(event):
    UserId = event.source.user_id
    ert = event.reply_token
    firebase_rec = {}
    profile = line_bot_api.get_profile(UserId)
    doc_ref = firedb.collection('是否訂位').document(UserId)
    doc = doc_ref.get()
    print(event.postback)

    ''' 訂位功能step6 - 同意訂位 '''
    if 'yes' in event.postback.data:
        InOrder = 1
        # 取得順位
        dict_doc = doc.to_dict()
        doc_ref = firedb.collection_group('訂位紀錄')
        docs = doc_ref.stream() # generator
        # 1個ID(collection)算一次迴圈
        for doc in docs:
            for d in doc.to_dict(): # for each in dict
                try:# 如果他訂的時間一小時內沒有人的話就第一順位, 有的話就後延      
                    selected_time = datetime.strptime(dict_doc['selected_time'], '%Y-%m-%dT%H:%M')
                    selected_time_plus = datetime.strptime(dict_doc['selected_time'], '%Y-%m-%dT%H:%M') + datetime.timedelta(hours = 1)
                    other_selected_time = datetime.strptime(doc.to_dict()[d][1], '%Y-%m-%dT%H:%M')
                    if selected_time <= other_selected_time and selected_time_plus >= other_selected_time: 
                        InOrder += 1
                    else:
                        pass
                except:
                    pass

        oreferencenumber = datetime.now().strftime("%Y%m%d%H%M%S") # 訂位編號
        data = event.postback.data.split(' ') # [1]: OrderName, [2]:Selected Time, [3]:number of man, [4]: Selected Seat, [5]:UserId
        print(data)
        doc_ref = firedb.collection('是否訂位').document(data[4])
        doc = doc_ref.get()
        firebase_rec['step'] = 'F'
        firebase_rec['status'] = 'free'
        firebase_rec['InOrder'] = str(InOrder)
        firebase_rec['orfn'] = oreferencenumber
        doc_ref.update(firebase_rec) # 接收並更新db的time
        
        rec = data[1:4] # rec[0]: OrderName, rec[1]:Selected Time, rec[2]:number of man, rec[3]:Selected Seatm, rec[4]:UserId
        ord_ref = firedb.collection('訂位紀錄').document(data[4])
        
        order_rec = {} 
        if ord_ref.get().to_dict() == None: # 無過往紀錄
            order_rec['record_1'] = rec
            ord_ref.set(order_rec)
        else:
            checkrec = 'record_'+str(len(ord_ref.get().to_dict()))
            lenrec = 'record_'+str(len(ord_ref.get().to_dict())+1)
            # 如果跟前一筆一樣的話 代表重複同意
            try:
                if ord_ref.get().to_dict()[checkrec][0] in rec[0] and ord_ref.get().to_dict()[checkrec][2] in rec[2] and ord_ref.get().to_dict()[checkrec][1] in rec[1] and ord_ref.get().to_dict()[checkrec][3] in rec[3]:
                    line_bot_api.push_message(UserId, TextSendMessage(text='已有其他管理員同意訂位, 本次同意不列入紀錄!'))
                    return 0
                else:
                    rec.append(str(InOrder))
                    rec.append(oreferencenumber) # 訂單編號
                    order_rec[lenrec] = rec
                    ord_ref.update(order_rec)
            except:
                rec.append(str(InOrder))
                rec.append(oreferencenumber) # 訂單編號
                order_rec[lenrec] = rec
                ord_ref.update(order_rec)
        
        doc = doc_ref.get()
        dict_doc = doc.to_dict()
        OrderMessage = AllMessage.Order_Message(dict_doc) # 回傳給Customer端成功訊息
        line_bot_api_client.push_message(data[4], OrderMessage)
        
        reply_message = '姓名: ' + data[1] + "\n訂單編號: " + oreferencenumber +'\n預約日期: ' + data[2].split('T')[0] + '\n預約時間: ' + data[2].split('T')[1] + '\n預約人數: ' +  data[3] + '\n預約順位: ' + str(InOrder) + '\n預約座位: 無'
        
        doc_ref = firedb.collection_group('控制端')
        docs = doc_ref.stream() # generator
        for doc in docs:
            line_bot_api.push_message(doc.to_dict()['User_Id'] , TextSendMessage(
                text='管理員 {0} 已同意客人訂位!\n訂單詳細內容如下:\n{1}'.format(profile.display_name, reply_message)) )
                #text='管理員 {0} 已同意客人訂位!\n訂單詳細內容如下:\n{1}'.format(profile.display_name, reply_message)) )
        return 0

    ''' 訂位功能step6 - 拒絕訂位 '''
    if 'no' in event.postback.data:
        firebase_rec['step'] = '4'
        doc_ref.update(firebase_rec) # 接收並更新db的time
        data = event.postback.data.split(' ') # [1]: OrderName, [2]:Selected Time, [3]:number of man, [4]:UserId
        reply_message = '姓名: ' + data[1] + '\n時間: ' + data[2].replace('T',' ') + '\n人數: ' +  data[3]
        line_bot_api_client.push_message(data[4], TextSendMessage(text='店家拒絕此次訂位!\n麻煩請於上方選時間處選其它時刻，感謝您~'))
        doc_ref = firedb.collection_group('控制端')
        docs = doc_ref.stream() # generator
        for doc in docs:
            line_bot_api.push_message(doc.to_dict()['User_Id'] , TextSendMessage(
                text='管理員 {0} 已拒絕客人訂位!\n訂單詳細內容如下:\n{1}'.format(profile.display_name, reply_message)) )
        return 0    

    ''' Manager取消功能step2 '''
    if event.postback.data == 'selected time':
        SelectTime = event.postback.params['date'] # 根據時間搜尋database # ex.2020-01-16
        ManagerCancelMessage = AllMessage.Manager_Cancel_Message(SelectTime)
        line_bot_api.push_message(UserId, ManagerCancelMessage)
        return 0

    ''' Manager取消功能step3 '''
    if "cancel" in event.postback.data:
        data = event.postback.data.split(' ') # 1:Customer Name, 2:Customer SelectTime, 3: num of customer
        doc_ref = firedb.collection_group('訂位紀錄')
        docs = doc_ref.stream() # generator
        # 1個ID(collection)算一次迴圈
        for doc in docs:
            for d in doc.to_dict(): # for each in dict
                try:                    
                    if (datetime.strptime(doc.to_dict()[d][1], '%Y-%m-%dT%H:%M') == datetime.strptime(data[2], '%Y-%m-%dT%H:%M')) and doc.to_dict()[d][0] in data[1] and doc.to_dict()[d][2] in data[3]: # 跟選取的為同一天
                        doc_ref = firedb.collection('訂位紀錄').document(doc.id)
                        cancel_rec = {}
                        cancel_rec[d] = None
                        doc_ref.update(cancel_rec) # 用None取代
                except:
                    pass
        reply_message = "姓名: " + data[1] + "\n訂位時間: " + data[2].replace('T',' ')+ "\n人數: " + data[3] + "\n桌號: " + data[4]
        line_bot_api_client.push_message(data[4], TextSendMessage(text='店家已取消您的訂位!\n訂單詳細內容如下:\n{0}'.format(reply_message))) # Client
        profile = line_bot_api.get_profile(UserId)
        doc_ref = firedb.collection_group('控制端')
        docs = doc_ref.stream() # generator
        for doc in docs:
            line_bot_api.push_message(doc.to_dict()['User_Id'] , TextSendMessage(
                text='管理員 {0} 已取消客人訂位!\n訂單詳細內容如下:\n{1}'.format(profile.display_name, reply_message)) )
        return 0

    else:
        line_bot_api.reply_message(ert, TextSendMessage(text='無效操作') )
        return 0
    #print(event.postback.params['datetime']) # {"data": "seleced", "params": {"datetime": "2019-12-21T18:44"}}


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 綁webhook
    if event.reply_token == '00000000000000000000000000000000':
        return 'ok'
    UserId = event.source.user_id
    UserMessage = event.message.text
    ert = event.reply_token
    firebase_rec = {}
        
    if '目前訂位' in UserMessage:# in c:
        doc_ref = firedb.collection_group('訂位紀錄')
        docs = doc_ref.stream() # generator
        reply_message = '目前有以下訂位: '
        for doc in docs:
            dic = doc.to_dict()
            for record in dic:
                try:
                    if datetime.strptime(dic[record][1], '%Y-%m-%dT%H:%M') > datetime.now():
                        reply_message += '\n\n姓名: ' + dic[record][0] + '\n預約時間: ' + dic[record][1].replace('T',' ') + "\n人數: " + dic[record][2]
                    else:
                        pass
                except: # NoneType
                    pass
            #print(u'{} => {}'.format(doc.id, doc.to_dict()))
        line_bot_api.reply_message(ert, TextSendMessage(text=reply_message) )
        return 0

    ''' 發送公告step1 '''
    if '發送公告' in UserMessage: 
        firebase_rec['step'] = 'b1'
        doc_ref = firedb.collection('發送公告').document(UserId)
        doc_ref.set(firebase_rec)
        line_bot_api.reply_message(ert, TextSendMessage(text="注意!!!\n下一句傳輸之訊息將會公告給所有客人，請確保訊息無誤再傳輸!") )
        return 0
    
    ''' 發送公告step2 '''
    doc_ref = firedb.collection('發送公告').document(UserId)
    doc = doc_ref.get()
    if doc.to_dict()['step'] == 'b1' and '目前訂位' not in UserMessage and '取消訂位' not in UserMessage and '發送公告' not in UserMessage:
        firebase_rec['step'] = 'b2'
        doc_ref = firedb.collection('發送公告').document(UserId)
        doc_ref.update(firebase_rec) # update 狀態

        doc_ref = firedb.collection_group('客戶端') # 收集客戶端全部的 User Id
        docs = doc_ref.stream() # generator
        for doc in docs:
            dic = doc.to_dict()
            line_bot_api_client.push_message(dic['User_Id'], TextSendMessage(text=UserMessage) ) # 客戶端的LineBot會傳公告訊息給客戶
        
        profile = line_bot_api.get_profile(UserId)
        doc_ref = firedb.collection_group('控制端')
        docs = doc_ref.stream() # generator
        for doc in docs:
            line_bot_api.push_message(doc.to_dict()['User_Id'] , TextSendMessage(
                text='管理員 {0} 已發送公告!\n公告內容如下:\n{1}'.format(profile.display_name, UserMessage)) )
        return 0
    elif doc.to_dict()['step'] == 'b1':
        firebase_rec['step'] = 'b2'
        doc_ref = firedb.collection('發送公告').document(UserId)
        doc_ref.update(firebase_rec)
        line_bot_api.reply_message(ert, TextSendMessage(text='取消公告'))
        if '目前訂位' in UserMessage:
            doc_ref = firedb.collection_group('訂位紀錄')
            docs = doc_ref.stream() # generator
            reply_message = '目前有以下訂位: '
            for doc in docs:
                dic = doc.to_dict()
                for record in dic:
                    try:
                        if datetime.strptime(dic[record][1], '%Y-%m-%dT%H:%M') > datetime.now():
                            reply_message += '\n\n姓名: ' + dic[record][0] + '\n預約時間: ' + dic[record][1].replace('T',' ') + "\n人數: " + dic[record][2]
                        else:
                            pass
                    except: # NoneType
                        pass
            line_bot_api.reply_message(ert, TextSendMessage(text=reply_message) )
            return 0
        elif '取消訂位' in UserMessage:
            TimeMessage = AllMessage.Time_Message()
            line_bot_api.reply_message(ert, TimeMessage) # 傳送選擇日期的Message
            return 0
        elif '發送公告' in UserMessage:
            firebase_rec['step'] = 'b1'
            doc_ref = firedb.collection('發送公告').document(UserId)
            doc_ref.set(firebase_rec)
            line_bot_api.reply_message(ert, TextSendMessage(text="注意!!!\n下一句傳輸之訊息將會公告給所有客人，請確保訊息無誤再傳輸!") )
            return 0

        return 0
    
    ''' Manager取消客戶訂位step1 '''
    if '取消訂位' in UserMessage:
        TimeMessage = AllMessage.Time_Message()
        line_bot_api.reply_message(ert, TimeMessage) # 傳送選擇日期的Message
        return 0
    
    ''' 清空過往訂單(暫時沒有開放) '''
    if '清空' in UserMessage:
        doc_ref = firedb.collection_group('訂位紀錄')
        docs = doc_ref.stream() # generator
        # 1個ID(collection)算一次迴圈
        for doc in docs:
            for d in doc.to_dict(): # for each in dict
                try:                    
                    if (datetime.strptime(doc.to_dict()[d][1].split("T")[0], '%Y-%m-%d') < datetime.today()):
                        doc_ref = firedb.collection('訂位紀錄').document(doc.id)
                        cancel_rec = {}
                        cancel_rec[d] = None
                        doc_ref.update(cancel_rec) # 用None取代
                except:
                    pass

    else:
        line_bot_api.reply_message(ert, TextSendMessage(text='無效操作') )
        return 0


# 使用者加入Line好友的時候
@handler.add(FollowEvent)
def handle_follow(event):
    UserId = event.source.user_id # 將新加入的(follow)使用者資訊寫入資料庫中
    user_rec = {}
    profile = line_bot_api.get_profile(UserId)
    user_rec['User_Id'] = UserId
    user_rec['User_Name'] = profile.display_name
    user_rec['User_imgurl'] = profile.picture_url
    doc_ref = firedb.collection('控制端').document(UserId)
    doc_ref.set(user_rec)
    # 發送「歡迎加入」給使用者
    line_bot_api.reply_message( event.reply_token, TextSendMessage(text='歡迎使用瑋瑋快易點\n此LineBot為控制端'))

# 初始化客戶端和控制端的Rich Menu圖文選單
def init_richmenu():
    doc_ref = firedb.collection_group('控制端')
    docs = doc_ref.stream() # generator
    for doc in docs:
        dic = doc.to_dict() 
        line_bot_api.link_rich_menu_to_user(dic['User_Id'], Richmenu_Server_Id) # 連控制端的richmenu

# 使用者封鎖Line帳號的時候
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    doc_ref = firedb.collection('控制端').document(event.source.user_id)
    doc_ref.delete()


if __name__ == "__main__":
    init_richmenu()
    app.run()