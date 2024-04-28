from PySide6.QtCore import QThread, Signal, QRunnable, Slot, QObject


class DownloadSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)

class DownloadThread(QRunnable):

    def __init__(self, function, *args, **kwargs):
        super().__init__()

        self.signals = DownloadSignals()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @Slot()
    def run(self):
        #result = web_parser.get_developers_list()
        #print(result)
        result = self.function(*self.args, **self.kwargs)
        self.signals.result.emit(result)