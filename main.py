from threading import Thread
from time import sleep


oxygen, fuel, energy = 100, 100, 100


def sample_collection() -> None:
    global energy
    energy -= 12

    print("The collection system is running...")
    print(f"Remaining resources: \nEnergy:{energy}\n")
    sleep(1.5)


def scientific_analysis() -> None:
    global energy, oxygen
    energy -= 7
    oxygen -= 3

    print("The analysis system is running...")
    print(f"Remaining resources: \nOxygen: {oxygen}\nEnergy:{energy}\n")
    sleep(1)


def communication_with_the_earth() -> None:
    global energy, oxygen
    energy -= 5
    oxygen -= 3

    print("The communication system is running...")
    print(f"Remaining resources: \nOxygen: {oxygen}\nEnergy:{energy}\n")
    sleep(1)


def navigation() -> None:
    global fuel, energy
    fuel -= 10
    energy -= 5

    print("The navigation system is running...")
    print(f"Remaining resources: \nFuel: {fuel}\nEnergy:{energy}\n")
    sleep(2)


def main():
    while True:
        navigation_task = Thread(target=navigation)
        collection_task = Thread(target=sample_collection)
        analysis_task = Thread(target=scientific_analysis)
        communication_task = Thread(target=communication_with_the_earth)

        ship_status = [False, False, False, False]

        if energy >= 5 and fuel >= 10:
            navigation_task.start()
            ship_status[0] = True

        if energy >= 5 and oxygen >= 3:
            communication_task.start()
            ship_status[1] = True

        if energy >= 12:
            collection_task.start()
            ship_status[2] = True

        if energy >= 7 and oxygen >= 3:
            analysis_task.start()
            ship_status[3] = True

        for i in range(len(ship_status)):
            active_subsystems = 0

            if ship_status[i] == True:
                active_subsystems += 1

                match i:
                    case 0:
                        navigation_task.join()
                    case 1:
                        communication_task.join()
                    case 2:
                        collection_task.join()
                    case _:
                        analysis_task.join()

        if active_subsystems == 0:
            break


if __name__ == "__main__":
    main()
