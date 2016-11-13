#!/usr/bin/python

import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def show_dialog(title="This is an INFO MessageDialog", text="And this is the secondary text that explains things."):
    win = Gtk.Window() # maybe remove
    dialog = Gtk.MessageDialog(win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, title)
    dialog.format_secondary_text(text)
    dialog.run()
    print("INFO dialog closed")
    dialog.destroy()
    win.destroy() # maybe remove
    while Gtk.events_pending():
        Gtk.main_iteration_do(True)

class Battery:
    _path = "/sys/class/power_supply/BAT0"
    _is_present = 0
    _is_charging = 0

    def __init__(self):
        with open(self._path + "/present", "r") as f:
            self._is_present = int(f.read())

        if not self._is_present:
            self.not_found()

    def not_found(self):
        print("Battery not found")

    def status(self):
        if not self._is_present:
            self.not_found()
        status = "Unknown"
        with open(self._path + "/status", "r") as f:
            status = f.read()
        self._is_charging = status.strip() == "Charging"
        return status

    def is_charging(self):
        self.status()
        return self._is_charging

    def percentage(self):
        if not self._is_present:
            self.not_found()
        full = 0
        now = 0
        with open(self._path + "/energy_full", "r") as f:
            full = f.read()
        with open(self._path + "/energy_now", "r") as f:
            now = f.read()

        return  int(float(now) / int(full) * 100)

battery = Battery()

while True:
    print(battery.status(), battery.percentage())
    if not battery.is_charging() and battery.percentage() == 15:
        show_dialog("Low power", "Maybe, you should to connect power.")
    elif not battery.is_charging() and battery.percentage() == 5:
        show_dialog("Extremelly low power", "You have to connect power.")
    elif battery.is_charging() and battery.percentage() == 95:
        show_dialog("Battery fully charged", "You may disconnect power.")
    time.sleep(30)