import random

class Scout:
    def __init__(self, world):
        self.world = world
        self.tribe = None
        self.current_pos = None
        self.exploration_timer = 0

    def execute(self, command, direction=None):
        if not self.current_pos:
            self.current_pos = self.tribe.location
        x, y = self.current_pos
        if direction:
            moves = {'north': (-1, 0), 'south': (1, 0), 'east': (0, 1), 'west': (0, -1)}
            dx, dy = moves.get(direction, (0, 0))
        else:
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        new_x = min(max(x + dx, 0), self.world.height - 1)
        new_y = min(max(y + dy, 0), self.world.width - 1)
        self.current_pos = (new_x, new_y)
        if not self.world.explored[new_x, new_y]:
            self.exploration_timer = 150  # 5 seconds at 30fps
            terrain = self.world.map[new_x, new_y]
            return f"I'm scouting a {terrain} at {self.current_pos}"
        else:
            return None

    def status(self):
        if self.current_pos:
            terrain = self.world.map[self.current_pos[0], self.current_pos[1]]
            status = f"Scout is at {terrain.title()} Tile {self.current_pos}\n"
            if self.world.explored[self.current_pos[0], self.current_pos[1]]:
                resources = self.world.resources.get(self.current_pos, {'food': 0, 'wood': 0, 'stone': 0})
                food = resources.get('food', 0)
                wood = resources.get('wood', 0)
                stone = resources.get('stone', 0)
                status += f"{food} food available {wood} wood available {stone} stone available"
            else:
                status += "Exploring tile..."
            # Check for gatherer on same tile
            gatherer_status = ""
            if self.tribe:
                for agent in self.tribe.agents:
                    if hasattr(agent, 'working_location') and agent.working_location == self.current_pos:
                        gatherer_status = f"\nGather G{agent.id} is gathering {agent.resource_type}. Backpack {sum(agent.carrying.values())}/20"
                # Also show gatherer returning to tribe if on same tile
                for agent in self.tribe.agents:
                    if hasattr(agent, 'carrying') and sum(agent.carrying.values()) > 0 and getattr(agent, 'current_pos', None) == self.current_pos and not agent.working_location:
                        gatherer_status = f"\nGather G{agent.id} returning to tribe. Backpack {sum(agent.carrying.values())}/20"
            status += gatherer_status
            return status
        else:
            return "Scout: At camp"