import os
import FreeCADGui as Gui
import FreeCAD as App
from freecad.mcm_addon import ICONPATH


class MCMWorkbench(Gui.Workbench):
    MenuText = "McMaster-Carr"
    ToolTip = "Insert McMaster-Carr parts"
    Icon = os.path.join(ICONPATH, "mcm_addon.svg")
    toolbox = []

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        from freecad.mcm_addon import mcmtools
        self.toolbox = ["mcm_toggleBrowser", "mcm_viewPart"]
        self.appendToolbar("Tools", self.toolbox)
        self.appendMenu("Tools", self.toolbox)

    def Activated(self):
        pass

    def Deactivated(self):
        pass


Gui.addWorkbench(MCMWorkbench())
