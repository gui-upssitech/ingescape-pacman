import ingescape as igs
import sys, uuid, time, random
from src.ingescape_utils import wait_for_agent
# variables and state
WHITEBOARD = "Whiteboard"

shapes = ["ellipse", "triangle", "rectangle"]
colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "black", "white"]

agent_state = {
    "whiteboard_exists": False
}

# igs agent definition
igs.agent_set_name("ItemGenerator")
igs.definition_set_version("1.0")
igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

def on_whiteboard_available():
    agent_state["whiteboard_exists"] = True
    generate()

def on_whiteboard_unavailable():
    agent_state["whiteboard_exists"] = False

wait_for_agent(WHITEBOARD, on_whiteboard_available, on_whiteboard_unavailable)

# main function
def generate():
    while (True):
        form = random.choice(shapes)
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        width = random.randint(10, 50)
        height = random.randint(10, 50)
        fill = random.choice(colors)
        stroke = random.choice(colors)
        strokeWidth = random.randint(1, 5)
        igs.service_call(WHITEBOARD, "addShape", [form, x, y, width, height, fill, stroke, strokeWidth])
        time.sleep(5)

# igs main loop
igs.run()

# program launch
igs.start_with_device("WLAN 2", 5670)
input()
igs.stop()