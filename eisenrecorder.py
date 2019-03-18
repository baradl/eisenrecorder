import user_interaction as ui
import helper as he
import print_fancy, delete_pycache

print_fancy

delete_pycache
#run_test


print("\n")
print("Eisenrecorder started".center(79))
#print("\n")

while True:
    ui.menu.user_start()
    print(he.indent())
    dec2 = input("Back to main menu [y/n]: ")
    if dec2 != "y":
        print("\n\n")
        print("Closing Eisenrecorder".center(79))
        print("\n\n")
        break


    
