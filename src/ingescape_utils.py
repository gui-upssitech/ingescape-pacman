import ingescape as igs

def wait_for_agent(agent_name, on_agent_entered, on_agent_exited):
    #igs check if whiteboard exists
    def on_agent_event(type, uuid, name, event_data, my_data):
        if type == igs.AGENT_ENTERED and name == agent_name:
            if on_agent_entered is not None:
                on_agent_entered()
        elif type == igs.AGENT_EXITED and name == agent_name:
            if on_agent_exited is not None: 
                on_agent_exited()

    igs.observe_agent_events(on_agent_event, None)


def parse_network_args():
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <device> <port=5670>")
        exit(1)

    device = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else 5670

    return device, port