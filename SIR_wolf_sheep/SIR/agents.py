from mesa import Agent
from SIR_wolf_sheep.SIR.random_walk import Walker

class Susceptible(Walker):
    '''
        A Person walking randomly or randomly with visits to a center (e.g. shop)
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)

        # movement
        self.energy = energy
        self.movement = "random"
        self.now_in_center = False
        self.last_pos = None

        # infection
        self.infected = False
        self.steps_since_infection = 0
        self.probability_recognized = 0.8
        self.infection_radius = 1.5 #cells
        self.spread_probability = 0.3

    def step(self):
        '''
        A model step. Move, then infect or get infected than
        '''
        if self.movement == "random":
            self.random_move()

        elif self.movement == "random_center":
            if self.now_in_center:
                self.now_in_center, self.last_pos = self.move_back(self.last_pos)
            else:
                self.now_in_center, self.last_pos = self.random_move_center()

        if self.infected and self.random.random() < self.probability_recognized and self.steps_since_infection > 1:
            # show symptons -> change class to infectious
            # methode -> check spread
            self.steps_since_infection += 1
        else:
            # spread virus
            x, y = self.pos
            cells = self.model.grid.get_neighborhood(self.pos, self.moore, True)
            for cell in cells:
                this_cell = self.model.grid.get_cell_list_contents([cell])
                susceptible = [obj for obj in this_cell if isinstance(obj, Susceptible)]
                if len(susceptible) > 0:
                    for sus in susceptible:
                        if self.random.random() < self.spread_probability:
                            # spread decease
                            # set to infected - set day to 0
                            sus.infected = True
                            sus.steps_since_infection = 0

            self.steps_since_infection += 1


class Infectious(Walker):
    """

    """
    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.model.wolf_gain_from_food

            # Kill the sheep
            self.model.grid._remove_agent(self.pos, sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf(self.model.next_id(), self.pos, self.model,
                           self.moore, self.energy)
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class Removed(Walker):
    pass


class Sheep(Walker):
    '''
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''
        self.random_move()
        living = True

        if self.model.grass:
            # Reduce energy
            self.energy -= 1

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell
                           if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.sheep_gain_from_food
                grass_patch.fully_grown = False

            # Death
            if self.energy < 0:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                living = False

        if living and self.random.random() < self.model.sheep_reproduce:
            # Create a new sheep:
            if self.model.grass:
                self.energy /= 2
            lamb = Sheep(self.model.next_id(), self.pos, self.model,
                         self.moore, self.energy)
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)


class Wolf(Walker):
    '''
    A wolf that walks around, reproduces (asexually) and eats sheep.
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.model.wolf_gain_from_food

            # Kill the sheep
            self.model.grid._remove_agent(self.pos, sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf(self.model.next_id(), self.pos, self.model,
                           self.moore, self.energy)
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)
