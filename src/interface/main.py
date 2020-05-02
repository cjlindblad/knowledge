import curses

def draw_screen(stdscr):
    data = [
        'first item',
        'second item',
        'third item',
        'fourth item',
        'fifth item'
    ]

    k = 0
    menu_index = 0

    # inital blank screen
    curses.curs_set(False)
    stdscr.clear()
    stdscr.refresh()

    # main loop
    while (k != ord('q')):
        # key listeners
        if k == curses.KEY_UP and menu_index > 0:
            menu_index = menu_index - 1
        elif k == curses.KEY_DOWN and menu_index < len(data) - 1:
            menu_index = menu_index + 1

        stdscr.clear()

        for i, item in enumerate(data):
            if menu_index == i:
                stdscr.addstr(i, 0, item, curses.A_REVERSE)
            else:
                stdscr.addstr(i, 0, item)

        stdscr.refresh()

        k = stdscr.getch()

def main():
    curses.wrapper(draw_screen)

main()
