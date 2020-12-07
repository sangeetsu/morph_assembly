import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import EllipseCollection
from matplotlib.text import Annotation
from world import World
from bitmap import BitMap
from scipy.misc.pilutil import imread
from math import floor

robotRadius = 0.5
sensorRadius = 6
swarmSize = 180
shapeWidth = 7
tick = 20 # milliseconds
velocity = 1
ang_velocity = 10
# robotRadius = 0.7
# sensorRadius = 6
# swarmSize = 90
# shapeWidth = 7
# tick = 20 # milliseconds
# velocity = 1
# ang_velocity = 5
file_path = "shapes/tumor100.png"

bitmap = BitMap(file_path)
origin = bitmap.origin
datafile = open(file_path)
img = imread(datafile, mode='L')
img[np.nonzero(img-255)] = 0

fieldSizeX1 = 0
fieldSizeX2 = 100 + fieldSizeX1
fieldSizeY1 = 0
fieldSizeY2 = 100 + fieldSizeY1

#shape to assemble
shapeX = np.array([0, 20, 20, 10, 10, 0, 0])
shapeY = np.array([0, 0, 10, 10, 20, 20, 0])
shapeOffsetX = 0
shapeOffsetY = 0
scaleX = 1
scaleY = 1



world = World(bitmap,  swarmSize, shapeWidth, robotRadius, sensorRadius, velocity, ang_velocity, tick)
fasePos = world.rotate(0.75*robotRadius)
'''
for i in xrange(100):
    world.updateWorld()
'''

startPos = list(zip(world.positions[0,:], world.positions[1,:]))
startPosFace = list(zip(world.positions[0,:] + fasePos[0,:], world.positions[1,:] + fasePos[1,:]))

fig = plt.figure(figsize=(8, 8))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(fieldSizeX1, fieldSizeX2), ax.set_xticks([])
ax.set_ylim(fieldSizeY1, fieldSizeY2), ax.set_yticks([])
plt.gca().set_aspect('equal', adjustable='box')

grad_vals = map(lambda x: -1 if x== float('inf') else int(floor(x)), world.gradients)
anns = []
for label, x, y in zip(grad_vals, world.positions[0,:] + origin[0], world.positions[1,:]+origin[1]):
    ann = Annotation(label,xy=(x,y), xytext = (0, 0),textcoords = 'offset points', ha = 'center', va = 'center')
    ax.add_artist(ann)
    anns.append(ann)

circles = ax.add_collection(EllipseCollection(widths=2*robotRadius, heights=2*robotRadius, angles=0,
                                    units='xy', edgecolors='black', linewidth=0.5,facecolors=world.colors,
                                    offsets=startPos, transOffset=ax.transData))

points = ax.add_collection(EllipseCollection(widths=0.5*robotRadius, heights=0.5*robotRadius, angles=0,
                                    units='xy', facecolors='black',
                                    offsets=startPosFace, transOffset=ax.transData))

def init():
    circles.set_offsets([])
    points.set_offsets([])
    return circles


def update(frame):
    circles.set_offsets(list(zip(frame[0], frame[1])))
    grad_vals = map(lambda x: -1 if x== float('inf') else int(floor(x)), world.gradients)
    i = 0
    for label, x, y in zip(grad_vals, world.positions[0,:] + origin[0], world.positions[1,:]+origin[1]):
        anns[i].remove()
        ann = Annotation(label,xy=(x,y), xytext = (0, 0),textcoords = 'offset points', ha = 'center', va = 'center')
        ax.add_artist(ann)
        anns[i] = ann
        i += 1

    circles.set_color(world.colors)
    circles.set_edgecolor('black')

    points.set_offsets(list(zip(frame[0] + frame[2], frame[1] + frame[3])))
    return circles


def mainLoop():
    while True:
        world.updateWorld()
        world.updateWorld()
        world.updateWorld()
        world.updateWorld()
        world.updateWorld()
        fasePos = world.rotate(0.75*robotRadius)
        yield world.positions[0,:] + origin[0], world.positions[1,:] + origin[1], fasePos[0,:], fasePos[1,:]
        

anim = animation.FuncAnimation(fig, update, mainLoop, init_func=init, interval=tick)
# anim.save('basic_animation.mp4', fps=int(1000/tick), extra_args=['-vcodec', 'libx264'])
plt.imshow(img, interpolation='none', cmap="hot", zorder=0)
plt.show()

