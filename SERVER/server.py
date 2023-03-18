import socket
import threading
import time
import gc
import sys
import random
############################################################################################################################################################################################################
class private_data() :
    def __init__(self) :
        self.allowed_ip = ["192.168.64.112","127.0.0.1"]
        self.token = True
        self.passwd = "123456789"
        self.key = "qazwsxedc"
############################################################################################################################################################################################################
class data() :
    def __init__(self) :
        self.message_queue = []
        self.message_queue_length = len(self.message_queue)

    def put_message(self, message) :
        self.message_queue.append(message)
        self.message_queue_length += 1

    def get_message(self) :
        try :
            self.message_queue_length -= 1
            return self.message_queue.pop(0)
        except : return ""

    def get_queue_length(self) :
        return self.message_queue_length

############################################################################################################################################################################################################
class data_stream_server() :
    def __init__(self, data) :
        self.server_status = True 

        self.clients = [] 
        self.clients_to_be_disconnected = []

        self.server_socket = socket.socket()
        print("socket created successfully")

        print(socket.gethostbyname(socket.gethostname()))

        self.server_port = 12345
        self.server_socket.bind(("", self.server_port))
        print("socket bind to port :", self.server_port)
        
        self.server_socket.listen(0) 
        self.server_socket.settimeout(1)
        print("socket is listening...")
        
        self.thread_lock = threading.Lock()
        print("created lock object...")

        self.data = data 

        self.server_main_thread = threading.Thread(target = self.server_mainloop , args = ())
        self.server_main_thread.start()

        self.message_sending_thread = threading.Thread(target = self.message_sending_loop, args = ())
        self.message_sending_thread.start()
        
        self.close_clients = threading.Thread(target = self.client_closing_loop ,args = ())
        self.close_clients.start()

    def message_sending_loop(self) :
        while self.server_status :
            if self.data.get_queue_length() != 0 :
                self.message_to_be_sent = self.data.get_message()
                for __ in self.clients :
                    try :
                        if __.can_recv_data :
                            if self.message_to_be_sent != "" :
                                __.send_data(self.message_to_be_sent)
                                print(self.message_to_be_sent)
                    except : pass
            else :
                time.sleep(1/60)                

    def server_mainloop(self) :
        print("server mainloop running...")
        while self.server_status :
            self.thread_lock.acquire()
            try :
                self.clients.append(client_connection_object(self.server_socket.accept(), self))
                self.clients[-1].par = self 
                self.clients[-1].data = self.data
                self.clients[-1].main_loop.start()
            except :
                print("no connection recieved")
            self.thread_lock.release()
        self.server_socket.close()
        print("server stopped !!")

    def client_closing_loop(self) :
        while (self.server_status or self.clients != []) :
            time.sleep(1) #:)
            for _ in self.clients :
                
                if (_.client_address ,_.client_port) in self.clients_to_be_disconnected :
                    #self.thread_lock.acquire()
                    self.qaz = (_.client_address ,_.client_port)
                    _.empty_client()

                    self.clients.remove(_)
                    print("deleted",self.qaz,"from home_server.clients")
                    self.clients_to_be_disconnected.remove(self.qaz)
                    print("removed",self.qaz,"from list of home_server.ip_to_be_deleted")
                    del self.qaz
                    print("client_list :" ,self.clients_to_be_disconnected)
                    #self.thread_lock.release()
            gc.collect()
        gc.collect()

############################################################################################################################################################################################################
class client_connection_object() :
    def __init__(self, connection, parent ) :
        self.client_status = True

        self.par = None
        self.data = None

        self.can_recv_data = False

        self.client_connection = connection[0]
        self.client_address = connection[1][0]
        self.client_port = connection[1][1] 
        print("got request from >" ,self.client_address ,"   ._._._._._._.")

        self.client_connection.settimeout(60*2)
        self.number_of_empty_responces = 0
        
        self.main_loop = threading.Thread(target = self.client_main_loop , args=())

        self.client_response = ""

    def client_main_loop(self) :
        print("client main loop running")
        self.send_initialising_data()
        
        try :
            temp = self.client_connection.recv(1024)
            self.client_response = ""
        except :
            self.par.clients_to_be_disconnected.append((self.client_address, self.client_port))
        
        self.can_recv_data = True
        
        while self.client_status :
            #try :
            try :
                self.client_temp_response = self.client_connection.recv(1024).decode('utf-8')
            except Exception as e :
                #self.number_of_empty_responces += 1
                self.client_temp_response = ""
                print(e)
            self.client_response += self.client_temp_response

            if self.client_temp_response == "" :
                self.number_of_empty_responces += 1
                print("incrementad")
            else :
                self.number_of_empty_responces = 0

            while chr(1)+chr(2) in self.client_response :
                temp_offset = self.client_response.find(chr(1)+chr(2))
                temp_message = self.client_response[:temp_offset+2]
                self.client_response = self.client_response[temp_offset+2:]
                if temp_message != chr(1)+chr(2) :
                    #self.par.thread_lock.acquire()
                    self.data.put_message(temp_message)
                    #self.par.thread_lock.release()
                    print(temp_message, "from", self.client_address,self.client_port)
                else : pass

                #print(self.data.message_queue)

                print("recieved")
            #except :
            #    self.number_of_empty_responces += 1

            #print(self.number_of_empty_responces)

            if self.number_of_empty_responces > 3 :
                self.client_status = False
            time.sleep(1) #:)

        self.par.clients_to_be_disconnected.append((self.client_address, self.client_port))
    
    def send_data(self, message) :
        self.data_str = ""
        self.client_connection.send(bytes(message, "utf-8"))


    def send_initialising_data(self) :
        data_str = "qwe12341234qazqaz"
        
        data_str += "!"
        self.client_connection.send(bytes(data_str, "utf-8"))

    def empty_client(self) :
        time.sleep(0.5) #:)
        self.can_recv_data = False
        self.client_connection.close()
        try :
            del self.client_status
        except :
            pass
        try :
            del self.par
        except :
            pass
        try :
            del self.client_connection
        except :
            pass
        try :
            del self.client_address
        except :
            pass
        try :
            del self.client_port
        except :
            pass
        try :
            del self.number_of_empty_responces
        except :
            pass
        try :
            del self.thread_lock
        except :
            pass
        try :
            del self.main_loop
        except :
            pass
        try :
            del self.client_response
        except :
            pass
        try :
            del self.data_str
        except :
            pass
        try :
            del self._
        except :
            pass
        try :
            del self.data
        except :
            pass
        try :
            del self.can_recv_data
        except :
            pass
        print("emptied client")
############################################################################################################################################################################################################
if __name__ == "__main__" :
    data_ = data()
    gc.enable() #enabling automatic garbage collection

    server_private = private_data() 
    home_server = data_stream_server(data_)

    qaz=input("press enter to stop server...")
    home_server.server_status = False

    print("trying to close server...")
    home_server.server_main_thread.join()
