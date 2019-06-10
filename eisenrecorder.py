"""
File to be executed to start the Eisenrecorder.
"""

import user_interaction as ui
import helper as he
import print_fancy, delete_pycache
import connect as con

print_fancy

delete_pycache
#run_test


print("\n")
print("Eisenrecorder started".center(79))
#print("\n")

if con.check_internet():
    client = con.connect_to_client()
else:
    client = None
    print("No connection. Only Cache and Backup available.")

while True:
    ui.menu.user_start(client)
    print(he.indent())
    dec2 = input("Back to main menu [y/n]: ")
    if dec2 != "y":
        print("\n\n")
        print("Closing Eisenrecorder".center(79))
        print("\n\n")
        break


    
