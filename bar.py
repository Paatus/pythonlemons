import subprocess

class barhandler:

    def __init__(self):
        bar_args = ['lemonbar', '-u','3','-g','1920x40+1920','-f','-*-terminus-*-*-*-*-12-*-*-*-*-*-*-*', '-f', 'FontAwesome:size=8', '-B#3e3e3e', '-F#ffffff']
        self.bar = subprocess.Popen(bar_args, stdin=subprocess.PIPE)
        self._time = ''
        self._workspaces = ''

    def refresh(self):
        output = '%{l}'+self._workspaces+'%{r}'+self._time+"\n"
        self.bar.stdin.write(output.encode('utf-8'))
        self.bar.stdin.flush()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = "%{F#ff00ff}" + time + "%{F-}"
        self.refresh()

    @property
    def workspaces(self):
        return self._workspaces
    
    @workspaces.setter
    def workspaces(self, workspaces):
        self._workspaces = workspaces
        self.refresh()
