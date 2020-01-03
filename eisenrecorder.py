from crud import insert
from utils import helper as he
from artwork import print_fancy
import connect as con
from menu.menu import user_start

print_fancy

print("\n")
print("Eisenrecorder started".center(79))

if con.check_internet():
    client = con.connect_to_client()
else:
    client = None
    print("No connection. Only Cache and Backup available.")

while True:
    user_start(client)
    print(he.indent())
    dec2 = input("Back to main menu [y/n]: ")
    if dec2 != "y":
        print("\n\n")
        print("Closing Eisenrecorder".center(79))
        print("\n\n")
        break

client.close()