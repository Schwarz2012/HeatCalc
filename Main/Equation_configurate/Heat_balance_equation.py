from Equation_configurate import Variables_list as vl
import Operations as oper #Additional operations and equations

#Const
sig = 5.67*10**(-8)

def heatbaleq(ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, insource, alpha):
    #Variables seting
    var = vl.variables(wallOp)
    #Equation configuration
    eq = 0
    #Floor
    #Floor RS to ceiling
    #if len(floorRS) != 0:
    #    eq += (sig * cfr['FCFRS'] *(floorRS[0].TRS**4 - var['Tci']**4))/(oper.eps(floorRS[0].eps, ceiling.eps))
    ##Floor RS to wall
    #if len(floorRS) != 0:
    #    for i in range(1,5,1):
    #        eq += (sig * ftwr['f' + str(i)]['FFRSW'] *(floorRS[0].TRS**4 - var['Twi' + str(i)]**4))/(oper.eps(floorRS[0].eps, wall[i-1].eps))
    # #Floor RS to opening
    #if len(floorRS) != 0:
    #    for i in range(1,5,1):
    #        if len(wallOp[i-1]) != 0:
    #            for opnum in range(len(wallOp[i-1])):
    #                on = str(opnum+1)
    #                eq += (sig * ftwr['f' + str(i)]['FFRSWOp'][opnum] * (floorRS[0].TRS**4 - var['TwOpi'][str(i) + on]**4))/(oper.eps(floorRS[0].eps, wallOp[i-1][opnum].eps))   
    ##Ceiling
    ##Ceiling RS to floor
    #if len(ceilingRS) != 0:
    #    eq += (sig * cfr['FCRSF'] *(ceilingRS[0].TRS**4 - var['Tfi']**4))/(oper.eps(ceilingRS[0].eps, floor.eps))
    ##Ceiling RS to walls
    #if len(ceilingRS) != 0:
    #    for i in range(1,5,1):
    #        eq += (sig * ctwr['c' + str(i)]['FCRSW'] *(ceilingRS[0].TRS**4 - var['Twi' + str(i)]**4))/(oper.eps(ceilingRS[0].eps, wall[i-1].eps))
    # #Ceiling RS to opening
    #if len(ceilingRS) != 0:
    #    for i in range(1,5,1):
    #        if len(wallOp[i-1]) != 0:
    #            for opnum in range(len(wallOp[i-1])):
    #                on = str(opnum+1)
    #                eq += (sig * ctwr['c' + str(i)]['FCRSWOp'][opnum] * (ceilingRS[0].TRS**4 - var['TwOpi'][str(i) + on]**4))/(oper.eps(ceilingRS[0].eps, wallOp[i-1][opnum].eps)) 
    ##Walls
    ##Wall RS to walls
    #for j in range(1,5,1):
    #    for i in range(1,5,1):
    #        if i == j:
    #            continue
    #        else:
    #            if len(wallRS[i-1]) != 0:
    #                eq += (sig * wtwr[str(j) + str(i)]['FW' + str(j) +'W' + str(i) + 'RS'] *(wallRS[i-1][0].TRS**4 - var['Twi' + str(j)]**4))/(oper.eps(wallRS[i-1][0].eps, wall[j-1].eps))
    ##Wall RS to ceiling
    #for i in range(1,5,1):        
    #    if len(wallRS[i-1]) != 0:
    #        eq += (sig * ctwr['c' + str(i)]['FCWRS'] *(wallRS[i-1][0].TRS**4 - var['Tci']**4))/(oper.eps(wallRS[i-1][0].eps, ceiling.eps))
    ##Wall RS to floor
    #for i in range(1,5,1):        
    #    if len(wallRS[i-1]) != 0:
    #        eq += (sig * ftwr['f' + str(i)]['FFWRS'] *(wallRS[i-1][0].TRS**4 - var['Tfi']**4))/(oper.eps(wallRS[i-1][0].eps, floor.eps))
    ##Wall RS to wall Op
    #for i in range(1,5,1):
    #    for j in range(1,5,1):
    #        if i == j:
    #            continue
    #        else:
    #            if len(wallRS[i-1]) != 0:
    #                if len(wallOp[j-1]) != 0:
    #                    for opnum in range(len(wallOp[j-1])):
    #                        on =str(opnum+1)
    #                        eq += (sig * wtor[str(i) + str(j)]['FW' + str(i) +'RSW' + str(j) + 'Op' + on] *(wallRS[i-1][0].TRS**4 - var['TwOpi'][str(j) + on]**4))/(oper.eps(wallRS[i-1][0].eps, wallOp[j-1][opnum].eps))
    
                            
    #Convection
    #RSs
    #Floor
    if len(floorRS) != 0:
        eq += alpha['Floor'] * oper.parsum(floorRS, 'area') * (floorRS[0].TRS - var['Tra'])
    #Ceiling
    if len(ceilingRS) != 0:
        eq += alpha['Ceiling'] * oper.parsum(ceilingRS, 'area') * (ceilingRS[0].TRS - var['Tra'])
    #Walls
    for i in range(1,5,1):
        if len(wallRS[i-1]) != 0:
            eq += alpha['Wall ' + str(i)] * oper.parsum(wallRS[i-1], 'area') * (wallRS[i-1][0].TRS - var['Tra'])
    #Constructions
    #Floor
    eq += alpha['Floor'] * oper.areacf(floor, floorRS) * (var['Tfi'] - var['Tra'])
    #Ceiling
    eq += alpha['Ceiling'] * oper.areacf(ceiling, ceilingRS) * (var['Tci'] - var['Tra'])
    #Walls
    for i in range(1,5,1):
        eq += alpha['Wall ' + str(i)] * oper.area(i, wall, wallRS, wallOp) * (var['Twi' + str(i)] - var['Tra'])
    #Openings
    for i in range(1,5,1):
        if len(wallOp[i-1]) != 0:
            for opnum in range(len(wallOp[i-1])):
                eq += alpha['Wall ' + str(i)] * wallOp[i-1][opnum].area * (var['TwOpi'][str(i) + str(opnum+1)] - var['Tra'])
            

    ##Looses
    ##Floor
    #eq += floor.U * oper.areacf(floor, floorRS) * (floor.Tex - var['Tfi'])
    ##Ceiling
    #eq += ceiling.U * oper.areacf(ceiling, ceilingRS) * (ceiling.Tex - var['Tci'])
    ##Walls
    #for i in range(1,5,1):
    #    eq += wall[i-1].U * oper.area(i, wall, wallRS, wallOp) * (wall[i-1].Tex - var['Twi' + str(i)])
    
    ##Openings
    #for i in range(1,5,1):
    #    if len(wallOp[i-1]) != 0:
    #        for opnum in range(len(wallOp[i-1])):               
    #            eq += wallOp[i-1][opnum].U * wallOp[i-1][opnum].area * (wallOp[i-1][opnum].Tex - var['TwOpi'][str(i) + str(opnum+1)])
    #Inner source
    eq += insource



    return(eq)