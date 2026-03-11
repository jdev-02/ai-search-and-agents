from time import sleep

import random
import copy
import collections
from collections.abc import Callable
import numbers

class Thing:
    """This represents any physical object that can appear in an Environment.
    You subclass Thing to get the things you want. Each thing can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        """Things that are 'alive' should return true."""
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        """Display the agent's internal state. Subclasses should override."""
        print("I don't know how to show_state.")

    def display(self, canvas, x, y, width, height):
        """Display an image of this Thing on the canvas."""
        # Do we need this?
        pass


class Agent(Thing):
    """An Agent is a subclass of Thing with one required instance attribute 
    (aka slot), .program, which should hold a function that takes one argument,
    the percept, and returns an action. (What counts as a percept or action 
    will depend on the specific environment in which the agent exists.)
    Note that 'program' is a slot, not a method. If it were a method, then the
    program could 'cheat' and look at aspects of the agent. It's not supposed
    to do that: the program can only look at the percepts. An agent program
    that needs a model of the world (and of the agent itself) will have to
    build and maintain its own model. There is an optional slot, .performance,
    which is a number giving the performance measure of the agent in its
    environment."""

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None or not isinstance(program, collections.abc.Callable):
            print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))

        self.program = program

    def can_grab(self, thing):
        """Return True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False
    
    
#------------------------------------------------------------------------------    
    
    
#loc_A, loc_B = (0, 0), (1, 0)  # The two locations for the Vacuum world
loc_A, loc_B, loc_C, loc_D, loc_E = 0, 1, 2, 3, 4

def RandomAgentProgram(actions):
    """An agent that chooses an action at random, ignoring all percepts.
    """
    return lambda percept: random.choice(actions)

def FiveRoomRandomAgent():
    '''random agent program that randomly chooses from actions up, down, left, suck,right noop'''
    return Agent(RandomAgentProgram(['Left','Right','Up','Down','Suck','NoOp']))

def RandomVacuumAgent():
    """Randomly choose one of the actions from the vacuum environment.
    >>> agent = RandomVacuumAgent()
    >>> environment = TrivialVacuumEnvironment()
    >>> environment.add_thing(agent)
    >>> environment.run()
    >>> environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """
    return Agent(RandomAgentProgram(['Right', 'Left', 'Suck', 'NoOp']))


def TableDrivenVacuumAgent():
    """Tabular approach towards vacuum world as mentioned in [Figure 2.3]
    >>> agent = TableDrivenVacuumAgent()
    >>> environment = TrivialVacuumEnvironment()
    >>> environment.add_thing(agent)
    >>> environment.run()
    >>> environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """
    table = {((loc_A, 'Clean'),): 'Right',
             ((loc_A, 'Dirty'),): 'Suck',
             ((loc_B, 'Clean'),): 'Left',
             ((loc_B, 'Dirty'),): 'Suck',
             ((loc_A, 'Dirty'), (loc_A, 'Clean')): 'Right',
             ((loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean')): 'Left',
             ((loc_A, 'Dirty'), (loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck'}
    return Agent(TableDrivenAgentProgram(table))

def FiveRoomReflexAgent():
    '''
    table = {((loc_A, 'Clean',)): 'Right',
             ((loc_A, 'Dirty'),): 'Suck',
             ((loc_B, 'Clean'),): 'Move_Random(A,C,D,E)',
             ((loc_B, 'Dirty'),): 'Suck',
             ((loc_C, 'Clean'),): 'Left',
             ((loc_C, 'Dirty'),): 'Suck',
             ((loc_D, 'Clean'),): 'Down',
             ((loc_D, 'Dirty'),): 'Suck',
             ((loc_E, 'Clean'),): 'Up',
             ((loc_E, 'Dirty'),): 'Suck'}
    '''
    def program(percept):
        location, status = percept
        if status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Move_Random(A,C,D,E)'
        elif location == loc_C:
            return 'Left'
        elif location == loc_D:
            return 'Down'
        elif location == loc_E:
            return 'Up' 
    
    return Agent(program)
        
def ReflexVacuumAgent():
    """
    [Figure 2.8]
    A reflex agent for the two-state vacuum environment.
    >>> agent = ReflexVacuumAgent()
    >>> environment = TrivialVacuumEnvironment()
    >>> environment.add_thing(agent)
    >>> environment.run()
    >>> environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """

    def program(percept):
        location, status = percept
        if status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'

    return Agent(program)

def FiveRoomModelBasedAgent():
    model = {loc_A: None, loc_B: None, loc_C: None, loc_D: None, loc_E: None}

    def program(percept):
        location, status = percept
        model[location] = status
        if model[loc_A] == model[loc_B] == model[loc_C] == model[loc_D] == model[loc_E] == 'Clean':
            return 'NoOp'
        elif status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Move_Random(A,C,D,E)'
        elif location == loc_C:
            return 'Left'
        elif location == loc_D:
            return 'Down'
        elif location == loc_E:
            return 'Up' 
    return Agent(program)


def ModelBasedVacuumAgent():
    """An agent that keeps track of what locations are clean or dirty.
    >>> agent = ModelBasedVacuumAgent()
    >>> environment = TrivialVacuumEnvironment()
    >>> environment.add_thing(agent)
    >>> environment.run()
    >>> environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """
    model = {loc_A: None, loc_B: None}

    def program(percept):
        """Same as ReflexVacuumAgent, except if everything is clean, do NoOp."""
        location, status = percept
        model[location] = status  # Update the model here
        if model[loc_A] == model[loc_B] == 'Clean':
            return 'NoOp'
        elif status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'

    return Agent(program)

#---------------------------------------------------------------------

class Environment:
    """Abstract class representing an Environment. 'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        """Return the percept that the agent sees at this point. (Implement this.)"""
        raise NotImplementedError

    def execute_action(self, agent, action):
        """Change the world to reflect this action. (Implement this.)"""
        raise NotImplementedError

    def default_location(self, thing):
        """Default location to place a new thing with unspecified location."""
        return None

    def exogenous_change(self):
        """If there is spontaneous change in the world, override this."""
        pass

    def is_done(self):
        """By default, we're done when we can't find a live agent."""
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do. If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def list_things_at(self, location, tclass=Thing):
        """Return all things exactly at a given location."""
        if isinstance(location, numbers.Number):
            return [thing for thing in self.things
                    if thing.location == location and isinstance(thing, tclass)]
        return [thing for thing in self.things
                if all(x == y for x, y in zip(thing.location, location)) and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this.)"""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = location if location is not None else self.default_location(thing)
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: {} at {}".format(thing, thing.location))
            print("  from list: {}".format([(thing, thing.location) for thing in self.things]))
        if thing in self.agents:
            self.agents.remove(thing)
            
class TrivialVacuumEnvironment(Environment):
    """This environment has two locations, A and B. Each can be Dirty
    or Clean. The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""

    def __init__(self):
        super().__init__()
        #self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       #loc_B: random.choice(['Clean', 'Dirty'])}
        self.status = {loc_A: 'Dirty',
                       loc_B: 'Dirty'}

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent, TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        """Returns the agent's location, and the location status (Dirty/Clean)."""
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        if action == 'Right':
            agent.location = loc_B
            agent.performance -= 1
        elif action == 'Left':
            agent.location = loc_A
            agent.performance -= 1
        elif action == 'Suck':
            if self.status[agent.location] == 'Dirty':
                self.status[agent.location] = 'Clean'
                agent.performance += 10

            

    def default_location(self, thing):
        """Agents start in either location at random."""
        return random.choice([loc_A, loc_B])

