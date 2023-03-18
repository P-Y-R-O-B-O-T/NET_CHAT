from PyQt5.QtCore import QObject, pyqtSignal
############################################################################################################################################################################################################
class WORKER_update_labels(QObject): #creating worker class
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, par) :
        super().__init__(par)
        QObject.__init__(self)

    def run(self):
        """Long-running task."""
        for i in range(20): #running 10 times
            try :
                self.progress.emit(i)
            except :
                pass
        self.finished.emit()