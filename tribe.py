import random
from gatherer import Gatherer

class Tribe:
    def __init__(self, name, starting_location=(0, 0)):
        self.name = name
        self.location = starting_location
        self.food = 50
        self.wood = 20
        self.stone = 0
        self.morale = 100
        self.population = 20
        self.health = 100
        self.agents = []
        self.chieftain_memory = {}

    def add_agent(self, agent):
        self.agents.append(agent)
        agent.tribe = self
        if hasattr(agent, 'current_pos'):
            agent.current_pos = self.location

    def issue_directive(self, agent_type, command, *args):
        for agent in self.agents:
            if isinstance(agent, agent_type):
                return agent.execute(command, *args)
        return f"No {agent_type.__name__} found in tribe."

    def chieftain_prompt(self, command):
        if command.lower().startswith('send gatherers to best food'):
            if 'scout_report' in self.chieftain_memory:
                best_loc = max(self.chieftain_memory['scout_report'],
                              key=lambda loc: self.agents[0].world.resources.get(loc, {'food': 0})['food'])
                return self.issue_directive(Gatherer, "gather", best_loc)
            return "No scout reports available."
        return "Unknown command."

    def consume_resources(self):
        consumption = self.population // 2
        self.food = max(0, self.food - consumption)
        if self.food <= 0:
            self.morale -= 10
            self.health -= 5

    def apply_event(self, event):
        if isinstance(event, dict) and event.get("type") == "predator":
            self.population = max(1, self.population - event["value"])
            self.morale -= 10
            return f"Predator attack! Lost {event['value']} population."
        return None

    def status(self):
        agent_statuses = [agent.status() for agent in self.agents]
        return (f"Tribe {self.name}: Food={self.food}, Wood={self.wood}, Stone={self.stone}, "
                f"Morale={self.morale}, Population={self.population}, Health={self.health}\n"
                f"Agents: {', '.join(agent_statuses)}")

    def update_memory(self, key, value):
        self.chieftain_memory[key] = value