try:
    from PySide2.QtWidgets import QListWidget, QListWidgetItem
    from PySide2.QtCore import Qt
except ImportError:
    from PySide.QtWidgets import QListWidget, QListWidgetItem
    from PySide.QtCore import Qt


class ObjectList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QListWidget.SingleSelection)

    def add_item(self, obj):
        """
        Adds an object to the list widget, displaying its string representation.
        The original object is stored in the item's UserRole data.
        """
        display_text = str(obj)
        item = QListWidgetItem(display_text)
        item.setData(Qt.UserRole, obj)
        self.addItem(item)

    def add_items(self, obj_list, clear_first=False):
        """
        Adds multiple objects to the list widget.

        :param obj_list: A list of objects to add.
        :param clear_first: If True, clear the list before adding new items.
        """
        if clear_first:
            self.clear()
        for obj in obj_list:
            self.add_item(obj)

    def get_selected_object(self):
        """
        Returns the original object associated with the currently selected item.
        If no item is selected, returns None.
        """
        item = self.currentItem()
        if item is None:
            return None
        return item.data(Qt.UserRole)

    def get_all_objects(self):
        """
        Returns a list of all stored objects in the list widget.
        """
        objects = []
        for index in range(self.count()):
            item = self.item(index)
            objects.append(item.data(Qt.UserRole))
        return objects

    def clear(self):
        """
        Clears the list widget.
        """
        super().clear()
