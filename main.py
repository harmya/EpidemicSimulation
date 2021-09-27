# imports
import tkinter as tk
import time
import random
import individual as p
from tkmacosx import Button

# main variables
individuals = []
infected_individuals = []
number_of_individuals = 250
number_of_individuals_in_community = 100
num_sus = 250
num_infec = 1
num_dec = 0
start = time.time() + 100000
quarantine = False
communities = True
normal = False


def simulator():
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    canvas = tk.Canvas(window, bg='black')
    if normal:
        canvas.create_line(9, 9, 9, 402, fill='white')
        canvas.create_line(9, 9, 402, 9, fill='white')
        canvas.create_line(402, 9, 402, 402, fill='white')
        canvas.create_line(9, 402, 402, 402, fill='white')
        for i in range(0, number_of_individuals):
            person = p.Individual(canvas, random.randint(10, 400), random.randint(10, 400), 5, window)
            person.make_individual()
            individuals.append(person)

    elif communities:
        for i in range(1, 4):
            canvas.create_line(9 + (300 * (i - 1) + 9 * (i - 1)), 9, 9 + (300 * (i - 1)) + 9 * (i - 1), 309,
                               fill='white')
            canvas.create_line(9 + (300 * (i - 1)) + 9 * (i - 1), 9, 309 + (300 * (i - 1)) + 9 * (i - 1), 9,
                               fill='white')
            canvas.create_line(309 + (300 * (i - 1)) + 9 * (i - 1), 9, 309 + (300 * (i - 1)) + 9 * (i - 1), 309,
                               fill='white')
            canvas.create_line(9 + (300 * (i - 1)) + 9 * (i - 1), 309, 309 + (300 * (i - 1)) + 9 * (i - 1), 309,
                               fill='white')
        for i in range(1, 4):
            canvas.create_line(9 + (300 * (i - 1) + 9 * (i - 1)), 318, 9 + (300 * (i - 1) + 9 * (i - 1)), 618,
                               fill='white')
            canvas.create_line(9 + (300 * (i - 1) + 9 * (i - 1)), 318, 309 + (300 * (i - 1) + 9 * (i - 1)), 318,
                               fill='white')
            canvas.create_line(309 + (300 * (i - 1) + 9 * (i - 1)), 318, 309 + (300 * (i - 1) + 9 * (i - 1)), 618,
                               fill='white')
            canvas.create_line(9 + (300 * (i - 1) + 9 * (i - 1)), 618, 309 + (300 * (i - 1) + 9 * (i - 1)), 618,
                               fill='white')
        j = 0
        for x in range(0, 6):
            check_com = 0
            if x >= 3:
                j = 1
                x = x - 3
                check_com = 1
            for i in range(0, number_of_individuals_in_community):
                person = p.Individual(canvas, random.randint(15 + (310 * x), 290 + (310 * x)),
                                      random.randint(10 + (310 * j), 300 + (310 * j)), 5, window)
                person.make_individual()

                if check_com == 1:
                    person.community_number = x + 4
                else:
                    person.community_number = x + 1

                individuals.append(person)

    # quarantine box
    if quarantine:
        if communities:
            canvas.create_line(368, 650, 568, 650, fill='red')
            canvas.create_line(368, 650, 368, 850, fill='red')
            canvas.create_line(368, 850, 568, 850, fill='red')
            canvas.create_line(568, 850, 568, 650, fill='red')
            canvas.create_text(465, 870, text='Quarantine', fill="white", font=('Helvetica 15'))
        else:
            canvas.create_line(500, 100, 500, 300, fill='red')
            canvas.create_line(500, 100, 700, 100, fill='red')
            canvas.create_line(500, 300, 700, 300, fill='red')
            canvas.create_line(700, 300, 700, 100, fill='red')
            canvas.create_text(608, 320, text='Quarantine', fill="white", font=('Helvetica 15'))

    canvas.pack(fill=tk.BOTH, expand=True)

    def clicker():
        temp = random.randint(0, len(individuals))
        individuals[temp].infect()
        individuals[temp].infected = True
        individuals[temp].can_infect = True
        infected_individuals.append(individuals[temp])
        individuals[temp].time_of_infection = time.time()

    infect_button = Button(window, borderwidth=3.5, text='Start Infection', command=clicker, bg='white', fg='red')
    infect_button.place(x=100, y=735)

    def infect_others(k):
        if not individuals[k].deceased:
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
                        ind.can_infect = True
                        infected_individuals.append(ind)

    finish = True
    while finish:
        global num_dec
        for i in range(0, len(individuals)):
            individuals[i].move_individual_communities()
            if individuals[i].infected:
                if (quarantine and time.time() - individuals[i].time_of_infection) >= 2 and individuals[i].quarantined == False:
                    individuals[i].quarantine()
                if (time.time() - individuals[i].time_of_infection) >= 5:
                    canvas.itemconfig(individuals[i].image, fill="grey")
                    canvas.itemconfig(individuals[i].radius_image, outline="")
                    num_dec += 1
                    individuals[i].deceased = True
                    individuals[i].can_infect = False
                    individuals[i].infected = False
                if individuals[i].infected:
                    individuals[i].radius_animation()
                if not individuals[i].quarantined and not individuals[i].deceased:
                    infect_others(i)

        if num_infec == 50:
            global start
            start = time.time()
        window.update()
    print(num_sus)
    print(num_infec)
    tk.mainloop()


simulator()

