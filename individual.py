import random
import math
import time

speed = 0.5


class Individual:
    def __init__(self, c, x, y, r, w):
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
        self.quarantined = False
        self.image = ()
        self.radius_image = ()
        self.sentinal = 1
        self.time_of_infection = 0
        self.can_infect = False
        self.is_social_distancing = False
        self.community_number = 0
        self.reached_quarantine = False
        self.reached_community = False
        self.mov_com = False
        self.toCom = 0

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
        self.can_infect = True
        self.time_of_infection = time.time()

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
        if self.quarantined:
            coordinates = self.c.coords(self.image)
            x = coordinates[0] + self.r
            y = coordinates[1] + self.r
            if not self.reached_quarantine:
                if x >= 592 and y >= 192:
                    self.reached_quarantine = True
                    self.c.move(self.image, random.randint(-10, 10), random.randint(-10, 10))
                else:
                    self.c.move(self.image, (600 - x) / 10, (200 - y) / 10)
            else:
                if coordinates[2] >= 700:
                    self.create_vector(-1, 0, -1, 1)

                if coordinates[0] <= 500:
                    self.create_vector(0, 1, -1, 1)

                if coordinates[3] >= 300:
                    self.create_vector(-1, 1, -1, 0)

                if coordinates[1] <= 100:
                    self.create_vector(-1, 1, 0, 1)
                self.c.move(self.image, self.x_vector, self.y_vector)

        else:
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

    def quarantine(self):
        self.quarantined = True

    def move_individual_communities(self):
        if self.mov_com:
            c = random.randint(0, 6)
            centers = [[150, 150], [350, 150], [550, 150], [150, 350, ], [350, 350], [550, 350]]
            coordinates = self.c.coords(self.image)
            x = coordinates[0] + self.r
            y = coordinates[1] + self.r
            if not self.reached_community:
                if x >= centers[c][0] - 5 and y >= centers[c][1] - 5:
                    self.reached_community = True
                    self.c.move(self.image, random.randint(-10, 10), random.randint(-10, 10))
                else:
                    self.c.move(self.image, (centers[self.community_number][0] - x),
                                (centers[self.community_number][1] - y))

        if self.quarantined:
            coordinates = self.c.coords(self.image)
            x = coordinates[0] + self.r
            y = coordinates[1] + self.r
            if not self.reached_quarantine:
                if x >= 464 and y >= 744:
                    self.reached_quarantine = True
                    self.c.move(self.image, random.randint(-10, 10), random.randint(-10, 10))
                else:
                    self.c.move(self.image, (468 - x) / 10, (750 - y) / 10)
            else:
                if coordinates[2] >= 568:
                    self.create_vector(-1, 0, -1, 1)

                if coordinates[0] <= 376:
                    self.create_vector(0, 1, -1, 1)

                if coordinates[3] >= 840:
                    self.create_vector(-1, 1, -1, 0)

                if coordinates[1] <= 660:
                    self.create_vector(-1, 1, 0, 1)
                self.c.move(self.image, self.x_vector, self.y_vector)
        else:
            coordinates = self.c.coords(self.image)
            j = 0
            i = self.community_number
            if self.community_number >= 4:
                i = self.community_number - 3
                j = 1

            if coordinates[2] >= (302 * i):
                self.create_vector(-1, 0, -1, 1)

            if coordinates[0] <= 15 + (310 * (i - 1)):
                self.create_vector(0, 1, -1, 1)

            if coordinates[3] >= 302 + (j * 308):
                self.create_vector(-1, 1, -1, 0)

            if coordinates[1] <= 15 + (j * 310):
                self.create_vector(-1, 1, 0, 1)

            self.c.move(self.image, self.x_vector, self.y_vector)
