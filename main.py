from UserInterfaces import UI,GUI
from Services import ServiceGame
from Repositories import PlayTable
from Tests import Tests

tests = Tests()
tests.RunAllTests()

Players_Table = PlayTable()
Computers_Table = PlayTable()

Service = ServiceGame(Players_Table,Computers_Table)

User_Interface = UI(Service)
Grafic_User_Interface = GUI(Service)

while True:
    UserInterface = input("Choose an interface between UI and GUI : ")
    if UserInterface.upper() == "UI":
        User_Interface.start()
        break
    elif UserInterface.upper() == "GUI":
        Grafic_User_Interface.start()
        break
    else:
        print("choose a valid user interface")
