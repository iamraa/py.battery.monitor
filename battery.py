#!/usr/bin/python

import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def show_dialog(title="This is an INFO MessageDialog",
                text="And this is the secondary text that explains things.",
                type=Gtk.MessageType.INFO):
    win = Gtk.Window() # maybe remove
    dialog = Gtk.MessageDialog(win, 0, type,
                               Gtk.ButtonsType.OK, title)
    dialog.format_secondary_text(text)
    dialog.run()  # Pause application
    print("Dialog closed")
    dialog.destroy()
    win.destroy() # maybe remove
    while Gtk.events_pending():
        Gtk.main_iteration_do(True)


class Battery:
    _path = "/sys/class/power_supply/BAT0"
    _is_present = 0
    _is_charging = 0
    _percentage = 0
    _stat_charge = []
    _stat_discharge = []
    _stat = {
        'charging': 0,
        'discharging': 0
    }

    def __init__(self):
        with open(self._path + "/present", "r") as f:
            self._is_present = int(f.read())

        if not self._is_present:
            self.not_found()

    def not_found(self):
        print("Battery not found")
        exit()

    def status(self):
        if not self._is_present:
            self.not_found()
        status = "Unknown"
        with open(self._path + "/status", "r") as f:
            status = f.read().strip()
        self._is_charging = status == "Charging"

        # log statistic
        self._log_stat()

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

        self._percentage = int(float(now) / int(full) * 100)

        return self._percentage

    def _log_stat(self):
        """
        Log charge & discharge statistics
        """
        if self._is_charging:
            if self._stat_discharge:
                self._stat_discharge = []
            self._stat_charge.append((time.time(), self._percentage))
            self._stat['charging'] = (
                self._stat_charge[-1][0] - self._stat_charge[0][0]) // 60
        else:
            if self._stat_charge:
                self._stat_charge = []
            self._stat_discharge.append((time.time(), self._percentage))
            self._stat['discharging'] = (
                self._stat_discharge[-1][0] - self._stat_discharge[0][0]) // 60

    def stat(self, what="charging"):
        """
        Return statistics
        """
        if what in self._stat:
            return self._stat[what]
        else:
            return 0


if __name__ == "__main__":
    battery = Battery()
    while True:
        print(battery.status(), battery.percentage(),
              'charging', battery.stat('charging'),
              'discharging', battery.stat('discharging'))
        if not battery.is_charging() and battery.percentage() == 15:
            show_dialog("Low power",
                        "Maybe, you should to connect power supply.")
        elif not battery.is_charging() and battery.percentage() <= 5:
            show_dialog(
                "Extremelly low power",
                "You have to connect power supply.\n" \
                "Battery discharged in {0:.0f} min.".format(
                    battery.stat('discharging')),
                Gtk.MessageType.MESSAGE_WARNING)
        elif battery.is_charging() and battery.percentage() >= 95:
            show_dialog(
                "Battery fully charged",
                "You may disconnect power supply.\n" \
                "Battery charged in {0:.0f} min.".format(
                    battery.stat('charging')))
        time.sleep(30)
