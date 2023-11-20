import ingescape as igs
import sys, uuid
import base64 as b64
from os import path
from gif_frames import load_frames, to_b64

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


# igs io pose
def on_new_dir(iop_type, input_name, value_type, value, data):
    speed = 10
    dx, dy = tuple(map(float, value.split(":")))
    x, y = agent_state["pose"]
    agent_state["pose"] = (x + dx * speed, y + dy * speed)
    print(f"new pose : {agent_state['pose']}")
    draw_pacman(*agent_state["pose"])

igs.input_create("pose", igs.STRING_T, None)
igs.observe_input("pose", on_new_dir, None)



# igs io whiteboard_title
def set_title(title):
    igs.output_set_string("whiteboard_title", title)

igs.output_create("whiteboard_title", igs.STRING_T, None)



#igs check if whiteboard exists
def on_agent_event(type, uuid, name, event_data, my_data):
    if type == igs.AGENT_ENTERED:
        my_data["agent_list"].append(name)
        if name == WHITEBOARD:
            my_data["whiteboard_exists"] = True
            run_whiteboard()
    elif type == igs.AGENT_EXITED:
        my_data["agent_list"].remove(name)
        if name == WHITEBOARD:
            my_data["whiteboard_exists"] = False

igs.observe_agent_events(on_agent_event, agent_state)



# igs service definition
def on_element_created(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    if sender_agent_name == WHITEBOARD and service_name == "elementCreated":
        agent_state["pacman_id"] = arguments[0]

igs.service_init("elementCreated", on_element_created, None)
igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)



# draw_functions
def draw_pacman(x: float, y: float):
    if not agent_state["whiteboard_exists"]:
        return
    
    print(agent_state["pacman_id"])
    if agent_state["pacman_id"] is None:
        gif_url = "https://media.discordapp.net/attachments/1164841141502480424/1164863287847034900/PacMan.gif"

        params = (gif_url, x, y)
        igs.service_call(WHITEBOARD, "addImageFromUrl", params, None)

        # params = ("Ellipse", x, y, 50.0, 50.0, "Yellow", "Black", 2.0)
        # igs.service_call(WHITEBOARD, "addShape", params, None)
    else:
        params = (agent_state["pacman_id"], x, y)
        igs.service_call(WHITEBOARD, "moveTo", params, None)



# program main_loop
def run_whiteboard():
    set_title("Get Pacmaned !")
    draw_pacman(*agent_state["pose"])



# program launch
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <device> <port=5670>")
        exit(1)

    device = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else 5670
    igs.start_with_device(device, port)

    input()
    igs.stop()