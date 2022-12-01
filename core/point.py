from __future__ import annotations
from math import inf


class Point:
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    def assign(self, p: Point):
        self.__x = p.get_x()
        self.__y = p.get_y()
        return self

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def equals_to(self, p: Point):
        return self.__x == p.get_x() and self.__y == p.get_y()

    def to_string(self, is_hex=True):
        if self.equals_to(POINT_AT_INFINITY):
            return 'POINT AT INFINITY'
        return f'({self.__x:x}, {self.__y:x})' if is_hex else f'({self.__x}, {self.__y})'


POINT_AT_INFINITY = Point(inf, inf)
