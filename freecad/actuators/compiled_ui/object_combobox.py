try:
    from PySide2.QtWidgets import QComboBox
except ImportError:
    from PySide.QtWidgets import QComboBox

class ObjectComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._object_map = {}  # Maps display text to original objects

    def add_item(self, obj):
        """Adds an object to the combo box, displaying its string representation."""
        display_text = str(obj)  # What the user sees
        self._object_map[display_text] = obj  # Store the object internally
        self.addItem(display_text)

    def add_items(self, obj_list):
        """Replaces all items with a new list of objects."""
        #self.clear()
        #self._object_map.clear()
        for obj in obj_list:
            self.add_item(obj)

    def get_selected_object(self):
        """Returns the original object associated with the selected item."""
        selected_text = self.currentText()  # Get the displayed text
        return self._object_map.get(selected_text, None)  # Return the stored object

    def clear(self):
        """Clears both the UI and internal object mapping."""
        super().clear()
        self._object_map.clear()
