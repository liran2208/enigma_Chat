import socket
import _thread
import threading
import sys
import enigma
from os import system
# -----daily enigma key & settings---------
rotors = [1, 2, 3, 'a']
states = [1, 1, 1]
rotors = enigma.initialize_states(rotors, states)
plugboard = ["ab", "xy", "hj", "po", "mn", "ld", "qw", "fr", "ev", "zs"]
# -----------------------------------------
def receive_messages(recieve_socket):
    while True:
        msg = recieve_socket.recv(1024).decode()
        print (enigma.cypher(msg, rotors, plugboard))


def send_messages(send_socket, userName):
    while True:
        msg = input()
        send_socket.send((enigma.cypher(userName + ": " + msg, rotors, plugboard)).encode())


def main():
    system('cls')
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
        
    userName = input("Connected. Welcome To This Chatroom. please enter username: ")
    
    t = threading.Thread(target=receive_messages, args=(my_socket, ))
    j = threading.Thread(target=send_messages, args=(my_socket, userName))
    t.start()
    j.start()
    t.join()
    j.join()
    
if __name__ == '__main__':
    main()
