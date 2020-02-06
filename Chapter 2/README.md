
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

target_host = "www.google.com"
target_port = 80

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


[簡易的なUDPクライアントの作成]()
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




**参考リンク**<br>
https://ja.wikipedia.org/wiki/Raw_socket<br>
https://docs.python.org/ja/3/library/socket.html<br>
https://qiita.com/__init__/items/5c89fa5b37b8c5ed32a4<br>