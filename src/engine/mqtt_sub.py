import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime, timedelta, timezone

# MySQL接続設定
connection = mysql.connector.connect(host='servdb', user='alice', password='a1icedb%', database='alice_services')

# subするトピック
SUB_TOPIC = 'daq'


# ブローカーに接続した時
def on_connect(client, userdata, flag, rc):
    print('Connected mqtt: ' + str(rc))
    client.subscribe(SUB_TOPIC)


# ブローカーとの接続が切れた時
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected disconnection.')


# メッセージ受信時   pub e.g.  $ mosquitto_pub -h localhost -t test -m 'E7476F72-0824-4E65-8F16-4548DC03326E, DAQ, test_0, 2.4'
def on_message(client, userdata, message):
    try:
        # print('Received message ' + str(message.payload) + 'on topic' + message.topic + 'with QoS' + str(message.qos))

        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(JST)
        # 受信メッセージをカンマでセパレート
        data_values = message.payload.decode('utf-8')
        data_values = [x.strip() for x in data_values.split(',')]

        # MySQLクエリ
        cursor = connection.cursor()
        node_id_query = "SELECT id, registration_code FROM node WHERE registration_code=%s"
        cursor.execute(node_id_query, (str(data_values[0]),))
        node_id = cursor.fetchone()

        sql = "INSERT INTO data(id, node, data_type, data_category, data_value, daq_datetime) VALUES (null, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            node_id[0], str(data_values[1]), str(data_values[2]), float(data_values[3]), str(now),))
        connection.commit()
        cursor.close()
        # MySQLに常時接続するためにコメントアウト
        # connection.close()
    except ValueError as e:
        # print('Catch ValueError: ', e)
        pass


# MQTT settings
# インスタンス生成
client = mqtt.Client()
# 接続時のコールバック
client.on_connect = on_connect
# 切断時のコールバック
client.on_disconnect = on_disconnect
# メッセージ受信時のコールバック
client.on_message = on_message

# Broker settings
BROKER_HOST = 'mqtt'
PORT_NUM = 1883
KEEPALIVE = 60

# ブローカーに接続
client.connect(BROKER_HOST, PORT_NUM, KEEPALIVE)

# Listen
client.loop_forever()
