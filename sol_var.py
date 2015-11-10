__author__ = 'Avi'
#This script is a library of variables and objects. All of the sprites' data and the sprite obj itself is contained here.

from tkinter import *
import random, sol_class

master = Tk()
my_can = sol_class.MainWindow(master)
Celestial_body = sol_class.Celestial_body
Asteroid = sol_class.Asteroid

#Solar distance values for inner_sol screen
AU = my_can.AU
LD = my_can.LD
MARS_SD = [AU * 1.666, AU * 1.3814]        #[aphelion, perihelion]
EARTH_SD = [AU * 1.0155, AU * 0.9832]
VENUS_SD = [AU * 0.728, AU * 0.718]
MERCURY_SD = [AU * 0.466, AU * 0.3074]
VULCAN_SD = [AU * .3, AU * .25]    #Urbain Le Verrier, mistaken Frence mathematician. Powned by Einstein.
SOL_SD = [AU * 0, AU * 0]   #The Sun is 0 AU from itself
LUNA_SD = [LD * 1.054432319, LD * 0.9431109]
PHOBOS_SD = [LD, LD]
DEIMOS_SD = [LD, LD]
ASTEROID_SD = [2 * AU, .35 * AU]
AST_BELT_SD = [random.uniform(1.8,2.3) * AU, random.uniform(1.8,2.3) * AU]

#Solar distance values for secondary screens
EARTH2_SD = [0 * AU, 0 * AU]
LUNA2_SD = [1.054432319 * AU, 0.9431109 * AU]
MARS2_SD = [0 * AU, 0 * AU]
PHOBOS2_SD = [0.024754918 * AU * 20, 0.024018428 * AU * 20]
DEIMOS2_SD = [0.061047054 * AU * 20, 0.061006999 * AU * 20]
JUPITER2_SD = [0 * AU, 0 * AU]

J_SD = AU / 1000000
IO2_SD = [423400 * J_SD, 420000 * J_SD]
EUROPA2_SD = [676938 * J_SD, 664862 * J_SD]
GANYMEDE_SD = [1071600 * J_SD, 1069200 * J_SD]
CALLISTO_SD = [1897000 * J_SD, 1869000 * J_SD]

#class instances for inner_sol screen
sol = Celestial_body(my_can, "Sol", 35, SOL_SD,"Yellow", False, "stationary", "inner_sol")
mars = Celestial_body(my_can, "Mars",7,MARS_SD,"Red", sol, "primary", "inner_sol")
earth = Celestial_body(my_can, "Earth",10, EARTH_SD,"Blue", sol, "primary", "inner_sol")
venus = Celestial_body(my_can, "Venus",7, VENUS_SD, "White", sol, "primary", "inner_sol")
mercury = Celestial_body(my_can, "Mercury",5,MERCURY_SD,"Grey", sol, "primary", "inner_sol")
vulcan = Celestial_body(my_can, "Vulcan",4,VULCAN_SD,"Purple", sol, "primary", "inner_sol", fictional=True)
luna = Celestial_body(my_can, "Luna", 3, LUNA_SD, "White", earth, "tertiary", "inner_sol")
phobos = Celestial_body(my_can, "Phobos",2,PHOBOS_SD,"#635957",mars,"tertiary", "inner_sol")
deimos = Celestial_body(my_can, "Deimos",2,DEIMOS_SD, "#C6AD95",mars,"tertiary", "inner_sol")
counter_earth = Celestial_body(my_can, "Counter-Earth",10,EARTH_SD,"Grey", sol, "primary", "inner_sol",counter_orbit=earth, fictional=True)
asteroid = Asteroid(my_can, "Asteroid",2,ASTEROID_SD,"Grey",sol,"irregular", "inner_sol")


#class instances for secondary screens
earth2 = Celestial_body(my_can, "Earth",35,EARTH2_SD,"Blue", False, "stationary","earth")
luna2 = Celestial_body(my_can, "Luna", 10, LUNA2_SD, "White", earth2, "primary","earth")

mars2 = Celestial_body(my_can, "Mars",35,MARS2_SD,"Red", False, "stationary", "mars")
phobos2 = Celestial_body(my_can, "Phobos",14,PHOBOS2_SD,"#635957",mars2,"primary", "mars")
deimos2 = Celestial_body(my_can, "Deimos",7.5,DEIMOS2_SD, "#C6AD95",mars2,"primary", "mars")

J_Constant = .005
jupiter2 = Celestial_body(my_can, "Jupiter",35,JUPITER2_SD,"#B78F70", False, "stationary", "jupiter", my_image="Jupiter_New_Horizons.gif")
Io2 = Celestial_body(my_can, "Io",1821.6 * J_Constant,IO2_SD,"Grey", jupiter2, "primary", "jupiter")
Europa2 = Celestial_body(my_can, "Europa",1560.8 * J_Constant,EUROPA2_SD,"Grey", jupiter2, "primary", "jupiter")
Ganymede2 = Celestial_body(my_can, "Ganymede",2634.1 * J_Constant,GANYMEDE_SD,"Grey", jupiter2, "primary", "jupiter")
Callisto2 = Celestial_body(my_can, "Callisto",2410.3 * J_Constant,CALLISTO_SD,"Grey", jupiter2, "primary", "jupiter")