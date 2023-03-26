import numpy as np

G = 6.67e-11 # Gravitational constant

class Planet:
    """Instantiates a gravitational body and contains physics and auxiliary methods."""
    
    def __init__(self, mass: int | float, position: tuple | list, velocity: tuple | list, name: str = "?", color: str = 'black', size: int = 5) -> None:
        self.name = name
        self.color = color
        self.size = size # Plot size, not the real size.
        
        self.mass = mass
        self.position = np.asarray(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.path = [list(position)]
        #self.path = [self.position] # Doesn't work
        
        #self.net_force = np.empty((3,), dtype=np.float64)
    
    def force(self, other) -> np.ndarray:
        """Gravitational force between itself and another body."""
        r = self.position - other.position #reverse?
        den = np.linalg.norm(r) ** 3
        k = -G * other.mass * self.mass / den
        return k * r
    
    def set_force(self, f: np.ndarray) -> None:
        """Updates the net force on the object."""
        self.net_force = f
        
    def update(self, dt: int) -> None:
        """
        Updates the velocity, position, and path.
        Run only after the net force on every body/object has been computed and updated.
        """
        self.velocity += self.net_force * dt / self.mass
        self.position += self.velocity * dt
        self.path.append(list(self.position))
        #self.path.append(self.position) # Doesn't work
        
    def path_to_array(self) -> None:
        """Converts a 2D list to a 2D array."""
        self.path = np.array(self.path)