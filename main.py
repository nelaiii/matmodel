import Model

# определение хар-к ВС №1
example1 = Model.Aircraft("АН-2", 10)
example1.add_cost_for_height(400, 1000)
example1.add_cost_for_height(1000, 2000)

example1.add_cost_for_par(10, 1000)
example1.add_cost_for_par(20, 2000)

# определение хар-к ВС №2
example2 = Model.Aircraft("АН-28", 17)
example2.add_cost_for_height(600, 1000)
example2.add_cost_for_height(1100, 2000)

example2.add_cost_for_par(10, 1000)
example2.add_cost_for_par(20, 2000)

# определение хар-к ВС №3
example3 = Model.Aircraft("Л-420", 12)
example3.add_cost_for_height(300, 1000)
example3.add_cost_for_height(1000, 2000)

example3.add_cost_for_par(10, 1000)
example3.add_cost_for_par(15, 2000)

# определение кол-во парашютистов на нужную высоту
clientExample0 = Model.ParachutistPerHeight()
clientExample0.set_par(1000, 9)
clientExample0.set_par(2000, 4)

# определение кол-во парашютистов на нужную высоту
clientExample1 = Model.ParachutistPerHeight()
clientExample1.set_par(1000, 0)
clientExample1.set_par(2000, 4)

# определение кол-во парашютистов на нужную высоту
clientExample2 = Model.ParachutistPerHeight()
clientExample2.set_par(1000, 3)
clientExample2.set_par(2000, 0)

# определение кол-во парашютистов на нужную высоту
clientExample3 = Model.ParachutistPerHeight()
clientExample3.set_par(1000, 10)
clientExample3.set_par(2000, 15)

# определение максимальной высоты подъема

# maxheight = clientExample0.get_max_height()
# print(maxheight)

# costForHeight1 = example1.dictCostForHeight[maxheight]
# costForHeight2 = example2.dictCostForHeight[maxheight]

# cost1 = 0

# определение стоимости
# print(Model.find_cost(example1, clientExample0))

# print(Model.find_cost(example2, clientExample0))
################################################
day = Model.Schedule()
day.add_to_schedule(clientExample0)
day.add_to_schedule(clientExample1)
day.add_to_schedule(clientExample2)
day.add_to_schedule(clientExample3)

airpark = Model.Airpark()
airpark.add_to_airpark(example1)
airpark.add_to_airpark(example2)
airpark.add_to_airpark(example3)

# print(day.schedule[0].dictParPerHeight)
# maxheight = day.schedule[0].get_max_height()
TBF = 10
TOF = 15 + TBF
TBMF = 0
noSorties = 0
aircraftNumber = 0
totalNoSorties = len(day.schedule)
print("Всего запланированных вылетов: ", totalNoSorties)
totalNoAircraft = len(airpark.airparkList)
print("Всего ВС на аэродроме: ", totalNoAircraft)
print("Пример работы:")
timeStep = 20
flag = 0
maxCapacity = 0

while noSorties < totalNoSorties:
    print()
    noAircrafts = 0
    maxheight2 = day.schedule[noSorties].get_max_height()
    print("Максимальная высота:", maxheight2)
    minCost = -1
    print(day.schedule[noSorties].dictParPerHeight)
    while noAircrafts < totalNoAircraft:

        if airpark.airparkList[noAircrafts].timeout != 0:
            print(airpark.airparkList[noAircrafts].name, "не готов к взлету")
            noAircrafts = noAircrafts + 1
            continue

        if day.schedule[noSorties].totalParachutist > airpark.airparkList[noAircrafts].maxPar:
            print("Все", day.schedule[noSorties].totalParachutist, "не помещаются в",
                  airpark.airparkList[noAircrafts].name)
            noAircrafts = noAircrafts + 1
            flag = 1
            if airpark.airparkList[noAircrafts - 1].maxPar > maxCapacity:
                maxCapacity = airpark.airparkList[noAircrafts - 1].maxPar
            if noAircrafts >= totalNoAircraft and flag != 0 and minCost == -1:
                noAircrafts = 0
                print("Не вмещаются в один самолет")
                flag = 2
            else:
                continue

        if flag == 2:
            Model.split_par(airpark.airparkList[noAircrafts], day.schedule[noSorties], day.schedule, noSorties)
            totalNoSorties = totalNoSorties + 1
            # print("totalNoSorties:", totalNoSorties)
            # print(day.schedule[noSorties].dictParPerHeight)
            flag = 0
            continue

        currentCost = Model.find_cost(airpark.airparkList[noAircrafts], day.schedule[noSorties])

        if minCost == -1:
            minCost = currentCost
            aircraftNumber = noAircrafts

        print(airpark.airparkList[noAircrafts].name, ": ", currentCost)

        if minCost > currentCost:
            minCost = currentCost
            aircraftNumber = noAircrafts

        noAircrafts = noAircrafts + 1

    print("Самый дешевый - ", airpark.airparkList[aircraftNumber].name, ": ", minCost)
    airpark.airparkList[aircraftNumber].timeout = TOF + TBMF
    print(airpark.airparkList[aircraftNumber].timeout)

    for index in range(len(airpark.airparkList)):
        if airpark.airparkList[index].timeout != 0:
            airpark.airparkList[index].timeout = airpark.airparkList[index].timeout - timeStep
            if airpark.airparkList[index].timeout < 0:
                airpark.airparkList[index].timeout = 0

    noSorties = noSorties + 1
