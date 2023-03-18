from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtGui import QFont 
############################################################################################################################################################################################################
class close_button(QFrame) :
    def __init__(self, parent=None) :
        super().__init__(parent)
        
        self.par = parent

        self.height = self.par.heading_height
        self.width = 80
        
        self.setGeometry(self.par.width-self.width,0,self.width,self.height)
        self.setStyleSheet(self.par.color.colors["close_button"])

        self.cross = QLabel(self)
        self.cross.setText("[X]")
        self.cross.setGeometry(0,0,self.width,self.height)
        self.cross.setFont(QFont('Showcard Gothic', int(self.height*(2/3)), QFont.Bold))
        self.cross.setStyleSheet(self.par.color.colors["close_button_text"])
        self.cross.show()
        
        self.show()

    def close_app(self) :
        self.par.close_application()

    def mousePressEvent(self, e) :
        self.close_app()

    def mouseMoveEvent(self, e) :
        pass
