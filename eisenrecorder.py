import user_interaction as ui
import helper as he
import print_fancy


print_fancy

#run_test


print("\n")
print("Eisenrecorder started".center(79))
#print("\n")

while True:
    ui.menu.user_start()
    print(he.indent())
    dec2 = input("Back to main menu: ")
    if dec2 != "yes":
        print("\n\n")
        print("Closing Eisenrecorder".center(79))
        print("\n\n")
        break


    
