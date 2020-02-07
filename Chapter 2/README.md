
## ソケットタイプ
|ソケットタイプ|意味|
----|----
|SOCK_STREAM|順序性と信頼性があり、双方向の接続されたバイトストリーム（byte stream）を提供する(TCP)|
|SOCK_DGRAM|データグラム（接続、信頼性なし、固定最大長メッセージ）をサポートする(UDP)|
<br>
「ストリームソケット」:TCP を使用したプロセスの通信を可能にする<br>
「データグラムソケット」：UDP を使用したプロセスの通信を可能にする<br>
「raw ソケット」:ICMP へのアクセスを提供する

## アドレスファミリ
|アドレスファミリ|意味|
----|----
|AF_INET|IPv4 によるソケット |
|AF_INET6 |IPv6 によるソケット |

**[簡易的なTCPクライアントの作成](https://github.com/mizuirorivi/cyber-security-programming_by_python/blob/master/Chapter%202/tcpclient.py)**
```python
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

```


**[簡易的なUDPクライアントの作成](https://github.com/mizuirorivi/cyber-security-programming_by_python/blob/master/Chapter%202/udpclient.py)**
```python
import socket

target_host = "www.google.com"
target_port=80

#socketオブジェクトの作成
#UDPではSOCK_DGRAMを使う
socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#UDPはコネクションレス型プロトコルなので、データを送る前にconnect()を呼ぶ必要はない
#データの送信
#udpだとsendoto?
socket.sendto(b"AAABBBCCC",(target_host,target_port))
#socket.recvfrom({バイト数}):{バイト数}だけデータを受けとり、byte型[byte]と
data, addr = socket.recvfrom(4096)

print(data)
```

**[簡易的TCPサーバの作成](https://github.com/mizuirorivi/cyber-security-programming_by_python/blob/master/Chapter%202/TCPserver.py)**
```python
import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#接続を待ち受けるIPアドレスとポート番号の指定
server.bind((bind_ip,bind_port))
#接続キューの最大数を5として待受けを開始する
server.listen(5)
print("[*] Listening on {0}:{1}".format(bind_ip,bind_port))

#クライアントからの接続を処理するスレッド
def handle_client(client_socket):
    #クライアントが送信してきたデータを表示
    request = client_socket.recv(1024)
    print("[*] Received:{0}".format(request))

    #パケットの返送
    client_socket.send(b"ACK!")
    client_socket.close()

while True:
    client, addr = server.accept()
    print("[*] Accepted connection from: {0}:{1}".format(addr[0],addr[1]))

    #受信データを処理するスレッドの起動
    client_handler = threading.Thread(target=handle_client,args=(client,))
    #スレッドの開始
    client_handler.start()

```
**[簡易的はHTTPサーバ]()**
```python
import socket 
from threading import Thread
from datetime import datetime

buf_size = 1024
bind_ip = "0.0.0.0"
bind_port = 8000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))

server.listen(5)

print("[*] Listening on {0}:{1}".format(bind_ip,bind_port))

def handle_client(client_socket):
    request = client_socket.recv(buf_size)
    print("[*]Received:\n{}{}".format(request.decode('utf-8'),"-"*24))

    now = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    html = """<!DOCTYPE html><html lang="ja"><body><p>Test Server<p></body></html>"""
    header = """HTTP/1.0 200 OK\r\nDate: {}\r\nServer:Test Http Server\r\nContent-Type: text/html;charset=utf-8\r\n\r\n""".format(now)
    if request.startswith(b'HEAD'):
        client_socket.send(header.encode('utf-8'))
    elif request.startswith(b'GET'):
        response = header[:-2]+"Content-Length:{}\r\n".format(len(html))+"\r\n"+html
        client_socket.send(response.encode('utf-8'))

while True:
    client, addr = server.accept()
    print("[*] Accpeted connection from:{}:{}".format(addr[0],addr[1]))
    client_handler = Thread(target=handle_client,args=[client])
    client_handler.start()
```
|python_function|意味|
----|----
|socket.accept()|接続を受け付けます。ソケットはアドレスにbind済みで、listen中である必要があります。戻り値は (conn, address) のペアで、 conn は接続を通じてデータの送受信を行うための 新しい ソケットオブジェクト、 address は接続先でソケットにbindしているアドレスを示します。|
|class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)|コンストラクタは常にキーワード引数を使って呼び出さなければなりません。各引数は以下の通りです:<br>target は run() メソッドによって起動される呼び出し可能オブジェクトです。デフォルトでは何も呼び出さないことを示す None になっています。<br>args は target を呼び出すときの引数タプルです。デフォルトは () です。|


## 疑問点
1. ローカルホストにサーバ(TCPserver.py)を建てて、そこに対してtcpclientを実行して繋ぐことは出来たけど、
virtualboxで仮想環境を建てた時にはうまくいかなかった。おそらく、ネットワークに対しての知見とvirtualboxに対しての知見が足りなかったのだと思う。

## 参考リンク

https://ja.wikipedia.org/wiki/Raw_socket<br>
https://docs.python.org/ja/3/library/socket.html<br>
https://qiita.com/__init__/items/5c89fa5b37b8c5ed32a4<br>
https://docs.python.org/ja/3/library/threading.html#threading.Thread<br>
https://engineeringnote.hateblo.jp/entry/python/bhp/2-4<br>
https://engineeringnote.hateblo.jp/entry/python/bhp/2-5#Netcat%E3%81%A8%E3%81%AF

<br>

<p><a href="https://www.amazon.co.jp/gp/product/4873117313/ref=as_li_tl?ie=UTF8&camp=247&creative=1211&creativeASIN=4873117313&linkCode=as2&tag=engineeringnote-22&linkId=5070b718494dc6c144d41fc0ef0d4d78"><img src="https://images-na.ssl-images-amazon.com/images/I/518ZyCCEKGL._SX350_BO1,204,203,200_.jpg" width=100></a></p>
