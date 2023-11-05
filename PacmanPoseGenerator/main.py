#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  PacmanPoseGenerator version 1.0
#  Created by Ingenuity i/o on 2023/11/05
#

import sys
import ingescape as igs
from agent_low_level import LowLevelPacmanPoseGenerator
import keyboard
import time

class PacmanPoseGenerator(LowLevelPacmanPoseGenerator):
        
        def __init__(self):
            super().__init__()
            self._pacman_exists = False
            self.x = 0
            self.y = 0
    
        # Main loop
        # =========================================================================
    
        def run_pacman(self):
            self.set_pose("Pacman")
    
        # Pacman detection
        # =========================================================================
    
        def on_agent_entered(self, name):
            if name == "Pacman":
                self._pacman_exists = True
                self.run_pacman()
    
        def on_agent_left(self, name):
            if name == "Pacman":
                self._pacman_exists = False


# main program

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python3 main.py network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    _, device, port = sys.argv
    port = int(port)

    running = True
    agent = PacmanPoseGenerator()
    igs.start_with_device(device, port)
    while running:
        if keyboard.is_pressed('q'):
            running = False
        else :
            if keyboard.is_pressed('UP'):
                agent.y += 1
            elif keyboard.is_pressed('DOWN'):
                agent.y -= 1
            if keyboard.is_pressed('RIGHT'):
                agent.x += 1
            elif keyboard.is_pressed('LEFT'):
                agent.x -= 1
            agent.set_pose(str(agent.x)+":"+str(agent.y))
            print(" pose generated :", agent.x, ":", agent.y)
        time.sleep(0.2)
    igs.stop()