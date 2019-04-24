"""
Collection of helper functions.
"""

from datetime import datetime
from tabulate import tabulate
import converter
import check
import os, glob



###############################################################################

"""
Returns current month/year.
"""
def month_now():
    return datetime.now().month

def year_now():
    return datetime.now().year

###############################################################################

"""
Returns list of all days in each month of the year.
"""
def monthly_days(year):
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    if leap(year): days[1] = 29
    
    return days

###############################################################################
    
"""
Returns boolean value indicating if the given year is a leap year.
"""
def leap(year):
    if year % 4 == 0: return True
    else: return False

###############################################################################
    
"""
Converts date to an integer which is the number of days since 01.01.2019.
"""
def get_day_in_year(date):
    date = date.split(".")
    day = int(date[0])
    month = int(date[1])
    
    
    if len(date) == 2:
        year = str(year_now())
    else:
        year = date[2]
        if len(year) == 2:
            year = "20" + year
    
    assert len(year) == 4
    year = int(year)
    assert year >= 2019
    assert month <= 12
    days = monthly_days(year)
    assert day <= days[month-1]
    
    
    consecutive_days = 0
    year_ = 2019
    while year_ < year:
        consecutive_days += 365
        if leap(year_): consecutive_days += 1
        
        year_ += 1
    
    for i in range(month-1):
        consecutive_days += days[i]
    
    return consecutive_days + day       

###############################################################################
    
def get_week(date):
    [day, month, year] = converter.convert_date(date)
    
    month = converter.convert_to_month(month)
    month = month[:3]
    
    date_ = datetime.strptime(str(month) + " " + str(day) + " " + str(year), 
                                "%b %d %Y")
    
    weekday = date_.weekday()
    
    start = get_day_in_year(date) - weekday
    end = get_day_in_year(date) + (7 - weekday)
    
    return [start, end]


###############################################################################

"""
For a given month the number of days in it is returned.
"""

def days_in_month(month):
    if type(month) == str:
        if len(month) <= 2: month = converter.convert_to_month(int(month))
    elif type(month) == int: month = converter.convert_to_month(month)
    
    months = ["January", "February", "March", "April","May", "June", "July",
              "August", "September", "October", "Novemver", "December"]
    
    days_in_months = monthly_days()
    
    index = months.index(month)
    return days_in_months[index]

###############################################################################


"""
Seperator for output.
"""
def indent(): 
    return "_______________________________________________________________________________\n"


###############################################################################

"""
Converts string to a list. Entries in list are converted to numbers. A seperator
is given to indicate how string shall be split.
"""
def string_to_list(string, sep = ","):
    list_ = string.split(sep)
    for i in range(len(list_)):
        try: list_[i] = int(list_[i])
        except: 
            try: list_[i] = float(list_[i])
            except: list_[i] = str(list_[i])
    return list_

###############################################################################

# =============================================================================
# """
# Returns a list of days in a given collection.
# """
# def get_days_col(col,*db):
#     if type(col) == str: col = db(col)
#     
#     days = []
#     for document in col.find():
#         days.append(int(document["day"]))
#     return days
# =============================================================================

###############################################################################
    
"""
Returns a list of days in the backup repository.
"""
def get_days_dir():
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/backup"
    os.chdir(directory)
    files = glob.glob("*.txt")
    days = []
    for file in files:
        file = file.replace(".txt","")
        file = int(file)
        days.append(file)
    return days

###############################################################################
    
"""
Divides a list of integers into a list of list. Each imbedded list contains
the same integer which had to be consecutively mentioned before:
    [1,1,2,2,3,2] --> [[1,1],[2,2],[3],[2]]
"""
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

###############################################################################
    
"""
Deletes integers from an integer list.
"""
def delete_ints(int_list, to_delete, number = 1):   
    for i in range(number):
        assert to_delete in int_list
        int_list.remove(to_delete)
    
###############################################################################
        
"""
Given a list of strings it returns all entries in the list that contain a given
substring.
"""
def find_substring_in_stringlist(stringlist, substring):
    result = []
    
    for string in stringlist:
        substring = substring.lower()
        stringnew = string.lower()
        if substring in stringnew: result.append(string)
    
    return result

###############################################################################

"""
Swaps two values.
"""
def swap(x1,x2):
    xh = x1
    x1 = x2
    x2 = xh
    return [x1,x2]      

###############################################################################

"""
List of a abbreveations for exercises.
"""
def abbreviation():
    abbrev = tabulate([['BP', "Benchpress"],
                    ["CGBP", "Closegrip-Benchpress"],
                    ["OHP","Overheadpress"],
                    ["Inc-BP", "Incline-Benchpress"],
                    ["DB", "Dumbell"],
                    ["BB", "Barbell"],
                    ["FP","Face-Pulls"],
                    ["PD1","Pushdown one arm"],
                    ["PD2","Pushdown two arms"],
                    ["OH1","Overhead Tricep one arm"],
                    ["OH2","Overhead Tricep two arms"],
                    ["M", "Machine"],
                    ["HC","Hammercurls"],
                    ['DL', "Deadlift"],
                    ["RDL","Romanian Deadlift"],
                    ["LZ(b)", "Lat-Zug (breit)"],
                    ["LZ(e)", "Lat-Zug (eng)"],
                    ["KZ(e)", "Klimmzug (eng)"],
                    ["KZ(b)", "Klimmzug (breit)"]],
            headers=['Abbreviation', 'Exercise'])
    
    print(indent())
    print("\n")    
    print(abbrev)    
    print(indent())
   
    
    
    
    
    
    
    
    
    
    