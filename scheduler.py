from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random

# Definizione dei turni
CONTINUOUS_SHIFTS = [
    [("08:00", "12:00")],
    [("08:00", "13:00")],
    [("08:00", "14:00")],
    [("15:00", "20:00")],
    [("14:00", "20:00")],
]

SPLIT_SHIFTS = [
    [("08:00", "12:00"), ("16:00", "20:00")],
    [("08:00", "12:00"), ("15:00", "19:00")],
]

ALL_SHIFT_OPTIONS = CONTINUOUS_SHIFTS + SPLIT_SHIFTS

# Orari di apertura della farmacia
pharmacy_hours = {
    'Lunedì':    {'am': ('08:00', '12:30'), 'pm': ('12:30', '20:00'), 'am_open': True, 'pm_open': True},
    'Martedì':   {'am': ('08:00', '12:30'), 'pm': ('12:30', '20:00'), 'am_open': True, 'pm_open': True},
    'Mercoledì': {'am': ('08:00', '12:30'), 'pm': ('12:30', '20:00'), 'am_open': True, 'pm_open': True},
    'Giovedì':   {'am': ('08:00', '12:30'), 'pm': ('12:30', '20:00'), 'am_open': True, 'pm_open': True},
    'Venerdì':   {'am': ('08:00', '12:30'), 'pm': ('12:30', '20:00'), 'am_open': True, 'pm_open': True},
    'Sabato':    {'am': ('08:00', '12:30'), 'pm': ('12:30', '20:00'), 'am_open': True, 'pm_open': True},
    'Domenica':  {'am': ('08:00', '12:30'), 'pm': ('12:30', '20:00'), 'am_open': True, 'pm_open': False}
}

employees = ['Alice', 'Bob', 'Chiara', 'Davide']

def parse_time(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%H:%M")

def shift_fits_in_opening_hours(shift: List[Tuple[str, str]], opening: Dict) -> bool:
    for part in shift:
        start, end = parse_time(part[0]), parse_time(part[1])
        if start < parse_time(opening['am'][0]) or end > parse_time(opening['pm'][1]):
            print(f"  ⚠️ Turno {part} NON compatibile con {opening['am'][0]}-{opening['pm'][1]}")
            return False
    print(f"  ✅ Turno {shift} compatibile")
    return True

def generate_schedule(pharmacy_hours: Dict, employees: List[str], year: int, month: int) -> Dict:
    schedule = {}
    day = datetime(year, month, 1)

    weekday_map = {
        "monday": "lunedì",
        "tuesday": "martedì",
        "wednesday": "mercoledì",
        "thursday": "giovedì",
        "friday": "venerdì",
        "saturday": "sabato",
        "sunday": "domenica",
    }

    while day.month == month:
        weekday_str = day.strftime("%A")
        print(weekday_str)
#        weekday = weekday_map[weekday_str]
        weekday = weekday_str

        opening = pharmacy_hours[weekday]

        print(f"\n📅 Giorno: {day.strftime('%Y-%m-%d')} ({weekday})")
        print(f"  Orari farmacia: {opening}")

        valid_shifts = []
        for shift in ALL_SHIFT_OPTIONS:
            if shift_fits_in_opening_hours(shift, opening):
                valid_shifts.append(shift)

        if not valid_shifts:
            print("  ❌ Nessun turno valido per questo giorno")
            day += timedelta(days=1)
            continue

        schedule[day.strftime("%Y-%m-%d")] = {}

        for emp in employees:
            shift = random.choice(valid_shifts)
            schedule[day.strftime("%Y-%m-%d")][emp] = shift
            print(f"  👤 {emp} assegnato al turno: {shift}")

        day += timedelta(days=1)

    return schedule

# Eseguiamo un test
#schedule_debug = generate_schedule(pharmacy_hours, employees, 2025, 5)
#schedule_debug.get("2025-05-01", "Nessun turno")
