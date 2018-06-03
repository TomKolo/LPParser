import sys
import pickle
from PyQt5.Qt import QRegularExpression
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from myGraph import myGraph
from LPParser import *

class TableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        #self.setMaximumSize(1400, 700)
        self.layout = QVBoxLayout(self)
 
        self.font = QFont("Times", 8, QFont.Bold) 

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(100,160) 
 
        # Add tabs
        self.tabs.addTab(self.tab1,"Properties")
        self.tabs.addTab(self.tab2,"Connections")
        self.tabs.addTab(self.tab3,"Graph")
        self.tabs.addTab(self.tab4,"Generate lp file")

        # Create first tab
        layout = QVBoxLayout()

        self.tab1.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.tab1.setPalette(p)

        self.labelNum = QLabel("Number of nodes:", self)
        self.labelNum.setFont(self.font)
         
        self.nodesTextField = QLineEdit(self)
        self.onlyInt = QIntValidator()
        self.nodesTextField.setValidator(self.onlyInt)

        self.nodesTextField.setPlaceholderText("Number of nodes")

        self.labelDirected = QLabel("Directed or not ?:", self)
        self.labelDirected.setFont(self.font)

        self.directed = QCheckBox("Directed",self)

        self.labelMinMax = QLabel("Min or max ?", self)
        self.labelMinMax.setFont(self.font)

        layoutMaxMin = QHBoxLayout()
        self.min =  QRadioButton("Min", self)
        self.min.setChecked(True)
        self.max =  QRadioButton("Max", self)
        buttonGroupMaxMin = QButtonGroup()
        buttonGroupMaxMin.addButton(self.min)
        buttonGroupMaxMin.addButton(self.max)
        buttonGroupMaxMin.setExclusive(True)
        layoutMaxMin.addWidget(self.min)
        layoutMaxMin.addWidget(self.max)

        layoutNodes = QHBoxLayout()
        self.labelNodes = QLabel("Startin and termination node ?:", self)
        self.labelNodes.setFont(self.font)

        self.startingNode = QLineEdit(self)
        self.startingNode.setPlaceholderText("Starting node") 
        self.terminationNode = QLineEdit(self)
        self.terminationNode.setPlaceholderText("Termination node")
        self.onlyIntStart = QIntValidator()
        self.startingNode.setValidator(self.onlyIntStart)
        self.onlyIntTermination = QIntValidator()
        self.terminationNode.setValidator(self.onlyIntTermination)
        layoutNodes.addWidget(self.startingNode)
        layoutNodes.addWidget(self.terminationNode)

        self.labelDatatype = QLabel("Data type ?:", self)
        self.labelDatatype.setFont(self.font)

        layoutDatatype = QHBoxLayout()
        self.boolean =  QCheckBox("Boolean", self)
        self.boolean.setChecked(True)
        self.integer =  QCheckBox("Integer", self)
        self.float =  QCheckBox("Float", self)
        buttonGroupDatatype = QButtonGroup()
        buttonGroupDatatype.addButton(self.boolean)
        buttonGroupDatatype.addButton(self.integer)
        buttonGroupDatatype.addButton(self.float)
        buttonGroupDatatype.setExclusive(True)
        layoutDatatype.addWidget(self.boolean)
        layoutDatatype.addWidget(self.integer)
        layoutDatatype.addWidget(self.float)

        self.acceptButton = QPushButton("Accept")
        self.acceptButton.clicked.connect(self.accept)


        layout.addWidget(self.labelNum)
        layout.addWidget(self.nodesTextField)
        layout.addStretch()
        layout.addWidget(self.labelDirected)
        layout.addWidget(self.directed)
        layout.addStretch()
        layout.addWidget(self.labelMinMax)
        layout.addLayout(layoutMaxMin)
        layout.addStretch()
        layout.addWidget(self.labelNodes)
        layout.addLayout(layoutNodes)
        layout.addStretch()
        layout.addWidget(self.labelDatatype)
        layout.addLayout(layoutDatatype)
        layout.addStretch()
        layout.addWidget(self.acceptButton)
        self.tab1.layout =  QHBoxLayout()
        self.tab1.layout.addStretch()
        self.tab1.layout.addLayout(layout)
        self.tab1.layout.addStretch()
        self.tab1.setLayout(self.tab1.layout)

 
        #second tab
        self.tab2.layout = QGridLayout(self)

        self.tab2.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.tab2.setPalette(p)

        self.buttons = []
        for i in range(0,18):
            temporaty = []
            for j in range(0,18):
                temporaty.append(0);
            self.buttons.append(temporaty)


        self.onlyIntMatrix = QIntValidator()
        self.onlyFloatMatrix = QDoubleValidator()
        re = QRegularExpression("[0-1]\\d{0}");
        self.onlyBinaryMatrix = QRegularExpressionValidator(re)

        for i in range (0,18):
            for j in range(0,18):
                self.buttons[i][j] = QLineEdit()
                self.buttons[i][j].setFixedWidth(60)
                self.buttons[i][j].setFixedHeight(30)
                self.buttons[i][j].setValidator(self.onlyIntMatrix)
                self.tab2.layout.addWidget(self.buttons[i][j],i+1,j+1)
        self.tab2.setLayout(self.tab2.layout)

        self.nodes = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","R","S"]
        self.labelsNodes = []
        for i in range(0,2):
            temporaty = []
            for j in range(0,18):
                temporaty.append(0);
            self.labelsNodes.append(temporaty)

        iterator = 0
        for i in self.nodes:
            iterator += 1
            tmp = QLabel(" " + i +" ", self)
            tmp.setAlignment(Qt.AlignVCenter)
            self.labelsNodes[0][iterator - 1] = tmp
            tmp.setFixedWidth(30)
            tmp.setFixedHeight(35)
            tmp.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            tmp.setFont(self.font)
            tmp2 = QLabel(i, self)
            tmp2.setAlignment(Qt.AlignVCenter)
            tmp2.setIndent(25)
            tmp2.setFixedHeight(35)
            tmp2.setFixedWidth(50)
            tmp2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            tmp2.setFont(self.font)
            self.labelsNodes[1][iterator - 1] = tmp2
            self.tab2.layout.addWidget(tmp,iterator,0)
            self.tab2.layout.addWidget(tmp2,0,iterator)

        #third tab - display graph
        self.tab3.layout = QVBoxLayout(self)
        self.graphLabel = QLabel("IMAGE")
        self.generateGraphButton = QPushButton("Generate graph")
        self.generateGraphButton.clicked.connect(self.displayGraph)
        self.tab3.layout.addWidget(self.graphLabel)
        self.tab3.layout.addWidget(self.generateGraphButton)
        self.tab3.setLayout(self.tab3.layout)

        #fourth tab
        self.tab4.layout = QVBoxLayout(self)
        self.generateButton = QPushButton("Accept")
        self.generateButton.clicked.connect(self.createLP)
        self.tab4.layout.addWidget(self.generateButton)
        self.tab4.setLayout(self.tab4.layout)

        # Add tabs to widget        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
 

    @pyqtSlot()

    def accept(self):
        if self.checkCorrectness() == True:
            directed = self.directed.isChecked()
            self.numberOfNodes = int(self.nodesTextField.text())
            for i in range(0, 18):
                self.labelsNodes[0][i].show()
                self.labelsNodes[1][i].show()
                for j in range(0,18):
                    self.buttons[i][j].show()
                    if self.float.isChecked() == True:
                        self.buttons[i][j].setValidator(self.onlyFloatMatrix)
                    elif self.integer.isChecked() == True:
                        self.buttons[i][j].setValidator(self.onlyIntMatrix)
                    else:
                        self.buttons[i][j].setValidator(self.onlyBinaryMatrix)


            for i in range(self.numberOfNodes, 18):
                self.labelsNodes[0][i].hide()
                self.labelsNodes[1][i].hide()
                for j in range(0, 18):
                    self.buttons[i][j].hide()

            for i in range(self.numberOfNodes, 18):
                for j in range(0, 18):
                    self.buttons[j][i].hide()

            for i in range(0,self.numberOfNodes):
                self.buttons[i][i].hide()

            if directed == False:
               for i in range(0,self.numberOfNodes):
                for j in range(0, i ):
                    self.buttons[i][j].hide()

            return True;
        else:
            QMessageBox().warning(self, "Incorrect data", "Input data is not correct", QMessageBox.Ok)
            return False;


    def checkCorrectness(self):
        try:
           self.size = int(self.nodesTextField.text())
           self.start = int(self.startingNode.text())
           self.end = int(self.terminationNode.text())
           if self.min.isChecked():
               self.type = "min"
           else:
               self.type = "max"

           if self.float.isChecked():
               self.datatype = "sec"
           elif self.integer.isChecked():
               self.datatype = "int"
           else:
               self.datatype = "bin"

           if self.directed.isChecked():
               self.isDirected = "d"
           else:
               self.isDirected = "un"

        except ValueError:
          return False
        
        if self.size >= 0 and self.size <= 18:
            if self.start >= 0 and self.start <= self.size:
                if self.end >= 0 and self.end <= self.size:
                    return True
        return False


    def generateMatrix(self):
        if self.checkCorrectness():
            self.checkCorrectness()
            self.matrix = []
            for i in range(0,self.numberOfNodes):
                temporaty = []
                for j in range(0,self.numberOfNodes):
                    temporaty.append(0);
                self.matrix.append(temporaty)
        


            if self.directed.isChecked() == True:
                for i in range(0, self.numberOfNodes):
                    for j in range(0,self.numberOfNodes):
                        if self.buttons[i][j].text() == "":
                            self.matrix[i][j] = 0
                        else:
                            if self.float.isChecked():
                               self.matrix[i][j] = float(self.buttons[i][j].text())
                            elif self.integer.isChecked():
                               self.matrix[i][j] = int(self.buttons[i][j].text())
                            else:
                               self.matrix[i][j] = int(self.buttons[i][j].text())
                        
            else:
                for i in range(0, self.numberOfNodes):
                    for j in range(i, self.numberOfNodes):
                        if self.buttons[i][j].text() == "":
                            self.matrix[i][j] = 0
                        else:
                           if self.float.isChecked():
                               self.matrix[i][j] = float(self.buttons[i][j].text())
                           elif self.integer.isChecked():
                               self.matrix[i][j] = int(self.buttons[i][j].text())
                           else:
                               self.matrix[i][j] = int(self.buttons[i][j].text())
            return 1
        else:
            return 0
        
    
    def createLP(self):
        if self.generateMatrix():
            LPParser(self.matrix, self.start, self.end, self.isDirected, self.type, self.datatype).run()

    def saveGraph(self):
        if self.generateMatrix():
            self.graph = myGraph(self.matrix, self.datatype,self.type,self.size,self.startingNode.text(),self.terminationNode.text())
            with open('myGraph.pickle', 'wb') as handle:
                pickle.dump(self.graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadGraph(self):
        with open('myGraph.pickle', 'rb') as handle:
            self.graph = pickle.load(handle)
        for i in range(0,18):
            for j in range(0,18):
                self.buttons[i][j].setText("");

        for i in range(0,self.graph.size):
            for j in range(0,self.graph.size):
                self.buttons[i][j].setText(str(self.graph.matrix[i][j]));

        self.nodesTextField.setText(str(self.graph.size))
        self.startingNode.setText(self.graph.startingNode)
        self.terminationNode.setText(self.graph.terminationNode)
        self.accept()

    def displayGraph(self):
        self.generateGraph()
        self.graphLabel.clear()
        pixmap = QPixmap('Graph.png')
        self.graphLabel.setPixmap(pixmap)

    def generateGraph(self):
        if(self.accept() == True):
            labels={}
            for i in range(0,self.numberOfNodes):
                labels[i] = self.nodes[i];

            self.generateMatrix()

            if(self.isDirected == "un"):
                G = nx.from_numpy_matrix(np.array(self.matrix))
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='yellow')
            else :
                G = nx.from_numpy_matrix(np.array(self.matrix),create_using = nx.DiGraph())
                pos = nx.spring_layout(G)       
                nx.draw(G,pos,node_color='orange')


            
            nx.draw_networkx_labels(G,pos,labels, font_size=20);
            plt.savefig("Graph.png", format="PNG")
            plt.clf() 
