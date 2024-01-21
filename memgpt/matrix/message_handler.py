from memgpt import MemGPT
from threading import Thread
import uuid
from memgpt.data_types import (
    Source,
    Passage,
    Document,
    User,
    AgentState,
    LLMConfig,
    EmbeddingConfig,
    Message,
    ToolCall,
    LLMConfig,
    EmbeddingConfig,
    Message,
    ToolCall,
)

class MessageHandler(Thread):
    def __init__(self, obj):
        Thread.__init__(self)
        self.obj = obj
        self.user_id = uuid.uuid5(uuid.NAMESPACE_URL, self.obj["message"].sender)
        self.agent_id = uuid.uuid5(uuid.NAMESPACE_URL, self.obj["room"].room_id)
        self.client = MemGPT(
            user_id=self.user_id,
            auto_save=True,
            config={
                "openai_api_key": "YOUR_API_KEY"
            }
        )
        self.response = []
        print("---------------")
        print("generated agent id: " + str(self.agent_id))

    def run(self):
        # This is where you can perform operations on the passed object
        self.get_or_create_user()
        self.agent_state = self.get_or_create_agent()
        response = self.client.user_message(agent_id=self.agent_id, message=self.obj["message"].body)
        self.response = response
        return response
    def assistant_message(self) -> str:
        # Loops through the response and returns the assistant's message
        return '\n'.join([item.get('assistant_message') for item in self.response if item.get('assistant_message') is not None])
    
    def get_or_create_user(self) -> User:
        """
        Creates a new user if one does not exist, otherwise returns the existing user.
        :param user_config: user configuration dictionary.
        :return: User object.
        """
        user = getattr(self, 'user', None)
        if user is None:
            user = self.client.server.get_user(user_id= self.user_id)
        if user is None:
            user = self.client.server.create_user(user_config={
                "name": self.obj["message"].sender,
                "id": self.user_id,
                "default_preset": "batnetwork"
            })
        if getattr(self, 'user', None) is None:
            self.user = user
        return user
    
    def get_or_create_agent(self) -> AgentState:
        agent = getattr(self, 'agent_state', None)
        if agent is None:
            agent = self.client.server.get_agent(user_id= self.user_id, agent_id=self.agent_id)
        if agent is None:
            agent = self.client.server.create_agent(user_id=self.user_id, agent_config={
                "persona": "deka",
                "name": self.obj["room"].room_id,
                "id": self.agent_id
            })
        if getattr(self, 'agent_state', None) is None:
            self.agent_state = agent
        return agent