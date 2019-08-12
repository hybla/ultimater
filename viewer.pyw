from graphics import *
from m_zones import *

import m_file

def delay(d):
    for i in range(d):
        for i in range(100):
            pass

def field_setup(cell_size, border, info_area):
    # cell_size: how many square pixels each cell will occupy
    # border: the size of the area surrounding the field (in cells)
    # info_area: the size (in cells) of the area text will be displayed.
    cs = cell_size
    b = border
    ia = info_area

    # define the colors of the different field areas
    field_c = color_rgb(40, 100, 40)
    border_c = color_rgb(130, 80, 5)
    info_c = color_rgb(40, 50, 70)
    line_c = color_rgb(130, 180, 130)
    
    # set the field size using the coordinates of the
    # top right corner of the end zone
    fw = field['EZ'][1][0]
    fh = field['EZ'][1][1]

    # set the overall window size
    w = ((b * 2) + fw) * cs
    h = ((b * 2) + ia + fh) * cs
    print('setting window to {} by {}'.format(w, h))

    # create the window
    win = GraphWin('The Ultimater Field', w, h)
    win.setBackground(border_c)

    # draw the playing area
    top_left = Point(b * cs, b * cs)
    bottom_right = Point((fw + b) * cs, (fh + b) * cs)
    field_rect = Rectangle(top_left, bottom_right)
    field_rect.setFill(field_c)
    field_rect.draw(win) 
    print('field area is at: {} {}'.format(top_left, bottom_right))

    # draw the info area
    top_left = Point(b * cs, (fh + b) * cs)
    bottom_right = Point((fw + b) * cs, h - (b * cs))
    info_rect = Rectangle(top_left, bottom_right)
    info_rect.setFill(info_c)
    info_rect.draw(win) 
    print('info area is at: {} {}'.format(top_left, bottom_right))

    # draw the zones on the field
    for zone in field:
        top_left =     Point((field[zone][0][0] + b) * cs,
                             (field[zone][0][1] + b) * cs)
        bottom_right = Point((field[zone][1][0] + b) * cs,
                             (field[zone][1][1] + b) * cs)
        rect = Rectangle(top_left, bottom_right)
        rect.setOutline(line_c)
        rect.draw(win) 
        text = Text(rect.getCenter(), zone)
        text.setTextColor(line_c)
        text.draw(win)
        print('{} is at: {} {}'.format(zone, top_left, bottom_right))
    return win

def bouncing_circle_test(win):
    # movement tester
    # based on https://www.youtube.com/watch?v=Rk7Q_VADBRQ
    p2 = win.getMouse()
    xmove = 8
    ymove = 10
    pt = Point(300, 260)
    c = Circle(pt, 50)
    c.setFill(color_rgb(250,200,50))
    c.draw(win)
    keep_going = True
    while keep_going == True:
        # delay(1)
        c.move(xmove, ymove)
        center = c.getCenter()
        p2 = win.checkMouse()
        if ((center.getX() < 60) or center.getX() > 1360):
            xmove =- xmove
        if ((center.getY() < 60) or center.getY() > 410):
            ymove =- ymove
        p3 = win.checkMouse()
        if p3 != p2:
            keep_going = False


def load_game_record(path, generation, away_team_num, home_team_num):
    p = path
    gen = generation
    a = away_team_num
    h = home_team_num
    file_name = ('GEN-' + gen + '_' + a + '_vs_' +
                 'GEN-' + gen + '_' + h)
    os.chdir(path)
    return m_file.read(file_name)

# turns a tuple into a point, and adjusts for cell size
def mk_pt(tup, cell_size, border_size):
    pt = Point((tup[0] + border_size) * cell_size,
               (tup[1] + border_size) * cell_size)
    return pt

