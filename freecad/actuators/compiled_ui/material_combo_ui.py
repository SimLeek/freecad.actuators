import traceback

try:
    import FreeCAD
    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False

try:
    from PySide2.QtWidgets import QComboBox, QCompleter
    from PySide2.QtCore import Qt
except ImportError:
    from PySide.QtWidgets import QComboBox, QCompleter
    from PySide.QtCore import Qt

class QMaterialComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.completer().setFilterMode(Qt.MatchContains)
        self.populate_materials()

    def populate_materials(self):
        """Populate combo box with materials if FreeCAD is available."""
        if FREECAD_AVAILABLE:
            try:
                material_dir = FreeCAD.getUserMacroDir(True) + "Materials/"
                materials = []
                if os.path.exists(material_dir):
                    for file in os.listdir(material_dir):
                        if file.endswith(".FCMat"):
                            materials.append(file.replace(".FCMat", ""))
                self.addItems(materials)
                self.setCurrentIndex(-1)
            except Exception as e:
                self.addItem("Error loading FreeCAD materials: " + str(e))
                self.setEnabled(False)
        else:
            self.addItem("FreeCAD materials not available outside of FreeCAD")
            self.setEnabled(False)

    def get_selected_material(self):
        """Return the selected material name if FreeCAD is available."""
        if FREECAD_AVAILABLE and self.currentText() and "Error" not in self.currentText():
            return self.currentText()
        return None