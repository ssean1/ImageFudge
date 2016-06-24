import math
import ntpath
import os
from random import random, randrange
from PIL import Image
from PIL import ImageDraw

from collections import namedtuple

class Fudged(object):
    """ """
    Point = namedtuple('Point', ['x', 'y'])
    Dimention = namedtuple('Dimention', ['width', 'height'])

    def __init__(self, image):
        try:
            self.image = Image.open(image)
        except TypeError as e:
            try:
                if image.__name__ == 'PIL.Image':
                    self.image = image
                else: raise e
            except AttributeError:
                raise e

        self.width = self.image.size[0]
        self.height = self.image.size[1]


    def draw_relative_arcs(self, origin, endpoints, arclength):
        if isinstance(endpoints, self.Point):
            endpoints = [endpoints]
        for endpoint in endpoints:
            color = self.image.getpixel(endpoint)
            angle = self.get_angle(origin, endpoint)
            distance = self.get_distance(origin, endpoint)
            bounding_box = self.make_bounding_box(origin, distance)
            try:
                if arclength > 360: raise ValueError
            except TypeError as e:
                try:
                    if arclength[0] > 360: raise ValueError
                    if arclength[1] > 360: raise ValueError
                    arclength = randrange(arclength[0], arclength[1])
                except IndexError: raise e

            draw = ImageDraw.Draw(self.image).arc(bounding_box,
                                                  angle,
                                                  arclength,
                                                  color)

    def select_point(self):
        return self.Point(int(random()*self.width),
                          int(random()*self.height))

    def get_center(self):
        return self.Point(x=self.width/2, y=self.height/2)

    def save(self, path):
        self.image.save(path)

    def random_points(self, point_number):
        for _ in range(point_number):
            yield self.select_point()


    def center_random_random(self, point_number):
        def rand_gen():
            yield(int(random()*360))

        self.draw_relative_arcs(self.get_center(),
                                self.random_points(point_number),
                                rand_gen())


    def center_random_fixed(self, point_number):
        self.draw_relative_arcs(self.get_center(),
                                self.random_points(point_number),
                                int(random()*360))

    def center_random_range(self, point_number):
        self.draw_relative_arcs(self.get_center(),
                                self.random_points(point_number),
                                (20, 100))

    @staticmethod
    def make_bounding_box(origin, distance):
        return [(origin.x-distance, origin.y-distance),
                (origin.x+distance, origin.y+distance)]

    @staticmethod
    def get_angle(origin, endpoint):
        dx = endpoint.x - origin.x
        dy = endpoint.y - origin.y
        return math.degrees(math.atan2(dy, dx))

    @staticmethod
    def get_distance(origin, endpoint):
        dx = endpoint.x - origin.x
        dy = endpoint.y - origin.y
        return math.floor(math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)))


def test_many_random(path, picture_num, num):
    if os.path.isdir(path): raise Exception #TODO
    file_path, extention = os.path.splitext(path)
    file_name = ntpath.basename(path)
    file_name = file_name[:-len(extention)]
    test_dir = 'test/fudgeTest-{}'.format(num)

    for i in range(picture_num):
        bob1 = Fudged(path)
        bob1.center_random_fixed(100)
        bob1.center_random_range(100)
        testpath1 = os.path.join(test_dir,
                                '{}_all_t{}v{}{}'.format(file_name,
                                                     num,
                                                     i,
                                                     extention))

        bob2 = Fudged(path)
        bob2.center_random_fixed(100)
        testpath2 = os.path.join(test_dir,
                                '{}_fixed_t{}v{}{}'.format(file_name,
                                                     num,
                                                     i,
                                                     extention))

        bob3 = Fudged(path)
        bob3.center_random_range(100)
        testpath3 = os.path.join(test_dir,
                                '{}_range_t{}v{}{}'.format(file_name,
                                                     num,
                                                     i,
                                                     extention))


        try:
            if i is 0: os.makedirs(test_dir)
        except FileExistsError:
            assert 0, "Please use different test number"

        bob1.save(testpath1)
        bob2.save(testpath2)
        bob3.save(testpath3)


if __name__ == '__main__':
    path = '../GodRoss.jpg'

    test_many_random(path, 5, 3)