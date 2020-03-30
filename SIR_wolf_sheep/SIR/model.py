'''
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from SIR_wolf_sheep.SIR.agents import Susceptible, Infectious, Removed
from SIR_wolf_sheep.SIR.schedule import RandomActivationByBreed


class SIR(Model):
    '''
        SIR-Simulation
    '''

    height = 40
    width = 40

    initial_susceptible = 25
    initial_infected = 1

    probability_recognized = 0.8
    infection_radius = 1.5
    spread_probability = 0.3
    duration_infection = 10

    movement = "random"

    verbose = False  # Print-monitoring

    description = 'A model for simulating SIR'

    def __init__(self, height=height, width=width,
                 initial_susceptible=100,
                 initial_infected=50,
                 probability_recognized=0.8,
                 infection_radius=1.5,
                 spread_probability=0.3,
                 movement="random"):
        '''
        Create a new SIR model with the given parameters.

        Args:
            todo
        '''
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width

        self.initial_susceptible = initial_susceptible
        self.initial_infected = initial_infected

        self.probability_recognized = probability_recognized
        self.infection_radius = infection_radius
        self.spread_probability = spread_probability
        self.movement = movement

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        self.datacollector = DataCollector(
            {"Susceptible": lambda m: m.schedule.get_breed_count(Susceptible),
             "Infected": lambda m: m.schedule.get_breed_count(Infectious),
             "Removed": lambda m: m.schedule.get_breed_count(Removed)})

        # Create sheep:
        for i in range(self.initial_susceptible):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            susc = Susceptible(self.next_id(), (x, y), self, True, None)
            self.grid.place_agent(susc, (x, y))
            self.schedule.add(susc)

        # Create wolves
        for i in range(self.initial_infected):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            inf = Infectious(self.next_id(), (x, y), self, True, None)
            self.grid.place_agent(inf, (x, y))
            self.schedule.add(inf)

        self.running = True
        self.datacollector.collect(self)


    def to_infected(self, agent):
        pos = agent.pos
        now_in_center = agent.now_in_center
        last_pos = agent.last_pos
        infected= agent.infected
        steps_since_infection = agent.steps_since_infection

        # remove agent - todo
        self.delete_agents.append(agent)

        # create new infected agent with same attributes
        inf = Infectious(agent.unique_id, pos, self, True, None,
                         now_in_center=now_in_center,
                         last_pos=last_pos,
                         infected=infected,
                         steps_since_infection=steps_since_infection
                         )

        self.grid.place_agent(inf, pos)
        self.schedule.add(inf)

    def to_removed(self, agent):
        pos = agent.pos
        now_in_center = agent.now_in_center
        last_pos = agent.last_pos

        # remove agent
        self.delete_agents.append(agent)

        # create new infected agent with same attributes
        rem = Removed(agent.unique_id, pos, self, True, None,
                         now_in_center=now_in_center,
                         last_pos=last_pos)
        self.grid.place_agent(rem, pos)
        self.schedule.add(rem)


    def step(self):
        # Models step function
        self.delete_agents = []
        self.schedule.step()
        if len(self.delete_agents) > 0:
            for agent in self.delete_agents:
                self.schedule.remove(agent)
                self.grid.remove_agent(agent)

        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Susceptible),
                   self.schedule.get_breed_count(Infectious),
                   self.schedule.get_breed_count(Removed)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number susceptible: ',
                  self.schedule.get_breed_count(Susceptible))
            print('Initial number infected: ',
                  self.schedule.get_breed_count(Infectious))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number removed: ',
                  self.schedule.get_breed_count(Removed))
            print('Final number susceptible: ',
                  self.schedule.get_breed_count(Susceptible))
            print('Final number infected: ',
                  self.schedule.get_breed_count(Infectious))
