import socket

target_host = "127.0.0.1"
target_port = 9999

#ソケットオブジェクトの作成
#AF_INETは標準的なIPv4のアドレスやホスト名を使用することを指していて、SOCK_STREAMはTCPを用いることを示している
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#サーバへの接続
client.connect((target_host,target_port))
#データの送信
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
#データの受信
while(True):
    response = client.recv(4096)
    if len(response)>0:
        print(response)
        break
