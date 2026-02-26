from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QTreeView
from collections.abc import Mapping, Sequence

def tree_model(window, data):

    print("touch")

    window.model = QStandardItemModel()
    window.model.setHorizontalHeaderLabels(["Key", "Value", "Lenght"])
    add_items(window.model.invisibleRootItem(), data)
    window.treeView.setModel(window.model)
    window.treeView.setEditTriggers(QTreeView.NoEditTriggers)

def add_items(parent, value):
    """
    Recursively populate the tree.
    Only show leaf values for bytes, int, float, str, bool
    """
    from collections.abc import Mapping, Sequence

    # Mapping = dict-like, Sequence = list/tuple-like
    if isinstance(value, Mapping):
        for k, v in value.items():
            key_item = QStandardItem(str(k))

            # Leaf vs nested
            if isinstance(v, (Mapping, Sequence)) and not isinstance(v, (str, bytes)):
                val_item = QStandardItem("")  # No value for nested
                length_item = QStandardItem(str(len(v)))  # Add length column
            else:
                val_item = QStandardItem(str(v))
                length_item = QStandardItem("")  # Leaf nodes have empty length

            parent.appendRow([key_item, val_item, length_item])

            # Recurse for nested items
            if isinstance(v, (Mapping, Sequence)) and not isinstance(v, (str, bytes)):
                add_items(key_item, v)

    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for i, v in enumerate(value):
            key_item = QStandardItem(f"[{i}]")

            if isinstance(v, (Mapping, Sequence)) and not isinstance(v, (str, bytes)):
                val_item = QStandardItem("")
                length_item = QStandardItem(str(len(v)))
            else:
                val_item = QStandardItem(str(v))
                length_item = QStandardItem("")

            parent.appendRow([key_item, val_item, length_item])

            if isinstance(v, (Mapping, Sequence)) and not isinstance(v, (str, bytes)):
                add_items(key_item, v)

    else:
        # Leaf values
        parent.appendRow([
            QStandardItem(str(value)),
            QStandardItem(str(value)),
            QStandardItem("")
        ])
