import socket
import threading
import time
import sys
############################################################################################################################################################################################################
class client() :
    def __init__(self, APP_STATUS) :
        self.APP_STATUS = APP_STATUS
        self.Lock = threading.Lock()
        self.name = " "
        try :
            self.name_file = open("NAME.txt", "r").read()
            if len(self.name_file) > 10 :
                self.name = self.name_file[0:10]
            else :
                self.name = self.name_file
            del self.name_file
        except : pass

    def connect_to_server(self) :
        self.splash.update_status('connecting to server...')
        self.app.processEvents()
        try :
            self.client_socket = socket.socket()
            self.splash.update_status('socket created ')
            self.app.processEvents()
        except :
            self.splash.update_status('unable to create socket')
            self.app.processEvents()
            time.sleep(1) #:)
            sys.exit()
        try :
            self.client_socket.connect(("127.0.0.1", 12345))
            self.splash.update_status('reached the server...')
            self.app.processEvents()
        except :
            self.client_socket.close()
            self.splash.update_status('unable to reach server')
            self.app.processEvents()
            time.sleep(1) #:)
            sys.exit()
        try :
            self.data_transmitting_loop = threading.Thread(target = self.transmitting_loop, args=())
            self.data_recieving_loop = threading.Thread(target = self.recieving_loop, args=())
            self.splash.update_status('thread created')
            self.app.processEvents()
        except :
            self.splash.update_status('unable to create thread')
            self.app.processEvents()
            time.sleep(1) #:)
            sys.exit()

    def client_initialisation(self) :
        self.splash.update_status('accepting data...')
        self.app.processEvents()
        self.client_socket.settimeout(10)
        
        self.exclaimation_recieved = False
        self.initialising_string = ""

        while not self.exclaimation_recieved :
            self.initial_string_part = self.client_socket.recv(1024*1024).decode("utf-8")

            if self.initial_string_part[-1] != "!" :
                self.initialising_string += self.initial_string_part
            else :
                self.initialising_string += self.initial_string_part[0:len(self.initial_string_part)-1]
                self.exclaimation_recieved = True
        self.initial_data_parser()

    def start_client_loops(self) :
        self.data_transmitting_loop.start()
        self.data_transmitting_loop_STATUS = True

        self.data_recieving_loop.start()
        self.data_recieving_loop_STATUS = True

    def transmitting_loop(self) :
        while self.APP_STATUS[0] :
            self.Lock.acquire()
            try :
                self.client_socket.send(bytes(chr(1)+chr(2), "utf-8"))
            except : pass
            self.Lock.release()
            time.sleep(1)
        print("closing the transmitting loop")
        self.data_transmitting_loop_STATUS = False

    def recieving_loop(self) :
        self.client_socket.send(bytes("", "utf-8"))
        self.recieved_data = ""
        while self.APP_STATUS[0] :
            try :
                self.server_responce = self.client_socket.recv(1024*1024)
                self.recieved_data += self.server_responce.decode("utf-8")
                try :
                    self.data_parser()
                except Exception as e :
                    print(e)
                self.update_ui_elements()
            except :
                pass
            try :
                #self.client_socket.send(bytes("*", "utf-8")) #sending the signal to the server to tell the server that "hey ! I still exist"
                pass
            except :
                pass
            time.sleep(1/60) #:)
        print("closing the recieving loop")
        while self.data_transmitting_loop_STATUS :
            time.sleep(1)
        
        self.close_connection()
        self.main_ui.close_q_app()
        
        self.data_recieving_loop_STATUS = False

        
        #sys.exit() #system exit call

    def send_data(self, message) :
        self.Lock.acquire()

        self.message_from_client = ""
        if len(message) != 0 :
            if self.validate_message(message) :
                self.client_socket.send(bytes(self.structure_the_message(message), "utf-8"))
        
        self.Lock.release()

    def validate_message(self, message) :
        if not ((chr(1) in message) or (chr(2) in message)) :
            return True
        return False

    def structure_the_message(self, message) :
        return "["+self.name+"]: "+message+chr(1)+chr(2)
        

    def initial_data_parser(self) :
        pass

    def data_parser(self) :
        while chr(1)+chr(2) in self.recieved_data :
            delimiter_loc = self.recieved_data.find(chr(1)+chr(2))
            message = self.recieved_data[:delimiter_loc]

            self.recieved_data = self.recieved_data[delimiter_loc+2:]

            self.data.add_strings(message)
            self.main_ui.update_ui_by_client()
        

    def add_splash_reference(self, splash) :
        self.splash = splash

    def add_q_app_reference(self, app) :
        self.app = app
    
    def add_data_reference(self, data) :
        self.data = data

    def add_main_ui_reference(self, main_ui) :
        self.main_ui = main_ui

    def close_connection(self) :
        try :
            self.client_socket.close()
        except :
            pass

    def update_ui_elements(self) :
        self.main_ui.update_ui_by_client()
