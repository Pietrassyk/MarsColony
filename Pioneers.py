#git push --set-upstream https://github.com/Pietrassyk/MarsColony master
import numpy as np
import names
import pandas as pd
import scipy.stats as stats

class Round():
    round_df = pd.DataFrame()
    def __init__(self,number):
        self.number = number
        self.accident_ticker = 0
        self.died_of_age_ticker = 0
        self.died = []
        self.new_borns = []
        self.birth_ticker = 0
        self.death_ticker = 0
        self.population_num = len(Population.colonists_list)
    def store(self):
        temp_df = pd.DataFrame(self.__dict__.values(), index = self.__dict__.keys()).T
        Round.round_df = pd.concat([Round.round_df,temp_df],axis = 0)


class Population():
    def __init__(self):
        Round.round_df = pd.DataFrame()
        Population.eternity_list = []
        Population.colonists_list = []
        Population.graveyard_list = []
        Population.females_list = []
        Population.males_list = []
        Population.round_ticker = 0
        Population.rounds_list = []

        Population.mortality_rate = 0.002
        Population.age_expectation = 70
        Population.num_interactions = 9
        Population.max_children = 8
        Population.min_rep_age = 15
        Population.max_reg_age = 45
        print("Population created")
        self.lost = 0
        self.new_round()

    def fertility(self,age):
        pass

    def new_round(self):
        if self.lost >1:
            print(f"Colony lost in Round: {Population.round_ticker}")
            return False
        Population.rounds_list.append(Round(Population.round_ticker))
        for person in Population.colonists_list:
            person.stay_alive()
        for person in Population.females_list:
            person.interact()
        Population.rounds_list[-1].store()
        if len(Population.colonists_list) == 0:
            self.lost += 1
        Population.round_ticker += 1
        return True

    def plot_history(self):
        pass

class Pioneer():
    home = "Earth"
    def __init__(self, name = None, parents = [] , birthyear = 0 ,sex = None):
        self.ID = len(Population.colonists_list) + len(Population.graveyard_list)
        self.name = name
        self.birthyear = birthyear
        if sex:
            self.sex = sex
        else:
            self.sex = np.random.choice(["m", "f"])

        if self.sex == "f":
            Female(name, parents=parents, birthyear=birthyear)
        if self.sex == "m":
            Male(name, parents=parents, birthyear=birthyear)

    def __repr__(self):
        return f"ID: {self.ID}, Name: {self.name} , Sex: {self.sex} , Age: {self.get_age()}"

    def create_name(self):
        if self.sex == "f":
            name = names.get_first_name(gender='female')
        else:
            name = names.get_first_name(gender='male')
        try:
            surname = self.parents[1].name.split(" ")[1]
            #print("Named after Father")
        except:
            #print("I am from Earth, so i will give me a Mars Name")
            surname = names.get_last_name()
        return name+" "+surname

    def beborn(self, name = None, parents = [] , birthyear = 0):
        self.parents = parents  # [0] = mother , [1] = father
        if name:
            self.name = name.title()
        else:
            self.name = self.create_name().title()
        # self.ancestors = []
        self.children = []
        self.siblings = []
        # self.ancestors.append(self.parents)
        if birthyear:
            self.birthyear = birthyear
        else:
            self.birthyear = Population.round_ticker
        self.ID = len(Population.colonists_list) + len(Population.graveyard_list)
        Population.rounds_list[-1].new_borns.append(self.name)
        Population.rounds_list[-1].birth_ticker += 1

        #### New
        #if self.sex == "f":
            #print("It's a girl")
        #if self.sex == "m":
            #print("It's a boy")
        #print(f"Hello World, I am: {self}")
        #print(f"My Parents are : {self.parents}")
        #print("::::::::::::::::::::::::::::::::::::::::")

    def stay_alive(self):
        survive = 1
        cur_age = self.get_age()
        if cur_age == Population.min_rep_age:
            #print(f"Sweet Fourteen {self}")
            #if self.sex == "f":
                #print(self.get_possible_partners())
            pass
        if cur_age > Population.age_expectation:
            if np.random.binomial(1, 0.25):
                #print("Died of Age")
                survive = 0
                Population.rounds_list[-1].died_of_age_ticker += 1
        elif np.random.binomial(1,Population.mortality_rate):
            print("Died by Accident")
            survive = 0
            Population.rounds_list[-1].accident_ticker += 1
        if survive == 0:
            self.die()


    def die(self):
        round = Population.round_ticker
        Population.graveyard_list.append((Population.colonists_list.pop(Population.colonists_list.index(self)),round))#
        if self.sex == "m":
            Population.males_list.pop(Population.males_list.index(self))
        else:
            Population.females_list.pop(Population.females_list.index(self))
        Population.rounds_list[-1].died.append(self.name)
        Population.rounds_list[-1].death_ticker += 1
        #print(f"{self} died in round {round} at age {self.get_age()}, it's a sad day' ")
        #print("")


    def get_grand_parents(self):
        grand_parents = []
        if len(self.parents)<2:
            return []
        for parent in self.parents:
            grand_parents += parent.parents
        return grand_parents

    def get_uncles(self):
        uncles = []
        if len(self.parents)<2:
            return []
        for parent in self.parents:
            uncles += parent.siblings
        return uncles

    def get_relation(self,person,verbose = False):
        if person in self.parents:
            return [1,"parent"][verbose]
        if person in self.children:
            return [1,"child"][verbose]
        if len(set(self.parents).intersection(set(person.parents))) == 2:
            return [2, "sibling"][verbose]
        if len(set(self.parents).intersection(set(person.parents)))==1:
            return [1.5, "half-sibling"][verbose]
        if person in self.get_grand_parents():
            if person.sex == "m":
                return [2,"granddad"][verbose]
            else:
                return [2,"grandma"][verbose]
        if person in self.get_uncles():
            if person.sex == "m":
                return [3,"uncle"][verbose]
            else:
                return [3,"aunt"][verbose]
        if bool(set(person.get_uncles()) & set(self.parents)):
            return [4,"cousin"][verbose]
        else:
            return [99,"unrelated"][verbose]

    def get_age(self):
        return Population.round_ticker-self.birthyear


