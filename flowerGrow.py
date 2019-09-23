from __future__ import division
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import math
import sympy as sym

pi=3.1415926
def solve(a, b, x0, y0, ratio):
    theta = (360.0 * ratio) / (1.0 + ratio)
    if theta > 180.0:
        theta = 360 - theta

    angle = theta / 360.0 * 2 * pi
    x1,y1 = sym.symbols('x1,y1')
    f = sym.Eq(x1**2+y1**2, b**b)
    g = sym.Eq(x0*x1+y0*y1, a*b*math.cos(angle))
    return sym.solve([f,g],(x1,y1))[0]

def extend(baseX, baseY, x, y, extend):
    signX_head = 1
    signY_head = 1

    if baseX > x:
        signX_head = -1
    else:
        signX_head = 1

    if baseY > y:
        signY_head = -1
    else:
        signY_head = 1

    length = math.sqrt((x-baseX)**2 + (y-baseY)**2)
    if length == 0:
        return (baseX, baseY)

    lfCos = math.fabs(math.fabs(x - baseX) / length)
    lfSin = math.fabs(math.fabs(y - baseY) / length)
    dx = extend * lfCos
    dy = extend * lfSin
    x = x + dx * signX_head
    y = y + dy * signY_head
    return (x, y)


def create_image_with_ball(width, height, points, ball_size):

    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # draw.ellipse takes a 4-tuple (x0, y0, x1, y1) where (x0, y0) is the top-left bound of the box
    # and (x1, y1) is the lower-right bound of the box.
    for point in points:
        draw.ellipse((point[0] + width / 2.0, point[1] + height / 2.0, point[0] + ball_size + width / 2.0, point[1] +
            ball_size + height / 2.0), fill='gray')
    return img


if __name__ == '__main__':

    # Create the frames
    frames = []
    ratio = 0.36
    x0, y0 = 0,0
    points = [(x0, y0)]
    deltaLen = 1
    for index in range(150):
        if len(points) == 1:
            points.append((200, 200 - deltaLen))
        elif len(points) == 2:
            points[1] = extend(x0, y0, points[1][0], points[1][1], deltaLen)
            a = deltaLen * 2
            b = deltaLen
            point = solve(a, b, points[1][0], points[1][1], ratio)
            points.append(point)
        else:
            for i in range(2, len(points)):
                points[i] = extend(x0, y0, points[i][0], points[i][1], deltaLen)

            lastPoint=points[-1]
            x1=lastPoint[0]
            y1=lastPoint[1]

            lenA = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            lenB = deltaLen
            point = solve(lenA, lenB, x1, y1, ratio)
            points.append(point)


    new_frame = create_image_with_ball(1200, 1200, points, 40)
    frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save('moving_ball.gif', format='GIF', append_images=frames[1:], save_all=True, duration=1000, loop=5)
