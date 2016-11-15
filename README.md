# pyBattery #

Battery warning notification for Ubuntu / Linux Mint.

Show message dialog with GTK 3 when battery is extremely low or fully charged. Work with python 2.7+ (May be work on Python 3+, have not test it).

No dependencies.

## Alert levels ##

* 5% - extremely low dialog
* 15% - low notification
* 95% - charged dialog

## Autostart ##

To add/remove script to autostart use:

* `./setup.py install`
* `./setup.py uninstall`

# Alternative #

* [Based on acpi & Java](http://linuxsoftware.moncerbae.com/2015/07/how-to-create-battery-warning-in-ubuntu.html)