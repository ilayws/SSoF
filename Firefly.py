import random
import numpy as np

flasht = 3 # Seconds of flashes
darkt = 10 # Seconds without flashes

State = {
    "DARK" : False,
    "FLASH" : True
}

class Firefly:

    def __init__(self, vision_radius, x, y, dt, sf):
        # Position
        self.x = x
        self.y = y

        # Data
        self.vr = vision_radius
        self.ngbrs = []

        # Timer
        self.state = bool(round(random.random()))
        timer = flasht if self.state else darkt
        self.t = float( random.choice(range(timer)) )
        self.init_t = self.t
        self.delta_time = dt
        self.sync_factor = sf


    # Change dark <-> flash
    def change_state(self):
        self.state = not self.state
        if self.state == State["FLASH"]:
            self.t = float( flasht )
        else:
            self.t = float( darkt )
        self.init_t = self.t

    # Receive neighbor flash
    def receive_flash(self, f):
        if self == f or self.state:
            return
        self.t -= self.t*self.sync_factor

    # Send flash to every ngbr
    def broadcast_flash(self):
        for f in self.ngbrs:
            f.receive_flash(self)

    # Called every frame
    def update(self):
        if 13 > self.t > 0:
            self.t -= self.delta_time
        else:
            self.change_state()
            if self.state == State["FLASH"]:
                self.broadcast_flash()

    # Determine neighbors
    def find_neighbors(self, fireflies):
        # p = np.array([np.array([f.x,f.y]) for f in fireflies]) # positions
        # self.ngbrs = fireflies[np.argwhere(np.hypot(self.x-p[0], self.y-p[1]))]
        for f in fireflies:
            dist = ( (self.x-f.x)**2 + (self.y-f.y)**2 )**0.5
            if dist <= self.vr:
                self.ngbrs.append(f)

#-------------------------------------------------------------------------------------------------------
