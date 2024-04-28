import time
import zipfile
import webbrowser
import os

from interface.Developer import Developer
from interface.DeveloperWidget import DeveloperWidget
from web_parser.web_parser import web_parser
from compare.compare import start_compare

from interface.DownloadThread import DownloadThread

from interface.Building import Building
from interface.BuildingWidgetItem import BuildingWidgetItem

from PySide6 import QtWidgets
from PySide6.QtCore import QRect, Slot, QThreadPool
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QMainWindow, QLabel, QStatusBar, \
    QListWidget, QListWidgetItem, QPushButton, QProgressBar, QInputDialog, QMessageBox


class MainWindow(QMainWindow):

    chosen_file = ""

    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

        self.setWindowTitle("My App")
        self.setFixedSize(1280, 1024)

        font = QFont()
        font.setFamilies([u"Comic Sans MS"])
        font.setPointSize(22)

        self.developers_label = QLabel(self)
        self.developers_label.setText("Список застройщиков:")
        self.developers_label.setObjectName(u"label")
        self.developers_label.setGeometry(QRect(90, 75, 400, 51))
        self.developers_label.setFont(font)

        self.compare_label = QLabel(self)
        self.compare_label.setText("♿Сравниваем...♿")
        self.compare_label.setGeometry(QRect(90, 520, 400, 40))
        self.compare_label.setFont(font)
        self.compare_label.setVisible(False)

        button_help = QAction("&О программе", self)
        button_help.setStatusTip("Показать данные о программе")

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        font_list = QFont()
        font_list.setFamilies([u"Comic Sans MS"])
        font_list.setPointSize(13)

        self.button_compare = QPushButton(self)
        self.button_compare.setGeometry(QRect(90, 470, 100, 40))
        self.button_compare.setFont(font_list)
        self.button_compare.setText("Сравнить")
        self.button_compare.clicked.connect(self.on_clicked_compare_button)
        self.button_compare.setVisible(False)

        self.buttonBack = QPushButton(self)
        self.buttonBack.setGeometry(QRect(310, 470, 100, 40))
        self.buttonBack.setFont(font_list)
        self.buttonBack.setText("Назад")
        self.buttonBack.clicked.connect(self.on_button_back_clicked)

        self.list_developer = QListWidget(self)
        self.list_developer.setGeometry(QRect(40, 140, 800, 301))
        self.list_developer.setStyleSheet("QLineEdit { background-color: white }")
        self.list_developer.setFont(font_list)

        self.list_object = QListWidget(self)
        self.list_object.setGeometry(QRect(40, 140, 800, 301))
        self.list_object.setStyleSheet("QLineEdit { background-color: white }")
        self.list_object.setFont(font_list)
        self.list_object.setVisible(False)

        self.list_pdf = QListWidget(self)
        self.list_pdf.setGeometry(QRect(40, 140, 800, 301))
        self.list_pdf.setStyleSheet("QLineEdit { background-color: white }")
        self.list_pdf.setFont(font_list)
        self.list_pdf.setVisible(False)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QRect(90, 140, 441, 20))
        self.progressBar.setVisible(False)

        self.list_all = {}

        thread = DownloadThread(web_parser.get_developers_list)
        thread.signals.result.connect(self.set_developers)
        self.threadpool.start(thread)

    @Slot(object)
    def set_developers(self, result):
        self.list_all = result

        for item in self.list_all:
            dev = Developer(id=item['id'], devInn=item['devInn'], name=item['name'])
            item_widget = DeveloperWidget(developer=dev)
            self.list_developer.addItem(item_widget)

        self.list_developer.itemClicked.connect(self.on_clicked_developer_list_item)

    def on_clicked_developer_list_item(self, item):
        self.list_developer.setVisible(False)
        self.list_object.setVisible(True)
        self.list_pdf.setVisible(False)
        self.button_compare.setVisible(False)
        self.developers_label.setText('Список объектов:')

        self.list_object.clear()
        id = item.id

        thread = DownloadThread(web_parser.get_developer_objects, id)
        thread.signals.result.connect(self.set_objects)
        self.threadpool.start(thread)

    @Slot(object)
    def set_objects(self, list_obj):

        for item in list_obj:
            obj = self.getBuilding(item)
            item_obj = BuildingWidgetItem(obj)
            self.list_object.addItem(item_obj)

        self.list_object.itemClicked.connect(self.on_clicked_building_list_item)

    def on_clicked_building_list_item(self, item):
        web_parser.get_object_declarations(item.buyld.objId)
        file = os.path.abspath(os.getcwd())
        self.delete_extracted_files()
        thread = DownloadThread(self.extractZip, f'{file}\obj{item.buyld.objId}_docs.zip')
        thread.signals.result.connect(self.set_extract)
        self.threadpool.start(thread)
        self.list_developer.setVisible(False)
        self.list_object.setVisible(False)
        self.list_pdf.setVisible(True)
        self.button_compare.setVisible(True)
        self.developers_label.setText('Список pdf-файлов:')

    def getBuilding(self, item):
        try:
            return Building(objId=item['objId'], shortAddr=item['shortAddr'], objCommercNm=item['objCommercNm'])
        except KeyError:
            return Building(objId=item['objId'], shortAddr=item['shortAddr'], objCommercNm='noname')

    def delete_extracted_files(self):
        directory = "ext_archive"
        files = os.listdir(directory)
        for file in files:
            path = os.path.join(directory, file)
            os.remove(path)

    def closeEvent(self, event):
        self.delete_extracted_files()

    @Slot(object)
    def set_extract(self, files):
        self.list_pdf.clear()
        for i in files:
            listWidgetItem = QListWidgetItem(i)
            self.list_pdf.addItem(listWidgetItem)

        self.list_pdf.itemClicked.connect(self.on_clicked_list_item)


    def extractZip(self, path):
        while True:
            try:
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall('ext_archive')

                directory = "ext_archive"
                files = os.listdir(directory)
                for file in files:
                    if not file.endswith('.pdf'):
                        os.rename(os.path.join(directory, file), os.path.join(directory, f"{file}.pdf"))
                os.remove(path)
                return os.listdir(directory)
            except PermissionError:
                pass
            except FileNotFoundError:
                pass


    def on_button_open_clicked(self):
        try:
            self.delete_extracted_files()

            chosen_file = QtWidgets.QFileDialog.getOpenFileName()[0]
            with zipfile.ZipFile(chosen_file, 'r') as zip_ref:
                zip_ref.extractall('ext_archive')
            directory = "ext_archive"
            files = os.listdir(directory)

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

    def on_clicked_list_item(self, item):
        new = 2
        path = os.getcwd()
        file = path + "/ext_archive/" + str(item.data(0))
        webbrowser.open(file, new=new)

    def on_clicked_compare_button(self):

        directory = "ext_archive"
        pdfs = os.listdir(directory)
        i = 0
        for file in pdfs:
            pdfs[i] = 'ext_archive/' + file
            i += 1
        self.compare_label.setVisible(True)
        thread = DownloadThread(start_compare, pdfs)
        thread.signals.result.connect(self.save_result)
        self.threadpool.start(thread)

    def start_progress_bar(self):
        self.progressBar.setVisible(True)
        self.progressBar.minimum = 0
        self.progressBar.maximum = 100
        self.progressBar.setValue(0)
        while self.progressBar.value() < 99:
            time.sleep(0.05)
            self.progressBar.setValue(self.progressBar.value()+1)

    @Slot(object)
    def save_result(self, result):
        try:
            chosen_file, _ = QtWidgets.QFileDialog.getSaveFileName(self,'Сохранить файл', 'result', 'xlsx files (*.xlsx);;All files*')
            result.to_excel(f"{chosen_file}.xlsx")
        except ValueError:
            pass
        self.compare_label.setVisible(False)

    def on_button_back_clicked(self):
        if self.list_developer.isVisible():
            pass
        elif self.list_object.isVisible():
            self.list_developer.setVisible(True)
            self.list_object.setVisible(False)
            self.list_pdf.setVisible(False)
            self.button_compare.setVisible(False)
            self.developers_label.setText('Список застройщиков:')
        elif self.list_pdf.isVisible():
            self.list_developer.setVisible(False)
            self.list_object.setVisible(True)
            self.list_pdf.setVisible(False)
            self.button_compare.setVisible(False)
            self.developers_label.setText('Список объектов:')
