import curses

screen= curses.initscr()
#curses.noecho()
curses.curs_set(1)
screen.keypad(1)

screen.addstr("This is a string")
top_pos=12
left_pos=20
screen.addstr(top_pos, left_pos ,"its kinda like matlab")

while True:
    event = screen.getch()
    print(event)
    print(curses.KEY_ENTER)
    if event == ord("q"):
        break
    elif event == 10:
        (y,x)=screen.getyx();
        screen.addstr(y,x,"You pushed enter")

curses.endwin()
