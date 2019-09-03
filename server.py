
import socket, select

# fungsi untuk mengirim pesan ke semua klien yang terkoneksi
def send_to_all (sock, message):
 # pesan tidak diteruskan dan pesan kembali kepada pengirim
 for socket in connected_list:
  if socket != server_socket and socket != sock :
   try :
    socket.send(message)
   except :
    # if connection not available
    socket.close()
    connected_list.remove(socket)

if __name__ == "__main__":
 name=""
 # dictionary untuk menyimpan alamat yang berhubungan dengan nama pengguna
 record={}
 # List to keep track of socket descriptors
 connected_list = []
 buffer = 4096
 port = 5001

 server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 server_socket.bind(("localhost", port))
 server_socket.listen(10) # mendengar hampir 10 koneksi dalam satu waktu

 connected_list.append(server_socket)

 print "\33[32m \t\t\t\tserver bekerja \33[0m" 

 while 1:
        
  rList,wList,error_sockets = select.select(connected_list,[],[])

  for sock in rList:
   #New connection
   if sock == server_socket:
    # Handle the case in which there is a new connection recieved through server_socket
    sockfd, addr = server_socket.accept()
    name=sockfd.recv(buffer)
    connected_list.append(sockfd)
    record[addr]=""
    #print "record and conn list ",record,connected_list
                
                #if repeated username
    if name in record.values():
     sockfd.send("\r\33[31m\33[1m nama pengguna sudah digunakan\n\33[0m")
     del record[addr]
     connected_list.remove(sockfd)
     sockfd.close()
     continue
    else:
                    #add name and address
     record[addr]=name
     print "Klien (%s, %s) terhubung" % addr," [",record[addr],"]"
     sockfd.send("\33[32m\r\33[1m selamat datang dalam obrolan'exit' kapanpun untuk keluar\n\33[0m")
     send_to_all(sockfd, "\33[32m\33[1m\r "+name+" masuk dalam obrolan \n\33[0m")

   # ada pesan masuk dari klien
   else:
    # data dari klien
    try:
     data1 = sock.recv(buffer)
     #print "sock is: ",sock
     data=data1[:data1.index("\n")]
     #print "\ndata received: ",data
                    
                    #get addr of client sending the message
     i,p=sock.getpeername()
     if data == "exit":
      msg="\r\33[1m"+"\33[31m "+record[(i,p)]+" left the conversation \33[0m\n"
      send_to_all(sock,msg)
      print "Klien (%s, %s) sedang tidak terhubung" % (i,p)," [",record[(i,p)],"]"
      del record[(i,p)]
      connected_list.remove(sock)
      sock.close()
      continue

     else:
      msg="\r\33[1m"+"\33[35m "+record[(i,p)]+": "+"\33[0m"+data+"\n"
      send_to_all(sock,msg)
            
                #abrupt user exit
    except:
     (i,p)=sock.getpeername()
     send_to_all(sock, "\r\33[31m \33[1m"+record[(i,p)]+" meninggalkan obrolan secara tiba-tiba\33[0m\n")
     print "Klien (%s, %s) sedang terhubug (error)" % (i,p)," [",record[(i,p)],"]\n"
     del record[(i,p)]
     connected_list.remove(sock)
     sock.close()
     continue



 server_socket.close()