class Female(Pioneer):
    def __init__(self, name = "unnamed colonist", parents = [None,None], birthyear = 0):
        self.sex = "f"
        self.pregnant = False
        self.beborn(name, parents, birthyear)
        Population.eternity_list.append(self)
        Population.colonists_list.append(self)
        Population.females_list.append(self)



    def intercourse(self,partner):
        age = self.get_age()
        if partner.sex == "f":
            print("wrong sex")
            pass
        if self.get_relation(partner) <=4:
            print(f"gross {self.ID}, its your relative")
            pass
        elif self.pregnant == True:
            #print(f"{self.name} you're already pregnant")
            pass
        elif np.random.binomial(1,stats.norm.pdf(age,30,15)):
                self.pregnant = True
                self.last_fertile_intercourse = partner
                #print(f"{self.name} got pregnant")
        else:
            #print(f"{self.name} sorry not this time")
            pass

    def give_birth(self):
        Pioneer(parents=[self,self.last_fertile_intercourse])
        offspring = Population.colonists_list[-1]
        offspring.siblings += self.children
        for child in self.children:
            child.siblings.append(offspring)
        self.children.append(offspring)
        self.last_fertile_intercourse.children.append(offspring)
        self.pregnant = False

    def get_possible_partners(self):
        # age span

        age_min = self.get_age()/2+7
        if self.get_age()<Population.min_rep_age:
            age_max = -99
        else:
            age_max = (self.get_age() - 7) * 2
        #print(f"min:{age_min}")
        #print(f"max:{age_max}")
        self.possible_partners = list(filter(lambda person: self.get_relation(person)>4 and (age_min <= person.get_age()<=age_max),Population.males_list))
        return self.possible_partners


    def interact(self):
        num_interactions = Population.num_interactions
        inter = 0
        pos_partners = self.get_possible_partners()
        if self.pregnant == False:
            if len(self.children) >=Population.max_children:
                return None
            if pos_partners:
                while inter < num_interactions:
                    person = np.random.choice(pos_partners,1)
                    #print(f"interaction with {person}")
                    self.intercourse(person[0])
                    inter += 1
        elif self.pregnant:
            self.give_birth()
        pass



class Male(Pioneer):
    def __init__(self, name = None, parents=[None, None], birthyear=0):
        self.sex = "m"
        self.beborn(name, parents, birthyear)
        Population.colonists_list.append(self)
        Population.eternity_list.append(self)
        Population.males_list.append(self)
