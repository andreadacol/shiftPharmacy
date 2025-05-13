from typing import List, Tuple, Dict

class Employee:
    def __init__(self, name: str):
        self.name = name
        self.restrictions = {}  # { "2025-05-13": ["afternoon"] }

class PharmacyDay:
    def __init__(self, name: str, am: Tuple[str, str], pm: Tuple[str, str], am_open=True, pm_open=True):
        self.name = name
        self.am = am
        self.pm = pm
        self.am_open = am_open
        self.pm_open = pm_open

