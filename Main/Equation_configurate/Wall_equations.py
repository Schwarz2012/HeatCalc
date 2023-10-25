import Operations as oper #Additional operations and equations
from Equation_configurate import Variables_list as vl
#Const
sig = 5.67*10**(-8)


def walleq(wallnum, ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, ctwr, ftwr, wtwr, wtor, alpha):
    wn = str(wallnum)
    #Variables seting
    var = vl.variables(wallOp)
    #Equation configuration
    eq = 0
    #Wall to wall
    for i in range(1,5,1):
        if i == wallnum:
            continue
        else:
            eq += (sig * wtwr[wn + str(i)]['FW' + wn + 'W' + str(i)]*(var['Twi' + str(i)]**4 - var['Twi' + wn]**4))/(oper.eps(wall[i-1].eps, wall[wallnum-1].eps))
    #Ceiling RS to wall
    if len(ceilingRS) != 0:
        eq += (sig * ctwr['c' + wn]['FCRSW'] *(ceilingRS[0].TRS**4 - var['Twi' + wn]**4))/(oper.eps(ceilingRS[0].eps, wall[wallnum-1].eps))
    #Ceiling to wall
    eq += (sig * ctwr['c' + wn]['FCW'] *(var['Tci']**4 - var['Twi' + wn]**4))/(oper.eps(ceiling.eps, wall[wallnum-1].eps))
    #Floor RS to wall
    if len(floorRS) != 0:
        eq += (sig * ftwr['f' + wn]['FFRSW'] *(floorRS[0].TRS**4 - var['Twi' + wn]**4))/(oper.eps(floorRS[0].eps, wall[wallnum-1].eps))
    #Floor to wall
    eq += (sig * ftwr['f' + wn]['FFW'] *(var['Tfi']**4 - var['Twi' + wn]**4))/(oper.eps(floor.eps, wall[wallnum-1].eps))
    #Wall RS to wall
    for i in range(1,5,1):
        if i == wallnum:
            continue
        else:
            if len(wallRS[i-1]) != 0:
                eq += (sig * wtwr[wn + str(i)]['FW' + wn +'W' + str(i) + 'RS'] *(wallRS[i-1][0].__dict__['TRS']**4 - var['Twi' + wn]**4))/(oper.eps(wallRS[i-1][0].eps, wall[wallnum-1].eps))
    #Wall Op to wall
    for i in range(1,5,1):
        if i != wallnum:
            for j in range(len(wallOp[i-1])):
                eq += (sig * wtor[wn + str(i)]['FW' + wn + 'W' + str(i) +'Op'+str(j+1)]*(var['TwOpi'][str(i)+str(j+1)]**4 - var['Twi' + wn]**4))/(oper.eps(wallOp[i-1][j].eps, wall[wallnum-1].eps))
    #Looses equation
    eq += wall[wallnum-1].U * oper.area(wallnum, wall, wallRS, wallOp) * (wall[wallnum-1].Tex - var['Twi' + wn])

    eq += alpha['Wall ' + wn] * oper.area(wallnum, wall, wallRS, wallOp) * (var['Tra'] - var['Twi' + wn])

    return(eq)

