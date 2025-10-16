import random

class Gatherer:
    _id_counter = 1
    def __init__(self, world):
        self.world = world
        self.tribe = None
        self.group_size = 5
        self.id = Gatherer._id_counter
        Gatherer._id_counter += 1
        self.working_location = None
        self.gathering_progress = 0
        self.gathering_target = 0
        self._gather_frame_counter = 0
        self.carrying = {'food': 0, 'wood': 0, 'stone': 0}
        self._store_frame_counter = 0
        self.current_pos = None
        self.returning = False
        self.storing_message_sent = False

    def execute(self, command, *args):
        if command == "gather":
            location = args[0]
            # Determine resource type by priority: food > wood > stone
            if location not in self.world.resources:
                return f"That location is out of bounds."
            if location == self.tribe.location:
                return "I can't gather at the tribe location."
            resources = self.world.resources[location]
            if resources['food'] > 0:
                resource_type = 'food'
            elif resources['wood'] > 0:
                resource_type = 'wood'
            elif resources['stone'] > 0:
                resource_type = 'stone'
            else:
                return "There are no resources available here."
            available = resources[resource_type]
            if sum(self.carrying.values()) >= 20:
                return f"My backpack is full, I need to return to the tribe to store resources."
            self.working_location = location
            self.gathering_progress = 0
            self.gathering_target = min(available, 20 - sum(self.carrying.values()))  # Only gather up to max carry
            self.resource_type = resource_type
            self._gather_frame_counter = 0
            self.storing_message_sent = False  # Reset for next storing session
            return f"I'm gathering at {location}"
        elif command == "return":
            if sum(self.carrying.values()) == 0:
                return "I have nothing to return with."
            if self.returning:
                return "I'm already heading back."
            self.current_pos = self.working_location
            self.working_location = None
            self.returning = True
            return f"I'm heading back to the tribe with {sum(self.carrying.values())} resources."

    def gather_tick(self):
        # Gathering from tile
        if self.working_location is not None:
            self._gather_frame_counter += 1
            if self._gather_frame_counter < 150:
                return None
            self._gather_frame_counter = 0
            speed = 1
            to_gather = min(speed, self.gathering_target - self.gathering_progress, 20 - sum(self.carrying.values()))
            self.carrying[self.resource_type] += to_gather
            self.world.deplete_resources(self.working_location, self.resource_type, to_gather)
            self.gathering_progress += to_gather
            if self.gathering_progress >= self.gathering_target:
                # Finished this resource, check for next
                resources = self.world.resources[self.working_location]
                next_resource = None
                for res in ['food', 'wood', 'stone']:
                    if resources[res] > 0:
                        next_resource = res
                        break
                if next_resource and sum(self.carrying.values()) < 20:
                    self.resource_type = next_resource
                    self.gathering_progress = 0
                    self.gathering_target = min(resources[next_resource], 20 - sum(self.carrying.values()))
                else:
                    # No more resources
                    if sum(self.carrying.values()) > 0:
                        # Have some resources, return to tribe to store
                        self.current_pos = self.working_location
                        self.working_location = None
                        self.returning = True
                        self.gathering_progress = 0
                        self.gathering_target = 0
                        return f"I'm heading back to the tribe with {sum(self.carrying.values())} resources."
                    else:
                        # No resources at all
                        loc = self.working_location
                        self.working_location = None
                        self.gathering_progress = 0
                        self.gathering_target = 0
                        return f"I'm idle"
            # Removed the separate full check
            return None
        # Returning to tribe
        if self.returning:
            tx, ty = self.tribe.location
            cx, cy = self.current_pos
            if cx < tx:
                cx += 1
            elif cx > tx:
                cx -= 1
            if cy < ty:
                cy += 1
            elif cy > ty:
                cy -= 1
            self.current_pos = (cx, cy)
            if self.current_pos == self.tribe.location:
                self.returning = False
            return None
        # Storing resources at tribe
        if sum(self.carrying.values()) > 0 and self.tribe.location == getattr(self, 'current_pos', None):
            self._store_frame_counter += 1
            if self._store_frame_counter < 120:
                return None
            self._store_frame_counter = 0
            
            # Send initial storing message if not sent yet
            if not self.storing_message_sent:
                self.storing_message_sent = True
                return "I've returned to the tribe to store resources"
            
            priority = ['food', 'wood', 'stone']
            for res in priority:
                if self.carrying[res] > 0:
                    self.carrying[res] -= 1
                    if res == 'food':
                        self.tribe.food += 1
                    elif res == 'wood':
                        self.tribe.wood += 1
                    elif res == 'stone':
                        self.tribe.stone += 1
                    if sum(self.carrying.values()) == 0:
                        self.returning = False
                        self.storing_message_sent = False  # Reset for next time
                        return f"I finished storing all my resources."
                    break  # Only store one resource per tick
        return None
        return None

    def status(self):
        carrying = self.carrying
        carrying_str = f"Food:{carrying['food']}, Wood:{carrying['wood']}, Stone:{carrying['stone']}"
        if self.working_location:
            return f"Gatherer G{self.id}: Gathering {self.resource_type} at {self.working_location} ({self.gathering_progress}/{self.gathering_target}), Carrying {carrying_str}"
        elif self.returning:
            return f"Gatherer G{self.id}: Returning to tribe, Carrying {carrying_str}"
        elif sum(carrying.values()) > 0:
            return f"Gatherer G{self.id}: Storing resources at tribe, Carrying {carrying_str}"
        else:
            return f"Gatherer G{self.id}: Idle"