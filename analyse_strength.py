import filter
import connect
import converter as conv
import calculations as calc
from tabulate import tabulate

DB = connect.connect_to_client()

def exercise_summary(db = DB, exercise):
    ex_list, days = filter.filter_exercise(db, exercise)
    
    headers = ["Date", "Workload", "Volume", "Max Weight", "Estimated 1RM"]
    content = []
    
    for ex, day in zip(ex_list, days):
        data = [conv.convert_int_todate(day)]
        
        assert len(ex) == 4 or len(ex) == 3
        
        if len(ex) == 4:
            setsreps = str(ex[1]) + "x" + str(ex[2]) + "x" + str(ex[3])
        else:
            setsreps = " "
            for rep,weight in zip(ex[1], ex[2]):
                setsreps += str(rep) + "x" + str(weight) + ", "
            setsreps = setsreps[:-2]
        
        data.append(setsreps)
        data.append(str(calc.vol(ex)))
        
        reps_max = calc.reps_max_weight(ex)
        weight_max = calc.max_w(ex)
        data.append(str(reps_max)+ "x" + str(weight_max))
        data.append(str(calc.estimate_onerm(reps_max, weight_max)))
        
        content.append(data)
    
    print(tabulate(content, headers))