import os
import FreeCADGui as Gui
import FreeCAD as App
from freecad.vendor_parts import ADDONPATH, ICONPATH

# setup preferences page
Gui.addPreferencePage(os.path.join(
    ICONPATH, 'Preferences.ui'), 'Vendor Parts')
Gui.addIconPath(ICONPATH)

UserParams = App.ParamGet(
    "User parameter:BaseApp/Preferences/Mod/VendorParts")
print("vendor list path is "+UserParams.GetString("VendorListPath"))
if not UserParams.GetString("VendorListPath"):
    print("filepath is none, overriding")
    UserParams.SetString("VendorListPath", os.path.join(
        ADDONPATH, "VendorList.txt"))


class MCMWorkbench(Gui.Workbench):
    MenuText = "Vendor Parts"
    ToolTip = "Import parts from supplier websites"
    Icon = os.path.join(ICONPATH, "vp_addon.svg")
    toolbox = []

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        from freecad.vendor_parts import vendorpartstools
        self.toolbox = vendorpartstools.commandlist
        self.appendToolbar("McMaster-Carr", self.toolbox)
        self.appendMenu("McMaster-Carr", self.toolbox)

    def Activated(self):
        pass

    def Deactivated(self):
        pass


Gui.addWorkbench(MCMWorkbench())
