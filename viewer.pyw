from graphics import *
from m_zones import *

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

def main():
    win = field_setup(10, 1, 5)
    
    pt = Point(300, 300)
    c = Circle(pt, 50)
    c.setFill(color_rgb(200,200,50))
    c.draw(win)

    win.getMouse() # pause for click in window
    win.close()

main()
