from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2 import QtWidgets, QtCore, QtGui

import sys, os, json, functools, webbrowser

class MainWindow(QtWidgets.QWidget):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        self.__init_file_sys__()
        self.__init_style__()
        self.__init_widgets__()
        self.__init_layout__()
        self.__load_ui__()

    def __init_file_sys__(self):
        appdata = os.getenv("APPDATA")
        app_folder = os.path.join(appdata, "THELauncher\\")
        self.btns_file = os.path.join(app_folder, "btns.json")

        if not os.path.exists(app_folder):
            os.makedirs(app_folder)

        if not os.path.exists(self.btns_file):
            with open(self.btns_file, "w") as f:
                json.dump([
                    {
                        "name":"Add New",
                        "function":"New",
                        "image": "",
                        "exe": ""
                    }
                ], f, indent=4)
                f.close()

        if os.path.exists(self.btns_file):
            self.read_f()

    def __init_layout__(self):
        self.main_layout.addWidget(self.btn_del, 1, 10)
        self.main_layout.addWidget(self.scroll_area, 2, 1, 1, 10)

        self.v_layout.addWidget(self.hwid)

        self.scrollwid.setLayout(self.v_layout)
        self.scroll_area.setWidget(self.scrollwid)

    def __init_style__(self):
        with open(self.appctxt.get_resource("stylesheet.qss"), "r") as stylesheetfile:
            self.setStyleSheet(stylesheetfile.read())
            stylesheetfile.close()

    def __init_widgets__(self):
        self.main_layout = QtWidgets.QGridLayout(self)
        self.main_layout.setMargin(5)
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setAlignment(QtCore.Qt.AlignHCenter)
        self.scroll_area.setWidgetResizable(True)

        self.scrollwid = QtWidgets.QWidget()
        
        self.v_layout = QtWidgets.QVBoxLayout()
        self.v_layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.h_layout_0 = QtWidgets.QGridLayout()
        self.h_layout_0.setAlignment(QtCore.Qt.AlignLeft)

        self.hwid = QtWidgets.QWidget()
        self.hwid.setFixedHeight(275)
        self.hwid.setLayout(self.h_layout_0)

        self.btn_del = QtWidgets.QPushButton("X")
        self.btn_del.setObjectName("close")
        self.btn_del.setFixedSize(15,15)
        self.btn_del.clicked.connect(self.delete)

        self.btns = []
        self.lbls = []
        self.layouts = [self.h_layout_0]
        self.hwidgets = [self.hwid]

    def __load_ui__(self):
        for i in self.btns:
            try:
                i.setParent(None)
            except:
                pass
        for i in self.lbls:
            try:
                i.setParent(None)
            except:
                pass

        self.btns = []
        self.lbls = []

        max = 2 * (self.width() / 200) -1

        for ind, config in enumerate(self.btns_config):
            btn = QtWidgets.QPushButton(config["name"])
            btn.setObjectName("game")
            btn.setFixedSize(179, 250)
            lbl = QtWidgets.QLabel()
            lbl.setFixedSize(179, 250)
            if config["function"] == "New":
                btn.clicked.connect(self.addbtn)
            elif config["function"] == "Link":
                btn.clicked.connect(functools.partial(self.open, ind))
            elif config["function"] == "Run":
                btn.clicked.connect(functools.partial(self.run, ind))
            if not config["image"] == "":
                lbl.setPixmap(QtGui.QPixmap(config["image"]))
            self.btns.append(btn)
            self.lbls.append(lbl)

        a = 0
        for i, btn in enumerate(self.btns):
            if self.layouts[a].count() < max:
                self.layouts[a].addWidget(self.lbls[i], 1, i+1)
                self.layouts[a].addWidget(btn, 1, i+1)
            else:
                a += 1
                try:
                    self.layouts[a].addWidget(self.lbls[i], 1, i+1)
                    self.layouts[a].addWidget(btn, 1, i+1)
                except:
                    newlay = QtWidgets.QGridLayout()
                    newlay.setAlignment(QtCore.Qt.AlignLeft)
                    newhwid = QtWidgets.QWidget()
                    newhwid.setFixedHeight(275)
                    self.layouts.append(newlay)
                    self.hwidgets.append(newhwid)
                    self.v_layout.addWidget(self.hwidgets[a])
                    self.hwidgets[a].setLayout(self.layouts[a])
                    self.layouts[a].addWidget(self.lbls[i], 1, i+1)
                    self.layouts[a].addWidget(btn, 1, i+1)

        for i, wid in enumerate(self.hwidgets):
            if wid.layout().count() > 0 and wid.parent() == None:
                self.v_layout.addWidget(self.hwidgets[i])
            if wid.layout().count() == 0:
                wid.setParent(None)

        self.scrollwid.setFixedHeight(275 * self.v_layout.count())

    def read_f(self):
        with open(self.btns_file, "r") as f:
            self.btns_config = json.load(f)
            f.close()
    
    def write_f(self, newbtn):
        with open(self.btns_file, "w") as f:
            self.btns_config.insert(-1, newbtn)
            json.dump(self.btns_config, f, indent=4)
            f.close()
        self.__load_ui__()

    def addbtn(self):
        self.dialog = NewBtn(self.write_f)
        self.dialog.showNormal()
    
    def delete(self):
        self.dialog = DelBtn(self.rm_btn, len(self.btns_config))
        self.dialog.showNormal()
    
    def rm_btn(self, ind):
        with open(self.btns_file, "w") as f:
            self.btns_config.pop(ind)
            json.dump(self.btns_config, f, indent=4)
            f.close()
        self.__load_ui__()

    def open(self, index):
        webbrowser.open(self.btns_config[index]["value"])
        self.close()
    
    def run(self, index):
        os.startfile(self.btns_config[index]["exe"])
        self.close()

    def resizeEvent(self, size):
        self.__load_ui__()
        return self, size

