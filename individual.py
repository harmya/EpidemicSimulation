import random
import math

speed = 1


class Individual:
    def __init__(self, c, x, y, r, w):
        self.x = x
        self.y = y
        self.c = c
        self.r = r
        self.x0 = x - r
        self.y0 = y - r
        self.x1 = x + r
        self.y1 = y + r
        x_v = random.uniform(-1, 1)
        y_v = random.uniform(-1, 1)
        r = math.sqrt((x_v * x_v) + (y_v * y_v))
        self.x_vector = speed * (x_v / r)
        self.y_vector = speed * (y_v / r)
        self.check = 0
        self.w = w
        self.infection_radius = 12
        self.infected = False
        self.susceptible = True
        self.deceased = False
        self.image = ()
        self.radius_image = ()
        self.sentinal = 1
        self.time_of_infection = 0

    def create_vector(self, x_low, x_high, y_low, y_high):
        x_v = random.uniform(x_low, x_high)
        y_v = random.uniform(y_low, y_high)
        r = math.sqrt((x_v * x_v) + (y_v * y_v))
        self.x_vector = speed * (x_v / r)
        self.y_vector = speed * (y_v / r)

    def make_individual(self):
        if self.infected:
            self.image = self.c.create_oval(self.x0, self.y0, self.x1, self.y1, fill="red")
        else:
            self.image = self.c.create_oval(self.x0, self.y0, self.x1, self.y1, fill="skyblue")

    def infect(self):
        self.c.itemconfig(self.image, fill="red")
        self.infected = True

    def radius_animation(self):

        self.c.itemconfig(self.radius_image, outline="")
        c = self.c.coords(self.image)
        f = 0.3
        x0 = c[0] - (f * self.sentinal)
        y0 = c[1] - (f * self.sentinal)
        x1 = c[2] + (f * self.sentinal)
        y1 = c[3] + (f * self.sentinal)

        if (x1 - x0) / 2 >= self.infection_radius:
            x0 = c[0]
            y0 = c[1]
            x1 = c[2]
            y1 = c[3]
            self.sentinal = 1
        self.sentinal += 1
        self.radius_image = self.c.create_oval(x0, y0, x1, y1, outline="red")

    def move_individual(self):
        coordinates = self.c.coords(self.image)
        if coordinates[2] >= 400:
            self.create_vector(-1, 0, -1, 1)

        if coordinates[0] <= 9:
            self.create_vector(0, 1, -1, 1)

        if coordinates[3] >= 400:
            self.create_vector(-1, 1, -1, 0)

        if coordinates[1] <= 9:
            self.create_vector(-1, 1, 0, 1)

        self.c.move(self.image, self.x_vector, self.y_vector)
