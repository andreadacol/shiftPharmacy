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

        self.list_widget.itemClicked.connect(self.load_employee_for_edit)
        self.editing_index = None

        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText("Ore settimanali (default 40)")
        layout.addWidget(self.hours_input)

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
        hours_text = self.hours_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Errore", "Nome vuoto.")
            return

        if any(emp['name'] == name for emp in self.employees):
            QMessageBox.warning(self, "Errore", "Dipendente già esistente.")
            return

        try:
            hours = int(hours_text) if hours_text else 40
            if hours <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Errore", "Ore settimanali non valide.")
            return

        employee = {"name": name, "hours": hours}
        self.employees.append(employee)
        self.list_widget.addItem(f"{name} ({hours}h)")
        self.name_input.clear()
        self.hours_input.clear()

    def load_employee_for_edit(self, item):
        row = self.list_widget.row(item)
        emp = self.employees[row]
        self.name_input.setText(emp["name"])
        self.hours_input.setText(str(emp["hours"]))
        self.editing_index = row

    def remove_employee(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            name = self.list_widget.item(row).text()
            self.employees.remove(name)
            self.list_widget.takeItem(row)

    def get_employees(self):
        return self.employees

