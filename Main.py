from Firefly import Firefly
from matplotlib import pyplot as plt
import Visualize, pygame
from random import uniform, randint
import numpy as np

WIDTH = 800
HEIGHT = 600

fireflies = []
time = 0.0

# Init Parameter Values:
args = {
    "eot" : 120.0, # End of time (CHANGE TO GET A LONGER/SHORTER SIMULATION)
    "num_of_fireflies" : 1000,
    "vision_radius" : 0.4,
    "delta_time" : 0.01,
    "sync_factor" : 0.005, # Shift of time when receiving flash [factor]
    "sync" : 0.0, # Setting this value will not affect the simulation (read only)
    "max_sync" : 0.0, # (read only)
}
list_x = []
list_y = []

total_x = []
total_y = []


vis = True
save_images = False

def get_bright():
    g = lambda x: 2.25-(x-1.5)*(x-1.5)
    flash_tvals = [g(f.t) for f in fireflies if f.state]
    return sum(flash_tvals)

# Generate Fireflies
def generate_fireflies(n, vr, dt, sf):
    fs = []
    fs_append = fs.append
    for i in range(n):
        fs_append( Firefly(vr*WIDTH, uniform(0,WIDTH), uniform(0,HEIGHT), dt, sf) )
    for f in fs:
        f.find_neighbors(fs)
    return fs

# Update fireflies
def update_all():
    global args, time
    time += args["delta_time"]
    for f in fireflies:
        if vis:
            Visualize.draw(f)
        f.update()

# Wrap around 13 subtraction
def wrap_sub(a,b):
    b = np.repeat(b,a.size)
    m = np.max(np.array([a,b]), axis=0)
    n = np.min(np.array([a,b]), axis=0)
    return np.min(np.array([m-n,13-m+n]), axis=0)

# Wrap around 13 average calculation
def wrap_avg(list):
    new_list = np.abs(list-6.5)+6.5
    return np.sum(new_list)/new_list.size

# Root mean square error from sync
def rms(list):
    l = np.array(list)
    avg = wrap_avg(l)
    ms = np.sum(np.power(wrap_sub(l, avg),2))/l.size
    return np.sqrt(ms)


# Get sync of fireflies
def get_sync():
    flash_tvals = [f.t+10 for f in fireflies if f.state]
    dark_tvals = [f.t for f in fireflies if not f.state]
    value = rms(flash_tvals + dark_tvals)
    value = 1 - (value / 3.25);
    return value

# Main Loop
def loop():
    global time, args
    args["sync"] = 0.0
    args["max_sync"] = 0.0
    time = 0
    while time < args["eot"]:
        if vis:
            Visualize.update()
            if save_images:
                Visualize.save_image()
        update_all()
        args["sync"] = get_sync()
        args["max_sync"] = max(args["sync"], args["max_sync"])

# Multiple runs
def multi_loop(n, xname, yname, x):
    global fireflies
    args[xname] = x
    values = []
    value_append = values.append
    for i in range(n):
        fireflies = generate_fireflies(args["num_of_fireflies"], args["vision_radius"], args["delta_time"], args["sync_factor"])
        loop()
        value_append(args[yname])
        total_x.append(x)
    total_y.extend(values)
    list_x.append(args[xname])
    list_y.append(sum(values) / len(values))


# Plot graph
def plot(xn, yn):
    global vis, list_x, list_y
    if vis:
        Visualize.image_to_vid()
    del list_x[0]
    del list_y[0]
    print(list_y)
    plt.plot(list_x, list_y)
    plt.title("Sync vs. Vision Radius Factor [eot=" + str(args["eot"])+"]")
    plt.xlabel(xn)
    plt.ylabel(yn)
    plt.show()


# Run program
def run(xn, yn, x_values):
    if vis:
        Visualize.start(WIDTH, HEIGHT)
    args[xn] = x_values[0]
    for x in x_values:
        print(xn + " : " + str(x))
        multi_loop(1, xn, yn, x) # parameter - number of repeats
    plot(xn, yn)

run("vision_radius", "sync", [0.3])
# To generate a graph, use this x_values -> np.arange(0.1,0.35,0.01) instead of [0.3]
# You can change parameters at the top (arg dictionary)
# Running the system without displaying is also faster
