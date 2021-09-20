import math
import tkinter as tk
import time
import random


import individual as p
import numpy as np
import matplotlib.pyplot as plt
# variable attributes
import self as self

individuals = []
infected_individuals = []
number_of_individuals = 250
passes = 0
FPS = 50
num_sus = 250
num_infec = 1
num_dec = 0
start = time.time() + 100000
quarantine = False


def simulator():
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    canvas = tk.Canvas(window, bg='black')
    canvas.create_line(9, 9, 9, 402, fill='white')
    canvas.create_line(9, 9, 402, 9, fill='white')
    canvas.create_line(402, 9, 402, 402, fill='white')
    canvas.create_line(9, 402, 402, 402, fill='white')
    # quarantine box
    if quarantine:
        canvas.create_line(500, 100, 500, 300, fill='white')
        canvas.create_line(500, 100, 700, 100, fill='white')
        canvas.create_line(500, 300, 700, 300, fill='white')
        canvas.create_line(700, 300, 700, 100, fill='white')
        canvas.create_text(608, 320, text='Quarantine', fill="white", font=('Helvetica 15'))

    canvas.pack(fill=tk.BOTH, expand=True)

    def clicker():
        temp = random.randint(0, number_of_individuals)
        individuals[temp].infect()
        individuals[temp].infected = True
        infected_individuals.append(individuals[temp])
        individuals[temp].time_of_infection = time.time()

    infect_button = tk.Button(window, text='infect', command=clicker)
    infect_button.pack(pady=20)
    for i in range(0, number_of_individuals):
        person = p.Individual(canvas, random.randint(10, 300), random.randint(10, 200), 5, window)
        person.make_individual()
        individuals.append(person)

    def infect_others(k):
        global num_sus, start
        global num_infec
        r = individuals[k].infection_radius
        c = individuals[k].c.coords(individuals[k].image)
        x_i = c[0] + r
        y_i = c[1] + r
        if random.randint(1, 100) <= 5:
            for x in range(0, len(individuals)):
                ind = individuals[x]
                c = ind.c.coords(ind.image)
                temp_x = c[0]
                temp_y = c[1]
                if abs((x_i - temp_x)) <= r and abs((y_i - temp_y)) <= r and ind.infected == False:
                    ind.infect()
                    num_infec += 1
                    num_sus -= 1
                    ind.infected = True
                    infected_individuals.append(ind)

    finish = True
    while finish:
        global num_dec
        for i in range(0, len(individuals)):
            individuals[i].move_individual()
            if individuals[i].infected:
                if (quarantine and time.time() - individuals[i].time_of_infection) >= 1 and individuals[i].quarantined == False:
                    individuals[i].quarantine()
                if (time.time() - individuals[i].time_of_infection) >= 4:
                    canvas.itemconfig(individuals[i].image, fill="grey")
                    canvas.itemconfig(individuals[i].radius_image, outline="")
                    num_dec += 1
                else:
                    individuals[i].radius_animation()
                    infect_others(i)

        if num_infec == 20:
            global start
            start = time.time()
        window.update()
    print(num_sus)
    print(num_infec)
    tk.mainloop()


simulator()
