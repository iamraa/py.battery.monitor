#!/usr/bin/python
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))

home = os.environ["HOME"]
name = "py.battery.warning"
comment = "Control battery status"
command = path + "/battery.py"

# print(name, command)

if len(sys.argv) < 2:
    print("To add script to autostart you have to call script with option.\nExecute: ./setup.py [install / uninstall]")
    exit()

# path to autostart
dr = home+"/.config/autostart/"
if not os.path.exists(dr):
    os.makedirs(dr)
file = dr+name.lower()+".desktop"

operation = sys.argv[1];
if operation == "install":

    launcher = ["[Desktop Entry]", "Name=", "Comment=", "Exec=", "Type=Application", "Terminal=false", "StartupNotify=false"]
    if not os.path.exists(file):
        with open(file, "wt") as out:
            for l in launcher:
                l = l+name if l == "Name=" else l
                l = l+comment if l == "Comment=" else l
                l = l+command if l == "Exec=" else l
                out.write(l+"\n")
        print("script added to autostart")
    else:
        print("script exists in autostart")

elif operation == "uninstall":

    if os.path.exists(file):
        os.unlink(file)
        print("script removed from autostart")
    else:
        print("script does not exist in autostart")