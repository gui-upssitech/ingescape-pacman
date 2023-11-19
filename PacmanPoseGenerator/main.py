import ingescape as igs
import sys, uuid, keyboard, time

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

# manual control of pacman function
def manual_control():
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
     if sender_agent_name == WHITEBOARD and service_name == "elements":
        waiting_for_elements = False
        print(arguments)
        ids = arguments[0]
        poses = arguments[1]
        

igs.service_init("elements", elements, None)
igs.service_arg_add("elements", "jsonArray", igs.STRING_T)

# automatic controle of pacman function
def auto_control():
    print("\n \n ##### Pacman is taking control #####")

    igs.service_call("elements", WHITEBOARD, (), None)
    while waiting_for_elements:
        time.sleep(0.1)

    pacman_id = get_pacman_id()
    
    nearest_pose = None

    for i in range(len(ids)):
        if ids[i] == pacman_id:
            pacman_pose = poses[i]
            break
    
    for pose in range(len(poses)):
        if pose != pacman_pose:
            if pose < nearest_pose:
                nearest_pose = pose
    
    agent_state["pose"] = nearest_pose
    print(agent_state["pose"])
    igs.output_set_string("pose", str(agent_state["pose"][0])+":"+str(agent_state["pose"][1]))


# program main_loop
def run_whiteboard():
    manual_control()


# program launch
igs.start_with_device("WLAN 2", 5670)

input()
igs.stop()