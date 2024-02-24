import sys, os
import pickle
import copy
from math import pi
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QTabWidget, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QDialog, QHBoxLayout, QFileDialog
from uncertaintytrack import TrackUncertainty  # Make sure to import your TrackUncertainty module

if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)
class AboutDialog(QDialog):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("About")
    self.setGeometry(100, 100, 400, 200)

    layout = QVBoxLayout()

    text_label = QLabel("This is a program designed for basic physics experiment data analysis, written by happyZYM.\nVisit the repository:")
    layout.addWidget(text_label)

    link_label = QLabel('<a href="https://dev.zymsite.ink/Academic/PEHelper">https://dev.zymsite.ink/Academic/PEHelper</a>')
    link_label.setOpenExternalLinks(True)
    layout.addWidget(link_label)

    self.setLayout(layout)

from intertab import *
from rawtab import *
class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("PEHelper - Physics Experiment Helper")
    self.setWindowIcon(QIcon(os.path.join(basedir,"static/icon.ico")))
    self.setGeometry(100, 100, 800, 600)

    menubar = self.menuBar()
    
    file_menu = menubar.addMenu("File")
    open_action = file_menu.addAction("Open", self.open_file)
    save_action = file_menu.addAction("Save", self.save_file)
    save_as_action = file_menu.addAction("Save As", self.save_as_file)

    about_action = menubar.addAction("About", self.show_about_dialog)

    self.data = {
      "independent_vars": {},
      "intermediate_vars": [],
      "dependent_var": {
        "name": "",
        "expr": ""
      },
      "confidence": 0.95,
      "accuracy": 20
    }
    self.data_backup=copy.deepcopy(self.data)
    # self.data = data_demo
    self.current_file_name=""

    self.tab_widget = QTabWidget(self)
    self.raw_variables_tab = QWidget()
    self.intermediate_variables_tab = QWidget()
    self.analysis_tab = QWidget()

    self.setup_raw_variables_tab()
    self.setup_intermediate_variables_tab()
    self.setup_analysis_tab()

    self.tab_widget.addTab(self.raw_variables_tab, "Raw Variables")
    self.tab_widget.addTab(self.intermediate_variables_tab, "Intermediate Variables")
    self.tab_widget.addTab(self.analysis_tab, "Analysis")

    layout = QVBoxLayout()
    layout.addWidget(self.tab_widget)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    self.setCentralWidget(central_widget)

  def setup_raw_variables_tab(self):
    self.raw_variables_tab = RawVariablesTab(self, self.data)
  def setup_intermediate_variables_tab(self):
    self.intermediate_variables_tab = IntermediateVariablesTab(self, self.data)

  def setup_analysis_tab(self):
    layout = QVBoxLayout()

    label_name = QLabel("Dependent Variable's Name:")
    self.input_name = QLineEdit()
    layout.addWidget(label_name)
    layout.addWidget(self.input_name)

    label_expr = QLabel("Expression:")
    self.input_expr = QLineEdit()
    layout.addWidget(label_expr)
    layout.addWidget(self.input_expr)

    label_confidence = QLabel("Confidence Level:")
    self.input_confidence = QLineEdit("0.95")  # Set default value
    layout.addWidget(label_confidence)
    layout.addWidget(self.input_confidence)

    label_accuracy = QLabel("Accuracy:")
    self.input_accuracy = QLineEdit("20")  # Set default value
    layout.addWidget(label_accuracy)
    layout.addWidget(self.input_accuracy)

    self.analysis_result_area = QTextEdit()
    self.analysis_result_area.setReadOnly(True)
    layout.addWidget(self.analysis_result_area)

    start_analysis_button = QPushButton("Start Analysis")
    start_analysis_button.clicked.connect(self.start_analysis)
    layout.addWidget(start_analysis_button)

    self.analysis_tab.setLayout(layout)

  def FetchInfoFromUI(self):
    # Retrieve user inputs in tab 3
    name = self.input_name.text()
    expr = self.input_expr.text()
    confidence = float(self.input_confidence.text())
    accuracy = int(self.input_accuracy.text())
    self.data["dependent_var"] = {"name": name, "expr": expr}
    self.data["confidence"] = confidence
    self.data["accuracy"] = accuracy
    # Retrieve user inputs in tab 2
    self.intermediate_variables_tab.update_data_from_list()
    # data in tab 1 is updated automatically
  
  def update_ui_with_data(self, new_data):
    # Update UI with the new data
    self.data = new_data
    self.input_name.setText(self.data["dependent_var"].get("name", ""))
    self.input_expr.setText(self.data["dependent_var"].get("expr", ""))
    self.input_confidence.setText(str(self.data.get("confidence", 0.95)))
    self.input_accuracy.setText(str(self.data.get("accuracy", 20)))

    # Update intermediate variables tab
    self.intermediate_variables_tab.setup_list(self.data)
    # clear the analysis result area
    self.analysis_result_area.clear()
    # Update raw variables tab
    self.raw_variables_tab.flush_list(self.data)

  def start_analysis(self):
    self.FetchInfoFromUI()
    name=self.data['dependent_var']['name']
    try:
      # Perform analysis using TrackUncertainty
      result = TrackUncertainty(self.data)

      # Display the result in the text area
      self.analysis_result_area.setPlainText(f"Analysis Result for {name}:\n\n"
                          f"Value: {result[name]['value']}\n"
                          f"Uncertainty: {result[name]['uncertainty']}\n")

      # Display origin independent variables' information
      self.analysis_result_area.append("\nOrigin Independent Variables:")
      for var_name, var_data in result.items():
        if var_name != name and var_name in self.data["independent_vars"]:
          self.analysis_result_area.append(f"{var_name}: "
                          f"Value: {var_data['value']}, "
                          f"Uncertainty: {var_data['uncertainty']}, "
                          f"Derivative: {var_data['derivative']}")
    except Exception as e:
      self.analysis_result_area.setPlainText(f"An error occurred during analysis:\n\n{e}")

  def open_file(self):
    self.FetchInfoFromUI()
    if self.data != self.data_backup:
      # Prompt the user to save current work before opening a new file
      reply = QMessageBox.question(self, 'Save Work', 'Do you want to save your current work before opening a new file?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
      if reply == QMessageBox.StandardButton.Yes:
        self.save_file()
      elif reply == QMessageBox.StandardButton.Cancel:
        return

    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "Pickle Files (*.pe)")
    if file_path:
      self.current_file_name = file_path
      with open(file_path, 'rb') as file:
        new_data = pickle.load(file)

      # Update the UI with the new data
      self.update_ui_with_data(new_data)
      self.data_backup=copy.deepcopy(self.data)

  def save_file(self):
    file_dialog = QFileDialog()
    if self.current_file_name == "":
      file_path, _ = file_dialog.getSaveFileName(self, "Save File", "", "Pickle Files (*.pe)")
    else:
      file_path=self.current_file_name
    if file_path:
      self.current_file_name=file_path
      with open(file_path, 'wb') as file:
        pickle.dump(self.data, file)
        self.data_backup=copy.deepcopy(self.data)

  def save_as_file(self):
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getSaveFileName(self, "Save As", "", "Pickle Files (*.pe)")
    if file_path:
      self.current_file_name=file_path
      with open(file_path, 'wb') as file:
        pickle.dump(self.data, file)
        self.data_backup=copy.deepcopy(self.data)

  def show_about_dialog(self):
    about_dialog = AboutDialog()
    about_dialog.exec()

def main():
  app = QApplication(sys.argv)
  try:
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
  except Exception as e:
    print(e)
    sys.exit(1)

if __name__ == "__main__":
  main()