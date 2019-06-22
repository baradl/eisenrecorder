import filter
import connect
import converter as conv
import calculations as calc
from tabulate import tabulate
from termcolor import colored
from helper import indexes_max

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
            headers = ["Date", "Workload", "Volume", "Max Weight", "1RM"]
        
    content = []
    total_reps = []
    volume = []
    onerm = []
    
    for ex, day in zip(ex_list, days):
        data = [conv.convert_int_todate(day)]
        
        
        assert len(ex) == 4 or len(ex) == 3
        
        
        if len(ex) == 4:
            setsreps = str(ex[1]) + "x" + str(ex[2]) + "x" + str(ex[3])
            total_reps.append(ex[1]*ex[2])
            if "BW" == ex[3]: bw_ = True
            else: bw_ = False
            
        else:
            setsreps = " "
            for rep,weight in zip(ex[1], ex[2]):
                setsreps += str(rep) + "x" + str(weight) + ", "
            setsreps = setsreps[:-2]
            total_reps.append(sum(ex[1]))
            if "BW" in ex[2]: bw_ = True
            else: bw_ = False
        
            
        data.append(setsreps)
        
        
        
        if not bw:
            if not bw_:
                volume.append(calc.vol(ex))
                data.append(str(volume[-1]))
             
                reps_max = calc.reps_max_weight(ex)
                weight_max = calc.max_w(ex)
                data.append(str(reps_max)+ "x" + str(weight_max))
            else:
                data.append("-")
                data.append("-")
                volume.append(0)
            try: 
                onerm.append(calc.estimate_onerm(reps_max, weight_max))
                data.append(str(onerm[-1]))
            except: 
                data.append("-")  
                onerm.append(0)                                                                       
        else:
            data.append(str(total_reps[-1]))
            
        content.append(data)
    
    if bw:
        index_reps = indexes_max(total_reps)
        content = color_content(content = content, index_reps = index_reps)
    else:
        index_volume = indexes_max(volume)
        index_onerm = indexes_max(onerm)
        content = color_content(content = content, index_volume = index_volume,
                                index_onerm = index_onerm)
    
    
    print(tabulate(content, headers))
    
    
    
def color_content(content, index_reps = [], index_volume = -1, index_onerm = -1):
    text_color = "grey"
    backround_color = "on_cyan"
    
    if index_reps != []:
        for index in index_reps:
            maxreps = content[index]
            maxreps[2] = colored(maxreps[2], text_color, backround_color)
        return content
    if index_volume != []:
        for index in index_volume:
            maxvolume = content[index]
            maxvolume[2] = colored(maxvolume[2], text_color, backround_color)
        
        for index in index_onerm:
            maxonerm = content[index]
            maxonerm[4] = colored(maxonerm[4], text_color, backround_color)
            
        return content
    
    

    
    
    
    
    