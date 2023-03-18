from PyQt5.QtWidgets import QDesktopWidget, QLabel, QMainWindow, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import QThread

import threading

import time
############################################################################################################################################################################################################
class main_window(QMainWindow) :
    def __init__(self , sys,
                 close_button, WORKER_update_labels,
                 APP_STATUS) :
        
        super().__init__()
        
        """storing the references"""
        self.sys = sys

        self.close_button = close_button

        self.WORKER_update_labels  = WORKER_update_labels

        self.APP_STATUS = APP_STATUS

        """######defining functions############defining functions############defining functions######"""
    def initialise_ui(self) :
        self.top = 0
        self.left = 0
        self.height = 482
        self.width = 352

        self.heading_height = self.height//10
        self.number_of_text_labels = 20
        self.text_label_height = 20

        self.heading_font = 'Showcard Gothic'
        self.heading_font_size = int(self.heading_height*(2/3))

        self.line_edit_v_coordinate = int((self.heading_height + (20*self.text_label_height)) + 2)
        self.line_edit_height = int(self.height-self.line_edit_v_coordinate)
        self.line_edit_font_size = int(self.line_edit_height*(1/2))

        self.label_font = 'consolas'
        self.label_font_size = int(self.text_label_height*(2/3))

        """some setting  work"""
        self.setWindowTitle("CHAAT")

        self.setWindowOpacity(0.7)

        self.setWindowIcon(QIcon(".\\IMAGES\\_logo.jpg"))

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        
        """some flag work"""
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        self.setStyleSheet(self.color.colors["main_windows"])

        self.Lock = threading.Lock()

        self.ui_updater = self.WORKER_update_labels(self)
        self.ui_updater_thread = QThread(self)
        self.ui_updater.moveToThread(self.ui_updater_thread)
        self.ui_updater_thread.started.connect(self.ui_updater.run)
        self.ui_updater.finished.connect(self.ui_updater_thread.quit)
        self.ui_updater.progress.connect(self.update_label)
        
        self.center()

        self.mouse_pressed = False
        
        #self.show()  #displaying the window
        #self.splash.hide() #hiding the splash screen after the main window opens

    def center(self) :
        geometry_of_current_window = self.frameGeometry()
        centre_point_of_screen = QDesktopWidget().availableGeometry().center()
        geometry_of_current_window.moveCenter(centre_point_of_screen)
        self.move(geometry_of_current_window.topLeft())

    def mousePressEvent(self, e) :
        self.mouse_pressed = True
        self.position = e.pos()
        if e.buttons() == Qt.LeftButton:
            self.dragPos = e.globalPos()
            #e.accept()

    def mouseReleaseEvent(self, e) :
        self.mouse_pressed = False

    def mouseMoveEvent(self, e) :
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.dragPos)
            self.dragPos = e.globalPos()
            #e.accept()

    def wheelEvent(self, e):
        if not self.mouse_pressed :
            self.shift_by_n_by_mouse_wheel(e.angleDelta().y())

    def keyPressEvent(self, e) :
        if e.key() == Qt.Key_Return :
            self.app_client.send_data(self.get_text_from_input_prompt())

    def shift_by_n_by_mouse_wheel(self, wheel_event) :
        if wheel_event > 0 :
            self.Lock.acquire()

            self.data.set_offset_for_mouse_movement(-2)
            self.ui_updater_thread.start()

            self.Lock.release()
        if wheel_event < 0 :
            self.Lock.acquire()

            self.data.set_offset_for_mouse_movement(2)
            self.ui_updater_thread.start()

            self.Lock.release()

    def initiate_ui_elements(self) :
        self.heading = QLabel(self)
        self.heading.setStyleSheet(self.color.colors["heading"])
        self.heading.move(0,0)
        self.heading.resize(self.width, self.heading_height)
        self.heading.setFont(QFont(self.heading_font, self.heading_font_size, QFont.Bold))
        self.heading.setText(" CHAAT")
        
        self.splash.no_of_operations = self.number_of_text_labels

        self.label_list = []
        self.text_label_y_coordinate = self.heading_height+1
        self.max_chars_in_one_line = 39

        for _ in range(20) :
            self.label_list.append(QLabel(self))
            self.label_list[-1].setStyleSheet(self.color.colors["text_label"])
            self.label_list[-1].move(0,self.text_label_y_coordinate)
            self.label_list[-1].resize(self.width, self.text_label_height)
            self.label_list[-1].setFont(QFont(self.label_font, self.label_font_size, QFont.Bold))
            self.label_list[-1].setText(self.data.text_strs[_])
            
            self.splash.update("Creating frames")

            self.text_label_y_coordinate += self.text_label_height

            time.sleep(0.005)

        self.input_prompt = QLineEdit(self)
        self.input_prompt.move(0, self.line_edit_v_coordinate)
        self.input_prompt.resize(self.width, self.line_edit_height)
        self.input_prompt.setStyleSheet(self.color.colors["input_prompt"])
        self.input_prompt.setFont(QFont(self.label_font, self.line_edit_font_size, QFont.Bold))
        self.input_prompt.setText("\U00002588")
        self.input_prompt.show()

        self.closing_button = self.close_button(self)


    def add_splash_reference(self, splash) :
        self.splash = splash

    def add_q_app_reference(self, app) :
        self.app = app
    
    def add_data_reference(self, data) :
        self.data = data

    def add_color_reference(self, color) :
        self.color = color

    def add_app_client_reference(self, app_client) :
        self.app_client = app_client

    def close_application(self) :
        self.hide()
        self.APP_STATUS[0] = False

        #self.app_client.close_connection() #closing client connection
        #self.sys.exit() #system exit call
        
    def close_q_app(self) :
        self.app_client.close_connection()
        
        self.Lock.acquire()

        try :
            self.ui_updater_thread.terminate()
        except :
            pass

        self.app.quit()

        self.Lock.release()

    def update_label(self, index) :
        self.label_list[index].setText(self.data.get_string_for_index(index))

    def get_text_from_input_prompt(self) :
        text = self.input_prompt.text()
        self.input_prompt.setText("")
        return text

    def update_ui_by_client(self) :
        self.Lock.acquire()

        self.ui_updater_thread.start()

        self.Lock.release()

    def get_label_data(self) :
        return [self.label_font, self.label_font_size]

    def qfont_reference(self) :
        return QFont
    
    def qfontmetrix_reference(self) :
        return QFontMetrics

    def label_data_fetch(self) :
        return [self.label_font_size, self.label_font]
