from mesa import Agent
from random_walk import RandomWalk


class GrassPatch(Agent):
    '''
    A patch of grass that grows at a fixed rate and is eaten by bunnies
    '''

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                #Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1

class Bunny(RandomWalk):
    '''
    Bunny walks around, reproduces and eats
    '''
    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        '''
        A model step. Move, then eat, then reproduce
        '''
        self.random_move()
        living = True

        if self.model.grass:
            #Reduce energy
            self.energy -= 1

            #If there is grass available, eat
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.bunny_gain_from_food
                grass_patch.fully_grown = False

            #Death
            if self.energy < 0:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                living = False
            
        if living and self.random.random() < self.model.bunny_reproduce:
            #Create baby bunny
            if self.model.grass:
                self.energy /= 2
            baby_bunny = Bunny(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(baby_bunny, self.pos)
            self.model.schedule.add(baby_bunny)


class Fox(RandomWalk):
    '''
    A fox that walks around, eats bunnies and reproduces
    '''
    
    energy = 0

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):

        self.random_move()
        self.energy -= 1

        #If there are bunnies present, eat one and remove from scheduler
        x,y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        bunny = [obj for obj in this_cell if isinstance(obj, Bunny)]
        
        #If more than one bunny around, randomly choose one
        if len(bunny) > 0:
            bunny_to_eat = self.random.choice(bunny)
            self.energy += self.model.fox_gain_from_food

            #Kill/remove the bunny from scheduler and grid
            self.model.grid._remove_agent(self.pos, bunny_to_eat)
            self.model.schedule.remove(bunny_to_eat)

        #If fox dies
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.fox_reproduce:
                #Create baby fox
                self.energy /= 2
                foxlet = Fox(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
                self.model.grid.place_agent(foxlet, foxlet.pos)
                self.model.schedule.add(foxlet)

