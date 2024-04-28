from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QListWidgetItem
from interface.Developer import Developer

class DeveloperWidget(QListWidgetItem):

    id: int
    devInn: int
    name: str

    def __init__(self, developer: Developer, parent=None):
        super(DeveloperWidget, self).__init__(parent)

        font_list = QFont()
        font_list.setFamilies([u"Comic Sans MS"])
        font_list.setPointSize(13)

        self.id = developer.id
        self.devInn = developer.devInn
        self.name = developer.name

        labelInn = QLabel(self.devInn)
        labelInn.setFont(font_list)
        labelName = QLabel(self.name)
        labelName.setFont(font_list)

        layout = QVBoxLayout()
        layout.addWidget(labelInn)
        layout.addWidget(labelName)

        self.setText(self.devInn + '\n' + self.name)
        self.setFont(font_list)
