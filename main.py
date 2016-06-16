#!/usr/bin/env python3
from apscheduler.schedulers.background import BlockingScheduler
import sys
import subprocess
from threading import Thread
from time import strftime
from bar import barhandler
from datetime import datetime
from bspc import BspcControl

OUTPUT = ""
wms_running=False

bar = barhandler()

def get_time():
    current_time = strftime("%a %d %b %H:%M")
    bar.time = current_time

if __name__ == "__main__":
    #Configure scheduler
    scheduler = BlockingScheduler()
    scheduler.configure(timezone='Europe/Stockholm')

    #Schedule jobs
    #scheduler.add_job(getmemory, 'interval', seconds=2, next_run_time=datetime.now())
    scheduler.add_job(get_time, 'interval', seconds=1, next_run_time=datetime.now())
    #scheduler.add_job(get_workspaces, 'interval', seconds=1, next_run_time=datetime.now())
    #scheduler.add_job(getbattery, 'interval', seconds=10, next_run_time=datetime.now())
    #scheduler.add_job(getip, 'interval', seconds=10, next_run_time=datetime.now())
    #scheduler.add_job(getwindowtitle, 'interval', seconds=.1, next_run_time=datetime.now())

    #Start continious jobs
    bspccontrol = BspcControl(bar)
    Thread(target=bspccontrol.inputhandler).start()

    #Start scheduler
    scheduler.start()
