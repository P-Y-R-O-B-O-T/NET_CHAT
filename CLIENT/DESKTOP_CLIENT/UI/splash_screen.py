from PyQt5.QtWidgets import QDesktopWidget, QLabel, QWidget
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
############################################################################################################################################################################################################
class splashScreen(QWidget) :
    def __init__(self) :
        super().__init__() 
        self.title = "CHAAT"

        self.top = 0  
        self.left = 0
        self.width = 250 
        self.height = 75 

    def initialise_splash_screen(self) :
        self.setWindowTitle(self.title)

        self.setWindowIcon(QIcon(".\\IMAGES\\_logo.jpg"))

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint )
        self.setWindowFlags(flags)
        self.setStyleSheet(self.color.colors[ "splash_screen"]["background_color"])

        #self.setAttribute(Qt.WA_TranslucentBackground)  #not required now baad me zarurat padi to chek karunga, makes ui transparent

        self.setWindowOpacity(0.7)

        #all labels
        self.border = QLabel(self)
        self.border.move(0,0)
        self.border.resize(250,75)
        self.border.setStyleSheet(self.color.colors[ "splash_screen"]["border"])
        self.border.show()

        self.top_label = QLabel(self)
        self.top_label.setText(self.title)
        self.top_label.setFont(QFont('Courier New',25,QFont.Bold))
        self.top_label.setStyleSheet(self.color.colors[ "splash_screen"]["heading"])
        self.top_label.move(70,1)
        self.top_label.show()

        self.progress_bar_max_length = 242
        self.operations_done = 0

        self.progress_bar = QLabel(self)
        self.progress_bar.setStyleSheet(self.color.colors[ "splash_screen"]["progress_bar"])
        self.progress_bar.move(4,40)
        self.progress_bar.resize(0,10)
        self.progress_bar.show()

        self.progress_bar_left_rest = QLabel(self)
        self.progress_bar_left_rest.setStyleSheet(self.color.colors[ "splash_screen"]["progress_bar_side_rest"])
        self.progress_bar_left_rest.move(1,38)
        self.progress_bar_left_rest.resize(3,14)
        self.progress_bar_left_rest.show()

        self.progress_bar_right_rest = QLabel(self)
        self.progress_bar_right_rest.setStyleSheet(self.color.colors[ "splash_screen"]["progress_bar_side_rest"])
        self.progress_bar_right_rest.move(246,38)
        self.progress_bar_right_rest.resize(3,14)
        self.progress_bar_right_rest.show()

        self.status_reporter = QLabel(self)
        self.status_reporter.setStyleSheet(self.color.colors[ "splash_screen"]["status_reporter"])
        self.status_reporter.move(1,55)
        self.status_reporter.setFont(QFont('Courier New',8,QFont.Bold))
        self.status_reporter.setText("*"*33)
        self.status_reporter.setText("trying to connect to server...")
        self.status_reporter.show()

        self.center()
        self.show()

    def update(self, string) :
        self.operations_done+=1
        self.new_bar_length = ((self.progress_bar_max_length*self.operations_done)//self.no_of_operations)
        self.progress_bar.resize(self.new_bar_length,10)
        self.update_status(string)
        self.app.processEvents()

    def center(self) :
        geometry_of_current_window = self.frameGeometry()
        centre_point_of_screen = QDesktopWidget().availableGeometry().center()
        geometry_of_current_window.moveCenter(centre_point_of_screen)
        self.move(geometry_of_current_window.topLeft())

    def update_status(self, string) :
        self.status_reporter.setText(string)

    def add_q_app_reference(self, app) :
        self.app = app

    def add_color_reference(self, color) :
        self.color = color
