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
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from typing import List

##### user-preferences ####
home = os.path.expanduser('~')
mod = "mod4"
myTerm = "alacritty"
myConfig = ([home + "/.config/qtile"])

##### keybindings #####
keys = [
    ##### usage
    Key([mod], "Return", lazy.spawn(myTerm)),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show run")),
    Key([mod], "c", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod, "control"], "l", lazy.layout.next()),
    ##### window management
    Key([mod, "control"], "k", lazy.layout.section_up()),
    Key([mod, "control"], "j", lazy.layout.section_down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_down()),
    Key([mod, "control"], "f", lazy.window.toggle_floating()),
]
##### mouse-usage #####
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

##### workspaces and groups ######
group_names = [
    ("Web" , {'layout' : 'monadtall'}),
    ("Dev" , {'layout' : 'monadtall'}),
    ("Sys" , {'layout' : 'monadtall'}),
    ("Term", {'layout' : 'monadtall'}),
    ("Rng" , {'layout' : 'monadtall'}),
]

groups = [Group(name, **kwargs) for name, kwargs  in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))

##### theme #####
layout_theme = {"border_width" : 2,
                "margin" : 3,
                "border_focus" : "#cccccc",
                "border_normal" : "#4d4d4d"}

##### prompt ######
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### layouts #####
layouts = [
    layout.Max(),
    layout.Stack(num_stacks = 2),
    layout.MonadTall(**layout_theme),
    layout.TreeTab(
        font = "Ubuntu-C",
        fontsize = "12",
        sections = ["FIRST", "SECOND"],
        section_fontsize = 11,
        bg_color = "#404040",
        active_bg = "#333333",
        active_fg = "#999999",
        inactive_bg = "#333333",
        inactive_fg = "#404040",
        padding_y = 6,
        sction_top = 10,
        panel_width = 150),
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
    fontsize = 10,
    padding = 6,
    background = "#cccccc"
)
exrension_defaults = widget_defaults.copy()

screens = [Screen(bottom=bar.Bar(
        [
            widget.GroupBox(),
            widget.WindowName(),
            widget.Systray(),
            widget.Volume(),
            widget.Battery(),
            widget.Clock(format='%I:%M %p %d-%m-%Y %a'),],18,),),
        ]

wmname = "LG3D"

##### auto-start #####
@hook.subscribe.startup_once
def start_once():
    subprocess.call("setxkbmap model abnt2 -layout br -variant abnt2")