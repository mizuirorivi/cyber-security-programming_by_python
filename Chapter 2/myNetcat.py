import sys
import socket
import getopt
import threading
import subprocess

#グローバル変数の定義
listen = False
command = False
upload = ""
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print("BHP Net Tool")
    print("Usage: myNetcat.py -t target_host -p port")
    print("-l --listen              - liten on [host]:[port] for")
    print("                           intcoming connections")
    print("-e --execute=file_to_run - execute the fiven file upon")
    print("                           receiving a connection")
    print("-c --command             - initialize a command shell")
    print("-u --upload=destination  - upon receiving connection upload a")
    print("                           file and write to [destination]")
    