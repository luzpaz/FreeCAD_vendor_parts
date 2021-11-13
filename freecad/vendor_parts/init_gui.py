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
if not UserParams.GetString("VendorListPath"):
    UserParams.SetString("VendorListPath", os.path.join(
        ADDONPATH, "VendorList.txt"))


class VendorPartsWorkbench(Gui.Workbench):
    MenuText = "Vendor Parts"
    ToolTip = "Import parts from supplier websites"
    Icon = os.path.join(ICONPATH, "preferences-vendor_parts.svg")
    toolbox = []

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        from freecad.vendor_parts import vendorpartstools
        self.toolbox = vendorpartstools.commandlist
        self.appendToolbar("Vendor Parts", self.toolbox)
        self.appendMenu("Vendor Parts", self.toolbox)

    def Activated(self):
        pass

    def Deactivated(self):
        pass


Gui.addWorkbench(VendorPartsWorkbench())
