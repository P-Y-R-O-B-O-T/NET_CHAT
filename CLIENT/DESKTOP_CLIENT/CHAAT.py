'''
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QFrame, QLabel, QMainWindow, QWidget
from PyQt5.QtGui import QBrush, QFont, QIcon, QImage, QPalette, QPixmap
from PyQt5 import QtCore , QtGui
from PyQt5.QtCore import QCoreApplication , Qt , QBasicTimer , QObject , QPoint , QRect , QPropertyAnimation , QThread , pyqtSignal
'''
from PyQt5.QtWidgets import QApplication

import time
import sys
import gc

gc.enable() #enabling automatic garbage collection

from UI.color import color
from UI.button import close_button
from UI.splash_screen import splashScreen
from UI.main_window import main_window
from UI.qworker import WORKER_update_labels

from BACKEND.data_dict import data_
from BACKEND.client import client

APP_STATUS = [True] #control variable for whole application

app = QApplication(sys.argv) #q application instance

splash = splashScreen() #creating splash screen
splash.add_color_reference(color) #adding color reference to splash screen
splash.add_q_app_reference(app) #adding q app reference to splash screen
splash.initialise_splash_screen() #initialising splash screen
app.processEvents() #processing events of q app

app_client = client(APP_STATUS) #creating client object
app_client.add_splash_reference(splash) #adding splash screen reference to app client
app_client.add_q_app_reference(app) #adding q app reference to app client
app_client.add_data_reference(data_) #adding data refernece to app client

app_client.connect_to_server() #connecting to server through app client

try :
    app_client.client_initialisation() #initialising app client
except :
    splash.update_status('unable to initialise data') #updating splash screen
    app.processEvents() #processing events of q app
    time.sleep(1)
    sys.exit() #closing application

main_ui = main_window(sys, close_button,
                      WORKER_update_labels,
                      APP_STATUS) #creating main window of the applicaiton

app_client.add_main_ui_reference(main_ui) #adding amin ui reference to app client

main_ui.add_splash_reference(splash) #adding splash screen reference to main ui
main_ui.add_q_app_reference(app) #adding q app reference to main ui
main_ui.add_data_reference(data_) #adding data reference to main ui
main_ui.add_color_reference(color) #adding color reference to main ui
main_ui.add_app_client_reference(app_client) #adding app client reference to main ui

main_ui.initialise_ui() #initialising main ui

main_ui.initiate_ui_elements() #calling function to initiate the ui elements

data_.add_main_ui_reference(main_ui)
data_.get_reference_for_calculation_of_width_of_string()
data_.get_label_data()

app_client.start_client_loops() #starting app client main loop

main_ui.show() #display main ui
splash.hide() #hide splash screen

app.exec() #running event loop for q app
sys.exit() #system call to exit
