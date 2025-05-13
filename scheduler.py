from datetime import datetime, timedelta
import calendar
import random

def generate_schedule(year, month, employees, pharmacy_hours):
    """
    Genera un piano turni base per il mese indicato.
    - year: es. 2025
    - month: es. 5 (Maggio)
    - employees: lista dei nomi dei dipendenti
    - pharmacy_hours: dizionario { 'YYYY-MM-DD': [('08:00', '12:00'), ('15:30', '19:30')] }
    """

    schedule = {}
    employee_hours = {e: 0 for e in employees}
    weekend_counts = {e: 0 for e in employees}

    days_in_month = calendar.monthrange(year, month)[1]
    base_date = datetime(year, month, 1)

    for day in range(1, days_in_month + 1):
        current_date = base_date.replace(day=day)
        day_str = current_date.strftime('%Y-%m-%d')
        weekday = current_date.weekday()

        if day_str not in pharmacy_hours:
            continue  # farmacia chiusa

        schedule[day_str] = []
        intervals = pharmacy_hours[day_str]

        for interval in intervals:
            start, end = interval
            hour_start = int(start.split(":")[0])
            hour_end = int(end.split(":")[0])
            hours = hour_end - hour_start

            # In certi orari, basta 1 persona
            if any(hour_start <= h < hour_end for h in [8, 12, 19]):
                required = 1
            else:
                required = 2

            # Prendiamo i dipendenti con meno ore
            sorted_emps = sorted(employees, key=lambda e: employee_hours[e])
            assigned = []

            for e in sorted_emps:
                if employee_hours[e] + hours <= 40:
                    assigned.append(e)
                    employee_hours[e] += hours
                    if weekday >= 5:
                        weekend_counts[e] += 1
                    if len(assigned) >= required:
                        break

            schedule[day_str].append({
                "interval": interval,
                "employees": assigned
            })

    return schedule

