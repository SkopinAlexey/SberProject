from PySide6.QtWidgets import  QListWidgetItem
from interface.Building import Building


class BuildingWidgetItem(QListWidgetItem):
    buyld: Building

    def __init__(self, build1: Building, parent=None):
        super(BuildingWidgetItem, self).__init__(parent)
        # self.setText('\n\n\n')
        self.buyld = build1
        self.setText(str(self.buyld.objId) + '\n' + self.buyld.shortAddr + '\n' + self.buyld.objCommercNm)
