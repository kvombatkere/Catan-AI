#Settlers of Catan

#Adapted from
#Generated code -- CC0 -- No Rights Reserved -- http://www.redblobgames.com/grids/hexagons/

#IMPORTS
import collections
import math

#Define the x y point for pixels
Point = collections.namedtuple("Point", ["x", "y"])
Axial_Point = collections.namedtuple("Axial_Point", ['q', 'r'])

_Hex = collections.namedtuple("Hex", ["q", "r", "s"])
def Hex(q, r, s):
    assert not (round(q + r + s) != 0), "q + r + s must be 0"
    return _Hex(q, r, s)

#Add function to create Hex from Axial Coordinates and an axial point as input
def Axial_Hex(axialPoint):
    s = -axialPoint.q-axialPoint.r
    assert not (round(axialPoint.q + axialPoint.r + s) != 0), "q + r + s must be 0"
    return _Hex(axialPoint.q, axialPoint.r, s)

def hex_add(a, b):
    return Hex(a.q + b.q, a.r + b.r, a.s + b.s)

def hex_subtract(a, b):
    return Hex(a.q - b.q, a.r - b.r, a.s - b.s)

def hex_scale(a, k):
    return Hex(a.q * k, a.r * k, a.s * k)

def hex_rotate_left(a):
    return Hex(-a.s, -a.q, -a.r)

def hex_rotate_right(a):
    return Hex(-a.r, -a.s, -a.q)

hex_directions = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]
def hex_direction(direction):
    return hex_directions[direction]

def hex_neighbor(hex, direction):
    return hex_add(hex, hex_direction(direction))

hex_diagonals = [Hex(2, -1, -1), Hex(1, -2, 1), Hex(-1, -1, 2), Hex(-2, 1, 1), Hex(-1, 2, -1), Hex(1, 1, -2)]
def hex_diagonal_neighbor(hex, direction):
    return hex_add(hex, hex_diagonals[direction])

def hex_length(hex):
    return (abs(hex.q) + abs(hex.r) + abs(hex.s)) // 2

def hex_distance(a, b):
    return hex_length(hex_subtract(a, b))

def hex_round(h):
    qi = int(round(h.q))
    ri = int(round(h.r))
    si = int(round(h.s))
    q_diff = abs(qi - h.q)
    r_diff = abs(ri - h.r)
    s_diff = abs(si - h.s)
    if q_diff > r_diff and q_diff > s_diff:
        qi = -ri - si
    else:
        if r_diff > s_diff:
            ri = -qi - si
        else:
            si = -qi - ri
    return Hex(qi, ri, si)

#Linear interpolation between 2 hexes
def hex_lerp(a, b, t):
    return Hex(a.q * (1.0 - t) + b.q * t, a.r * (1.0 - t) + b.r * t, a.s * (1.0 - t) + b.s * t)

def hex_linedraw(a, b):
    N = hex_distance(a, b)
    a_nudge = Hex(a.q + 1e-06, a.r + 1e-06, a.s - 2e-06)
    b_nudge = Hex(b.q + 1e-06, b.r + 1e-06, b.s - 2e-06)
    results = []
    step = 1.0 / max(N, 1)
    for i in range(0, N + 1):
        results.append(hex_round(hex_lerp(a_nudge, b_nudge, step * i)))
    return results


#Specify Orientation and layout for Hex <-> Pixel conversion
Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])

layout_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
layout_flat = Orientation(3.0 / 2.0, 0.0, math.sqrt(3.0) / 2.0, math.sqrt(3.0), 2.0 / 3.0, 0.0, -1.0 / 3.0, math.sqrt(3.0) / 3.0, 0.0)

#Layout has the orientation, size and origin
Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])

#Function to covert axial hex coordinates to pixel
def hex_to_pixel(layout, h):
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    x = (M.f0 * h.q + M.f1 * h.r) * size.x
    y = (M.f2 * h.q + M.f3 * h.r) * size.y
    return Point(x + origin.x, y + origin.y)

#Function to convert pixel coordinates to Hex
def pixel_to_hex(layout, p):
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
    q = M.b0 * pt.x + M.b1 * pt.y
    r = M.b2 * pt.x + M.b3 * pt.y
    return Hex(q, r, -q - r)

#Get the corner offset depending on the layout (using start angle)
def hex_corner_offset(layout, corner):
    M = layout.orientation
    size = layout.size
    angle = 2.0 * math.pi * (M.start_angle - corner) / 6.0
    return Point(size.x * math.cos(angle), size.y * math.sin(angle))

#Get the corners of the Polygon in pixel coordinates
def polygon_corners(layout, h):
    corners = []
    center = hex_to_pixel(layout, h)
    for i in range(0, 6):
        offset = hex_corner_offset(layout, i)
        corners.append(Point(round(center.x + offset.x,2), round(center.y + offset.y,2)))
    return corners


# import pygame
# pygame.init()

# def test_layout():
#     #h = Hex(2, -1, -1)
#     flat = Layout(layout_flat, Point(75.0, 75.0), Point(500.0, 400.0))
#     h = pixel_to_hex(flat, Point(500,400))
#     hex_corners_arr = polygon_corners(flat, h)
#     print(hex_corners_arr)

#     h_corner_arr_0 = polygon_corners(flat, Hex(0, 0, 0))
#     h_corner_arr_1 = polygon_corners(flat, Axial_Hex(1, -1))
#     h_corner_arr_2 = polygon_corners(flat, Hex(3, -1, -2))
#     h_corner_arr_3 = polygon_corners(flat, Hex(2, -1, -1))
#     #Draw
#     #clock = pygame.time.Clock()
#     window_size = width, height = 1000, 800

#     screen = pygame.display.set_mode(window_size)
#     for i in range (3000):
#         pygame.draw.polygon(screen, pygame.Color(200, 0, 0), h_corner_arr_0, width==0)
#         pygame.draw.polygon(screen, pygame.Color(0, 200, 0), h_corner_arr_2, width==0)
#         pygame.draw.polygon(screen, pygame.Color(0, 0, 200), h_corner_arr_3, width==0)
#         pygame.draw.polygon(screen, pygame.Color(20, 200, 200), h_corner_arr_1, width==0)

#         pygame.display.set_caption('Catan')
#         pygame.display.update()


#     return None

#test_layout()