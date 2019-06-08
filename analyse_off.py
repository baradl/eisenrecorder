from tabulate import tabulate

import converter as conv
import request as re
import helper as he
import check
import filter


def summary_off(db):
   
    off_days = filter.filter_type(db, "off")
    strength_days = filter.filter_filtered(db["AllSessions"].find(), "strength")
    run_days = filter.filter_type(db, "run")
    
    print(he.indent())
    
    print("Number off days:", len(off_days))
    print("Number Stength days:", len(strength_days))
    print("Number Runs:", len(run_days))
    
    today = he.today()
    print("Total days:", he.get_day_in_year(today))
    
    last_off = off_days[-1]
    last_off_day = conv.convert_int_todate(last_off["day"])
    print("Last off day:", last_off_day)
    
    days_since_off = he.get_day_in_year(today) - last_off["day"]
    print("Days since off:", days_since_off)
    
    print(he.indent())
    
    content = []
    year = he.year_now()
    for month in range(1,he.month_now()+1):
        monthly_days = he.monthly_days(int(year))
        days = [sum(monthly_days[:month-1])+1,sum(monthly_days[:month])]
        
        counter_month_off = 0
        for session in off_days:
            if session["day"] <= days[1] and session["day"] >= days[0]:
                counter_month_off += 1
        
        counter_month_strength = 0
        for session in strength_days:
            if session["day"] <= days[1] and session["day"] >= days[0]:
                counter_month_strength += 1
                
        counter_month_run = 0
        for session in run_days:
            if session["day"] <= days[1] and session["day"] >= days[0]:
                counter_month_run += 1
            
        
        content.append([conv.convert_to_month(month), str(counter_month_strength), 
                        str(counter_month_run),str(counter_month_off)])
        #print(conv.convert_to_month(month)+ ":" ,counter_month)
    
    header = ["Month", "Strength days", "Runs", "Off days"]
    out = tabulate(content, header)
    print(out)
    
    missing = get_missing(db)
    if missing != []:
        missing_dates = []
        for day in missing:
            missing_dates.append(conv.convert_int_todate(day))
        
        print("These dates are missing:", missing_dates)   
        dec = input("Fill with off days [y/n]: ")
    
        if dec == "y":
            fill_off(db, missing)

   
def fill_off(db, missing):
    for day in missing:
        #print(conv.convert_int_todate(day))
        dic = re.construct_dict_session(day, "off")
        re.insert_session(db["AllSessions"], dic)
    
       
def get_missing(db):
    today = he.today()
    today_as_int = he.get_day_in_year(today)
    
    days = he.get_days_col(db)
    for i in range(days[-1], today_as_int):
        days.append(i)
        
    [multi, missing] = check.check_int_list(days)
    return missing
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    