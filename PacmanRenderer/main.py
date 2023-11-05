#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  PacmanRenderer version 1.0
#  Created by Ingenuity i/o on 2023/11/05
#

import sys
import ingescape as igs
from agent_low_level import LowLevelPacmanRenderer

class PacmanRenderer(LowLevelPacmanRenderer):
    
    def __init__(self):
        super().__init__()
        self._whiteboard_exists = False

    # Main loop
    # =========================================================================

    def run_whiteboard(self):
        self.set_whiteboard_title("Get Pacmaned !")

    # Whiteboard detection
    # =========================================================================

    def on_agent_entered(self, name):
        if name == "Whiteboard":
            self._whiteboard_exists = True
            self.run_whiteboard()

    def on_agent_left(self, name):
        if name == "Whiteboard":
            self._whiteboard_exists = False





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


    agent = PacmanRenderer()
    igs.start_with_device(device, port)
    input()
    igs.stop()

