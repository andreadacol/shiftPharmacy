from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QTimeEdit, QLabel,
    QPushButton, QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import QTime

class PharmacyHoursDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Orari Farmacia")
        self.days = ["Lunedì", "Martedì", "Mercoledì", "Giovedì",
                     "Venerdì", "Sabato", "Domenica"]

        self.time_fields = {}

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        for day in self.days:
            am_start = QTimeEdit(); am_end = QTimeEdit()
            pm_start = QTimeEdit(); pm_end = QTimeEdit()
            am_open = QCheckBox("Mattina Aperto")
            pm_open = QCheckBox("Pomeriggio Aperto")
            am_open.setChecked(True); pm_open.setChecked(True)

            am_start.setTime(QTime(8, 30)); am_end.setTime(QTime(12, 30))
            pm_start.setTime(QTime(15, 30)); pm_end.setTime(QTime(19, 0))

            self.time_fields[day] = {
                "am_start": am_start, "am_end": am_end,
                "pm_start": pm_start, "pm_end": pm_end,
                "am_open": am_open, "pm_open": pm_open
            }

            row_layout = QHBoxLayout()
            row_layout.addWidget(am_open)
            row_layout.addWidget(am_start)
            row_layout.addWidget(am_end)
            row_layout.addWidget(pm_open)
            row_layout.addWidget(pm_start)
            row_layout.addWidget(pm_end)

            form_layout.addRow(QLabel(day), row_layout)

        layout.addLayout(form_layout)
        save_button = QPushButton("Salva")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)
        self.setLayout(layout)

    def get_hours(self):
        result = {}
        for day, data in self.time_fields.items():
            result[day] = {
                "am": (data["am_start"].time().toString("HH:mm"),
                       data["am_end"].time().toString("HH:mm")),
                "pm": (data["pm_start"].time().toString("HH:mm"),
                       data["pm_end"].time().toString("HH:mm")),
                "am_open": data["am_open"].isChecked(),
                "pm_open": data["pm_open"].isChecked()
            }
        return result

