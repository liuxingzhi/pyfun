# from __future__ import division
from vpython import *

# scene = display(width=400, height=400)
scene = canvas(title='show electric field', width=600, height=500, background=color.cyan)
# constants
k = 9e9  # force constant
q = 1.6e-19  # unit of charge
ASCALE = .1
x = 0
y = 0
z = 0

# variables
l = 5
L = 10
N = 5
Q = 1e-8
dq = Q / N
dx = L / N
dis = 1e-8

# observasion point
ro = vector(0, L / 4, 0)

# calc the field

# creat a list of charge
charges = []
for x in arange(-5, 5.1, L / N):
    q = sphere(pos=vector(x, 0, 0), radius=1, color=color.red, charge=dq)
    charges.append(q)

# arrows = []
# creat arrow along x axis
for x in arange(-1 * l, 1.1 * l, 0.3 * l):
    rate(20)
    E = 0
    for y in arange(-1 * l, 1.1 * l, 0.5 * l):
        rate(20)
        # arrow1.pos.y = y
        for z in arange(-1 * l, 1.1 * l, 0.5 * l):
            rate(20)
            # arrow1.pos.z = z
            arrow1 = arrow(pos=vector(x, y, z), color=color.white, opacity=0.0)
            field = vector(0, 0, 0)
            # infinity large arrows will be ignored
            infinity = False
            # each arrow is affected by all of the charges
            for q in charges:
                rate(20)
                R = arrow1.pos - q.pos
                # print("what happen?", arrow1.pos, q.pos, R)
                if mag(R) == 0:
                    infinity = True
                    break
                E = (k * dq / (R.mag) ** 2) * R.norm()
                # print("E is ", (k * dq / (R.mag) ** 2))
                # sum electric field at the each point
                field += E
            if infinity:
                continue

            #if arrow is not too large, display it
            if mag(field) < 10:
                arrow1.axis = field
                arrow1.shaftwidth = 0.2
                arrow1.opacity = 1.0
                # arrows.append(arrow1)
