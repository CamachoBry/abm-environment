from mesa import Agent

class RandomWalk(Agent):
    '''
    Class implementing random walk methods.
    '''

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        '''
        Step one cell in any direction
        '''
        #Picks the next cell from the adjacent cells
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore,True)
        next_move = self.random.choice(next_moves)

        #Now move from random decision
        self.model.grid.move_agent(self, next_move)