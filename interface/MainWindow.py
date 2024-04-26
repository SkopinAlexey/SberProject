import zipfile
import webbrowser
import os

from web_parser.utils import rename_file
from web_parser.utils import driver_config
from web_parser.web_parser import WebParser
#from web_parser.utils import *

from PySide6 import QtWidgets
from PySide6.QtCore import QRect
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QMainWindow, QLabel, QStatusBar,\
    QListWidget, QListWidgetItem, QPushButton, QProgressBar

class MainWindow(QMainWindow):

    chosen_file = ""

    def __init__(self):
        super().__init__()

        self.webparser = WebParser(driver_config())

        self.setWindowTitle("My App")
        self.resize(800, 600)

        self.label = QLabel(self)
        self.label.setText("Список файлов в архиве:")
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 75, 400, 51))
        font = QFont()
        font.setFamilies([u"Comic Sans MS"])
        font.setPointSize(22)
        self.label.setFont(font)

        button_open = QAction("&Открыть", self)
        button_open.setStatusTip("Открыть архив с PDF-документами")
        button_open.triggered.connect(self.onButtonOpenClicked)

        button_download = QAction("&Скачать", self)
        button_download.setStatusTip("Скачать архив по ИНН")
        button_download.triggered.connect(self.onButtonDownloadClicked)

        button_help = QAction("&О программе", self)
        button_help.setStatusTip("Показать данные о программе")
        #button_help.triggered.connect(self.onButtonOpenClicked)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("&Файл")
        file_menu.addAction(button_open)
        file_menu.addAction(button_download)
        #file_menu.addAction(button_close)
        file_menu.addSeparator()

        file_menu = menu.addMenu("&Помощь")
        file_menu.addAction(button_help)

        font_list = QFont()
        font_list.setFamilies([u"Comic Sans MS"])
        font_list.setPointSize(13)

        self.buttonCompare = QPushButton(self)
        self.buttonCompare.setGeometry(QRect(90, 470, 100, 40))
        self.buttonCompare.setFont(font_list)
        self.buttonCompare.setText("Сравнить")
        self.buttonCompare.clicked.connect(self.onClickedCompareButton)

        self.buttonClose = QPushButton(self)
        self.buttonClose.setGeometry(QRect(200, 470, 100, 40))
        self.buttonClose.setFont(font_list)
        self.buttonClose.setText("Убрать")
        self.buttonClose.clicked.connect(self.onButtonCloseClicked)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(QRect(90, 140, 441, 301))
        self.listWidget.setStyleSheet("QLineEdit { background-color: white }")
        self.listWidget.setFont(font_list)

        self.makeDefaultList()

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QRect(90, 140, 441, 20))
        self.progressBar.setVisible(False)

    def makeDefaultList(self):
        self.listWidget.clear()
        QListWidgetItem("Не выбран архив", self.listWidget)

    def deleteExtractedFiles(self):
        directory = "ext_archive"
        files = os.listdir(directory)
        for file in files:
            path = os.path.join(directory, file)
            os.remove(path)

    def closeEvent(self, event):
        self.deleteExtractedFiles()

    def onButtonOpenClicked(self, s):
        self.deleteExtractedFiles()

        chosen_file = QtWidgets.QFileDialog.getOpenFileName()[0]
        print(chosen_file)

        with zipfile.ZipFile(chosen_file, 'r') as zip_ref:
            zip_ref.extractall('ext_archive')

        directory = "ext_archive"
        files = os.listdir(directory)
        print(files)

        self.listWidget.clear()
        for i in files:
            listWidgetItem = QListWidgetItem(i)
            self.listWidget.addItem(listWidgetItem)

        self.listWidget.itemClicked.connect(self.onClickedListItem)

    def onButtonCloseClicked(self):
        self.deleteExtractedFiles()
        self.makeDefaultList()

    def onClickedListItem(self, item):
        if item.data(0) == 'Не выбран архив':
            return
        new = 2
        path = os.getcwd()
        file = path + "/ext_archive/" + str(item.data(0))
        webbrowser.open(file, new=new)

    def onButtonDownloadClicked(self):
        self.webparser.get_object_declarations(8242)
        rename_file()

    def onClickedCompareButton(self):
        ...