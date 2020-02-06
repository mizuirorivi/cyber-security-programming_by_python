import socket

target_host = "127.0.0.1"
target_port=80

#socketオブジェクトの作成
#UDPではSOCK_DGRAMを使う
socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#データの送信
#udpだとsendoto?
socket.sendto("AAABBBCCC",(target_port))

data,addr = socket.recvfrom(4096)

print(data)