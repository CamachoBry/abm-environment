from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import Fox, Bunny, GrassPatch
from schedule import RandomActivationByBreed

class Environment(Model):
    '''
    Our bunny-fox environment which we will use for the Ranger
    '''
    height = 20
    width = 20

    initial_bunny = 100
    initial_fox = 50

    bunny_reproduce = 0.06
    fox_reproduce = 0.04

    fox_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    bunny_gain_from_food = 4

    verbose = True

    def __init__(self, height=20, width=20, initial_bunny=100, initial_fox=50, 
                                            bunny_reproduce=0.06, fox_reproduce=0.04,
                                            bunny_gain_from_food=4, fox_gain_from_food=20,
                                            grass=False, grass_regrowth_time=30):
        super().__init__()

        #Set parameters
        self.height = height
        self.width = width
        self.initial_bunny = initial_bunny
        self.initial_fox = initial_fox
        self.bunny_reproduce = bunny_reproduce
        self.fox_reproduce = fox_reproduce
        self.fox_gain_from_food = fox_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.bunny_gain_from_food = bunny_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector({"Fox": lambda x: x.schedule.get_breed_count(Fox),
                                            "Bunny": lambda x: x.schedule.get_breed_count(Bunny)})

        
        #Create bunny
        for i in range(self.initial_bunny):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.bunny_gain_from_food)
            bunny = Bunny(self.next_id(),(x,y), self, True, energy)
            self.grid.place_agent(bunny, (x,y))
            self.schedule.add(bunny)

        #Create foxes
        for i in range(self.initial_fox):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.fox_gain_from_food)
            foxlet = Fox(self.next_id(),(x,y), self, True, energy)
            self.grid.place_agent(foxlet, (x,y))
            self.schedule.add(foxlet)

        #Create the patches of grass
        if self.grass:
            for agent, x, y, in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x,y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x,y))
                self.schedule.add(patch)

            self.running = True
            self.datacollector.collect(self)

    def step(self):
        self.schedule.step()

        #Collect data on every step taken in the environment
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Fox),
                   self.schedule.get_breed_count(Bunny)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number foxes: ',
                  self.schedule.get_breed_count(Fox))
            print('Initial number bunnies: ',
                  self.schedule.get_breed_count(Bunny))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number foxes: ',
                  self.schedule.get_breed_count(Fox))
            print('Final number bunnies: ',
                  self.schedule.get_breed_count(Bunny))

        

