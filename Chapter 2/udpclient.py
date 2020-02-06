import socket

target_host = "www.google.com"
target_port=80

#socketオブジェクトの作成
#UDPではSOCK_DGRAMを使う
socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#データの送信
#udpだとsendoto?
socket.sendto(b"AAABBBCCC",(target_host,target_port))

data,addr = socket.recvfrom(4096)

print(data)