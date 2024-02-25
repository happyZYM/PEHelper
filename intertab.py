from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QTabWidget, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QDialog, QHBoxLayout, QFileDialog

class IntermediateVariableWidget(QWidget):
  def __init__(self, name, expr, parent):
    super().__init__()
    self.parent_reference = parent

    self.layout = QHBoxLayout()

    self.name_label = QLabel("Name:")
    self.name_input = QLineEdit(name)
    self.name_input.textChanged.connect(self.parent_reference.parent_reference.update_window_title)
    self.name_input.setFixedWidth(100)  # Set a fixed width for the name field
    self.equal_label = QLabel("=")
    self.expr_input = QLineEdit(expr)
    self.expr_input.textChanged.connect(self.parent_reference.parent_reference.update_window_title)

    self.layout.addWidget(self.name_label)
    self.layout.addWidget(self.name_input)
    self.layout.addWidget(self.equal_label)
    self.layout.addWidget(self.expr_input)

    self.setLayout(self.layout)

  def get_name(self):
    return self.name_input.text()

  def get_expr(self):
    return self.expr_input.text()

class DragDropListWidget(QListWidget):
  def dropEvent(self, event):
    super().dropEvent(event)
    self.parent().track_order()
class IntermediateVariablesTab(QWidget):
  def track_order(self):
    print("track_order")
    self.parent_reference.update_window_title()
  def __init__(self, parent, _data):
    super().__init__(parent)
    self.parent_reference = parent

    self.layout = QVBoxLayout()

    self.intermediate_list = DragDropListWidget()
    self.intermediate_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
    self.intermediate_list.setDefaultDropAction(Qt.DropAction.MoveAction)
    self.intermediate_list.setSortingEnabled(True)

    self.setup_list(_data)
    self.layout.addWidget(self.intermediate_list)

    # Add "+" button for adding an intermediate variable
    add_button = QPushButton("+ Add Intermediate")
    add_button.clicked.connect(self.add_intermediate_variable)
    self.layout.addWidget(add_button)

    self.setLayout(self.layout)

  def setup_list(self, _data):
    # clear existing items
    self.intermediate_list.clear()
    # Add your logic to create items in the list based on self.data["intermediate_vars"]
    self.data=_data
    for i in range(len(self.data["intermediate_vars"])):
      var=self.data["intermediate_vars"][-i-1]
      item = QListWidgetItem(self.intermediate_list)
      widget = IntermediateVariableWidget(var["name"], var["expr"], self)
      item.setSizeHint(widget.sizeHint())
      self.intermediate_list.setItemWidget(item, widget)

  def update_data_from_list(self):
    # Update self.data["intermediate_vars"] based on the current order in the list
    intermediate_vars = []
    for i in range(self.intermediate_list.count()):
        item = self.intermediate_list.item(i)
        widget = self.intermediate_list.itemWidget(item)
        intermediate_vars.append({"name": widget.get_name(), "expr": widget.get_expr()})
    self.data["intermediate_vars"] = intermediate_vars
  def add_intermediate_variable(self):
    # Add an intermediate variable to the end of the list
    item = QListWidgetItem(self.intermediate_list)
    widget = IntermediateVariableWidget("NewVar", "expr", self)
    item.setSizeHint(widget.sizeHint())
    self.intermediate_list.setItemWidget(item, widget)
    self.parent_reference.update_window_title()

  def contextMenuEvent(self, event):
    # Context menu for right-clicking on an item
    context_menu = QMenu(self)

    delete_action = QAction("Delete", self)
    delete_action.triggered.connect(self.delete_selected_item)
    context_menu.addAction(delete_action)

    context_menu.exec(event.globalPos())

  def delete_selected_item(self):
    # Delete the selected item from the list
    selected_item = self.intermediate_list.currentItem()
    if selected_item:
      row = self.intermediate_list.row(selected_item)
      self.intermediate_list.takeItem(row)

    # Update the data after deleting an item
    self.update_data_from_list()
    self.parent_reference.update_window_title()