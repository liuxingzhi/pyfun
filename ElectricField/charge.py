from vpython import color, arrow, vector, sphere, rate, canvas
from numpy import arange

# some useful constants
k = 9e9  # force constant
q = 1.6e-19  # unit of charge
view_space_length = 10


# Electric charge class
class ElectricBall(sphere):
    def __init__(self, color=color.red, radius=0, charge=0, pos=vector(0, 0, 0)):
        sphere.__init__(self, pos=pos, radius=radius, color=color)
        self.charge = charge


# create a list of charges to simulate a eletric bar
def draw_electrical_field(num_charge):
    scene = canvas(title='electric field of a list of charges', width=800, height=600, background=color.magenta)
    # dx = L / num_charge
    Q = 1e-8  # total charges
    # dq = 1e-8 / 6  # define charge of electrons
    dq = Q / num_charge
    charges = []
    space_between = 2 * view_space_length / (num_charge + 1)  # evenly divide space between each electrons
    for x in arange(-view_space_length + space_between, view_space_length, space_between):
        q = ElectricBall(pos=vector(x, 0, 0), radius=1, color=color.red, charge=dq)
        charges.append(q)

    # creat arrow around electric balls
    arrows = []
    observe_points_dis = 0.5 * view_space_length
    for x in arange(-1.5 * view_space_length, 1.51 * view_space_length, observe_points_dis):
        for y in arange(-1.0 * view_space_length, 1.01 * view_space_length, observe_points_dis):
            for z in arange(-1.0 * view_space_length, 1.01 * view_space_length, observe_points_dis):
                pointer = arrow(pos=vector(x, y, z), color=color.blue, opacity=0.0)
                electrical_vector = vector(0, 0, 0)

                # infinity large arrows will be ignored
                infinity = False

                # each arrow is affected by all of the charges
                for q in charges:
                    direction_vector = pointer.pos - q.pos
                    if direction_vector.mag == 0:
                        infinity = True
                        break
                    # calculate electric field affected by each electric ball
                    E = (k * dq / direction_vector.mag ** 2) * direction_vector.norm()
                    # sum electric field at the each point
                    electrical_vector += E

                if infinity:
                    continue

                # if arrow is not too large, display it
                if electrical_vector.mag < observe_points_dis:
                    # "rate(30)" tells the program to not do the loop more than 30 times a second.
                    rate(20 * num_charge)
                    pointer.axis = electrical_vector
                    pointer.shaftwidth = 0.1
                    pointer.opacity = 1.0
                    arrows.append(pointer)


def main():
    draw_electrical_field(200)


if __name__ == '__main__':
    main()
