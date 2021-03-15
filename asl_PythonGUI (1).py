# filename asl_PythonGUI.py
# For this program to work correctly, asl_net.py needs to be in the same folder as asl_PythonGUI.py

# for arguments passed to asl_net.py, see function run_asl_net()

# install PyQt5
# https://realpython.com/python-pyqt-gui-calculator/#installing-pyqt

import sys
import os
import asl_net

# Import required modules and classes from PyQt5.QtWidgets.
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QLabel
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView, QFormLayout, QTextEdit


# GLOBAL CONSTANTS
#ERROR_MSG = 'ERROR'
TITLE = 'ASL Grading Program' #window title
TXT1 = 'The program will generate a PDF of your results with the name you give below.'
TXT2 = '\n      \u2022 If no name is given, PDF of results will not generate.'
TXT3 = '\n      \u2022 If no picture folder is selected, PDF will not generate.'
TXT4 = '\n      \u2022 If no save folder is selected, PDF will not generate.\n'
TXT5 = '\nOnce you have chosen a name for your PDF of results and a folder of pictures to process, click grade to generate PDF.\n'
TXT6 = '\nThe window will close once the PDF is generated.\n'
TXT = TXT1 + TXT2 + TXT3 + TXT4 + TXT5 + TXT6
# buttons labels
LBL1 = 'Save PDF as:'
UPL = 'Choose Picture Folder'
GRD = 'Grade and Generate PDF'
DOWN = 'Choose folder to save PDF'
# window sizes constants
W_LENGTH = 550  # window length
W_HEIGHT = 260  # window height
T_HEIGHT = 140  # textbox height


# Subclass of QMainWindow to setup GUI.
# (inherits from QMainWindow)
class GUI(QMainWindow):
    def __init__(self):
        super().__init__()\
        # Set window title.
        self.setWindowTitle(TITLE)
        # Give window a fixed size.
        self.setFixedSize(W_LENGTH, W_HEIGHT)

        # Set central widget and general layout (QVBox is one-column layout)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout = QVBoxLayout()

        # Create a layout for the read only text box
        self.textboxLayout = QVBoxLayout()
        # Create a layout for the PDF file name
        self.topLayout = QFormLayout()
        # Create a layout for the buttons
        self.optionsLayout = QVBoxLayout()

        # Nest the inner layouts into the outer layout
        self.generalLayout.addLayout(self.textboxLayout)
        self.generalLayout.addLayout(self.topLayout)
        self.generalLayout.addLayout(self.optionsLayout)

        # Set the window's main layout
        self._centralWidget.setLayout(self.generalLayout)

        # Create and display buttons
        self._displayButtons()

        # Display beginning message using global constants
        self.display.setText(TXT)

    def _displayButtons(self):

        # Create read only display
        # Create the display widget
        self.display = QTextEdit()
        # Set some display's properties
        self.display.setFixedHeight(T_HEIGHT)
        self.display.setAlignment(QtCore.Qt.AlignCenter)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); border: rgba(0, 0, 0, 0);}")
        # Add the display to the general layout
        self.textboxLayout.addWidget(self.display)

        # Create buttons
        self.button1 = QPushButton(UPL)
        self.button2 = QPushButton(DOWN)
        self.button3 = QPushButton(GRD)

        # Add buttons to layout
        self.optionsLayout.addWidget(self.button1)
        self.optionsLayout.addWidget(self.button2)
        self.optionsLayout.addWidget(self.button3)

        # Add a label and a line edit to the form layout
        self.line = QLineEdit()
        self.topLayout.addRow(LBL1, self.line)

        # Set upload_from and down_to to 0 for error checking
        self.upload_from = ''
        self.down_to = ''


    def button1_clicked(self, view):
        #print("Button 1 clicked - " + UPL)
        self.upload_from = QFileDialog.getExistingDirectory(self,"Choose Directory","E:\\")
        self.display_info()
        
   
    def button2_clicked(self, view):
        #print("Button 2 clicked - " + DOWN)
        self.down_to = QFileDialog.getExistingDirectory(self,"Choose Directory","E:\\")
        self.display_info()


    def button3_clicked(self, view):
        #print("Button 3 clicked - " + GRD)
        #if there is no upload folder, no PDF name or no folder to save to, error
        if (self.upload_from == ''):
            self.display.setText('Make sure you have selected a folder of pictures.')
        elif (self.line.text() == ''):
            self.display.setText('Make sure you have entered a PDF name.')
        elif (self.down_to == ''):
            self.display.setText('Make sure you have entered a folder to save the PDF to.')
        else:
            self.display.setText('Grading...\nProgram will quit when finished.')
            # run asl_net.py
            self.run_asl_net()


    def run_asl_net(self):
        # argv[1] folder path of pictures to be graded
        # argv[2] batch size, hard coded to 1
        # argv[3] path to trained model
        # argv[4] file path to save PDF (filepath from user + 'user entered text' + '.pdf'
        asl_net.TestNetworkNotTraining(self.upload_from, 1, 'Model.hdf5', os.path.join(self.down_to, self.line.text() + '.pdf'))
        sys.exit()


    def display_info(self):
        self.display.setText('Will use pictures in ' + self.upload_from + 
                             '\nPDF will be named: ' + self.line.text() + '.pdf'
                             '\nPDF will be saved to ' + self.down_to)


class GUICtrl:
    # controller class
    def __init__(self, view):
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    def _connectSignals(self):     
        self._view.button1.clicked.connect(self._view.button1_clicked)
        self._view.button2.clicked.connect(self._view.button2_clicked)
        self._view.button3.clicked.connect(self._view.button3_clicked)



def main():
    # Create QApplication object.
    asl_gui = QApplication(sys.argv)
    # Display GUI.
    view = GUI()
    view.show()
    # Create instances of the controller
    GUICtrl(view=view)
    # Runs application's event loop.
    sys.exit(asl_gui.exec())

if __name__ == '__main__':
    main()
