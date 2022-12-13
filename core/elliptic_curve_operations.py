from core.mod_operations import divide
from core.point import POINT_AT_INFINITY, Point


def is_on_curve(a, b, p, point: Point):
    x, y = point.get_x(), point.get_y()
    return (y ** 2) % p == (x ** 3 + a * x + b) % p


def negative(p, point: Point):
    return Point(point.get_x(), p - point.get_y())


def add(a, b, p, p1: Point, p2: Point):
    if p1.equals_to(POINT_AT_INFINITY) and is_on_curve(a, b, p, p2):
        return p2

    if p2.equals_to(POINT_AT_INFINITY) and is_on_curve(a, b, p, p1):
        return p1

    if is_on_curve(a, b, p, p1) or is_on_curve(a, b, p, p2):
        x1, y1 = p1.get_x(), p1.get_y()
        x2, y2 = p2.get_x(), p2.get_y()
        if (p1.equals_to(p2) and y1 == 0) or (not p1.equals_to(p2) and x1 == x2):
            return POINT_AT_INFINITY

        global slope
        if p1.equals_to(p2):
            slope = divide(3 * x1 ** 2 + a, 2 * y1, p)
        else:
            slope = divide(y2 - y1, x2 - x1, p)
        x_sum = (slope ** 2 - x1 - x2) % p
        y_sum = (slope * (x1 - x_sum) - y1) % p

        return Point(x_sum, y_sum)

    return POINT_AT_INFINITY


def double(a, b, p, point: Point):
    return add(a, b, p, point, point)


def multiply(a, b, p, k, point: Point):
    if point.equals_to(POINT_AT_INFINITY) or k == 0:
        return POINT_AT_INFINITY
    
    if k < 0:
        return multiply(a, b, p, -k, negative(p, point))

    if k == 1:
        return point

    if k == 2:
        return double(a, b, p, point)

    r_0 = POINT_AT_INFINITY
    r_1 = Point(point.get_x(), point.get_y())
    while k > 0:
        d = k % 2
        if d == 0:
            r_1 = add(a, b, p, r_0, r_1)
            r_0 = double(a, b, p, r_0)
        else:
            r_0 = add(a, b, p, r_0, r_1)
            r_1 = double(a, b, p, r_1)
        k //= 2
    return r_0
