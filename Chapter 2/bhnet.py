# coding: utf-8

import sys
import socket
import argparse
import threading
import subprocess

#グローバル変数の定義
listen             = False
command            = False
upload             = False
execute            = ""
target             = ""
upload_distination = ""
port               = 0

desc = """
    BHP Net Tool
    Usage: bhnet.py -t target_host -p port
    -l --listen              - listen on [host]:[port] for
                               incoming connections
    -e --execute=file_to_run - execute the given file upon
                               receiving a connection
    -c --command             - initialize a command shell
    -u --upload=destination  - upon receiving connection upload a
                               file and write to [destination]
    
    
    Examples:
    bhnet.py -t 192.168.0.1 -p 5555 -l -c
    bhnet.py -t 192.168.0.1 -p 5555 -l -u c:\\target.exe
    bhnet.py -t 192.168.0.1 -p 5555 -l -e \"cat /etc/passwd\"
    echo 'ABCDEFGHI' | ./bhnet.py -t 192.168.11.12 -p 135"""

def main():
    global listen
    global port
    global execute
    global command
    global upload_distination
    global target

    global desc

    #コマンドラインオプションの読み込み    
    parse = argparse.ArgumentParser(description=desc)
    parse.add_argument('-l', '--listen', action='store_true')
    parse.add_argument('-e', '--execute')
    parse.add_argument('-c', '--command', action='store_true')
    parse.add_argument('-u', '--upload')
    parse.add_argument('-t', '--target')
    parse.add_argument('-p', '--port', type=int)

    args = parse.parse_args()

    if args.listen:
        listen = True
    if args.execute:
        execute = args.execute
    if args.command:
        command = True
    if args.upload:
        upload_distination = args.upload
    if args.target:
        target = args.target
    if args.port:
        port = args.port

    #接続を待機する？　それとも標準入力からデータを受け取って送信する？
    if not listen and len(target) and port > 0:
        #コマンドラインからの入力を'buffer'に格納する
        #入力が来ないと処理が継続されないので
        #標準入力にデータを送らない場合は、Ctrl-Dを入力
        while True:
            try:
                buffer = input()
            except EOFError:
                break


        #データ送信
        client_sender(buffer.encode('utf-8'))

    #接続待機を開始
    #コマンドラインオプションに応じて、ファイルアップロード
    #コマンド実行、コマンドシェルの実行を行う
    if listen:
        server_loop()

def client_sender(buffer):
    global target
    global port

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #接続ホストへの接続
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:
            #動的ホストからのデータを待機
            recv_len = 1
            response = b""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response.decode('shift-jis'))

            #追加の入力を待機
            buffer = input().encode()

            buffer += b"\n"

            #データの送信
            client.send(buffer)


    except:
        print("[*] Exception! Exiting.")
        #接続の終了
        client.close()

def server_loop():
    global target
    global port

    #待機するIPアドレスが指定されていない場合は
    #すべてのインタフェースで接続を待機
    if not len(target):
        target = "127.0.0.1"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        #クライアントからの新しい接続を処理するスレッドの起動
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    #文字列の末尾の改行を削除
    command = command.rstrip()
    command = command.decode('ascii')
    #コマンドを実行し出力結果を取得
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = b"Failed to execute command."

    #出力結果をクライアントに送信
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    global upload_distination

    # ファイルアップロードを指定されているかどうかの確認
    if len(upload_distination):

        # すべてのデータを読み取り、指定されたファイルにデータを書き込み
        file_buffer = b""

        # 受信データがなくなるまでデータ受信を継続
        while True:
            data = client_socket.recv(1024)

            if len(data) == 0:
                break
            else:
                file_buffer += data

        # 受信したデータをファイルに書き込み
        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # ファイル書き込みの成否を通知
            client_socket.send(
                "Successfully saved file to {}\n".format(upload_distination).encode('utf-8'))
        except:
            client_socket.send(
                "Failed to save file to {}\n".format(upload_distination).encode('utf-8'))


    # コマンド実行を指定されているかどうかの確認
    if len(execute):

        # コマンドの実行
        output = run_command(execute)

        client_socket.send(output)


    # コマンドシェルの実行を指定されている場合の処理
    if command:
        # プロンプトの表示
        prompt = b"<BHP:#>"
        client_socket.send(prompt)

        while True:

            # 改行（エンターキー）を受け取るまでデータを受信
            cmd_buffer = b""
            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # コマンドの実行結果を取得
            response = run_command(cmd_buffer)
            response += prompt

            # コマンドの実行結果を送信
            client_socket.send(response)

if __name__ == '__main__':
    main()