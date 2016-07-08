#!/usr/bin/env python3
from apscheduler.schedulers.background import BlockingScheduler
import sys
import subprocess
from threading import Thread
from time import strftime
from bar import barhandler
from datetime import datetime
from bspc import BspcControl
from util import *
from theme import Theme
import psutil
import configparser
import json
import os
import sys

OUTPUT = ""
wms_running=False
charg_step = 0
warning = 0

# TO ADD
# scrolling song
# theme support

def get_volume(colors):
    # get whether source is muted
    p1 = subprocess.Popen(("pulseaudio-ctl"), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(("grep", "muted"), stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.check_output(("awk", 'FNR==1 {print $5}'), stdin=p2.stdout)
    muted = "yes" in p3.decode()
    # get volume
    b1 = subprocess.Popen(("pulseaudio-ctl"), stdout=subprocess.PIPE)
    b2 = subprocess.Popen(("grep", "Volume"), stdin=b1.stdout, stdout=subprocess.PIPE)
    b4 = subprocess.Popen(("awk", '{print $4}'), stdin=b2.stdout, stdout=subprocess.PIPE)
    volume = int(subprocess.check_output(("sed", "-r", "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"), stdin=b4.stdout).decode().strip())
    if muted:
        icon = "\uf581"
        color = colors['ERROR_FG']
    else:
        color = colors['DEFAULT_FG']
        if volume > 80:
            icon = "\uf57e"
        elif volume < 20:
            icon = "\uf57f"
        else:
            icon = "\uf580"
    bar.volume = colorize("{} {}%".format(icon, volume), color)

def get_wifi(colors):
    try:
        ESSID = subprocess.check_output(("iwgetid", "-r")).decode().strip()
        icon = "\uf5a9"
    except subprocess.CalledProcessError as e:
        icon = "\uf5aa"
        ESSID = "No connection"
    bar.network = colorize("{} {}".format(icon, ESSID), colors['DEFAULT_FG'])

def get_mpd(colors):
    try:
        mpc_stat = subprocess.check_output(('mpc','status')).decode('utf-8')
    except:
        pass
    else:
        playing = "playing" in mpc_stat
        song = mpc_stat.split("\n")[0]
        if playing:
            play_button = clickable(" \uf3e6 ", "mpc toggle &> /dev/null")
        else:
            play_button = clickable(" \uf40d ", "mpc toggle &> /dev/null")
        prev_button = clickable(" \uf664 ", "mpc prev &> /dev/null")
        next_button = clickable(" \uf662 ", "mpc next &> /dev/null")
        bar.music = colorize("{}{}{} {}".format(prev_button, play_button, next_button, song), colors['DEFAULT_FG'])

def get_cpu(colors):
    percent = psutil.cpu_percent(interval=4, percpu=False)
    bar.cpu = colorize("{} {}%".format("\uf29A", percent), colors['DEFAULT_FG'])

def get_time(colors):
    current_time = strftime("%a %d %b %H:%M")
    bar.time = colorize(current_time, colors['DEFAULT_FG'])

def get_battery(colors):
    with open("/sys/class/power_supply/ACAD/online", "r") as f:
        adapter_online = int(f.readline().strip())
    with open("/sys/class/power_supply/BAT1/capacity", "r") as f:
        percent = f.readline().strip()
    out = ""
    levels = ["\uf08e","\uf07a", "\uf07b", "\uf07c", "\uf07d", "\uf07e", "\uf07f", "\uf080", "\uf081", "\uf082", "\uf079"]
    icon = levels[(int(percent)//10)]
    if adapter_online:
        global charg_step
        icon = levels[charg_step]
        if charg_step < 10:
            charg_step+=1
        else:
            charg_step = int(percent)//10
    if int(percent) < 10:
        global warning
        color = colors['ERROR_FG']
        if warning == 10:
            subprocess.run(('notify-send','-t','2','-u','critical','Battery Low!\nBattery at {}%'.format(percent)))
            warning = 0
        warning += 1
    else:
        color = colors['DEFAULT_FG']
    out += "{} {}%".format(icon, percent)
    bar.battery = colorize(out, color)

def parse_settings():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config['SETTINGS']

def get_theme_colors(theme_name):
    with open(theme_name, "r") as f:
        t = json.load(f)
        return t['colors']

if __name__ == "__main__":
    settings = parse_settings()
    theme = Theme(settings['theme'])
    colors = theme.colors

    # create the bar
    bar = barhandler(theme)

    #Configure scheduler
    scheduler = BlockingScheduler()
    scheduler.configure(timezone='Europe/Stockholm')

    #Schedule jobs
    scheduler.add_job(get_time, 'interval', seconds=30, next_run_time=datetime.now(), args=[colors])
    scheduler.add_job(get_battery, 'interval', seconds=1, next_run_time=datetime.now(), args=[colors])
    scheduler.add_job(get_cpu, 'interval', seconds=5, next_run_time=datetime.now(), args=[colors])
    scheduler.add_job(get_mpd, 'interval', seconds=1, next_run_time=datetime.now(), args=[colors])
    scheduler.add_job(get_volume, 'interval', seconds=1, next_run_time=datetime.now(), args=[colors])
    scheduler.add_job(get_wifi, 'interval', seconds=1, next_run_time=datetime.now(), args=[colors])

    #Start continious jobs
    bspccontrol = BspcControl(bar)
    Thread(target=bspccontrol.inputhandler, args=(colors,)).start()

    #Start scheduler
    scheduler.start()
