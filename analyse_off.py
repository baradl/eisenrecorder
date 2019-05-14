from tabulate import tabulate

import converter as conv
import helper as he
import filter

def summary_off(db):
    
    off_days = filter.filter_type(db, "off")
    
    print(he.indent())
    print("Number off days:", len(off_days))
    today = he.today()
    print("Total days:", he.get_day_in_year(today))
    last_off = off_days[-1]
    print("Last off day:", conv.convert_int_todate(last_off["day"]))
    print(he.indent())
    
    content = []
    year = he.year_now()
    for month in range(1,he.month_now()+1):
        monthly_days = he.monthly_days(int(year))
        days = [sum(monthly_days[:month-1])+1,sum(monthly_days[:month])]
        
        counter_month = 0
        for session in off_days:
            if session["day"] <= days[1] and session["day"] >= days[0]:
                counter_month += 1
        
        content.append([conv.convert_to_month(month), str(counter_month)])
        #print(conv.convert_to_month(month)+ ":" ,counter_month)
    
    header = ["Month", "Off days"]
    out = tabulate(content, header)
    print(out)