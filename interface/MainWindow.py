import time
import zipfile
import webbrowser
import os

from interface.Developer import Developer
from typing import List
from interface.DeveloperWidget import DeveloperWidget
from web_parser.utils import driver_config, rename_file
from web_parser.web_parser import web_parser
from compare.compare import start_compare

from interface.Building import Building
from interface.BuildingWidgetItem import BuildingWidgetItem
from interface.BuildingWidget import BuildingWidget

from PySide6 import QtWidgets
from PySide6.QtCore import QRect
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QMainWindow, QLabel, QStatusBar, \
    QListWidget, QListWidgetItem, QPushButton, QProgressBar, QInputDialog, QMessageBox


class MainWindow(QMainWindow):

    chosen_file = ""

    def __init__(self):
        super().__init__()

        # self.webparser.get_developer_objects(375)
        # self.webparser.get_object_declarations(45247)

        self.setWindowTitle("My App")
        self.setFixedSize(1280, 1024)

        self.developers_label = QLabel(self)
        self.developers_label.setText("Список застройщиков:")
        self.developers_label.setObjectName(u"label")
        self.developers_label.setGeometry(QRect(90, 75, 400, 51))
        font = QFont()
        font.setFamilies([u"Comic Sans MS"])
        font.setPointSize(22)
        self.developers_label.setFont(font)

        self.objects_label = QLabel(self)
        self.objects_label.setText("Список застройщиков:")
        self.objects_label.setObjectName(u"label")
        self.objects_label.setGeometry(QRect(90, 75, 400, 51))
        self.objects_label.setFont(font)

        button_open = QAction("&Открыть", self)
        button_open.setStatusTip("Открыть архив с PDF-документами")
        button_open.triggered.connect(self.on_button_open_clicked)

        button_download = QAction("&Скачать", self)
        button_download.setStatusTip("Скачать архив по ИНН")
        button_download.triggered.connect(self.on_button_download_clicked)

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
        self.buttonCompare.clicked.connect(self.on_clicked_compare_button)

        self.buttonClose = QPushButton(self)
        self.buttonClose.setGeometry(QRect(200, 470, 100, 40))
        self.buttonClose.setFont(font_list)
        self.buttonClose.setText("Убрать")
        self.buttonClose.clicked.connect(self.on_button_close_clicked)

        self.buttonBack = QPushButton(self)
        self.buttonBack.setGeometry(QRect(310, 470, 100, 40))
        self.buttonBack.setFont(font_list)
        self.buttonBack.setText("Назад")
        self.buttonBack.clicked.connect(self.on_button_back_clicked)

        self.list_developer = QListWidget(self)
        self.list_developer.setGeometry(QRect(40, 140, 500, 301))
        self.list_developer.setStyleSheet("QLineEdit { background-color: white }")
        self.list_developer.setFont(font_list)

        self.list_object = QListWidget(self)
        self.list_object.setGeometry(QRect(40, 140, 500, 301))
        self.list_object.setStyleSheet("QLineEdit { background-color: white }")
        self.list_object.setFont(font_list)
        self.list_object.setVisible(False)

        self.list_pdf = QListWidget(self)
        self.list_pdf.setGeometry(QRect(40, 140, 500, 301))
        self.list_pdf.setStyleSheet("QLineEdit { background-color: white }")
        self.list_pdf.setFont(font_list)
        self.list_pdf.setVisible(False)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QRect(90, 140, 441, 20))
        self.progressBar.setVisible(False)

        self.list_all = web_parser.get_developers_list()

        for item in self.list_all:
            dev = Developer(id=item['id'], devInn=item['devInn'], name=item['name'])
            item_widget = DeveloperWidget(developer=dev)
            self.list_developer.addItem(item_widget)

        print(self.list_developer)
        self.list_developer.itemClicked.connect(self.on_clicked_developer_list_item)


    def on_clicked_developer_list_item(self, item):
        self.list_developer.setVisible(False)
        self.list_object.setVisible(True)
        self.list_pdf.setVisible(False)
        self.list_object.clear()
        id = item.id
        list_obj = web_parser.get_developer_objects(id)

        for item in list_obj:
            obj = self.getBuilding(item)
            item_obj = BuildingWidgetItem(obj)
            self.list_object.addItem(item_obj)
            # item_obj = BuildingWidgetItem(self.list_object)
            # item_widget = BuildingWidget(build=obj)
            # self.list_object.addItem(item_obj)
            # self.list_object.setItemWidget(item_obj, item_widget)

        self.list_object.itemClicked.connect(self.on_clicked_building_list_item)

    def on_clicked_building_list_item(self, item):
        web_parser.get_object_declarations(item.buyld.objId)
        file = os.path.abspath(os.getcwd())
        print(os.listdir(file))
        self.delete_extracted_files()
        while True:
            try:
                self.extractZip(f'{file}\obj{item.buyld.objId}_docs.zip')
                os.remove(f'{file}\obj{item.buyld.objId}_docs.zip')
                break
            except FileNotFoundError:
                pass
        self.list_developer.setVisible(False)
        self.list_object.setVisible(False)
        self.list_pdf.setVisible(True)

    def getBuilding(self, item):
        try:
            return Building(objId=item['objId'], shortAddr=item['shortAddr'], objCommercNm=item['objCommercNm'])
        except KeyError:
            return Building(objId=item['objId'], shortAddr=item['shortAddr'], objCommercNm='noname')

    def make_default_list(self):
        self.list_developer.clear()

    def delete_extracted_files(self):
        directory = "ext_archive"
        files = os.listdir(directory)
        for file in files:
            path = os.path.join(directory, file)
            os.remove(path)

    def closeEvent(self, event):
        self.delete_extracted_files()

    def extractZip(self, path):
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall('ext_archive')

        directory = "ext_archive"
        files = os.listdir(directory)
        print(files)

        self.list_pdf.clear()
        for i in files:
            listWidgetItem = QListWidgetItem(i)
            self.list_pdf.addItem(listWidgetItem)

        self.list_pdf.itemClicked.connect(self.on_clicked_list_item)


    def on_button_open_clicked(self, s):
        try:
            self.delete_extracted_files()

            chosen_file = QtWidgets.QFileDialog.getOpenFileName()[0]
            print(chosen_file)

            with zipfile.ZipFile(chosen_file, 'r') as zip_ref:
                zip_ref.extractall('ext_archive')

            directory = "ext_archive"
            files = os.listdir(directory)
            print(files)

            self.list_developer.clear()
            for i in files:
                listWidgetItem = QListWidgetItem(i)
                self.list_developer.addItem(listWidgetItem)

            self.list_developer.itemClicked.connect(self.on_clicked_list_item)
        except zipfile.BadZipfile:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Выбран файл с неправильным расширением")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def on_button_close_clicked(self):
        self.delete_extracted_files()
        self.make_default_list()

    def on_clicked_list_item(self, item):
        if item.data(0) == 'Не выбран архив':
            return
        new = 2
        path = os.getcwd()
        file = path + "/ext_archive/" + str(item.data(0))
        webbrowser.open(file, new=new)

    def on_button_download_clicked(self):
        ...
        #self.webparser.get_object_declarations(8242)
        #rename_file()

    def on_clicked_compare_button(self):
        directory = "ext_archive"
        pdfs = os.listdir(directory)
        i = 0
        for file in pdfs:
            pdfs[i] = 'ext_archive/' + file
            i += 1
        df = start_compare(pdfs)
        chosen_file, _ = QtWidgets.QFileDialog.getSaveFileName()
        print(f"{chosen_file}.xlsx")
        df.to_excel(f"{chosen_file}.xlsx")
        print(df)

    def on_button_back_clicked(self):
        if self.list_developer.isVisible():
            pass
        if self.list_object.isVisible():
            self.list_developer.setVisible(True)
            self.list_object.setVisible(False)
            self.list_pdf.setVisible(False)
        if self.list_pdf.isVisible():
            self.list_developer.setVisible(False)
            self.list_object.setVisible(True)
            self.list_pdf.setVisible(False)