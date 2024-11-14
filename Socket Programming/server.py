# Server

from socket import socket

s = socket()

port = 12345
s.bind(('localhost', port))

print("Next Action?")
print("Menu:")
print("1) Wait for connection from client for next pickup request")
print("2) Dequeue")
menu_option = input("Type an option: ")

if menu_option == '1':
    # Connecting to client and receiving data
    s.listen(3)
    print('Awaiting connection from pickup client...')
    
    while True:
        c, addr = s.accept()
        print('Connection established!')
        
        print('Receiving data from client...')
        data = c.recv(4096)
        data = data.decode()
        
        print("Checking client's secret key...")
        
        try:
            # client's data = "[password, team name, group's size]"
            data = decrypt(password, data)
            temp = data
            data = eval(data)
            if generateKey(data[0],temp) == generateKey(password,temp):
                print("Client's secret key is correct!")

                print(f"Client's Team name: {data[1]}")
                print(f"Group size: {data[2]}")
                print(f"Number of passengers in queue: {q.current_size()}")
                
                if (266-q.current_size()) > data[2]:
                    print("You have capacity for them.")
                    confirm = input("Confirm pickup (Y/N): ")
                    if confirm == 'Y':
                        for i in range(data[2]):
                            q.enqueue(data[1])
                        print("Added to queue. Items in queue now are:")
                        q.display()
                        server_data = "Accepted"
                        server_data = encrypt(password, server_data)
                        c.send(server_data.encode())
                        c.close()
                        print("Connection disconnected.")
                        break
                        
                    if confirm == 'N':
                        server_data = "Rejected"
                        server_data = encrypt(password, server_data)
                        c.send(server_data.encode())
                        c.close()
                        print("Connection disconnected.")
                        break
                
                if (266-q.current_size()) < data[2]:
                    print("You do NOT have the capacity for them.")
                    server_data = "Rejected"
                    server_data = encrypt(password, server_data)
                    c.send(server_data.encode())
                    c.close()
                    print("Connection disconnected.")
                    break
                
            else:
                print("Wrong secret key.")
                server_data = "No access"
                server_data = encrypt(password,server_data)
                c.send(server_data.encode())
                c.close()
                print("Connection disconnected.")
                break
                
        except:
            print("Wrong secret key.")
            server_data = "No access"
            server_data = encrypt(password,server_data)
            c.send(server_data.encode())
            c.close()
            print("Connection disconnected.")
            break

    
if menu_option == '2':
    if q.dequeue() == "Queue is empty!":
        print(q.dequeue())
        s.close()
        print("Connection disconnected.")
    else:
        num = int(input("How many to dequeue: "))
        for i in range(num):
            q.dequeue()
        print("Items in queue now are:")
        q.display()
        s.close()
        print("Connectiom disconnected.")
        
