import subprocess
from bar import barhandler
import re
from util import *

class BspcControl:
    def __init__(self, bar):
        self.bar = bar
        self.bspc = subprocess.Popen(('bspc', 'subscribe', 'report'), stdout=subprocess.PIPE)
        self.monitors = []

    def inputhandler(self, colors):
        with subprocess.Popen(["bspc", "subscribe", "report"], stdout=subprocess.PIPE) as ws:
            for line in ws.stdout:
                out = ""
                line = line.decode('utf-8')
                line2 = handle(line)
                for part in line.split(":"):
                    p = part[:1]
                    if p == "O":
                        #out += underline(colorize(replace_name(part[1:]), "#11bb44"), "#11bb44")
                        out += underline(colorize(pad(part[1:], 1), colors['HIGHLIGHT_FG']), colors['HIGHLIGHT_FG'])
                    if p == "o":
                        out += clickable(colorize(pad(part[1:], 1), colors['HIGHLIGHT_FG']), "bspc desktop -f "+part[1:])
                    if p == "f":
                        #out += clickable(colorize(pad(part[1:], 1), "bspc desktop -f "+part[1:]))
                        out += clickable(colorize(pad(part[1:], 1), colors['DEFAULT_FG']), "bspc desktop -f "+part[1:])
                    if p == "F":
                        #out += underline(colorize(replace_name(part[1:]), "#11bb44"), "#11bb44")
                        out += underline(colorize(pad(part[1:], 1), colors['HIGHLIGHT_FG']), colors['HIGHLIGHT_FG'])
                self.bar.workspaces = out

def replace_name(string):
    if string[-1:] == "2":
        return "|"
    if string == "DP-0_1":
        return "\uf269"
    return string

def handle(f):
    stat_line = f.split(":")
    #cmd = subprocess.Popen(["bspc", "query", "-H"], stdout=subprocess.PIPE)
    #cmd2 = subprocess.Popen(["tail", "-n", "1"], stdin=cmd.stdout, stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(["bspc", "wm", "-g"], stdout=subprocess.PIPE)
    cmd3 = subprocess.Popen(["awk", "{print $1}"], stdin=cmd2.stdout, stdout=subprocess.PIPE)
    curr_screen = cmd3.communicate()[0].decode("utf-8")[:-1]
    for i, item in enumerate(stat_line):
        if curr_screen not in item:
            stat_line[i] = item.replace("F", "f")
            stat_line[i] = item.replace("O", "o")
    return ":".join(stat_line)[:-1]
