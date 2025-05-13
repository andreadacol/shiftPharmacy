from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLabel, QHBoxLayout, QTextEdit, QSpinBox
)
from PyQt5.QtCore import QDate
import sys
from datetime import datetime

from pharmacy_hours_dialog import PharmacyHoursDialog
from employee_dialog import EmployeeDialog
from scheduler import generate_schedule


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestore Turni Farmacia")
        self.setGeometry(100, 100, 900, 700)

        self.pharmacy_hours = {}
        self.employees = ["Alice", "Bob", "Chiara", "Davide"]

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # ===== Selettore mese/anno =====
        date_layout = QHBoxLayout()
        self.year_input = QSpinBox()
        self.year_input.setMinimum(2020)
        self.year_input.setMaximum(2100)
        self.year_input.setValue(datetime.now().year)

        self.month_input = QSpinBox()
        self.month_input.setMinimum(1)
        self.month_input.setMaximum(12)
        self.month_input.setValue(datetime.now().month)

        date_layout.addWidget(QLabel("Anno:"))
        date_layout.addWidget(self.year_input)
        date_layout.addWidget(QLabel("Mese:"))
        date_layout.addWidget(self.month_input)
        self.layout.addLayout(date_layout)

        # ===== Lista dipendenti =====
        self.employee_list = QListWidget()
        self.employee_list.addItems(self.employees)
        self.layout.addWidget(QLabel("Dipendenti"))
        self.layout.addWidget(self.employee_list)

        # ===== Pulsanti modifiche =====
        buttons_layout = QHBoxLayout()

        self.edit_employees_button = QPushButton("Modifica Dipendenti")
        self.edit_employees_button.clicked.connect(self.edit_employees)
        buttons_layout.addWidget(self.edit_employees_button)

        self.edit_hours_button = QPushButton("Orari Farmacia")
        self.edit_hours_button.clicked.connect(self.edit_hours)
        buttons_layout.addWidget(self.edit_hours_button)

        self.generate_button = QPushButton("Genera Turni")
        self.generate_button.clicked.connect(self.generate_schedule_ui)
        buttons_layout.addWidget(self.generate_button)

        self.layout.addLayout(buttons_layout)

        # ===== Risultato turni =====
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.layout.addWidget(QLabel("Turni Generati"))
        self.layout.addWidget(self.result_output)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def edit_employees(self):
        dialog = EmployeeDialog(self, self.employees)
        if dialog.exec_():
            self.employees = dialog.get_employees()
            self.employee_list.clear()
            self.employee_list.addItems(self.employees)

    def edit_hours(self):
        dialog = PharmacyHoursDialog(self)
        if dialog.exec_():
            self.pharmacy_hours = dialog.get_hours()

    def generate_schedule_ui(self):
        year = self.year_input.value()
        month = self.month_input.value()

        if not self.employees:
            self.result_output.setText("Errore: nessun dipendente inserito.")
            return

        if not self.pharmacy_hours:
            self.result_output.setText("Errore: orari farmacia non definiti.")
            return

        schedule = generate_schedule(year, month, self.employees, self.pharmacy_hours)

        if not schedule:
            self.result_output.setText("Nessun turno generato.")
            return

        # Mostra i turni in output
        output = ""
        for day, shifts in sorted(schedule.items()):
            output += f"\n📅 {day}:\n"
            for shift in shifts:
                interval = f"{shift['interval'][0]} - {shift['interval'][1]}"
                names = ", ".join(shift['employees'])
                output += f"  🕒 {interval}: {names}\n"

        self.result_output.setText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

