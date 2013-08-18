__author__ = 'rembo'

__projectname__ = 'git comander'

__description__ = '''Console tool for git that helps with merge and rebase and with other commit and branches manipulations.'''

import optparse
import os
import sys
import time
import curses
import curses.textpad
import subprocess
import json
from threading import Thread


import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

path = None
res = None

def render(win):
    parser = optparse.OptionParser()
    parser.add_option('-p', dest='path', default=None, help='Repo path.')
    (options, args) = parser.parse_args(sys.argv[1:])
    path = options.path
    if path == None:
       path = os.getcwd()
    print path 
    time.sleep(3)

    global stdscr
    stdscr = win
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)
    stdscr.timeout(0)
    stdscr.clearok(1)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    stdscr.bkgd(' ', curses.color_pair(2))
    #res = subprocess.Popen('git log --pretty=format:"{\\\"ahesh\\\":\\\"%h\\\", \\\"hesh\\\":\\\"%H\\\", \\\"author\\\":\\\"%an\\\", \\\"commit_date\\\":\\\"%cd\\\", \\\"subject\\\":\\\"%s\\\"}"', stdout=subprocess.PIPE, shell=True, cwd="/home/rembo/repo/core/").communicate()[0].split('\n')
    res = subprocess.Popen('git log --pretty=format:"%h[@#$]%H[@#$]%s[@#$]%an[@#$]%cd" --date=short', stdout=subprocess.PIPE, shell=True, cwd=path).communicate()[0].split('\n')

    top = 0
    while True:
        curses.napms(100)
        rows, colls = stdscr.getmaxyx()
        tabsize = colls//2 - 3
        stdscr.border()
        curses.textpad.rectangle(win, 0, 0, rows-1, tabsize+3)
        stdscr.addstr(0, 2, "rows = %s colls = %s" % (rows, colls), curses.A_BOLD)
        #tab1
        for i in range((rows - 5)//2):
	    try:
                item = res[i + top].split('[@#$]')
                #stdscr.addstr(i+1, 2, res[i + top][:colls-20])
                str = "%s %s %s" % (item[0], item[4], item[3])
                stdscr.addstr(2*i+2, 2, str[:tabsize])
                stdscr.addstr(2*i+2+1, 2, ("        %s" % item[2])[:tabsize], curses.color_pair(1))
            except:
                pass
        #tab2
        for i in range((rows - 5)//2):
            try:
                item = res[i + 2*top].split('[@#$]')
                #stdscr.addstr(i+1, 2, res[i + top][:colls-20])
                str = "%s %s %s" % (item[0], item[4], item[3])
                stdscr.addstr(2*i+2, tabsize+5, str[:tabsize], curses.A_REVERSE)
                stdscr.addstr(2*i+2+1, tabsize+5, ("        %s" % item[2])[:tabsize])
            except:
                pass
        stdscr.refresh()
        ch = stdscr.getch()



        if ch == 27:
            return 0
        if ch == curses.KEY_DOWN:
            top = top + 1
        if ch == curses.KEY_UP:
            top = top - 1
            if top < 0:
                top = 0
        '''
        if ch == curses.KEY_IC:
            nw = curses.newwin(1,10,11,11)
            txtbox = curses.textpad.Textbox(nw)
            curses.textpad.rectangle(win, 10, 10, 12, 20)
            txtbox.edit()
        '''

 





def main():
    #try:
        curses.wrapper(render)
    #except Exception, e:
        #print e
        #print res






main()
