from datetime import datetime
from tabulate import tabulate
import converter
import check


def month_now():
    return datetime.now().month

def year_now():
    return datetime.now().year

        

def days_in_month(month, leap = False):
    if type(month) == str:
        if len(month) <= 2: month = converter.convert_to_month(int(month))
    elif type(month) == int: month = converter.convert_to_month(month)
    
    months = ["January", "February", "March", "April","May", "June", "July",
              "August", "September", "October", "Novemver", "December"]
    days_in_months = [31,28,31,30,31,30,31,31,30,31,30,31]
    if leap: days_in_months[1] = 29
    
    index = months.index(month)
    return days_in_months[index]
    
def indent(): 
    return "_______________________________________________________________________________\n"



def string_to_list(string, sep = ","):
    list_ = string.split(sep)
    for i in range(len(list_)):
        try: list_[i] = int(list_[i])
        except: list_[i] = float(list_[i])
    return list_


def check_day(day):
    if len(day) == 1: 
        day = "0" + day
        return day
    if len(day) > 2: 
        print("ATTENTION: Incorrect day format: ", day)
        print("Deleting every digit but the first two.")
        day = day[0] + day[1]
    if int(day) > 31: 
        print("Number too high for day format. Shutting down.")
        raise SystemExit
    return day

def get_days(col,*db):
    if type(col) == str: col = db(col)
    
    days = []
    for document in col.find():
        days.append(int(document["day"]))
    return days



def divide_int_list(int_list):
    n = len(int_list)
    div = [[int_list[0]]]
    j = 0
    for i in range(1,n):
        if int_list[i] == int_list[i-1]:
            div[j].append(int_list[i])
        else: 
            div.append([int_list[i]])
            j += 1
    return div


def delete_ints(int_list, to_delete, number = 1):   
    for i in range(number):
        assert to_delete in int_list
        int_list.remove(to_delete)
    

def find_substring_in_stringlist(stringlist, substring):
    result = []
    
    for string in stringlist:
        string = string.lower()
        if substring in string: result.append(string)
    
    return result


        

    
def abbreviation():
    abbrev = tabulate([['BP', "Benchpress"],
                    ["CGBP", "Closegrip-Benchpress"],
                    ["OHP","Overheadpress"],
                    ["Inc-BP(DB)", "Incline-Benchpress with Dumbells"],
                    ["FP","Face-Pulls"],
                    ["PD1","Pushdown one arm"],
                    ["M", "Machine"],
                    ["HC","Hammercurls"],
                    ['DL', "Deadlift"],
                    ["RDL","Romanian Deadlift"],
                    ["LZ", "Lat-Zug"]],
            headers=['Abbreviation', 'Exercise'])
    
    print(indent())
    print("\n")    
    print(abbrev)    
    print(indent())
   
    
    
    
    
    
    
    
    
    
    