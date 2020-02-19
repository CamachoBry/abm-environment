from collections import defaultdict
from mesa.time import RandomActivation


class RandomActivationByBreed(RandomActivation):
    '''
    A scheduler which activates each type of agent once per step, 
    in random order, with order reshuffled every step/
    '''
    def __init__(self, model):
        super().__init__(model)
        self.agents_by_breed = defaultdict(dict)

    def add(self, agent):
        '''
        Add an agent to the scheduler
        '''

        self._agents[agent.unique_id] = agent
        agent_class = type(agent)
        self.agents_by_breed[agent_class][agent.unique_id] = agent

    def remove(self, agent):

        '''
        Remove an agent from the scheduler
        '''

        del self._agents[agent.unique_id]

        agent_class = type(agent)
        del self.agents_by_breed[agent_class][agent.unique_id]

    def step(self, by_breed=True):
        '''
        Executes the step of each agent breed, one at a time, random order.
        '''
        if by_breed:
            for agent_class in self.agents_by_breed:
                self.step_breed(agent_class)
            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_breed(self, breed):
            '''
            Shuffle order and run all agents of a given breed.
            Args:
                breed: Class object of the breed to run.
            '''
            agent_keys = list(self.agents_by_breed[breed].keys())
            self.model.random.shuffle(agent_keys)
            for agent_key in agent_keys:
                self.agents_by_breed[breed][agent_key].step()



    def get_breed_count(self, breed_class):
        return len(self.agents_by_breed[breed_class].values())