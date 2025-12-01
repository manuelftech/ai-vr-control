from config.config_vars import config

class AgentHistory():
    def __init__(self, tag="agent_history", role="user", message=None):
        self.tag = tag
        self.role = role
        self.message = message

    def create_completed_response(self):
        return [{"Tag": self.tag, "Role": self.role, "Content": self.message}, config.CHAT_GENERIC_FULFILLED_MESSAGE]