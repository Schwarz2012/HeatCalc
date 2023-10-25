import Operations as oper #Additional operations and equations
from Equation_configurate import Variables_list as vl
sig = 5.67*10**(-8)


def results(sol, ceilingRS, floorRS, wallRS, wallOp, ceiling, floor, wall, CV):
    var_list = oper.varkey(vl.variables(wallOp))
    areas = {}
    var_list_correct = []
    for var in var_list:
        if ('Twi' in var) == True:
            var_list_correct.append('Wall ' + var[-1])
            areas['Wall ' + var[-1]] = oper.area(int(var[-1]), wall, wallRS, wallOp)
        elif ('Tfi' in var) == True:
            var_list_correct.append('Floor')
            areas['Floor'] = oper.areacf(floor, floorRS)
        elif ('Tci' in var) == True:
            var_list_correct.append('Ceiling')
            areas['Ceiling'] = oper.areacf(ceiling, ceilingRS)
        elif ('Op' in var) == True:
            var_list_correct.append('Wall ' + var[-4] + ' Window/Door ' + var[-1])
            areas['Wall ' + var[-4] + ' Window/Door ' + var[-1]] = wallOp[int(var[-4])-1][int(var[-1]) - 1].area
        elif ('Tra' in var) == True:
            var_list_correct.append('Average room temperature')

    sol1 = []
    for temp in sol:
        if (temp > 400) or (temp < 173):
            sol1.append('-')
        else:
            sol1.append(str(round(temp - 273.15, 1)))
    Res = dict(zip(var_list_correct, sol1))
    Res = dict(sorted(Res.items()))
    value = Res['Average room temperature']
    Res.pop('Average room temperature')
    
    if CV == False:
        T_room = 0
        areas_sum = 0
        for key in Res:
            if Res[key] != '-':
                T_room += float(Res[key])*areas[key]
            areas_sum += areas[key]
        Res['Average room temperature'] = str(round(T_room/areas_sum, 1))
    else:
        Res['Average room temperature'] = value
    return(Res)