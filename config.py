# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


#  _     ___  _   _ __________ ____     
# | |   / _ \| | | |__  / ____|  _ \ 
# | |  | | | | | | | / /|  _| | |_) |   
# | |__| |_| | |_| |/ /_| |___|  _ < 
# |_____\___/ \___//____|_____|_| \_\
                                   




import os, re, socket, subprocess
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile import layout, bar, widget, hook
from typing import List

##### user-preferences ####
home = os.path.expanduser('~')
mod = "mod4"
myTerm = "alacritty"
home_directory = ""
myConfig = ([home + "/.config/qtile"])

##### colors #####
colors = [
    ["#404040", "#404040"],
    ["#999999", "#999999"],
    ["#ffffff", "#ffffff"]
]

##### keybindings #####
keys = [
    ##### usage
    Key([mod], "return", lazy.spawn(myTerm)),
    Key([mod, "shift"], "return", lazy.spawn("rofi -show run")),
    Key([mod], "c", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod], "tab", lazy.next_layout()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    ##### window management
    Key([mod, "control"], "k", lazy.layout.section_up()),
    Key([mod, "control"], "j", lazy.layout.section_down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_down()),
    Key([mod, "control"], "f", lazy.window.toggle_floating()),
]

##### workspaces and groups ######
group_names = [
    ("Web" , {'layout' : 'monadtall'}),
    ("Dev" , {'layout' : 'monadtall'}),
    ("Sys" , {'layout' : 'monadtall'}),
    ("Term", {'layout' : 'monadtall'}),
    ("Rng" , {'layout' : 'monadtall'}),
]
for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscren()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))

##### theme #####
layout_theme = {"border_width" : 2,
                "margin" : 3,
                "boder_focus" : "#cccccc",
                "border_normal" : "#4d4d4d"}

##### prompt ######
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### layouts #####
layouts = [
    layout.max(),
    layout.Stack(num_stacks = 2),
    layout.MonadTall(**layout_theme),
    layout.TreeTab(
        font = "Ubuntu-C",
        fontsize = "14",
        sections = ["FIRST", "SECOND"],
        section_fontsize = 11,
        bg_color = "#404040",
        active_bg = "#333333",
        active_fg = "#999999",
        inactive_bg = "#333333",
        inactive_fg = "#404040",
        padding_y = 6,
        sction_top = 10,
        panel_width = 200),
    layout.Floating(**layout_theme)
]

##### floating windows ######
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'}, 
    {'wname': 'branchdialog'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},
])
auto_fullscreen = True
focus_on_window_activation = "smart"

##### widgets #####
widget_defaults = dict(
    font = "Ubuntu-C",
    fontsize = 12,
    padding = 2,
    backgroud = "#cccccc"
)
exrension_defaults = widget_defaults.copy()

screens = [Screen(bottom=bar.Bar(
        [
            widget.GroupBox(),
            widget.Prompt(),
            widget.WindowName(),
            widget.TextBox("default config", name="default"),
            widget.Systray(),
            widget.Clock(format='%Y-%m-%d %a %I:%M %p'),],24,),),
        ]


##### auto-start #####
#def start_once():
#    subprocess.call()