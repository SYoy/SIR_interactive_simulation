'''
Generalized behavior for random walking, one grid cell at a time.
'''

from mesa import Agent


class Walker(Agent):
    '''
    Class implementing random walker methods in a generalized manner.

    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.

    '''

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)

        # Now move:
        self.model.grid.move_agent(self, next_move)

    def random_move_center(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)

        # move to center
        if self.random.random() < 0.2:
            h_center = round((self.model.grid.height - 1)/2)
            w_center = round((self.model.grid.w - 1)/ 2)
            last_pos = self.pos

            # make move
            self.model.grid.move_agent(self, (h_center, w_center))
            return True, last_pos

        # Now move:
        self.model.grid.move_agent(self, next_move)
        return False, None

    def move_back(self, last_pos):
        self.model.grid.move_agent(self, last_pos)
        return False, None