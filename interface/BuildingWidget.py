from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from interface.Building import Building

class BuildingWidget(QWidget):

    objId: str
    shortAddr: str
    objCommercNm: str

    def __init__(self, build: Building, parent=None):
        super(BuildingWidget, self).__init__(parent)

        self.objId = str(build.objId)
        self.shortAddr = build.shortAddr
        self.objCommercNm = build.objCommercNm

        id_label = QLabel(self.objId)
        adress_label = QLabel(self.shortAddr)
        name_label = QLabel(self.objCommercNm)

        layout = QVBoxLayout()
        layout.addWidget(id_label)
        layout.addWidget(adress_label)
        if build.objCommercNm != 'noname':
            layout.addWidget(name_label)


        self.setFixedHeight(100)
        self.setLayout(layout)