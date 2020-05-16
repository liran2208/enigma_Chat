import socket
import _thread
import threading
import time
import sys
import enigma
from os import system
import datetime
# -----daily enigma key & settings---------
rotors = [5, 3, 1, 'b']
states = [21, 13, 11]
rotors = enigma.initialize_states(rotors, states)
plugboard = ["ab", "xy", "hj", "po", "mn", "ld", "qw", "fr", "ev", "zs"]
# -----------------------------------------
def receive_messages(recieve_socket):
    while True:
        msg = recieve_socket.recv(1024).decode()
        print (enigma.cypher(msg, rotors, plugboard))
        # print (recieve_socket.recv(1024).decode())

def send_messages(send_socket, userName):
    while True:
        msg = input()
        if msg == "exit()":
            print ("exiting code...")
            # send_socket.close()
            sys.exit()
        send_socket.send((enigma.cypher(userName + ": " + msg, rotors, plugboard)).encode())
        # send_socket.send(input().encode())

def main():
    system('cls')
    """
    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        exit()
    """
    my_socket = socket.socket()

    again = True
    while again:
        try: 
            
            IP_address = str(input("Enter the chat's IP: ")) # str(sys.argv[1])
            Port = int(input("Enter the chat's port number: ")) # int(sys.argv[2])
            
            my_socket.connect((IP_address, Port))
            again = False
        except Exception as e:
            print (e)
            system('cls')
            print ("IP/Port not found. please try again")
            again = True
        
    # my_socket.connect((IP_address, Port))
    userName = input("Connected. Welcome To This Chatroom. please enter username: ")
    # print (my_socket)
    t = threading.Thread(target=receive_messages, args=(my_socket, ))
    j = threading.Thread(target=send_messages, args=(my_socket, userName))
    t.start()
    j.start()
    t.join()
    j.join()
    """
    time.sleep(1)  #this delay lets the threads kick in, otherwise the thread count is zero and it crashes
    while _thread._count() > 1:
        pass
    """

if __name__ == '__main__':
    main()