def view_game(game_record, cell_size, border_size, win):
    r = game_record
    c = cell_size
    b = border_size
    circle_size = c
    home_color = color_rgb(250, 150, 15)
    away_color = color_rgb(180, 80, 240)
    label_color = color_rgb(40, 50, 70)
    # find the starting positions for each player
    home_left_loc =   mk_pt(r['Start_Spots']['home_left'],   c, b)
    home_center_loc = mk_pt(r['Start_Spots']['home_center'], c, b)
    home_right_loc =  mk_pt(r['Start_Spots']['home_right'],  c, b)
    away_left_loc =   mk_pt(r['Start_Spots']['away_left'],   c, b)
    away_center_loc = mk_pt(r['Start_Spots']['away_center'], c, b)
    away_right_loc =  mk_pt(r['Start_Spots']['away_right'],  c, b)
    print('home_left_loc point = {}'.format(home_left_loc))
    # make the circles for each player
    hl_circle = Circle(home_left_loc, circle_size)
    hl_circle.setFill(home_color)
    hl_circle.draw(win)
    hl_label = Text(hl_circle.getCenter(), 'HL')
    hl_label.setTextColor(label_color)
    hl_label.draw(win)

    hc_circle = Circle(home_center_loc, circle_size)
    hc_circle.setFill(home_color)
    hc_circle.draw(win)
    hc_label = Text(hc_circle.getCenter(), 'HC')
    hc_label.setTextColor(label_color)
    hc_label.draw(win)

    hr_circle = Circle(home_right_loc, circle_size)
    hr_circle.setFill(home_color)
    hr_circle.draw(win)
    hr_label = Text(hr_circle.getCenter(), 'HR')
    hr_label.setTextColor(label_color)
    hr_label.draw(win)

    al_circle = Circle(away_left_loc, circle_size)
    al_circle.setFill(away_color)
    al_circle.draw(win)
    al_label = Text(al_circle.getCenter(), 'AL')
    al_label.setTextColor(label_color)
    al_label.draw(win)

    ac_circle = Circle(away_center_loc, circle_size)
    ac_circle.setFill(away_color)
    ac_circle.draw(win)
    ac_label = Text(ac_circle.getCenter(), 'AC')
    ac_label.setTextColor(label_color)
    ac_label.draw(win)

    ar_circle = Circle(away_right_loc, circle_size)
    ar_circle.setFill(away_color)
    ar_circle.draw(win)
    ar_label = Text(ar_circle.getCenter(), 'AR')
    ar_label.setTextColor(label_color)
    ar_label.draw(win)

    win.getMouse() # pause for click in window before we play the moves
    
    # actually move the circles
    for time in range(r['Duration']):
        print('t = {}'.format(time))
        t = str(time)
        for move in r[t]['Moves']:
            if move == 'home_left':
                x = r[t]['Moves']['home_left']['offset'][0] * c
                y = r[t]['Moves']['home_left']['offset'][1] * c
                hl_circle.move(x, y)
                hl_label.move(x, y)
                print('Moving {} ({}, {})'.format(move, x, y))
            elif move == 'home_center':
                x = r[t]['Moves']['home_center']['offset'][0] * c
                y = r[t]['Moves']['home_center']['offset'][1] * c
                hc_circle.move(x, y)
                hc_label.move(x, y)
                print('Moving {} ({}, {})'.format(move, x, y))
            elif move == 'home_right':
                x = r[t]['Moves']['home_right']['offset'][0] * c
                y = r[t]['Moves']['home_right']['offset'][1] * c
                hr_circle.move(x, y)
                hr_label.move(x, y)
                print('Moving {} ({}, {})'.format(move, x, y))
            elif move == 'away_left':
                x = r[t]['Moves']['away_left']['offset'][0] * c
                y = r[t]['Moves']['away_left']['offset'][1] * c
                al_circle.move(x, y)
                al_label.move(x, y)
                print('Moving {} ({}, {})'.format(move, x, y))
            elif move == 'away_center':
                x = r[t]['Moves']['away_center']['offset'][0] * c
                y = r[t]['Moves']['away_center']['offset'][1] * c
                ac_circle.move(x, y)
                ac_label.move(x, y)
                print('Moving {} ({}, {})'.format(move, x, y))
            elif move == 'away_right':
                x = r[t]['Moves']['away_right']['offset'][0] * c
                y = r[t]['Moves']['away_right']['offset'][1] * c
                ar_circle.move(x, y)
                ar_label.move(x, y)
                print('Moving {} ({}, {})'.format(move, x, y))
            





path = '/Users/testuser/Projects/ultimater/data/teams/test/games'
record = load_game_record(path, 'TEST3', '004', '003')
print('game record is:\n{}'.format(record))
print('game record 0 is:\n{}'.format(record['0']))

def main():
    cell_size = 10
    border_size = 1
    info_area = 5
    win = field_setup(cell_size, border_size, info_area)

    # bouncing_circle_test(win)
    view_game(record, cell_size, border_size, win)

    win.getMouse() # pause for click in window
    win.close()

main()
