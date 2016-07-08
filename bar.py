import subprocess
from util import *

class barhandler:

    def __init__(self, theme):
        self.__colors = theme.colors
        bar_args = self.parse_args(theme)
        self.bar = subprocess.Popen(bar_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        subprocess.Popen(('bash'), stdin=self.bar.stdout)
        if "height" in theme.bar_options:
            if is_num(theme.bar_options['height'], 'height'):
                __height = str(theme.bar_options['height'])
        else:
            __height = '20'
        subprocess.Popen(('bspc', 'config', 'top_padding', __height))
        bspwm_p = subprocess.check_output(('xdo', 'id', '-N', 'Bspwm', '-n', 'root')).decode().strip()
        got_connection = False
        while not got_connection:
            try:
                bar_p = subprocess.check_output(('xdo', 'id', '-a', 'bar')).decode().strip()
                got_connection = True
            except subprocess.CalledProcessError:
                got_connection = False
        subprocess.Popen(('xdo', 'above', '-t', bspwm_p, bar_p))
        self._time = ''
        self._workspaces = ''
        self._battery = ''
        self._cpu = ''
        self._music = ''
        self._volume = ''
        self._network = ''
        self._divider = colorize('\uF1DD', self.__colors['DIVIDER_FG'])

    def parse_args(self, theme):
        colors = theme.colors
        __height = ""
        __width = ""
        __x_pos = ""
        __y_pos = ""
        __bg = "-B"+colors['MAIN_BG']
        __fg = "-F"+colors['DEFAULT_FG']
        bar_args = ['lemonbar', __bg, __fg]
        #bar_args = ['lemonbar', '-d','-u','3','-g','x40','-o','-2','-f','Monofur:size=10', '-o', '0', '-f', 'Source Han Sans KR Regular:size=10', '-o', '0','-f', 'Material Design Icons:size=13', '-B'+colors['MAIN_BG'], '-F#ffffff', '-a', '20']
        #bar_args = ['lemonbar','-o','-2','-f','Monofur:size=10', '-o', '0', '-f', 'Source Han Sans KR Regular:size=10', '-o', '0','-f', 'Material Design Icons:size=13', '-B'+colors['MAIN_BG'], '-F#ffffff', '-a', '20']
        args = theme.bar_options
        geom_string = ""
        for option in args:
            # geometry
            if option.lower() == "width":
                __width     = args[option]
            if option.lower() == "height":
                __height    = "x{}".format(args[option]) if "height" in option.lower() else ""
            if option.lower() == "x_pos":
                if not args['center']:
                    __x_pos     = "+{}".format(args[option]) if "x_pos" in option.lower() else ""
            if option.lower() == "y_pos":
                __y_pos     = "+{}".format(args[option]) if "y_pos" in option.lower() else ""
            # center horizontally
            if option.lower() == "center":
                if __x_pos != "":
                    print("For centering to work correctly, do not supply a X position")
                elif not args['width']:
                    print("Centering does nothing when no width is supplied, please supply a width")
                else:
                    xrandr = subprocess.Popen(("xrandr"), stdout=subprocess.PIPE)
                    screen_width = subprocess.check_output(("grep current | awk '{print $8}'"), stdin=xrandr.stdout, shell=True).decode().strip()
                    __x_pos = "+{}".format((int(screen_width) - args['width']) // 2)
            # underline
            if option.lower() == "underline_height":
                height = is_num(args[option], option)
                if height:
                    bar_args.append('-u')
                    bar_args.append(str(args[option]))
            # position at bottom
            if option.lower() == "bottom":
                if args[option].lower() == "true":
                    bar_args.append("-b")
            # Dock mode
            if option.lower() == "dock":
                if args[option].lower() == "true":
                    bar_args.append("-d")
            # number of clickable areas
            if option.lower() == "click_areas":
                amount = is_num(args[option], option)
                if amount:
                    bar_args.append('-a')
                    bar_args.append(str(amount))
            # fonts
            if option.lower() == "fonts":
                for font in args[option]:
                    bar_args.append('-f')
                    bar_args.append(font)
        geom_string = "{}{}{}{}".format(__width,__height,__x_pos,__y_pos)
        #print("'{}'".format(geom_string))
        if geom_string != "":
            bar_args.append("-g")
            bar_args.append(geom_string)
        return bar_args

    def refresh(self):
        cpu = getattr(self, '_cpu', '')
        network = getattr(self, '_network', '')
        battery = getattr(self, '_battery', '')
        volume = getattr(self, '_volume', '')
        time = getattr(self, '_time', '')
        divider = getattr(self, '_divider', '|')
        output = '%{l}'+self._workspaces+self._divider+self._music+"%{r}"+cpu+divider+volume+divider+battery+divider+network+divider+time+" \n"
        self.bar.stdin.write(output.encode('utf-8'))
        self.bar.stdin.flush()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time
        self.refresh()

    @property
    def workspaces(self):
        return self._workspaces

    @workspaces.setter
    def workspaces(self, workspaces):
        self._workspaces = workspaces
        self.refresh()

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, battery):
        self._battery = battery
        self.refresh()

    @property
    def cpu(self):
        return self._cpu

    @cpu.setter
    def cpu(self, cpu):
        self._cpu = cpu
        self.refresh()

    @property
    def music(self):
        return self._music

    @music.setter
    def music(self, music):
        self._music = music
        self.refresh()

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume
        self.refresh()

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network
        self.refresh()
