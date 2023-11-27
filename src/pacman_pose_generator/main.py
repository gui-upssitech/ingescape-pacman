import ingescape as igs
import sys, uuid, keyboard, time
from src.ingescape_utils import wait_for_agent, parse_network_args

# variables and state
WHITEBOARD = "Whiteboard"
waiting_for_elements = True
poses = []
ids = []

agent_state = {
    "pose": (0.0, 0.0),
    "pacman_id": None,

    "agent_list": [],
    "whiteboard_exists": False,
}

# igs agent definition
igs.agent_set_name("PacmanPoseGenerator")
igs.definition_set_version("1.0")
igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

# igs io
igs.output_create("pose", igs.STRING_T, None)

#igs check if whiteboard exists
def on_whiteboard_available():
    agent_state["whiteboard_exists"] = True
    manual_control()

def on_whiteboard_unavailable():
    agent_state["whiteboard_exists"] = False

wait_for_agent(WHITEBOARD, on_whiteboard_available, on_whiteboard_unavailable)


# manual control of pacman function
def manual_control():
    if not agent_state["whiteboard_exists"]:
        print("Whiteboard not found")
        return
    
    print("##### Manual control of pacman #####")
    print("\n Press 'q' to quit, 'a' to activate auto control, arrows to move \n")
    running = True
    while running:
        agent_state["pose"] = (0, 0)
        if keyboard.is_pressed('q'):
            running = False
        if keyboard.is_pressed('a'):
            auto_control()
        else :
            if keyboard.is_pressed('UP'):
                agent_state["pose"] = (0, -1)
            elif keyboard.is_pressed('DOWN'):
                agent_state["pose"] = (0, 1)
            elif keyboard.is_pressed('LEFT'):
                agent_state["pose"] = (-1, 0)
            elif keyboard.is_pressed('RIGHT'):
                agent_state["pose"] = (1, 0)
            time.sleep(0.1)  
        print(agent_state["pose"])      
        igs.output_set_string("pose", str(agent_state["pose"][0])+":"+str(agent_state["pose"][1]))

# gets the id of our pacman
def get_pacman_id():
    # Replace this with your actual implementation
    return "dummy_pacman_id"

# igs service definition
def elements(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
     print("receiving")

     if sender_agent_name == WHITEBOARD and service_name == "getElements":
        waiting_for_elements = False

        print(arguments)
        ids = arguments[0]
        poses = arguments[1]
        
igs.service_init("elements", elements, None)
igs.service_arg_add("elements", "jsonArray", igs.STRING_T)

# automatic controle of pacman function
def auto_control():
    print("\n \n ##### Pacman is taking control #####")

    igs.service_call(WHITEBOARD, "getElements", (), None)
    print("calling_service")

    while waiting_for_elements:
        #print("waiting")
        time.sleep(0.1)

    pacman_id = get_pacman_id()
    
    nearest_pose = None

    for id in range(len(ids)):
        if ids[id] == pacman_id:
            pacman_pose = poses[id]
            break
    
    for pose in range(len(poses)):
        if pose != pacman_pose:
            if pose < nearest_pose:
                nearest_pose = pose
    
    agent_state["pose"] = nearest_pose
    print(agent_state["pose"])
    igs.output_set_string("pose", str(agent_state["pose"][0])+":"+str(agent_state["pose"][1]))


# program launch
device, port = parse_network_args()
igs.start_with_device(device, port)

input()
igs.stop()