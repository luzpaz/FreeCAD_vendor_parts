'''
from PySide import QtGui, QtUiTools, QtCore
from PySide2 import QtWidgets
from PySide2 import QtWebEngineWidgets
try:
    from PySide2 import QtWebChannel
except ImportError:
    raise Exception(
        "Missing package. Please install: python3-pyqt5.qtwebchannel.")
'''
from PySide import QtGui, QtUiTools, QtCore
from PySide2 import QtWidgets
from PySide2 import QtWebEngineWidgets
from PySide2 import QtWebChannel

import FreeCADGui
import FreeCAD
import ImportGui
from freecad.vendor_parts import ICONPATH
import os
from zipfile import ZipFile
import string
import random
import tempfile


# parse the list of available vendor urls
UserParams = FreeCAD.ParamGet(
    "User parameter:BaseApp/Preferences/Mod/VendorParts")
vendors = {}
with open(UserParams.GetString("VendorListPath")) as f:
    for line in f.readlines():
        url = line[:-1]
        sitename = url.removeprefix("https://")
        sitename = sitename.removeprefix("www.")
        sitename = ".".join(sitename.split(".")[:-1])
        vendors[sitename] = (url,sitename+".ico")
print(vendors)


class Dialog(QtGui.QDockWidget):
    def __init__(self):
        mw = FreeCAD.Gui.getMainWindow()
        super(Dialog, self).__init__()
        self.setParent(mw)
        # Setup the widget.
        self.setObjectName("MCM_Dock")
        self.setWindowTitle("Embedded Part Vendor Browser")
        # Grab the browser.
        self.webView = QtWebEngineWidgets.QWebEngineView()
        # Prepare a widget & layout.
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(QtWidgets.QHBoxLayout())
        self.layout.addWidget(self.webView)
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        profile = QtWebEngineWidgets.QWebEngineProfile(
            "McmAddon", self.webView)
        profile.downloadRequested.connect(self.on_downloadRequested)
        page = QtWebEngineWidgets.QWebEnginePage(profile, self.webView)
        self.webView.setPage(page)
        channel = QtWebChannel.QWebChannel(self)
        self.webView.page().setWebChannel(channel)
        self.webView.setUrl(vendors["mcmaster"][0])

    def on_downloadRequested(self, download):
        self.objpath = download.path()
        download.finished.connect(self.insert_obj)
        download.accept()

    def insert_obj(self):
        doc = FreeCAD.ActiveDocument
        # just create a new document if there isn't one open
        if not doc:
            doc = FreeCAD.newDocument()
        fileExtension = self.objpath.split(".")[-1]
        if fileExtension.lower() in ("step", "stp"):
            label = os.path.basename(self.objpath).split("_")[0]
            ImportGui.insert(self.objpath, doc.Name)
            docObj = doc.Objects[-1]
            os.remove(self.objpath)
            self.objpath = None
            # upgrade weirdly imported parts to have a nicer document structure
            if docObj.TypeId == 'Part::Compound2':
                subobjects = docObj.Links
                doc.removeObject(docObj.Name)
                newObj = doc.addObject("App::Part", label)
                newObj.Group = subobjects
                for x in subobjects:
                    x.Visibility = True
            else:
                newObj = docObj
        elif fileExtension.lower() == "zip":
            tmpExtractFolder = os.path.join(tempfile.gettempdir(), "".join(
                random.choice(string.ascii_lowercase) for _ in range(10)))
            os.mkdir(tmpExtractFolder)
            print(f"extract folder is {tmpExtractFolder}")
            with ZipFile(self.objpath, 'r') as zip:
                zip.extractall(tmpExtractFolder)
            print("files are:", os.listdir(tmpExtractFolder))
            for thefile in os.listdir(tmpExtractFolder):
                if thefile.split(".")[-1].lower() in ("step", "stp"):
                    ImportGui.insert(os.path.join(
                        tmpExtractFolder, thefile), doc.Name)
            pass
        # error if the user didn't download the part as a supported fmt:
        else:
            FreeCAD.Console.PrintError(
                f"Error: Download format ({fileExtension}) not supported!\n")
            os.remove(self.objpath)
            return
        doc.recompute()


class toggleBrowserCmd():
    def __init__(self, vendor):
        self.vendor = vendor

    def GetResources(self):
        return {'Pixmap': os.path.join(ICONPATH, vendors[self.vendor][1]),
                'MenuText': self.vendor + " browser",
                'ToolTip': f"Show {self.vendor} browser"}

    def Activated(self):
        pe = FreeCAD.Gui.getMainWindow().findChild(QtGui.QWidget, 'MCM_Dock')
        if not pe:
            FreeCAD.Gui.getMainWindow().addDockWidget(
                QtCore.Qt.RightDockWidgetArea, Dialog())
            pe = FreeCAD.Gui.getMainWindow().findChild(QtGui.QWidget, 'MCM_Dock')
        else:
            pe.setVisible(True)
        pe.webView.setUrl(vendors[self.vendor][0])

    def IsActive(self):
        return True


commandlist = []
for key in vendors.keys():
    commandname = key+"_toggleBrowser"
    FreeCADGui.addCommand(commandname, toggleBrowserCmd(key))
    commandlist.append(commandname)
