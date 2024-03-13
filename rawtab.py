from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QTabWidget, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QDialog, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QKeySequence, QShortcut

class DragDropListWidget(QListWidget):
  def __init__(self, parent, parent_reference):
    super().__init__(parent)
    self.parent_reference = parent_reference
  def dropEvent(self, event):
    super().dropEvent(event)
    # update the order of the list
    self.parent_reference.update_var_list_order()
class RawVariablesTab(QWidget):
  def write_data_full_value(self, text):
    self.data["independent_vars"][self.variable_list.currentItem().text()]["var"]=text
    self.parent_reference.update_window_title()
  def write_data_full_uncertainty(self, text):
    self.data["independent_vars"][self.variable_list.currentItem().text()]["uncertainty"]=text
    self.parent_reference.update_window_title()
  def write_data_single_value(self, text):
    self.data["independent_vars"][self.variable_list.currentItem().text()]["var"]=text
    self.parent_reference.update_window_title()
  def write_data_single_tolerance(self, text):
    self.data["independent_vars"][self.variable_list.currentItem().text()]["tolerance"]=text
    self.parent_reference.update_window_title()
  def write_data_single_scale(self, text):
    self.data["independent_vars"][self.variable_list.currentItem().text()]["scale"]=text
    self.parent_reference.update_window_title()
  def write_data_single_system_error(self, text):
    self.data["independent_vars"][self.variable_list.currentItem().text()]["system_error"]=text
    self.parent_reference.update_window_title()
  def write_data_muiltiple_tolerance(self, text):
    self.data["independent_vars"][self.variable_list.currentItem().text()]["tolerance"]=text
    self.parent_reference.update_window_title()
  def write_data_muiltiple_scale(self, text):
    self.data["independent_vars"][self.variable_list.currentItem().text()]["scale"]=text
    self.parent_reference.update_window_title()
  def write_data_muiltiple_system_error(self, text):
    self.data["independent_vars"][self.variable_list.currentItem().text()]["system_error"]=text
    self.parent_reference.update_window_title()
  def __init__(self, parent, data):
    super().__init__(parent)
    self.parent_reference = parent
    self.data = data
    # Variable List
    self.variable_list = QListWidget(self)
    self.variable_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
    self.variable_list.itemClicked.connect(self.show_variable_details)
    self.variable_list.itemDoubleClicked.connect(self.edit_variable_name)
    self.variable_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    self.variable_list.customContextMenuRequested.connect(self.show_context_menu)

    # Add Raw Variable Button
    add_variable_button = QPushButton("Add Raw Variable", self)
    add_variable_button.clicked.connect(self.add_raw_variable)

    # Right Panel
    self.right_panel=QWidget()
    self.right_panel_layout=QVBoxLayout(self.right_panel)
    self.variable_type_combobox = QComboBox()
    self.variable_type_combobox.addItems(["Full", "Single", "Multiple"])
    self.variable_type_combobox.currentIndexChanged.connect(self.change_variable_type)
    self.variable_type_combobox.setEnabled(False)  # Initially disabled until a variable is selected
    self.variable_type_combobox.setCurrentIndex(-1)
    self.right_panel_info = QStackedWidget()
    self.right_panel_layout.addWidget(self.variable_type_combobox)
    self.right_panel_layout.addWidget(self.right_panel_info)

    # Placeholder Widget when no variable is selected
    placeholder_widget = QWidget(self.right_panel_info)
    placeholder_layout = QVBoxLayout(placeholder_widget)
    placeholder_label = QLabel("Please select a variable", placeholder_widget)
    placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    placeholder_layout.addWidget(placeholder_label)
    placeholder_layout.addStretch()
    self.right_panel_info.addWidget(placeholder_widget)

    # Full Variable Widget
    self.full_variable_widget = QWidget(self.right_panel_info)
    self.full_variable_layout = QVBoxLayout(self.full_variable_widget)
    self.full_var_value_label_hint = QLabel("Value:", self.full_variable_widget)
    self.full_var_value_label = QLineEdit("", self.full_variable_widget)  # Modified to QLineEdit
    self.full_var_value_label.textChanged.connect(self.write_data_full_value)
    self.full_var_value_label_container = QHBoxLayout()
    self.full_var_value_label_container.addWidget(self.full_var_value_label_hint)
    self.full_var_value_label_container.addWidget(self.full_var_value_label)
    self.full_var_uncertainty_label_hint = QLabel("Uncertainty:", self.full_variable_widget)
    self.full_var_uncertainty_label = QLineEdit("", self.full_variable_widget)  # Modified to QLineEdit
    self.full_var_uncertainty_label.textChanged.connect(self.write_data_full_uncertainty)
    self.full_var_uncertainty_label_container = QHBoxLayout()
    self.full_var_uncertainty_label_container.addWidget(self.full_var_uncertainty_label_hint)
    self.full_var_uncertainty_label_container.addWidget(self.full_var_uncertainty_label)
    self.full_variable_layout.addLayout(self.full_var_value_label_container)
    self.full_variable_layout.addLayout(self.full_var_uncertainty_label_container)
    self.full_variable_layout.addStretch()
    self.right_panel_info.addWidget(self.full_variable_widget)

    # Single Variable Widget
    self.single_variable_widget = QWidget(self.right_panel_info)
    self.single_variable_layout = QVBoxLayout(self.single_variable_widget)
    self.single_var_value_label_hint = QLabel("Value:", self.full_variable_widget)
    self.single_var_value_label = QLineEdit("", self.single_variable_widget)  # Modified to QLineEdit
    self.single_var_value_label.textChanged.connect(self.write_data_single_value)
    self.single_var_value_label_container = QHBoxLayout()
    self.single_var_value_label_container.addWidget(self.single_var_value_label_hint)
    self.single_var_value_label_container.addWidget(self.single_var_value_label)
    self.single_var_tolerance_label_hint = QLabel("Tolerance:", self.single_variable_widget)
    self.single_var_tolerance_label = QLineEdit("", self.single_variable_widget)  # Modified to QLineEdit
    self.single_var_tolerance_label.textChanged.connect(self.write_data_single_tolerance)
    self.single_var_tolerance_label_container = QHBoxLayout()
    self.single_var_tolerance_label_container.addWidget(self.single_var_tolerance_label_hint)
    self.single_var_tolerance_label_container.addWidget(self.single_var_tolerance_label)
    self.single_var_scale_label_hint = QLabel("Scale:", self.single_variable_widget)
    self.single_var_scale_label = QLineEdit("", self.single_variable_widget)  # Modified to QLineEdit
    self.single_var_scale_label.textChanged.connect(self.write_data_single_scale)
    self.single_var_scale_label_container = QHBoxLayout()
    self.single_var_scale_label_container.addWidget(self.single_var_scale_label_hint)
    self.single_var_scale_label_container.addWidget(self.single_var_scale_label)
    self.single_var_system_error_label_hint = QLabel("Systematic Error:", self.single_variable_widget)
    self.single_var_system_error_label = QLineEdit("", self.single_variable_widget)  # Modified to QLineEdit
    self.single_var_system_error_label.textChanged.connect(self.write_data_single_system_error)
    self.single_var_system_error_label_container = QHBoxLayout()
    self.single_var_system_error_label_container.addWidget(self.single_var_system_error_label_hint)
    self.single_var_system_error_label_container.addWidget(self.single_var_system_error_label)
    self.single_variable_layout.addLayout(self.single_var_value_label_container)
    self.single_variable_layout.addLayout(self.single_var_tolerance_label_container)
    self.single_variable_layout.addLayout(self.single_var_scale_label_container)
    self.single_variable_layout.addLayout(self.single_var_system_error_label_container)
    self.single_variable_layout.addStretch()
    self.right_panel_info.addWidget(self.single_variable_widget)
    

    # Multiple Variable Widget
    self.multiple_variable_widget = QWidget(self.right_panel_info)
    self.multiple_variable_layout = QVBoxLayout(self.multiple_variable_widget)
    self.multiple_var_tolerance_label_hint = QLabel("Tolerance:", self.multiple_variable_widget)
    self.multiple_var_tolerance_label = QLineEdit("", self.multiple_variable_widget)
    self.multiple_var_tolerance_label.textChanged.connect(self.write_data_muiltiple_tolerance)
    self.multiple_var_tolerance_label_container = QHBoxLayout()
    self.multiple_var_tolerance_label_container.addWidget(self.multiple_var_tolerance_label_hint)
    self.multiple_var_tolerance_label_container.addWidget(self.multiple_var_tolerance_label)
    self.multiple_var_scale_label_hint = QLabel("Scale:", self.multiple_variable_widget)
    self.multiple_var_scale_label = QLineEdit("", self.multiple_variable_widget)
    self.multiple_var_scale_label.textChanged.connect(self.write_data_muiltiple_scale)
    self.multiple_var_scale_label_container = QHBoxLayout()
    self.multiple_var_scale_label_container.addWidget(self.multiple_var_scale_label_hint)
    self.multiple_var_scale_label_container.addWidget(self.multiple_var_scale_label)
    self.multiple_var_system_error_label_hint = QLabel("Systematic Error:", self.multiple_variable_widget)
    self.multiple_var_system_error_label = QLineEdit("", self.multiple_variable_widget)
    self.multiple_var_system_error_label.textChanged.connect(self.write_data_muiltiple_system_error)
    self.multiple_var_system_error_label_container = QHBoxLayout()
    self.multiple_var_system_error_label_container.addWidget(self.multiple_var_system_error_label_hint)
    self.multiple_var_system_error_label_container.addWidget(self.multiple_var_system_error_label)
    self.add_data_button = QPushButton("Add Data", self.multiple_variable_widget)
    self.add_data_button.clicked.connect(self.add_data_to_multiple_var)
    shortcut = QShortcut(QKeySequence("Ctrl+A"), self)
    shortcut.activated.connect(self.add_data_to_multiple_var)

    self.data_list = DragDropListWidget(self.multiple_variable_widget, self)
    self.data_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.data_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    self.data_list.customContextMenuRequested.connect(self.show_data_context_menu)
    # allow drag and drop
    self.data_list.setDragEnabled(True)
    self.data_list.setAcceptDrops(True)
    self.data_list.setDropIndicatorShown(True)
    self.data_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
    self.data_list.setDragDropOverwriteMode(False)

    self.multiple_variable_layout.addLayout(self.multiple_var_tolerance_label_container)
    self.multiple_variable_layout.addLayout(self.multiple_var_scale_label_container)
    self.multiple_variable_layout.addLayout(self.multiple_var_system_error_label_container)
    self.multiple_variable_layout.addWidget(self.add_data_button)
    self.multiple_variable_layout.addWidget(self.data_list)
    self.right_panel_info.addWidget(self.multiple_variable_widget)

    # Layout Setup
    layout = QHBoxLayout(self)

    # Container for Variable List and Add Button
    variable_container = QVBoxLayout()
    variable_container.addWidget(self.variable_list)
    variable_container.addWidget(add_variable_button)

    # Set stretch factor for the variable container to give more space to the right panel
    layout.addLayout(variable_container, stretch=1)
    layout.addWidget(self.right_panel, stretch=4)  # Adjust the stretch factor as needed

    self.setLayout(layout)
  def change_variable_type(self, index):
    print("change_variable_type called")
    current_item = self.variable_list.currentItem()
    if current_item:
      variable_name = current_item.text()
      print("current name=", variable_name)
      variable_data = self.data["independent_vars"].get(variable_name, {})
      new_type = self.variable_type_combobox.currentText().lower()
      print("new type is", new_type)

      # Update the data with the new variable type
      actually_changed= (variable_data["type"] != new_type)
      if actually_changed:
        print("type actually changed, from {} to {}".format(variable_data["type"], new_type))
      variable_data["type"] = new_type

      # Update the right panel based on the new variable type
      if actually_changed:
        self.parent_reference.update_window_title()
        if new_type == "full":
          variable_data["var"] = "0"
          variable_data["uncertainty"] = "0"
          self.show_full_variable_details(variable_data)
        elif new_type == "single":
          variable_data["var"] = "0"
          variable_data["tolerance"] = "0"
          variable_data["scale"] = "1"
          variable_data["system_error"] = "0"
          self.show_single_variable_details(variable_data)
        elif new_type == "multiple":
          variable_data["var"] = []
          variable_data["tolerance"] = "0"
          variable_data["scale"] = "1"
          variable_data["system_error"] = "0"
          self.show_multiple_variable_details(variable_data)
  def show_variable_details(self, item):
    # clear previous selection
    self.variable_list.clearSelection()
    item.setSelected(True)
    self.variable_list.setCurrentItem(item)
    if self.variable_list.currentItem():
      print("currentItem is not None, it is", self.variable_list.currentItem().text())
    self.variable_type_combobox.setEnabled(True)
    variable_name = item.text()
    variable_data = self.data["independent_vars"].get(variable_name, {})

    if variable_data.get("type") == "full":
      self.show_full_variable_details(variable_data)
    elif variable_data.get("type") == "single":
      self.show_single_variable_details(variable_data)
    elif variable_data.get("type") == "multiple":
      self.show_multiple_variable_details(variable_data)
    else:
      self.right_panel_info.setCurrentIndex(0)  # Show placeholder when no valid type

  def show_full_variable_details(self, variable_data):
    self.variable_type_combobox.setCurrentText("Full")
    self.full_var_value_label.setText(f"{variable_data.get('var', '')}")
    self.full_var_uncertainty_label.setText(f"{variable_data.get('uncertainty', '')}")
    self.right_panel_info.setCurrentIndex(1)

  def show_single_variable_details(self, variable_data):
    self.variable_type_combobox.setCurrentText("Single")
    self.single_var_value_label.setText(f"{variable_data.get('var', '')}")
    self.single_var_tolerance_label.setText(f"{variable_data.get('tolerance', '')}")
    self.single_var_scale_label.setText(f"{variable_data.get('scale', '')}")
    self.single_var_system_error_label.setText(f"{variable_data.get('system_error', '')}")
    self.right_panel_info.setCurrentIndex(2)

  def show_multiple_variable_details(self, variable_data):
    self.variable_type_combobox.setCurrentText("Multiple")
    self.multiple_var_tolerance_label.setText(f"{variable_data.get('tolerance', '')}")
    self.multiple_var_scale_label.setText(f"{variable_data.get('scale', '')}")
    self.multiple_var_system_error_label.setText(f"{variable_data.get('system_error', '')}")
    self.right_panel_info.setCurrentIndex(3)

    # Update data list for multiple variable
    self.data_list.clear()
    for data_point in variable_data.get("var", []):
      item = QListWidgetItem(f"{data_point}")
      self.data_list.addItem(item)

  def flush_list(self, _data):
    self.data=_data
    self.variable_list.clear()
    self.right_panel_info.setCurrentIndex(0)
    self.variable_type_combobox.setEnabled(False)
    self.variable_type_combobox.setCurrentIndex(-1)
    for variable_name in self.data["independent_vars"]:
      print("find a var called", variable_name)
      item = QListWidgetItem(variable_name)
      self.variable_list.addItem(item)
  def add_raw_variable(self):
    new_variable_name, ok = QInputDialog.getText(self, "Add Raw Variable", "Enter Variable Name:")
    if ok and new_variable_name:
      # Add the new variable to the data
      self.data["independent_vars"][new_variable_name] = {"type": "full", "var": 0, "uncertainty": 0}
      # Update the variable list
      item = QListWidgetItem(new_variable_name)
      self.variable_list.addItem(item)
      # clear previous selection
      self.variable_list.clearSelection()
      # Automatically select the new variable
      item.setSelected(True)
      self.variable_list.setCurrentItem(item)
      # Show the details of the new variable
      self.show_variable_details(item)
      self.parent_reference.update_window_title()

  def edit_variable_name(self, item):
    variable_name, ok = QInputDialog.getText(self, "Edit Variable Name", "Enter Variable Name:", text=item.text())
    if ok and variable_name:
      # Update the data with the new variable name
      old_variable_name = item.text()
      variable_data = self.data["independent_vars"].pop(old_variable_name)
      self.data["independent_vars"][variable_name] = variable_data
      # Update the variable list
      item.setText(variable_name)
      self.parent_reference.update_window_title()

  def show_context_menu(self, position):
    # Make custom Item and selected Item always the same
    self.variable_list.clearSelection()
    item = self.variable_list.itemAt(position)
    if item:
      item.setSelected(True)
      menu = QMenu(self)
      delete_action = QAction("Delete", self)
      delete_action.triggered.connect(self.delete_selected_variables)
      menu.addAction(delete_action)
      change_name_action = QAction("Edit Name", self)
      change_name_action.triggered.connect(lambda: self.edit_variable_name(self.variable_list.currentItem()))
      menu.addAction(change_name_action)
      menu.exec(self.variable_list.mapToGlobal(position))

  def delete_selected_variables(self):
    selected_items = self.variable_list.selectedItems()
    for item in selected_items:
      variable_name = item.text()
      # Remove the variable from the data
      self.data["independent_vars"].pop(variable_name, None)
      # Remove the variable from the list
      row = self.variable_list.row(item)
      self.variable_list.takeItem(row)
      self.variable_list.setCurrentItem(None)
      # Clear the right panel if the deleted variable was being displayed
      self.right_panel_info.setCurrentIndex(0)
      self.variable_type_combobox.setEnabled(False)
      self.variable_type_combobox.setCurrentIndex(-1)
      self.parent_reference.update_window_title()

  def update_var_list_order(self):
    # Update the order of the var list after dropping
    current_item = self.variable_list.currentItem()
    if current_item:
      variable_name = current_item.text()
      variable_data = self.data["independent_vars"].get(variable_name, {})
      if variable_data.get("type") == "multiple":
        # Update the data list
        new_order = []
        for i in range(self.data_list.count()):
          item = self.data_list.item(i)
          new_order.append(item.text())
        variable_data["var"] = new_order
        self.parent_reference.update_window_title()

  def add_data_to_multiple_var(self):
    current_item = self.variable_list.currentItem()
    if current_item:
      variable_name = current_item.text()
      variable_data = self.data["independent_vars"].get(variable_name, {})
      if variable_data.get("type") == "multiple":
        new_data_point, ok = QInputDialog.getText(self, "Add Data", "Enter Data Point:")
        if ok:
          # Add the new data point to the data
          variable_data["var"].append(new_data_point)
          # Update the data list
          item = QListWidgetItem(f"{new_data_point}")
          self.data_list.addItem(item)
          self.parent_reference.update_window_title()

  def show_data_context_menu(self, position):
    # check if an item is right-clicked
    item = self.data_list.itemAt(position)
    if item:
      menu = QMenu(self)
      delete_action = QAction("Delete", self)
      delete_action.triggered.connect(self.delete_selected_data_points)
      menu.addAction(delete_action)
      edit_action = QAction("Edit", self)
      edit_action.triggered.connect(self.edit_selected_data_point)
      menu.addAction(edit_action)
      menu.exec(self.data_list.mapToGlobal(position))
  def edit_selected_data_point(self):
    current_item = self.variable_list.currentItem()
    if current_item:
      variable_name = current_item.text()
      variable_data = self.data["independent_vars"].get(variable_name, {})
      if variable_data.get("type") == "multiple":
        selected_items = self.data_list.selectedItems()
        for item in selected_items:
          data_point = item.text()
          new_data_point, ok = QInputDialog.getText(self, "Edit Data", "Enter Data Point:", text=data_point)
          if ok:
            # Update the data point in the data
            index = self.data_list.row(item)
            variable_data["var"][index] = new_data_point
            # Update the data point in the list
            item.setText(new_data_point)
            self.parent_reference.update_window_title()
  def delete_selected_data_points(self):
    current_item = self.variable_list.currentItem()
    if current_item:
      variable_name = current_item.text()
      variable_data = self.data["independent_vars"].get(variable_name, {})
      if variable_data.get("type") == "multiple":
        selected_items = self.data_list.selectedItems()
        for item in selected_items:
          data_point = item.text()
          # Remove the data point from the data
          accurate_index=self.data_list.row(item)
          variable_data["var"].pop(accurate_index)
          # Remove the data point from the list
          row = self.data_list.row(item)
          self.data_list.takeItem(row)
          self.parent_reference.update_window_title()
