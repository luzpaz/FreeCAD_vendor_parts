from PySide import QtGui, QtUiTools, QtCore
from PySide2 import QtWidgets
from PySide2 import QtWebEngineWidgets
from PySide2 import QtWebChannel
import FreeCADGui
import FreeCAD
import ImportGui
from freecad.mcm_addon import ICONPATH
import os


class Dialog(QtGui.QDockWidget):
    def __init__(self):
        mw = FreeCAD.Gui.getMainWindow()
        super(Dialog, self).__init__()
        self.setParent(mw)
        # Setup the widget.
        self.setObjectName("MCM_Dock")
        self.setWindowTitle("MCMaster Carr Browser")
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
        self.webView.setUrl("https://www.mcmaster.com/")

    def on_downloadRequested(self, download):
        self.objpath = download.path()
        download.finished.connect(self.insert_obj)
        download.accept()

    def insert_obj(self):
        doc = FreeCAD.ActiveDocument
        # just create a new document if there isn't one open
        if not doc:
            doc = FreeCAD.newDocument()
        # error if the user didn't download the part as a supported fmt:
        if self.objpath.split(".")[-1] != "STEP":
            FreeCAD.Console.PrintError(
            "McMaster-Carr Error: Download format must be STEP!\n")
            os.remove(self.objpath)
            return    
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
        newObj.addProperty("App::PropertyString", "McmasterPartNumber")
        newObj.McmasterPartNumber = label#.split("_")[0]
        newObj.setPropertyStatus("McmasterPartNumber", "ReadOnly")
        doc.recompute()


class toggleBrowserCmd():
    def GetResources(self):
        return {'Pixmap': os.path.join(ICONPATH, "mcm_addon.svg"),
                'MenuText': "McMaster-Carr browser",
                'ToolTip': "Toggle McMaster-Carr browser"}

    def Activated(self):
        pe = FreeCAD.Gui.getMainWindow().findChild(QtGui.QWidget, 'MCM_Dock')
        if not pe:
            FreeCAD.Gui.getMainWindow().addDockWidget(
                QtCore.Qt.RightDockWidgetArea, Dialog())
        else:
            pe.setVisible(pe.isHidden())

    def IsActive(self):
        return True


class viewPartCmd():
    def GetResources(self):
        return {'Pixmap': os.path.join(ICONPATH, "open_part.svg"),
                'MenuText': "McMaster-Carr part lookup",
                'ToolTip': "open the catalog page for the selected McMaster part"}

    def Activated(self):
        pe = FreeCAD.Gui.getMainWindow().findChild(QtGui.QWidget, 'MCM_Dock')
        if not pe:
            pe = Dialog()
            FreeCAD.Gui.getMainWindow().addDockWidget(
                QtCore.Qt.RightDockWidgetArea, pe)
        else:
            pe.setVisible(True)
        partNumber = FreeCADGui.Selection.getSelection()[0].McmasterPartNumber
        pe.webView.setUrl("https://www.mcmaster.com/"+partNumber)

    def IsActive(self):
        return ("McmasterPartNumber" in FreeCADGui.Selection.getSelection()[0].PropertiesList)


FreeCADGui.addCommand('mcm_toggleBrowser', toggleBrowserCmd())
FreeCADGui.addCommand('mcm_viewPart', viewPartCmd())
