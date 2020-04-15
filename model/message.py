from datetime import datetime, timedelta
from linebot.models import (
    FlexSendMessage, TextSendMessage
)
from App_Config import Firebase_JsonPath
''' firebase setting'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(Firebase_JsonPath)
firedb = firestore.client()
''' firebase setting end '''

class AllMessage():
    
    @staticmethod
    def Time_Message(): # 選日期
        ntime = datetime.now()
        mtime = ntime + timedelta(days = 30)
        if len(str(ntime.month)) == 1:
            month = '0'+str(ntime.month)
        else:
            month = str(ntime.month)
        if len(str(ntime.day)) == 1:
            day = '0'+str(ntime.day)
        else:
            day = str(ntime.day)
        nowtime = str(ntime.year) + '-' + month + '-' + day
        if len(str(mtime.month)) == 1:
            month = '0'+str(mtime.month)
        else:
            month = str(mtime.month)
        if len(str(mtime.day)) == 1:
            day = '0'+str(mtime.day)
        else:
            day = str(mtime.day)
        maxtime = str(mtime.year) + '-' + month + '-' + day
        TimeMessage = FlexSendMessage(
            alt_text='選時間',
            position = 'absolute',
            contents={
                'type': 'bubble', 'direction': 'ltr',
                'hero': {
                    'type': 'image',
                    'url': 'https://i.imgur.com/ezmisvf.jpg',
                    'size': 'full',
                    'action': { 
                        "type":"datetimepicker",
                        "label":"select time", # 方便用post接收資料
                        "data":"selected time",
                        "mode":"date",
                        "initial":nowtime, # format: date
                        "max":maxtime,
                        "min":nowtime
                    }
                }
            }
        )
        return TimeMessage

    @staticmethod
    def Order_Message(dict_doc): # dict_doc = {}, dict_doc['name'], dict_doc['selected_time'], dict_doc['Num_People']
        
        OrderMessage =  FlexSendMessage(
            alt_text='訂位成功!!',
            position = 'absolute',
            contents={
                'type': 'bubble', 'direction': 'ltr',
                'body':{
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "[訂位成功]",
                            "size": "md",
                            #"align": "center",
                            "margin": "md",
                            "color": "#3855FF"
                        },
                        {
                            "type": "text",
                            "text": "姓名 : " + dict_doc['Name'],
                            "size": "md",
                            #"align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "預定日期 : " + dict_doc['selected_time'][:10],
                            "size": "md",
                            #"align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "預定時間 : " + dict_doc['selected_time'][11:],
                            "size": "md",
                            #"align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "預約人數 : " + dict_doc['Num_People'],
                            "size": "md",
                            #"align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "預約順位 : " + dict_doc['InOrder'],
                            "size": "md",
                            #"align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "預約位置 : 暫時不開放",
                            "size": "md",
                            #"align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "text",
                            "text": "訂位編號 : " + dict_doc['orfn'],
                            "size": "md",
                            #"align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        }
                    ]
                },
                'footer': {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "spacer",
                            "size": "xl"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#905c44",
                            "action": 
                            {
                                "type": "message",
                                "label": "我要取消預約",
                                "text": '取消預約'
                            }
                        }
                    ]
                } 
            }
        )

        return OrderMessage

    @staticmethod
    def Manager_Cancel_Message(SelectTime):
        firebase_rec = []
        r = []
        doc_ref = firedb.collection_group('訂位紀錄')
        docs = doc_ref.stream() # generator
        # 1個ID(collection)算一次迴圈
        for doc in docs:
            for d in doc.to_dict(): # for each in dict
                try:
                    print(doc.to_dict()[d][1][:-6])
                    if datetime.strptime(doc.to_dict()[d][1][:-6], '%Y-%m-%d') == datetime.strptime(SelectTime, '%Y-%m-%d'): # 跟選取的為同一天
                        r = doc.to_dict()[d]
                        r.append(doc.id)
                        firebase_rec.append(r)
                except:
                    pass
        Contents = []
        if len(firebase_rec) != 0:
            for t in range(len(firebase_rec)):
                Contents.append(
                    {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    # [['黃先生', '2020-02-08T11:30', '4', 'C桌(4人)', '1', 'Ue7d3f74f2e5108ceadf2faca070a3f50']]
                                    "text": "姓名: " + firebase_rec[t][0] + "\n訂位時間: " + firebase_rec[t][1][-5:] + "\n人數: " + firebase_rec[t][2] + "\n桌號: " + firebase_rec[t][3],
                                    "margin": "md",
                                    "wrap": True
                                },
                                {
                                    "type": "button",
                                    "action":{
                                        "type":"postback",
                                        "label": "取消這位客人",
                                        "data": "cancel " + firebase_rec[t][0] + " " + firebase_rec[t][1] + " " + firebase_rec[t][2] + " " + firebase_rec[t][3] + " " + firebase_rec[t][5]
                                    },
                                    "margin": "md",
                                    "weight": "bold",
                                    "align": "center"
                                }
                            ]
                        },
                        "styles": { "footer": { "separator": True } }
                    }
                )
            ManagerCancelMessage = FlexSendMessage(
                alt_text = '選取欲取消訂位的客人',
                position = 'absolute',
                contents = {
                    "type": "carousel",
                    "contents": Contents
                }
            )
        else:
            ManagerCancelMessage = TextSendMessage(text = "選取日期內沒有客人訂位")

        return ManagerCancelMessage
        