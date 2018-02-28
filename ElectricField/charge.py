from vpython import *

# some useful constants
k = 9e9  # force constant
q = 1.6e-19  # unit of charge


# Electric charge class
class ElectricBall(sphere):
    def __init__(self, color=color.red, radius=0, charge=0, pos=vector(0, 0, 0)):
        self.charge = charge
        sphere.__init__(self, pos=pos, radius=radius, color=color)


# create a list of charges to simulate a eletric bar
def draw_field(num_charge):
    scene = canvas(title='electric field of a list of charges', width=800, height=600, background=color.magenta)
    # variables
    # bar length
    l = num_charge

    # total charge, a defined constant
    Q = 1e-8
    dq = Q / num_charge
    # dx = L / num_charge
    charges = []
    for x in arange(-l, 1.1 * l, 2 * l / (num_charge - 1)):
        q = ElectricBall(pos=vector(x, 0, 0), radius=1, color=color.red, charge=dq)
        charges.append(q)

    # creat arrow around electric balls
    arrows = []
    for x in arange(-1.5 * l, 1.51 * l, 0.3 * l):
        for y in arange(-1 * l, 1.1 * l, 0.4 * l):
            for z in arange(-1 * l, 1.1 * l, 0.4 * l):
                pointer = arrow(pos=vector(x, y, z), color=color.white, opacity=0.0)
                total_field = vector(0, 0, 0)

                # infinity large arrows will be ignored
                infinity = False

                # each arrow is affected by all of the charges
                for q in charges:
                    dir = pointer.pos - q.pos
                    if dir.mag == 0:
                        infinity = True
                        break
                    # calculate electric field affected by each electric ball
                    E = (k * dq / (dir.mag) ** 2) * dir.norm()
                    # sum electric field at the each point
                    total_field += E

                if infinity:
                    continue

                # if arrow is not too large, display it
                if total_field.mag < 10:
                    rate(25)
                    pointer.axis = total_field
                    pointer.shaftwidth = 0.2
                    pointer.opacity = 1.0
                    arrows.append(pointer)


def main():
    draw_field(8)


if __name__ == '__main__':
    main()
