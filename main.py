__author__ = 'aschwartz, Schwartz210@gmail.com'

from sol_var import *

master.title("Inner Sol")
display_flight_path = True
view_screen = "inner_sol"

def part1():
    for obj in my_can.all_obj:
        obj.get_orbit()

def draw():
    '''
    This is the draw handler.
    '''
    my_can.all_set = my_can.asteroid_group.union(my_can.non_asteroid_group)
    view_dict = {"inner_sol":my_can.all_set,
                 "earth":my_can.earth_obj,
                 "mars":my_can.mars_obj,
                 "jupiter":my_can.jupiter_obj
                 }

    for obj in view_dict[my_can.view_screen]:
        obj.display_it()

    group_group_collide(my_can.non_asteroid_group, my_can.asteroid_group)

def asteroid_spawner():
    if len(my_can.asteroid_group) < 15:
        a_asteroid = Asteroid(my_can,"Asteroid",2,ASTEROID_SD,"Grey",sol,"irregular", "inner_sol")
        a_asteroid.get_orbit()
        my_can.asteroid_group.add(a_asteroid)

def event_timer():
    my_can.screen_overlay()
    asteroid_spawner()
    draw()
    my_can.canvas.after(50, event_timer)

def group_collide(group, other_object):
    remove_set = set([])
    for item in group:
        if item.collide(other_object):
            remove_set.add(item)
    group.difference_update(remove_set)

def group_group_collide(group1, group2):
    for item in list(group1):
        group_collide(group2, item)

asteroid_spawner()
my_can.all_celestrial_obj()
part1()
event_timer()

my_can.canvas.bind("<Button-1>", my_can.callback)
my_can.canvas.mainloop()
