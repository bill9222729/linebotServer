from app import firedb

doc_ref = firedb.collection('發送公告').document(UserId)
doc = doc_ref.get()
for doc in docs:
    dic = doc.to_dict()
    line_bot_api_client.push_message(dic['User_Id'], TextSendMessage(text=UserMessage) ) # 客戶端的LineBot會傳公告訊息給客戶

    doc_ref = firedb.collection('發送公告').document(UserId)
    doc = doc_ref.get()
    if doc.to_dict()[
        'step'] == 'b1' and '目前訂位' not in UserMessage and '取消訂位' not in UserMessage and '發送公告' not in UserMessage:
        firebase_rec['step'] = 'b2'
        doc_ref = firedb.collection('發送公告').document(UserId)
        doc_ref.update(firebase_rec)  # update 狀態

        doc_ref = firedb.collection_group('客戶端')  # 收集客戶端全部的 User Id
        docs = doc_ref.stream()  # generator
        for doc in docs:
            dic = doc.to_dict()
            line_bot_api_client.push_message(dic['User_Id'], TextSendMessage(text=UserMessage))  # 客戶端的LineBot會傳公告訊息給客戶