class NewBtn(QtWidgets.QWidget):

    def __init__(self, writef):
        super().__init__()
        self.setFixedSize(300,180)

        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.writef = writef
        self.lay = QtWidgets.QVBoxLayout(self)

        self.name = QtWidgets.QLineEdit()
        self.name.setPlaceholderText("Name")

        self.function = QtWidgets.QComboBox()
        self.function.addItems(["Link", "Run"])

        self.link = QtWidgets.QLineEdit()
        self.link.setPlaceholderText("Link to open (if LINK)")

        self.exe = QtWidgets.QLineEdit()
        self.exe.setPlaceholderText("Executable path (if RUN)")

        self.image = QtWidgets.QLineEdit()
        self.image.setPlaceholderText("FULL Path to image (175px/250px)")

        self.donebtn = QtWidgets.QPushButton("Done")
        self.donebtn.clicked.connect(self.done_)

        self.lay.addWidget(self.name)
        self.lay.addWidget(self.function)
        self.lay.addWidget(self.link)
        self.lay.addWidget(self.exe)
        self.lay.addWidget(self.image)
        self.lay.addWidget(self.donebtn)
    
    def done_(self):
        self.writef({
                        "name": self.name.text(),
                        "function": self.function.currentText(),
                        "value": self.link.text(),
                        "image": self.image.text(),
                        "exe": self.exe.text()
                    })
        self.close()

class DelBtn(QtWidgets.QWidget):

    def __init__(self, rm_btn, len):
        super().__init__()
        self.setFixedSize(400,50)

        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.rm_btn = rm_btn
        self.len = len

        self.lay = QtWidgets.QHBoxLayout(self)

        self.lbl = QtWidgets.QLabel("Index of btn (starting by 0)")

        self.nbr = QtWidgets.QSpinBox()
        self.nbr.setMinimum(0)
        self.nbr.setMaximum(self.len - 2)
        self.nbr.setSingleStep(1)

        self.donebtn = QtWidgets.QPushButton("Done")
        self.donebtn.clicked.connect(self.done_)

        self.lay.addWidget(self.lbl)
        self.lay.addWidget(self.nbr)
        self.lay.addWidget(self.donebtn)

    def done_(self):
        if not self.len == 1:
            self.rm_btn(self.nbr.value())
        else:
            self.error = QtWidgets.QMessageBox.critical(None,'Error!',"Cannot remove AddBtn!!", QtWidgets.QMessageBox.Ok)
        self.close()

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow(appctxt)
    window.showMaximized()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)