# 3D animation of solar system post simulation (10 years).

import numpy as np
from plotting import Plots
from planet import Planet
from constants import *

sun = Planet(M_sun, (0,0,0), (0,0,0), name='S', color='yellow')
earth = Planet(M_earth, (d_earth,0,0), (0,earth_v,0), name='E', color='blue')
mars = Planet(M_mars, (d_mars, 0, 0), (0, mars_v, 0), name='M', color='red')
jupiter = Planet(M_jupiter, (-d_jupiter,0,0), (0,-jupiter_v,0), name='J', color='orange')
bodies = [sun, earth, mars, jupiter]

def simulation(system: list = bodies, dt: int = 24*60**2, years: int = 10) -> None:
    """
    Performs the simulation for a number of years.
    """
    t = 0
    daysec = 24 * 60 * 60 # Seconds in a day
    while t < years*365*daysec:
        
        # Works, less memory
        #for i in system:
        #    f = np.array((0,0,0), dtype=np.float64)
        #    for j in system:
        #        if i == j:
        #            continue
        #        f += i.force(j)
        #    i.set_force(f)
        
        # Net force (Superposition)
        for i in system:
            f = np.add.reduce([i.force(j) for j in system if i != j]) # np.sum([], axis=0) also works
            i.set_force(f)
        
        # Update after all forces have been computed
        for i in system:
            i.update(dt)
                
        t += dt

if __name__ == "__main__":
    
    simulation(years=10)

    # 2D list to 2D array
    for i in bodies:
        i.path_to_array()

    Plots(bodies).plot_3d(trail_len=365)