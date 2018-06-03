import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, 
    QPushButton, QApplication, QMainWindow, QAction)
from TableWidget import TableWidget

class Application(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):               
        
        self.statusBar().showMessage('Ready')
        self.setGeometry(100, 100, 1000, 500)
        #self.setMaximumSize(1400, 700)
        self.setWindowTitle('Graph -> lp_slove parser')

        #create menu
        mainMenu = self.menuBar() 
        fileMenu = mainMenu.addMenu('File')
        
        readButton = QAction('Read from file', self)
        readButton.setStatusTip('Import a graph from file')
        readButton.triggered.connect(self.load)
        fileMenu.addAction(readButton)

        saveGraph = QAction('Save graph to file', self)
        saveGraph.setStatusTip('Export a graph to file')
        saveGraph.triggered.connect(self.save)
        fileMenu.addAction(saveGraph)

        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


    def save(self):
        self.table_widget.saveGraph();

    def load(self):
        self.table_widget.loadGraph();

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())