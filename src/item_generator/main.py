import ingescape as igs
import sys, uuid, time, random
from src.ingescape_utils import wait_for_agent
# variables and state
WHITEBOARD = "Whiteboard"

shapes = ["Rectangle", "Ellipse"]
colors = ["Yellow", "Black", "Red", "Blue", "Green", "Purple", "Orange", "Pink", "Brown", "White"]

agent_state = {
    "whiteboard_exists": False,
    "running": True
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
    while agent_state["running"]:
        form = random.choice(shapes)

        x = float(random.randint(0, 600))
        y = float(random.randint(0, 450))
        width = float(random.randint(10, 50))
        height = float(random.randint(10, 50))

        fill = random.choice(colors)
        stroke = random.choice(colors)
        strokeWidth = float(random.randint(1, 8))

        params = (form, x, y, width, height, fill, stroke, strokeWidth)
        print(f"generating : {params}")
        igs.service_call(WHITEBOARD, "addShape", params, None)
        print("generated")
        time.sleep(5)


# program launch
igs.start_with_device("wlo1", 5670)
input()
agent_state["running"] = False
igs.stop()