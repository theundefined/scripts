#!/usr/bin/python
import subprocess
import re
import time
def get_active_window_title():
    root_check = ''
    root = subprocess.Popen(['xprop', '-root'],  stdout=subprocess.PIPE)

    if root.stdout != root_check:
        root_check = root.stdout

        for i in root.stdout:
            if '_NET_ACTIVE_WINDOW(WINDOW):' in i:
                id_ = i.split()[4]
                id_w = subprocess.Popen(['xprop', '-id', id_], stdout=subprocess.PIPE)
        id_w.wait()
        buff = []
        for j in id_w.stdout:
            buff.append(j)

        for line in buff:
            match = re.match("WM_NAME\((?P<type>.+)\) = (?P<name>.+)", line)
            if match != None:
                type = match.group("type")
                if type == "STRING" or type == "COMPOUND_TEXT":
                    return match.group("name")
        return "Active window not found"

oldtime=time.time()
oldtitle=''
while (1):
    curtitle=get_active_window_title()
    curtime=time.time()
    if curtitle != oldtitle:
        print oldtitle, curtime - oldtime
        oldtime=curtime
        oldtitle=curtitle
    time.sleep(1)
