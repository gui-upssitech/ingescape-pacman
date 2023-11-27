import ingescape as igs
import sys, uuid
import base64 as b64
from os import path

from src.ingescape_utils import wait_for_agent, parse_network_args

# variables and state
WHITEBOARD = "Whiteboard"

agent_state = {
    "pose": (0.0, 0.0),
    "pacman_id": None,

    "agent_list": [],
    "whiteboard_exists": False,
}



# igs agent definition
igs.agent_set_name("PacmanRenderer")
igs.definition_set_version("1.0")
igs.set_command_line(sys.executable + " " + " ".join(sys.argv))



# igs io cmd_vel
def on_cmd_vel(iop_type, input_name, value_type, value, data):
    print(value)
    speed = 10
    dx, dy = tuple(map(float, value.split(":")))
    x, y = agent_state["pose"]
    agent_state["pose"] = (x + dx * speed, y + dy * speed)

    print(f"new pose : {agent_state['pose']}")
    draw_pacman(*agent_state["pose"])

def cmd_vel_callback(*args):
    print(args)

igs.input_create("cmdVel", igs.STRING_T, None)
igs.observe_input("cmdVel", lambda *args: print(args), None)



# igs io whiteboard_title
def set_title(title):
    igs.output_set_string("whiteboard_title", title)

igs.output_create("whiteboard_title", igs.STRING_T, None)



# igs service definition
def on_element_created(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    if sender_agent_name == WHITEBOARD and service_name == "elementCreated":
        agent_state["pacman_id"] = arguments[0]
        print(f"Pacman ID: {agent_state['pacman_id']}")

igs.service_init("elementCreated", on_element_created, None)
igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)



# draw_functions
def draw_pacman(x: float, y: float):
    if not agent_state["whiteboard_exists"]:
        return

    if agent_state["pacman_id"] is None:
        gif_url = "https://media.discordapp.net/attachments/1164841141502480424/1164863287847034900/PacMan.gif"

        params = (gif_url, x, y)
        igs.service_call(WHITEBOARD, "addImageFromUrl", params, None)

        # params = ("Ellipse", x, y, 50.0, 50.0, "Yellow", "Black", 2.0)
        # igs.service_call(WHITEBOARD, "addShape", params, None)
    else:
        params = (float(agent_state["pacman_id"]), x, y)
        igs.service_call(WHITEBOARD, "moveTo", params, None)



# program main_loop
def on_start():
    agent_state["whiteboard_exists"] = True

    set_title("Get Pacmaned !")
    draw_pacman(*agent_state["pose"])

def on_pause():
    agent_state["whiteboard_exists"] = False

wait_for_agent(WHITEBOARD, on_start, on_pause)


# program launch
device, port = parse_network_args()
igs.start_with_device(device, port)

input()
igs.stop()