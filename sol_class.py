__author__ = 'aschwartz'
import random, math, gc
from tkinter import *


class MainWindow():
    def __init__(self, main):
        self.WIDTH = 800
        self.HEIGHT = 800
        self.canvas = Canvas(main, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.grid(row=0, column=0)
        self.CENTER = [self.WIDTH // 2, self.HEIGHT // 2]
        self.button_width = 100
        self.button_height = 20
        self.half_button_width = self.button_width / 2
        self.half_button_height = self.button_height / 2
        self.AU = self.WIDTH // 4
        self.LD = self.AU / 10
        self.show_fictional = False
        self.display_flight_path = True
        self.view_screen = "inner_sol"
        self.all_obj = set([])
        self.inner_sol_obj = set([])
        self.earth_obj = set([])
        self.mars_obj = set([])
        self.jupiter_obj = set([])
        self.asteroid_group = set([])
        self.non_asteroid_group = set([])

    def callback(self, event):
        '''
        Mouseclick handler. Toggles between display_flight_path (True/False)
        '''
        coord = [event.x, event.y]
        if coord[0] < self.button_width and coord[1] < self.button_height:
            if self.display_flight_path:
               self.display_flight_path = False
            else:
                self.display_flight_path = True
        elif coord[0] < self.button_width and coord[1] > self.button_height and coord[1] < self.button_height * 2:
            if self.show_fictional:
                self.show_fictional = False
            else:
                self.show_fictional = True
        elif coord[0] > self.WIDTH - self.button_width and coord[1] < self.button_height:
            self.view_screen = "inner_sol"

        elif coord[0] > self.WIDTH - self.button_width and coord[1] > self.button_height and coord[1] < self.button_height * 2:
            self.view_screen = "earth"

        elif coord[0] > self.WIDTH - self.button_width and coord[1] > self.button_height * 2 and coord[1] < self.button_height * 3:
            self.view_screen = "mars"

        elif coord[0] > self.WIDTH - self.button_width and coord[1] > self.button_height * 3 and coord[1] < self.button_height * 4:
            self.view_screen = "jupiter"

    def refresh_flight_path(self):
        dict_mode = {"inner_sol":self.inner_sol_obj,
                     "earth":self.earth_obj,
                     "mars":self.mars_obj,
                     "jupiter":self.jupiter_obj}

        for obj in dict_mode[self.view_screen]:
            obj.flight_path()

    def all_celestrial_obj(self):
        '''
        This function packs sprite objects into various sets for various purposes.
        '''
        for obj in gc.get_objects():
            if isinstance(obj, Celestial_body):
                self.all_obj.add(obj)
                if obj.view == "inner_sol":
                    self.inner_sol_obj.add(obj)
                elif obj.view == "earth":
                    self.earth_obj.add(obj)
                elif obj.view == "mars":
                    self.mars_obj.add(obj)
                elif obj.view == "jupiter":
                    self.jupiter_obj.add(obj)
            if isinstance(obj, Asteroid):
                self.asteroid_group.add(obj)
            self.non_asteroid_group = self.inner_sol_obj.difference(self.asteroid_group)

    def screen_overlay(self):
        self.canvas.delete(ALL)  #clears all canvas obj so it doesn't lag.
        self.canvas.create_rectangle(0,0,self.WIDTH,self.HEIGHT, fill="Black") #black space background
        self.canvas.create_rectangle(0,0,self.button_width,self.button_height,fill="Grey",outline="Green") #Create toggle flightpath button
        self.canvas.create_text(self.button_width/2,self.button_height / 2,text="Toggle flight path",fill="Black") #Text for toggle flightpath button
        self.canvas.create_rectangle(0,self.button_height,self.button_width,self.button_height * 2,fill="Grey",outline="Green") #Create fictional obj button
        self.canvas.create_text(self.button_width/2,2 * self.button_height - self.half_button_height,text="Fictional obj",fill="Black") #Text for fictional obj button
        self.canvas.create_rectangle(self.WIDTH - self.button_width, self.button_height * 0, self.WIDTH, self.button_height * 1,fill="Grey",outline="Green")
        self.canvas.create_text(self.WIDTH - self.button_width/2,1 * self.button_height - self.half_button_height,text="Inner Sol view",fill="Black") #Text for Inner Sol view button
        self.canvas.create_rectangle(self.WIDTH - self.button_width, self.button_height * 1, self.WIDTH,self.button_height * 2,fill="Grey",outline="Green")
        self.canvas.create_text(self.WIDTH - self.button_width/2,2 * self.button_height - self.half_button_height,text="Earth view",fill="Black") #Text for Earth view button
        self.canvas.create_rectangle(self.WIDTH - self.button_width, self.button_height * 2, self.WIDTH,self.button_height * 3,fill="Grey",outline="Green")
        self.canvas.create_text(self.WIDTH - self.button_width/2,3 * self.button_height - self.half_button_height,text="Mars view",fill="Black") #Text for Mars view button
        self.canvas.create_rectangle(self.WIDTH - self.button_width, self.button_height * 3, self.WIDTH,self.button_height * 4,fill="Grey",outline="Green")
        self.canvas.create_text(self.WIDTH - self.button_width/2,4 * self.button_height - self.half_button_height,text="Jupiter view",fill="Black") #Text for Jupiter view button

        if self.display_flight_path == True:
            self.refresh_flight_path()


class Celestial_body():
    def __init__(self, canvas, name, radius, solar_distance, color, revolves, mode, view, counter_orbit = None, fictional = None, my_image = None):
        self.canvas = canvas
        self.name = name
        self.radius = radius
        self.solar_distance = solar_distance
        self.color = color
        self.revolves = revolves   #obj that self orbits
        self.stationary_coord = [self.canvas.WIDTH // 2, self.canvas.HEIGHT // 2]
        self.orbit = [] #list of coordinates the object travels through
        self.pos = [0,0]
        self.mode = mode    #Parameter options: stationary(doesn't orbit), primary(orbits stationary obj), tertiary(orbits primary obj, irregular)
        self.view = view
        self.i = 0   #iteration variable
        self.rand_i = False
        self.aphelion = solar_distance[0]     #point in orbit where planet is greatest distance from star
        self.perihelion = solar_distance[1]     #point in orbit where planet is least distance from star
        self.revolutions = 0    #number of times planet revolves around stay (i.e years elapsed)
        self.year_mark = 0     #lap marker
        self.counter_orbit = counter_orbit
        self.fictional = fictional
        self.sides = round(self.solar_distance[0] / 1.5)
        if my_image:
            self.image = PhotoImage(file=my_image)
        else:
            self.image = None

    def __str__(self):
        print(self.name, str(self.color))

    def display_it(self):
        '''
        Draws object on canvas.
        var p1, p2... are x,y coordinates for oval parameter upper-left, lower-right corners, respectively.
        '''
        if self.rand_i == False:
            self.randomize_loc()


        if self.i >= len(self.orbit):
            self.i = 0

        if self.i == self.year_mark:
            self.revolutions += 1

        if not self.canvas.show_fictional and self.fictional:
            pass

        else:
            if self.mode == "stationary":
                self.pos = self.canvas.CENTER
            elif self.mode == "primary" or self.mode == "irregular":
                self.pos = self.orbit[self.i]
            elif self.mode == "tertiary":
                self.get_orbit()
                self.pos = self.orbit[self.i]

            p1 = self.pos[0] - self.radius #upper-left x coord
            p2 = self.pos[1] - self.radius #upper-left y coord
            p3 = self.pos[0] + self.radius #lower-right x coord
            p4 = self.pos[1] + self.radius #lower-right y coord

            if self.image:
                self.canvas.canvas.create_image(self.pos[0],self.pos[1], image=self.image)
            else:
                self.canvas.canvas.create_oval(p1,p2,p3,p4,fill=self.color)

            if self.mode == "stationary":
                self.canvas.canvas.create_text(self.pos[0],self.pos[1],text=self.name,fill="Black")
            elif self.mode == "primary":
                self.canvas.canvas.create_text(p1,p2,text=self.name,fill="White")
            elif self.mode == "tertiary":
                pass

            self.i += 1

    def flight_path(self):
        '''
        Draw's orbit onto plain
        '''
        if not self.canvas.show_fictional and self.fictional:
            pass
        else:
            if self.mode == "stationary":
                p1 = self.stationary_coord[0] - self.radius #upper-left x coord
                p2 = self.stationary_coord[1] - self.radius #upper-left y coord
                p3 = self.stationary_coord[0] + self.radius #lower-right x coord
                p4 = self.stationary_coord[1] + self.radius #lower-right y coord
                self.canvas.canvas.create_oval(p1,p2,p3,p4, outline="Green")

            elif self.mode == "primary":
                p1 = self.canvas.CENTER[0] - self.aphelion
                p2 = self.canvas.CENTER[1] - self.perihelion
                p3 = self.canvas.CENTER[0] + self.aphelion
                p4 = self.canvas.CENTER[1] + self.perihelion
                self.canvas.canvas.create_oval(p1,p2,p3,p4, outline="Green")

            elif self.mode == "tertiary":
                pass

    def test_pass(self):
        print(self.revolves.lookup)

    def distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def get_orbit(self):
        '''
        Generates all the points in the object's orbit around the Star.
        '''
        self.orbit = []


        if self.counter_orbit:
            self.orbit = self.counter_orbit.orbit

        elif self.mode == "stationary":
            self.orbit.append([CENTER[0], CENTER[1]])

        elif self.mode == "primary":
            for i in range(self.sides):
                x = (self.aphelion * math.cos(i * 2 * math.pi / self.sides)) + self.canvas.CENTER[0]
                y = (self.perihelion * math.sin(i * 2 * math.pi / self.sides)) + self.canvas.CENTER[1]
                self.orbit.append([x, y])

        elif self.mode == "tertiary":
            for i in range(self.sides):
                x = (self.aphelion * math.cos(i * 2 * math.pi / self.sides)) + self.revolves.pos[0]
                y = (self.perihelion * math.sin(i * 2 * math.pi / self.sides)) + self.revolves.pos[1]
                self.orbit.append([x, y])

        return self.orbit

    def randomize_loc(self):
        if self.counter_orbit:
            a = self.counter_orbit.i - (len(self.counter_orbit.orbit) // 2)
            if a < 0: self.i = a + len(self.counter_orbit.orbit)

            else: self.i = a

        elif self.mode == "stationary": pass

        else:   #primary, tertiary
            self.i = random.randrange(len(self.orbit))
            self.year_mark = self.i - 1
            self.rand_i = True

    def collide(self, other_object):
        d = self.distance(self.pos, other_object.pos)
        r1 = self.radius
        r2 = other_object.radius
        if d <= r1 + r2:
            return True
        else:
            return False


class Asteroid(Celestial_body):
    def __init__(self, canvas, name, radius, solar_distance, color, revolves, mode, view, counter_orbit = None, fictional = None):
        Celestial_body.__init__(self, canvas, name, radius, solar_distance, color, revolves, mode, view, counter_orbit = None, fictional = None)

    def get_orbit(self):
        '''
        Generates all the points in the object's orbit around the Star.
        '''
        if self.counter_orbit:
            self.orbit = self.counter_orbit.orbit
        else:
            my_range = [random.randrange(180,320),random.randrange(-320,-180)]
            orient = [random.choice(my_range),0]
            a = random.choice(orient)
            orient.pop(orient.index(a))
            b = orient[0]
            if a != 0:
                greater = self.aphelion
                lesser = self.perihelion
            else:
                greater = self.perihelion
                lesser = self.aphelion

            for i in range(self.sides):
                x = (greater * math.cos(i * 2 * math.pi / self.sides)) + self.canvas.CENTER[0] - a
                y = (lesser * math.sin(i * 2 * math.pi / self.sides)) + self.canvas.CENTER[1] - b
                self.orbit.append([x, y])
        return self.orbit