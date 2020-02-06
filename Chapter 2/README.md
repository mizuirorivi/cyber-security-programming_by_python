**ソケットタイプ**<br>
「ストリームソケット」:TCP を使用したプロセスの通信を可能にする<br>
「データグラムソケット」：UDP を使用したプロセスの通信を可能にする<br>
「raw ソケット」:ICMP へのアクセスを提供する

[簡易的なtcpクライアントの作成](https://github.com/mizuirorivi/cyber-security-programming_by_python/blob/master/Chapter%202/tcpclient.py)
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










**参照リンク**<br>
https://ja.wikipedia.org/wiki/Raw_socket
