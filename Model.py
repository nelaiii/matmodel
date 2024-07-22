def find_cost(aircraft, parachutist):
    maxheight = parachutist.get_max_height()
    ##print(maxheight)
    cost = aircraft.dictCostForHeight[maxheight]
    ##print(cost)
    for i in parachutist.dictParPerHeight:
        cost = cost + parachutist.dictParPerHeight[i] * aircraft.dictCostForPar[i]
    return cost


def split_par(aircraft, parachutist, day, i):
    currPar = 0

    copyDict = dict(sorted(parachutist.dictParPerHeight.items())).copy()  # улетели
    parachutist.dictParPerHeight = dict.fromkeys(parachutist.dictParPerHeight, 0)  # остались
    parachutist.totalParachutist = 0
    for height in copyDict:
        while (copyDict[height] != 0) and (currPar != aircraft.maxPar):
            currPar = currPar + 1
            copyDict[height] = copyDict[height] - 1
            parachutist.dictParPerHeight[height] = parachutist.dictParPerHeight[height] + 1
            parachutist.totalParachutist = parachutist.totalParachutist + 1
    day.insert(i, ParachutistPerHeight())
    day[i].dictParPerHeight = copyDict
    # print("CopyDict", copyDict)
    # print("parachutist.dictParPerHeight", parachutist.dictParPerHeight)
    day[i].totalParachutist = sum(day[i].dictParPerHeight.values())


class Aircraft:

    def __init__(self, name, maxPar):
        self.name = name
        self.dictCostForHeight = {}
        self.dictCostForPar = {}
        self.maxPar = maxPar
        self.timeout = 0

    def add_cost_for_height(self, cost, height):
        self.dictCostForHeight[height] = cost

    def add_cost_for_par(self, cost, height):
        self.dictCostForPar[height] = cost


class ParachutistPerHeight:
    def __init__(self):
        self.dictParPerHeight = {}
        self.totalParachutist = 0

    def set_par(self, height, number):
        self.dictParPerHeight[height] = number
        self.totalParachutist = sum(self.dictParPerHeight.values())

    def get_max_height(self):
        return max(k for k, v in self.dictParPerHeight.items() if v != 0)


class Schedule:
    def __init__(self):
        self.schedule = []

    def add_to_schedule(self, sortie):
        self.schedule.append(sortie)

    def insert_to_schedule(self, i, sortie):
        self.schedule.insert(i, sortie)


class Airpark:
    def __init__(self):
        self.airparkList = []

    def add_to_airpark(self, aircraft):
        self.airparkList.append(aircraft)


class MathematicalConditions:

    def __init__(self, parachutists, places):
        self.parachutists = parachutists  # кол-во парашютистов, которым необходимо подняться
        self.places = places  # кол-во пассажирских мест в самолете
        self.counter = 0

    def possibility_of_jumping(self):
        if self.places > 0 and self.parachutists > 0:
            if self.parachutists <= self.places:
                self.counter += 1
                # return True
            else:
                self.counter = self.counter
                # return False
        else:
            return False
