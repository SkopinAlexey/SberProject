from PySide6.QtWidgets import QWidgetItem, QListWidgetItem
from interface.BuildingWidget import BuildingWidget
from interface.Building import Building

class BuildingWidgetItem(QListWidgetItem):

    build: Building

    def __init__(self, build: Building, parent=None):
        super(BuildingWidgetItem, self).__init__(parent)
        self.setText('\n\n\n')
        self.build = build
