# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, './from_3b1b/active/')
from manimlib.imports import *
from sir import Person, SIRSimulation, RunSimpleSimulation

class DotPerson(Person):
    def get_body(self):
        return Dot()

class SquarePerson(Person):
    def get_body(self):
        return Square()

class MultiPopSIRSimulation(SIRSimulation):
    CONFIG = {
        "n_cities": 1,
        "city_population": 100,
        "box_size": 7,
        "population_ratios": {SquarePerson: 0.2, DotPerson: 0.8},
        "p_infection_per_day": 0.2,
        "infection_time": 5,
        "travel_rate": 0,
        "limit_social_distancing_to_infectious": False        
        }

    def add_people(self):
        people = VGroup()
        for box in self.boxes:
            dl_bound = box.get_corner(DL)
            ur_bound = box.get_corner(UR)
            box.people = VGroup()
            
            for person_type, ratio in self.population_ratios.items():
                population_size = int(ratio * self.city_population)
                for x in range(population_size):
                    person = person_type(
                        dl_bound=dl_bound,
                        ur_bound=ur_bound,
                        **self.person_config
                    )
                    person.move_to([
                        interpolate(lower, upper, random.random())
                        for lower, upper in zip(dl_bound, ur_bound)
                    ])
                    person.box = box
                    box.people.add(person)
                    people.add(person)

        # Choose a patient zero
        random.choice(people).set_status("I")
        self.add(people)
        self.people = people

class SIRDeconfSim(SIRSimulation):
    CONFIG={
        "initial_infected_ratio": 0.1,
        "initial_recovered_ratio": 0.1
        }
    
    def add_people(self):
        people = VGroup()
        for box in self.boxes:
            dl_bound = box.get_corner(DL)
            ur_bound = box.get_corner(UR)
            box.people = VGroup()
            for x in range(self.city_population):
                person = self.person_type(
                    dl_bound=dl_bound,
                    ur_bound=ur_bound,
                    **self.person_config
                )
                person.move_to([
                    interpolate(lower, upper, random.random())
                    for lower, upper in zip(dl_bound, ur_bound)
                ])
                person.box = box
                box.people.add(person)
                people.add(person)
                
                
        # CUSTOM CODE STARTS HERE
        num_infected = int(self.initial_infected_ratio * self.city_population * self.n_cities)
        num_recovered = int(self.initial_recovered_ratio * self.city_population * self.n_cities)
        special_status = random.sample(list(people), num_infected + num_recovered)
        
        infected = special_status[:num_infected]
        recovered = special_status[num_infected:]
        
        for person in infected:
            person.set_status("I")
        for person in recovered:
            person.set_status("R")
        self.add(people)
        self.people = people
        

class RunSimpleDeconfSimulation(RunSimpleSimulation):

    def add_simulation(self):
        self.simulation = MultiPopSIRSimulation(**self.simulation_config)
        self.add(self.simulation)

