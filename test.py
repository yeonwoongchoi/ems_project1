
import logging
import eventlet
import time
import json
from flask_bootstrap import Bootstrap
import paho.mqtt.client as paho

broker = "localhost"

data_char= []
def on_connect( client, userdata, flags, rc):
        print ("connect with result code "+str(rc))
        client.subscribe("temp")

def on_message(client, userdata, message):
    time.sleep(1)
    recvData = str(message.payload.decode("utf-8"))
    print(recvData)
    data_char.append(recvData)
    print(data_char)
    print("received message =", recvData)
    # return recvData

    # print("received message =", recvData)
    # jsonData = json.loads(recvData) #json 데이터를 dict형으로 파싱
    # print("Temprature : " + str(jsonData["Temp"]))
    # print("Humiditiy : " + str(jsonData["Humi"]))

# client = paho.Client()
# client.on_message = on_message

# client = paho.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect(broker, 1883)#connect
# client.loop_start() #start loop to process received messages


client = paho.Client()
client.on_connect = on_connect
client.on_message = on_message
print("jflsj",data_char)
client.connect('localhost', 1883, 60)
client.loop_forever()



# while True:
    
#     data = message.payload.decode("utf-8")
#     print('data : ' + str(data))
#     print("connecting to broker ",broker)
   
#     print("subscribing ")


#     client.subscribe("temp")#Sensor 토픽을 구독해 줍니다.
#     client.on_message
    
#     time.sleep(5)
#     client.disconnect() #disconnect
#     client.loop_stop() #stop loop
#     time.sleep(5)