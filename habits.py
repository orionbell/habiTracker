#!/usr/bin/env python3

import json
import datetime
import os
import curses
import argparse

HEIGHT = 15
WIDTH = 40
PADDING = (0,0)

def init(win):
    curses.init_pair(1,curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_CYAN)
    win.clear()
    win.attrset(curses.A_BOLD)
    win.attrset(curses.color_pair(1))

def draw_calander(win):
    calander_win = curses.newwin(HEIGHT, WIDTH, PADDING[1], curses.COLS - WIDTH - PADDING[0])
    calander_win.attrset(curses.A_BOLD)
    calander_win.attrset(curses.color_pair(1))
    calander_win.border()
    win.refresh()
    calander_win.addstr(0, (WIDTH//2)-4,"Calander")
    calander_win.refresh()

def draw_progress(win):
    progress_win = curses.newwin(curses.LINES - PADDING[1], curses.COLS - WIDTH - PADDING[0])
    progress_win.attrset(curses.A_BOLD)
    progress_win.attrset(curses.color_pair(1))
    progress_win.border()
    win.refresh()
    progress_win.addstr(0, ((curses.COLS - WIDTH)//2)-4,"Progress")
    progress_win.refresh()

def draw_habits(win):
    habits_win = curses.newwin(curses.LINES - PADDING[1] - HEIGHT, WIDTH, HEIGHT, curses.COLS - WIDTH)
    habits_win.attrset(curses.A_BOLD)
    habits_win.attrset(curses.color_pair(1))
    habits_win.border()
    win.refresh()
    habits_win.addstr(0, ((WIDTH)//2)-7,"Today's habits")
    habits_win.refresh()

def main(main_win):
    init(main_win)
    draw_calander(main_win)
    draw_progress(main_win)
    draw_habits(main_win)
    main_win.getch()
curses.wrapper(main)
