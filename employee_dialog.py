from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QMessageBox
)

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employees=None):
        super().__init__(parent)
        self.setWindowTitle("Gestione Dipendenti")
        self.employees = employees if employees else []

        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.employees)
        layout.addWidget(self.list_widget)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome dipendente")
        layout.addWidget(self.name_input)

        add_btn = QPushButton("Aggiungi")
        add_btn.clicked.connect(self.add_employee)
        remove_btn = QPushButton("Rimuovi selezionato")
        remove_btn.clicked.connect(self.remove_employee)

        hlayout = QHBoxLayout()
        hlayout.addWidget(add_btn)
        hlayout.addWidget(remove_btn)
        layout.addLayout(hlayout)

        save_btn = QPushButton("Salva")
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def add_employee(self):
        name = self.name_input.text().strip()
        if name and name not in self.employees:
            self.employees.append(name)
            self.list_widget.addItem(name)
            self.name_input.clear()
        else:
            QMessageBox.warning(self, "Errore", "Nome vuoto o già esistente")

    def remove_employee(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            name = self.list_widget.item(row).text()
            self.employees.remove(name)
            self.list_widget.takeItem(row)

    def get_employees(self):
        return self.employees

