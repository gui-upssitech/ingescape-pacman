import ingescape as igs
import sys

class LowLevelPacmanRenderer:

    def __init__(self):
        self._agent_list = []
        self._whiteboard_title = None
        self._pose = None

        # igs agent setup
        igs.agent_set_name("PacmanRenderer")
        igs.definition_set_version("1.0")
        igs.log_set_console(True)
        igs.log_set_file(True, None)
        igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

        # igs io
        igs.input_create("pose", igs.STRING_T, None)
        igs.output_create("whiteboard_title", igs.STRING_T, None)
        igs.observe_input("pose", self.input_callback, None)

        # igs agent observe
        igs.observe_agent_events(self.on_agent_event, None)

    # igs io handlers
    # =========================================================================

    def input_callback(self, iop_type, name, value_type, value, my_data):
        if name == "pose":
            self._pose = value

    def set_whiteboard_title(self, value):
        self._whiteboard_title = value
        igs.output_set_string("whiteboard_title", value)

    # igs agent handlers
    # =========================================================================

    def on_agent_event(self, type, uuid, name, event_data, my_data):
        if type == igs.AGENT_ENTERED:
            self._agent_list.append(name)
            self.on_agent_entered(name)
        elif type == igs.AGENT_EXITED:
            self._agent_list.remove(name)
            self.on_agent_left(name)

    def on_agent_entered(self, name):
        pass

    def on_agent_left(self, name):
        pass