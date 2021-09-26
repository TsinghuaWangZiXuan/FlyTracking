import sys
import os

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from tracker import *

sys.path.append('yolov5')
from yolov5.train import Train, train_parse_opt
from yolov5.detect import Detect, detect_parse_opt
from yolov5.split_data import split_data
from yolov5.utils.parser import get_config

sys.path.append('deepsort')
from deepsort.track import Track, track_parse_opt


class Thread(QThread):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self):
        self.func()


class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class MainWindow(QMainWindow, Ui_Tracker):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

        self.Label.clicked.connect(self.run_label)
        self.Train.clicked.connect(self.run_train)
        self.Detect.clicked.connect(self.run_detect)
        self.Track.clicked.connect(self.run_track)

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def run_label(self):
        print('Starting...')
        self.Thread = Thread(self.start_label)
        self.Thread.start()

    def start_label(self):
        os.system('labelImg/labelImg.exe')

    def run_train(self):
        print('Starting...')
        self.Thread = Thread(self.start_train)
        self.Thread.start()

    def start_train(self):
        cfg = get_config('yolov5/config/train_config.yaml')
        opt = train_parse_opt(weights=cfg.YOLOV5.WEIGHTS,
                              data=cfg.YOLOV5.DATA,
                              epochs=cfg.YOLOV5.EPOCHS,
                              batch_size=cfg.YOLOV5.BATCH_SIZE)
        print(opt)
        split_data()
        Train(opt)

    def run_detect(self):
        print('Starting...')
        self.Tread = Thread(self.start_detect)
        self.Tread.start()

    def start_detect(self):
        cfg = get_config('yolov5/config/detect_config.yaml')
        opt = detect_parse_opt(weights=cfg.YOLOV5.WEIGHTS,
                               source=cfg.YOLOV5.SOURCE,
                               conf_thres=cfg.YOLOV5.CONF_THRES,
                               iou_thres=cfg.YOLOV5.IOU_THRES,
                               max_det=cfg.YOLOV5.MAX_DET)
        Detect(opt)

    def run_track(self):
        print('Starting...')
        self.Tread = Thread(self.start_track)
        self.Tread.start()

    def start_track(self):
        cfg = get_config('deepsort/config/track_config.yaml')
        opt = track_parse_opt(yolo_weights=cfg.DEEPSORT.WEIGHTS,
                              source=cfg.DEEPSORT.SOURCE,
                              conf_thres=cfg.DEEPSORT.CONF_THRES,
                              iou_thres=cfg.DEEPSORT.IOU_THRES)
        Track(opt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWin = MainWindow()
    MainWin.setWindowTitle("Tracker")
    MainWin.setWindowIcon(QIcon('fly.ico'))
    MainWin.show()
    sys.exit(app.exec_())
