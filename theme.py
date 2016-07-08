#!/usr/bin/env
import json

class Theme:

    def __init__(self, theme_path):
        self._name = ''
        self._creator = ''
        self._version = ''
        self._bar_options = ''
        self._colors = ''
        self.__parse_theme(theme_path)

    def __parse_theme(self, path):
        with open(path, "r") as f:
            theme = json.load(f)
        for option in theme:
            if option.lower() == "options":
                self.name =     theme[option]['name'] if "name" in theme[option] else ""
                self.creator =  theme[option]['creator'] if "creator" in theme[option] else ""
                self.version =  theme[option]['version'] if "version" in theme[option] else ""
            if option.lower() == "bar":
                self.bar_options = theme[option]
            if option.lower() == "colors":
                self.colors = theme[option]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors):
        self._colors = colors

    @property
    def creator(self):
        return self._creator

    @creator.setter
    def creator(self, creator):
        self._creator = creator

    @property
    def bar_options(self):
        return self._bar_options

    @bar_options.setter
    def bar_options(self, bar_options):
        self._bar_options = bar_options

