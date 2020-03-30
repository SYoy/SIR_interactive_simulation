from mesa import Agent
from SIR_wolf_sheep.SIR.random_walk import Walker

class Susceptible(Walker):
    '''
        A Person walking randomly or randomly with visits to a center (e.g. shop)
    '''
    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)

        # movement
        self.now_in_center = False
        self.last_pos = None

        # infection
        self.infected = False
        self.steps_since_infection = 0

    def step(self):
        '''
            A model step. Move, then infect or get isolated if infected
        '''
        # virus spreading
        if self.infected and self.random.random() < self.model.probability_recognized and self.steps_since_infection > 1:
            # identified as infected
            self.steps_since_infection += 1
            self.model.to_infected(self)

        elif self.infected:
            # spread virus as uninfected
            cells = self.model.grid.get_neighborhood(self.pos, self.moore, True)
            for cell in cells:
                this_cell = self.model.grid.get_cell_list_contents([cell])
                susceptibles = [obj for obj in this_cell if isinstance(obj, Susceptible)]
                if len(susceptibles) > 0:
                    for sus in susceptibles:
                        if self.random.random() < self.model.spread_probability and not sus.infected:
                            # spread decease: set to infected - set day to 0
                            sus.infected = True
                            sus.steps_since_infection = 0

            # recovery
            if self.steps_since_infection > self.model.duration_infection:
                self.model.to_removed(self)
            else:
                self.steps_since_infection += 1

        # movement
        if self.model.movement == "random":
            self.random_move()

        elif self.model.movement == "random_center":
            if self.now_in_center:
                self.now_in_center, self.last_pos = self.move_back(self.last_pos)
            else:
                self.now_in_center, self.last_pos = self.random_move_center()

class Infectious(Walker):
    """
        A infected Person walking randomly or randomly with visits to a center (e.g. shop)
    """
    def __init__(self, unique_id, pos, model, moore, energy=None, now_in_center=False,
                 last_pos=None, infected=True, steps_since_infection=0):
        super().__init__(unique_id, pos, model, moore=moore)

        # movement
        self.now_in_center = now_in_center
        self.last_pos = last_pos

        # infection
        self.infected = infected
        self.steps_since_infection = steps_since_infection

    def step(self):
        # virus spreading
        if self.steps_since_infection > self.model.duration_infection:
            self.model.to_removed(self)
        else:
            # spread virus
            x, y = self.pos
            cells = self.model.grid.get_neighborhood(self.pos, self.moore, True)
            for cell in cells:
                this_cell = self.model.grid.get_cell_list_contents([cell])
                susceptible = [obj for obj in this_cell if isinstance(obj, Susceptible)]
                if len(susceptible) > 0:
                    for sus in susceptible:
                        if self.random.random() < self.model.spread_probability:
                            # spread decease
                            # set to infected - set day to 0
                            sus.infected = True
                            sus.steps_since_infection = 0
            self.steps_since_infection += 1

        # movement
        if self.model.movement == "random":
            self.random_move()

        elif self.model.movement == "random_center":
            if self.now_in_center:
                self.now_in_center, self.last_pos = self.move_back(self.last_pos)
            else:
                self.now_in_center, self.last_pos = self.random_move_center()


class Removed(Walker):
    """
        A removed Person.
    """
    def __init__(self, unique_id, pos, model, moore, energy=None, now_in_center=False,
                 last_pos=None):
        super().__init__(unique_id, pos, model, moore=moore)

        # movement
        self.now_in_center = now_in_center
        self.last_pos = last_pos

    def step(self):
        # movement
        if self.model.movement == "random":
            self.random_move()

        elif self.model.movement == "random_center":
            if self.now_in_center:
                self.now_in_center, self.last_pos = self.move_back(self.last_pos)
            else:
                self.now_in_center, self.last_pos = self.random_move_center()