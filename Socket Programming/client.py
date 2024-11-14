# Client

password = input("Please type the password: ")
team_name = input("What is your Team name: ")
group_size = int(input("Group size: "))

client_data = [password, team_name, group_size]
client_data = str(client_data)

from socket import socket

s = socket()

print("Establishing connection...")
port = 12345
s.connect(('localhost', port))
print("Connection established!")

client_data = encrypt(password, client_data)
s.send(client_data.encode())
print("Data sent!")

print("Waiting for the server to confirm your request...")
data = s.recv(4096).decode()
data = decrypt(password, data)

if data == "Accepted":
    print("Pickup confirmed! Please wait for pickup.")
    s.close()
    print("Connection disconnected.")
    
elif data == "Rejected":
    print("Pickup rejected!")
    print("Wrong password or request rejected.")
    print("Please try again.")
    s.close()
    print("Connection disconnected.")
    
else:
    print("Pickup cancelled.")
    print("Wrong password or request rejected.")
    print("Please try again.")
    s.close()
    print("Connection disconnected.")
