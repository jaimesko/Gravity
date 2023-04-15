import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import animation

AU = 1.5e11

class Plots:
    """Contains methods for 3 different plots along with an auxiliary path trail length limiting method."""
    
    def __init__(self, system: list) -> None:
        self.system = system
    
    def plot_path(self, figsize: tuple = (8,8)) -> None:
        """2D static path plot"""
        plt.figure(figsize=figsize)
        for i in self.system:
            plt.plot(i.path[:,0], i.path[:,1],lw=1, c=i.color)
        plt.axis('equal')
        plt.show()
    
    def plot_2d(self, figsize: tuple = (8,8), trail_len: int = 30, aus: int = 6) -> None:
        """2D animation"""
        
        # Runs before first frame
        def init() -> list:
            ax.set_xlim(-aus*AU, aus*AU)
            ax.set_ylim(-aus*AU, aus*AU)
            return lines

        def update(frame: int) -> list:
            texts = []
            for i, point, line in zip(self.system, points, lines):
                point.set_data(i.path[frame, 0], i.path[frame, 1])
                xy = self.trail_len(i.path, frame, trail_len)
                line.set_data(xy[:, 0], xy[:, 1]) # xy[:,:2].T also works
                texts.append(ax.text(*i.path[frame, :2], i.name))
                
            return points + lines + texts
        
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_aspect("equal")
        
        points = [ax.plot([], [], marker='o', markersize=i.size, c=i.color)[0] for i in self.system]
        lines = [ax.plot([], [], lw=1, c=i.color)[0] for i in self.system]
        
        anim = animation.FuncAnimation(fig, func=update, frames=len(self.system[0].path), init_func=init, interval=20/5, blit=True)
        plt.show()
    
    def plot_3d(self, figsize: tuple = (8,8), trail_len: int = 30, aus: int = 6) -> None:
        """3D animation"""

        def update(frame: int) -> list:
            for i, line, point, text in zip(self.system, lines, points, texts):
                x = self.trail_length(i.path, frame, trail_len)#[:]
                line.set_data(x[:,:2].T)
                line.set_3d_properties(x[:,2])
                point.set_data_3d(i.path[frame, :3])
                text.set_position(i.path[frame, :3])
            return lines + points + texts
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(projection="3d")
        #ax.axis('auto')
        ax.set(xlim3d=(-aus*AU,aus*AU), xlabel='X')
        ax.set(ylim3d=(-aus*AU,aus*AU), ylabel='Y')
        ax.set(zlim3d=(-1*AU,1*AU), zlabel='Z')
        
        points = [ax.plot([], [], [], marker='o', markersize=i.size, c=i.color)[0] for i in self.system]
        lines = [ax.plot([], [], [], lw=1, c=i.color)[0] for i in self.system]
        texts = [ax.text(i.path[0, 0], i.path[0, 1], i.path[0,2], i.name) for i in self.system]
        
        anim = animation.FuncAnimation(fig, func=update, frames=len(self.system[0].path), interval=1, blit=True)
        plt.show()
    
    def trail_length(self, path: np.ndarray, frame: int, n: int) -> np.ndarray:
        """Returns a path trail with a maximum length of n."""
        return path[frame-n:frame] if frame > n else path[:frame]