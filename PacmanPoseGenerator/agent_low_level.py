import ingescape as igs
import sys

class LowLevelPacmanPoseGenerator:

    def __init__(self):
        self.pose = None
        self._agent_list = []

        # igs agent setup
        igs.agent_set_name("PacmanPoseGenerator")
        igs.definition_set_version("1.0")
        igs.log_set_console(True)
        igs.log_set_file(True, None)
        igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

        # igs io
        igs.output_create("pose", igs.STRING_T, None)

        # igs agent observe
        igs.observe_agent_events(self.on_agent_event, None)

    # igs io handlers
    # =========================================================================

    def set_pose(self, x, y):
        self.pose = str(x)+":"+str(y)
        igs.output_set_string("pose", self.pose)

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