class FiveRoomVacuumEnvironment(Environment):
    """The environment is initialized, all squares should be dirty. 
    This environment allows two new actions: up and down. 
    Performance measure that adds +10 points to the agent.performance variable
    when a "suck" action is completed, and subtracts -1 point from 
    agent.performance when the agent makes a move. """

    def __init__(self):
        super().__init__()
        #self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       #loc_B: random.choice(['Clean', 'Dirty'])}
        self.status = {loc_A: 'Dirty',
                       loc_B: 'Dirty',
                       loc_C: 'Dirty',
                       loc_D: 'Dirty',
                       loc_E: 'Dirty'}

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent, TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        """Returns the agent's location, and the location status (Dirty/Clean)."""
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        old_loc = agent.location
        new_loc = old_loc

        #handle move_random action
        if action == 'Move_Random(A,C,D,E)':
            new_loc = random.choice([loc_A,loc_C,loc_D,loc_E])
        elif action == 'NoOp':
            #do nothing, no penalty
            new_loc = old_loc

        elif action == 'Right': #account for posible right moves
            if old_loc == loc_A:
                new_loc = loc_B
            elif old_loc == loc_B:
                new_loc = loc_C
            elif old_loc == loc_C:
                new_loc = loc_C  #edge so no change
            else:
                new_loc = old_loc

        elif action == 'Left':
            if old_loc == loc_C:
                new_loc = loc_B
            elif old_loc == loc_B:
                new_loc = loc_A
            elif old_loc == loc_A:
                new_loc = loc_A  #edge
            else:
                new_loc = old_loc

        elif action == 'Up':
            if old_loc == loc_B:
                new_loc = loc_D
            elif old_loc == loc_E:
                new_loc = loc_B
            elif old_loc == loc_A:
                new_loc = old_loc
            elif old_loc == loc_C:
                new_loc = old_loc
            elif old_loc == loc_D:
                new_loc = old_loc  #edge
            else:
                new_loc = old_loc

        elif action == 'Down':
            if old_loc == loc_B:
                new_loc = loc_E
            elif old_loc == loc_D:
                new_loc = loc_B
            elif old_loc == loc_A or old_loc == loc_C or old_loc == loc_E:
                new_loc = old_loc
            else:
                new_loc = old_loc

        elif action == 'Suck':
            # Clean if dirty and reward +10
            if self.status.get(agent.location) == 'Dirty':
                self.status[agent.location] = 'Clean'
                agent.performance += 10
            # sucking does not move agent
            new_loc = old_loc

        # apply move and penalize only if location actually changed
        agent.location = new_loc
        if agent.location != old_loc:
            agent.performance -= 1 

    def default_location(self, thing):
        """Agents start in either location at random."""
        return random.choice([loc_A, loc_B,loc_C,loc_D,loc_E])
    
    
    
    
    
    
    
    
    

