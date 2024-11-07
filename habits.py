#!/usr/bin/env python3

import json
import datetime
import os
import curses
import argparse
import calendar
import time

HEIGHT = 16
WIDTH = 40
PADDING = (0,0)
FILEPATH = 'habits.json' 

def init(win):
    if not os.path.isfile(FILEPATH):
        with open(FILEPATH,'w') as f:
            data = {"habits":[],"states":[]}
            json.dump(data,f,indent=4)
    curses.init_pair(1,curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.curs_set(0)
    win.clear()
    win.attron(curses.A_BOLD)
    win.attron(curses.color_pair(1))

def draw_calander(win,factor = 0, days=0, isFocused=True):
    calendar_win = curses.newwin(HEIGHT, WIDTH, PADDING[1], curses.COLS - WIDTH - PADDING[0])
    if isFocused:
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

def draw_progress(win, isFocused=False):
    progress_win = curses.newwin(curses.LINES - PADDING[1] - 1, curses.COLS - WIDTH - PADDING[0])
    if isFocused:
        progress_win.attrset(curses.A_BOLD)
        progress_win.attrset(curses.color_pair(1))
    progress_win.border()
    win.refresh()
    progress_win.addstr(0, ((curses.COLS - WIDTH)//2)-4,"Progress")
    progress_win.refresh()
    return progress_win

def draw_habits(win,isFocused=False):
    habits_win = curses.newwin(curses.LINES - PADDING[1] - HEIGHT - 1, WIDTH, HEIGHT, curses.COLS - WIDTH)
    if isFocused:
        habits_win.attrset(curses.A_BOLD)
        habits_win.attrset(curses.color_pair(1))
    habits_win.border()
    win.refresh()
    habits_win.addstr(0, ((WIDTH)//2)-7,"Today's habits")
    habits_win.refresh()
    return habits_win
    
def main(main_win):
    init(main_win)
    cal_win = draw_calander(main_win)
    prog_win = draw_progress(main_win)
    habits_win = draw_habits(main_win)
    tab = 0 
    factor = 0
    days = 0
    while True:
        if tab == 0:
            cal_win = draw_calander(main_win,factor,days)
            prog_win = draw_progress(main_win)
            habits_win = draw_habits(main_win)
            cal_win.nodelay(True)
            while True:
                try:
                    key = cal_win.getch()
                    if key == ord('m'):
                        factor += 1
                        cal_win = draw_calander(main_win,factor,days)
                    elif key == ord('M'):
                        factor -= 1
                        cal_win = draw_calander(main_win,factor,days)
                    elif key == ord('y'):
                        factor += 12
                        cal_win = draw_calander(main_win,factor,days)
                    elif key == ord('Y'):
                        factor -= 12
                        cal_win = draw_calander(main_win,factor,days)
                    elif key == ord('h'):
                        days -= 1
                        cal_win = draw_calander(main_win,factor,days)
                    elif key == ord('j'):
                        days += 7
                        cal_win = draw_calander(main_win,factor,days)
                    elif key == ord('k'):
                        days -= 7
                        cal_win = draw_calander(main_win,factor,days)
                    elif key == ord('l'):
                        days += 1
                        cal_win = draw_calander(main_win,factor,days)
                    elif key == ord('b'):
                        cal_win = draw_calander(main_win)
                        factor = 0
                        days = 0
                    elif key == 9:
                        tab = (tab + 1) % 3
                        break
                    elif key == ord('Q'):
                        return
                except:
                    continue
        elif tab == 1:
            cal_win = draw_calander(main_win,isFocused=False,factor=factor, days=days)
            prog_win = draw_progress(main_win,isFocused=True)
            habits_win = draw_habits(main_win)
            while True:
                prog_win.nodelay(True)
                try:
                    char = prog_win.getch()
                except:
                    continue
                if char == ord('Q'):
                    return
                elif char == 9:
                    tab = (tab + 1) % 3
                    break
        else:
            cal_win = draw_calander(main_win,isFocused=False,factor=factor,days=days)
            prog_win = draw_progress(main_win)
            habits_win = draw_habits(main_win,isFocused=True)
            habits_win.nodelay(True)
            while True:
                try:
                    char = habits_win.getch()
                except:
                    continue
                if char == ord('Q'):
                    return
                elif char == ord('a'):
                    prompts_win = curses.newwin(1,curses.COLS - 1, curses.LINES - 1, 1)
                    try:
                        curses.echo()
                        prompt = "Habit title:"
                        error = "Empty title is invalid!, press Enter to continue."
                        title = ""
                        rate = ""
                        week_days = []
                        dates = []
                        start_time = ""
                        end_time = ""
                        goal = 0
                        time_obj = { "is_daily": True, "is_weekly": False, "is_monthly": False}
                        habit_type = ""

                        while True:    
                            prompts_win.addstr(prompt)
                            title = prompts_win.getstr(0, len(prompt) + 1, 50).decode()
                            if title:
                                break
                            prompts_win.clear()
                            prompts_win.addstr(error)
                            prompts_win.getch()
                            prompts_win.clear()
                        
                        prompt = "habit type (health, workout, intelligent, skill or else):"
                        while True:
                            error = "Type cannot be empty, press Enter to continue."
                            prompts_win.addstr(prompt)
                            habit_type = prompts_win.getstr(0, len(prompt) + 1, 50).decode()
                            if habit_type:
                                error = "Invalid type!, press Enter to continue."
                                if habit_type in 'health':
                                    habit_type = "health"
                                    break
                                elif habit_type in 'workout':
                                    habit_type = "workout"
                                    break
                                elif habit_type in 'intelligent':
                                    habit_type = "intelligent"
                                    break
                                elif habit_type in 'skill':
                                    habit_type = "skill"
                                    break
                                elif habit_type in 'else':
                                    habit_type = "else"
                                    break
                            prompts_win.clear()
                            prompts_win.addstr(error)
                            prompts_win.getch()
                            prompts_win.clear()
                        


                        prompts_win.clear()
                        main_win.refresh()
                        prompts_win.refresh()
                        prompt = "Rate (daily/weekly/monthly):"
                        error = "Invalid habite rate!, press Enter to continue"
                        while True:
                            prompts_win.addstr(prompt)
                            rate = prompts_win.getstr(0, len(prompt) + 1, 10).decode()
                            if rate and rate.lower() in "daily":
                                rate = "daily"
                                break
                            if rate and rate.lower() in "weekly":
                                rate = "weekly"
                                break
                            if rate and rate.lower() in "monthly":
                                rate = "monthly"
                                break
                            prompts_win.clear()
                            prompts_win.addstr(error)
                            prompts_win.getch()
                            prompts_win.clear()

                        prompts_win.clear()
                        main_win.refresh()
                        prompts_win.refresh()
                        if rate == "weekly":
                            prompt = "Habit day number(s):"
                            error = "Invalid values for day numbers (1-7), press Enter to continue"
                            prompts_win.addstr(prompt)
                            while True:
                                week_days = prompts_win.getstr(0, len(prompt) + 1, 30).decode().split(' ')
                                try:
                                    if all([ int(day) > 0 and int(day) < 7 for day in week_days ]):
                                        day_names = []
                                        for day in week_days:
                                            if int(day) == 1:
                                                day = 6
                                            else:
                                                day = int(day) - 2
                                            day_names.append(calendar.day_abbr[day])
                                        week_days = day_names
                                        time_obj['is_weekly'] = True
                                        time_obj['is_daily'] = False
                                        time_obj['habit_days'] = week_days
                                        break
                                except ValueError: 
                                    prompts_win.clear()
                                    prompts_win.addstr(error)
                                    prompts_win.getch()
                                    prompts_win.clear()
                                    continue
                                
                        elif rate == "monthly":
                            prompt = "Habit date(s):"
                            error = "Invalid date has been giving!, press Enter to continue"
                            prompts_win.addstr(prompt)
                            while True:
                                dates = prompts_win.getstr(0,len(prompt) + 1, 50).decode().split(' ')
                                try:
                                    dates = [int(date) for date in dates]
                                    if any([ x >= 1 or x <= 28 for x in dates ]):
                                        time_obj['habit_dates'] = dates
                                        time_obj['is_monthly'] = True
                                        time_obj['is_daily'] = False
                                        break
                                except ValueError:
                                    prompts_win.clear()
                                    prompts_win.addstr(error)
                                    prompts_win.getch()
                                    prompts_win.clear()
                                    continue
                        prompt = "start time(hh:mm or \"after <habit id>\"):"
                        error = "Invalid start time, press Enter to continue"
                        while True:
                            prompts_win.addstr(prompt)
                            start_time = prompts_win.getstr(0,len(prompt) + 1, 10).decode()
                            if 'after' in start_time:
                                try:
                                    id = int(start_time.split(' ')[1])
                                except:
                                    error = "Invalid id, press enter to continue"
                                    prompts_win.clear()
                                    prompts_win.addstr(error)
                                    prompts_win.getch()
                                    prompts_win.clear()
                                    continue
                                with open(FILEPATH,'r') as f:
                                    habits = json.load(f)
                                    start_time = ""
                                    for habit in habits['habits']:
                                        if habit['id'] == id:
                                            start_time = habit['times']['startTime']
                                            break

                                    if start_time == '':
                                        error = "End time cannot be empty, press enter to continue"
                                        prompts_win.clear()
                                        prompts_win.addstr(error)
                                        prompts_win.getch()
                                        prompts_win.clear() 
                                        continue
                            else:
                                try:
                                    time.strptime(start_time,'%H:%M')
                                    time_obj['start_time'] = start_time
                                    break
                                except ValueError:
                                    prompts_win.clear()
                                    prompts_win.addstr(error)
                                    prompts_win.getch()
                                    prompts_win.clear()
                                    continue
                        prompt = "end time(hh:mm or \"before <habit id>\"):"
                        prompts_win.clear()
                        while True:
                            prompts_win.addstr(prompt)
                            error = "Invalid end time, press Enter to continue"
                            end_time = prompts_win.getstr(0,len(prompt) + 1, 10).decode()
                            if 'before' in end_time:
                                try:
                                    id = int(end_time.split(' ')[1])
                                except IndexError:
                                    error = "Invalid id, press enter to continue"
                                    prompts_win.clear()
                                    prompts_win.addstr(error)
                                    prompts_win.getch()
                                    prompts_win.clear()
                                    continue
                                with open(FILEPATH,'r') as f:
                                    habits = json.load(f)
                                    end_time = ""
                                    for habit in habits['habits']:
                                        if habit['id'] == id:
                                            end_time = habit['times']['endTime']
                                            break

                                    if end_time == '':
                                        error = "End time cannot be empty, press enter to continue"
                                        prompts_win.clear()
                                        prompts_win.addstr(error)
                                        prompts_win.getch()
                                        prompts_win.clear()
                                        continue
                            else:
                                try:
                                    time.strptime(end_time,'%H:%M')
                                    time_obj['end_time'] = end_time
                                    break
                                except ValueError:
                                    prompts_win.clear()
                                    prompts_win.addstr(error)
                                    prompts_win.getch()
                                    prompts_win.clear()
                                    continue
                        prompt = "days goal:"
                        prompts_win.clear()
                        while True:
                            error = "Invalid goal number, press Enter to continue"
                            prompts_win.addstr(prompt)
                            try:
                                goal = int(prompts_win.getstr(0,len(prompt) + 1, 3))
                            except ValueError:
                                prompts_win.clear()
                                prompts_win.addstr(error)
                                prompts_win.getch()
                                prompts_win.clear()
                                continue
                            if goal > 0:
                                break
                            else:
                                error = "Goal can't less then or equals to zero!, press Enter to continue."
                                prompts_win.clear()
                                prompts_win.addstr(error)
                                prompts_win.getch()
                                prompts_win.clear()

                        prompts_win.clear()
                        with open(FILEPATH, 'r') as f:
                            habits = json.load(f)
                            if len(habits['habits']) > 0:
                                id = habits['habits'][-1]['id']
                            else:
                                id = 0
                            new_habit = { 
                                            "id": id,
                                            "title": title,
                                            "last_updated": datetime.datetime.now().strftime("%M %B, %Y"),
                                            "type": habit_type,
                                            "time":time_obj,
                                            "strikes":{
                                                "max":0,
                                                "current":0
                                            },
                                            "goals":{
                                                "previous":0,
                                                "current":goal,
                                                "scale_factor":0.35
                                            }
                                        }
                            habits['habits'].append(new_habit)
                            with open(FILEPATH, 'w') as wf:
                                json.dump(habits,wf,indent=4)
                        prompts_win.addstr('Habit has been saved, good luck :)')
                        time.sleep(3)
                        prompts_win.clear()
                        curses.noecho()
                        main_win.refresh()
                        prompts_win.refresh()
                    except KeyboardInterrupt:
                        curses.noecho()
                        prompts_win.clear()
                        prompts_win.refresh()
                        continue
                elif char == 9:
                    tab = (tab + 1) % 3
                    break
                        
curses.wrapper(main)
