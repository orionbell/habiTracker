#!/usr/bin/env python3

import json
import datetime
import os
import curses
import argparse
import calendar

HEIGHT = 16
WIDTH = 40
PADDING = (0,0)

def init(win):
    curses.init_pair(1,curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.curs_set(0)
    win.clear()
    win.attron(curses.A_BOLD)
    win.attron(curses.color_pair(1))

def draw_calander(win,factor = 0, days=0):
    calendar_win = curses.newwin(HEIGHT, WIDTH, PADDING[1], curses.COLS - WIDTH - PADDING[0])
    calendar_win.attron(curses.A_BOLD)
    calendar_win.attron(curses.color_pair(1))
    calendar_win.border()
    win.refresh()
    calendar_win.addstr(0, (WIDTH//2)-4,"Calendar")
    current_today = datetime.datetime.today()
    month_last_date = calendar.monthrange(current_today.year, current_today.month)[1]
    today = current_today + datetime.timedelta(days = factor * month_last_date + days)
    month = today.month
    year = today.year
    day_num = today.day
    current_today_num = current_today.day
    current_month = current_today.month
    current_year = current_today.year
    first_day_num = today.replace(day=1).weekday()
    month_name = today.strftime("%B")
    calendar_win.addstr(1, (WIDTH//2)-len(month_name),f"{month_name} - {year}")
    line = 2
    col = 2
    calendar_win.move(line, col)
    calendar_win.attrset(curses.color_pair(2))
    calendar_win.addstr(f" {calendar.day_abbr[-1]} ")
    calendar_win.move(line, col)
    for day in calendar.day_abbr[:-1]:
        col += 5
        calendar_win.move(line, col)
        calendar_win.addstr(f" {day} ")
    calendar_win.attroff(curses.color_pair(2))
    if first_day_num != 6:
        col = 4 + 5 * (first_day_num + 1) 
    else:
        col = 4
    line += 2
    row = 0
    calendar_win.move(line, col)
    for i in range(1,calendar.monthrange(year,month)[1] + 1):
        if (first_day_num == 6 and i % 7 == 0) or (i == (6 - first_day_num) + row * 7):
            line += 2
            col = 4
            row += 1
        else:
            col += 5
        if i == current_today_num and month == current_month and year == current_year:
                calendar_win.attron(curses.color_pair(1))
        if i == day_num:
            calendar_win.attron(curses.color_pair(2))
        calendar_win.addstr(f"{i}")
        if i == current_today_num and month == current_month and year == current_year:
                calendar_win.attroff(curses.color_pair(1))
        if i == day_num:
           calendar_win.attroff(curses.color_pair(2))
        calendar_win.move(line,col)
    calendar_win.refresh()
    return calendar_win

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
    cal_win = draw_calander(main_win)
    draw_progress(main_win)
    draw_habits(main_win)
    cal_win.nodelay(True)
    factor = 0
    days = 0
    while True:
        try:
            key = cal_win.getkey()
            if key == 'm':
                factor += 1
                cal_win = draw_calander(main_win,factor,days)
            elif key == 'M':
                factor -= 1
                cal_win = draw_calander(main_win,factor,days)
            elif key == 'y':
                factor += 12
                cal_win = draw_calander(main_win,factor,days)
            elif key == 'Y':
                factor -= 12
                cal_win = draw_calander(main_win,factor,days)
            elif key.lower() == 'h':
                days -= 1
                cal_win = draw_calander(main_win,factor,days)
            elif key.lower() == 'j':
                days += 7
                cal_win = draw_calander(main_win,factor,days)
            elif key.lower() == 'k':
                days -= 7
                cal_win = draw_calander(main_win,factor,days)
            elif key.lower() == 'l':
                days += 1
                cal_win = draw_calander(main_win,factor,days)
            elif key.lower() == 'b':
                cal_win = draw_calander(main_win)
            elif key.lower() == 'q':
                break
        except:
            continue
curses.wrapper(main)
