import filter
import connect
import converter as conv
import calculations as calc
from tabulate import tabulate

DB = connect.connect_to_client()
BW_EXERCISES = ["KZ", "Toe-Up", "Role-Out"]

def exercise_summary(db, exercise):
    ex_list, days = filter.filter_exercise(db, exercise)
    global BW_EXERCISES
    
    for ex in BW_EXERCISES:
        if ex in exercise:
            bw = True
            headers = ["Date", "Workload", "Total Reps"]
            break
        else: 
            bw = False
            headers = ["Date", "Workload", "Volume", "Max Weight", "Estimated 1RM"]
        
    content = []
    
    for ex, day in zip(ex_list, days):
        data = [conv.convert_int_todate(day)]
        
        
        assert len(ex) == 4 or len(ex) == 3
        
        
        if len(ex) == 4:
            setsreps = str(ex[1]) + "x" + str(ex[2]) + "x" + str(ex[3])
            total_reps = ex[1]*ex[2]
            if "BW" == ex[3]: bw_ = True
            else: bw_ = False
            
        else:
            setsreps = " "
            for rep,weight in zip(ex[1], ex[2]):
                setsreps += str(rep) + "x" + str(weight) + ", "
            setsreps = setsreps[:-2]
            total_reps = sum(ex[1])
            if "BW" in ex[2]: bw_ = True
            else: bw_ = False
        
            
        data.append(setsreps)
        
        
        
        if not bw:
            if not bw_:
                data.append(str(calc.vol(ex)))
             
                reps_max = calc.reps_max_weight(ex)
                weight_max = calc.max_w(ex)
                data.append(str(reps_max)+ "x" + str(weight_max))
            else:
                data.append("-")
                data.append("-")
            try: data.append(str(calc.estimate_onerm(reps_max, weight_max)))
            except: data.append("-")                                                                         
        else:
            data.append(str(total_reps))
            
        
        
        
        content.append(data)
    
    print(tabulate(content, headers))