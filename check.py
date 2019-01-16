import helper as he

def check_days(col_name, db):
    days = he.get_days(col_name, db)
    [multi,missing] = check_int_list(days)
    mistakes = [multi, missing]
    return mistakes
        
        
def check_int_list(int_list):
    int_list.sort()
    n = len(int_list)
    missing = []
    multi   = []
    for i in range(1,n):
        if int_list[i] == int_list[i-1]:
            multi.append(int_list[i])
        if int_list[i] != int_list[i-1] + 1:
            for j in range(int_list[i-1] + 1, int_list[i]):
                missing.append(j)
    return [multi, missing]