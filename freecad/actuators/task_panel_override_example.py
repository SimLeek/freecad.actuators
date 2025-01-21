import FreeCADGui as Gui
import PySide.QtGui as QtGui
# NOTE: Use pyside2 or "designer" for FreeCAD, then change the pyside2 imports to pyside
class CustomTaskPanel(QtGui.QWidget):
    def __init__(self):
        self.base = QtGui.QWidget()
        self.form = self.base

        label = QtGui.QLabel(self.form)
        label.setText("something")

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Cancel
                   | QtGui.QDialogButtonBox.Ok
                   | QtGui.QDialogButtonBox.Apply)

    def clicked(self, bt):
        if bt == QtGui.QDialogButtonBox.Apply:
            print("Apply")

    def accept(self):
        print("Accept")
        self.finish()

    def reject(self):
        print("Reject")
        self.finish()

    def finish(self):
        Gui.Control.closeDialog()
        # Gui.ActiveDocument.resetEdit()


Gui.Control.showDialog(CustomTaskPanel())