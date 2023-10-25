import Operations as oper #Additional operations and equations
from Equation_configurate import Variables_list as vl
sig = 5.67*10**(-8)


def results(sol, ceilingRS, floorRS, wallRS, wallOp, cfr, ctwr, ftwr, wtwr, wtor, ceiling, floor, wall, insource, alpha, CV):

    var_list = oper.varkey(vl.variables(wallOp))
    temp_res_list = dict(zip(var_list, sol))
    #RS power
    Res = {'RS power':{}, 'RS flux':{}, 'Conv power':{}, 'Conv flux':{}, 'Add power':{}, 'Total power':{}, 'Total flux':{}}
    #Ceiling RS
    if len(ceilingRS) != 0:
        QCRS = (sig * cfr['FCRSF'] * (ceilingRS[0].TRS**4 - temp_res_list['Tfi']**4))/(oper.eps(ceilingRS[0].eps, floor.eps))
        for i in range(1,5,1):
            QCRS += (sig * ctwr['c' + str(i)]['FCRSW'] *(ceilingRS[0].TRS**4 - temp_res_list['Twi' + str(i)]**4))/(oper.eps(ceilingRS[0].eps, wall[i-1].eps))
        for i in range(1,5,1):
            for j in range(len(wallOp[i-1])):
                QCRS += (sig * ctwr['c' + str(i)]['FCRSWOp'][j-1] * (ceilingRS[0].TRS**4 - temp_res_list['Tw' + str(i) + 'Op' + str(j+1)]**4))/(oper.eps(ceilingRS[0].eps, wallOp[i-1][j].eps))
        Res['RS power']['Ceiling'] = str(round(QCRS, 2))
        Res['RS flux']['Ceiling'] = str(round(QCRS/oper.parsum(ceilingRS, 'area'), 2))
        if CV == True:
            Res['Conv power']['Ceiling'] = str(round(alpha['Ceiling'] * oper.parsum(ceilingRS, 'area') * (ceilingRS[0].TRS - temp_res_list['Tra']), 2))
            Res['Conv flux']['Ceiling'] = str(round(float(Res['Conv power']['Ceiling'])/oper.parsum(ceilingRS, 'area'), 2))
        else:
            Res['Conv power']['Ceiling'] = '0'
            Res['Conv flux']['Ceiling'] = '0'
        Res['Add power']['Ceiling'] = '0'
        Res['Total power']['Ceiling'] = str(round(float(Res['RS power']['Ceiling']) + float( Res['Conv power']['Ceiling']), 2))
        Res['Total flux']['Ceiling'] = str(round(float(Res['RS flux']['Ceiling']) + float( Res['Conv flux']['Ceiling']), 2))
    else:
        Res['RS flux']['Ceiling'] = '0'
        Res['RS power']['Ceiling'] = '0'
        Res['Conv power']['Ceiling'] = '0'
        Res['Conv flux']['Ceiling'] = '0'
        Res['Add power']['Ceiling'] = '0'
        Res['Total power']['Ceiling'] = '0'
        Res['Total flux']['Ceiling'] = '0'
    #Floor RS
    if len(floorRS) != 0:
        QFRS = (sig * cfr['FCFRS'] * (floorRS[0].TRS**4 - temp_res_list['Tci']**4))/(oper.eps(floorRS[0].eps, ceiling.eps))
        for i in range(1,5,1):
            QFRS += (sig * ftwr['f' + str(i)]['FFRSW'] *(floorRS[0].TRS**4 - temp_res_list['Twi' + str(i)]**4))/(oper.eps(floorRS[0].eps, wall[i-1].eps))
        for i in range(1,5,1):
            for j in range(len(wallOp[i-1])):
                QFRS += (sig * ftwr['f' + str(i)]['FFRSWOp'][j-1] * (floorRS[0].TRS**4 - temp_res_list['Tw' + str(i) + 'Op' + str(j+1)]**4))/(oper.eps(floorRS[0].eps, wallOp[i-1][j].eps))
        Res['RS power']['Floor'] = str(round(QFRS, 2))
        Res['RS flux']['Floor'] = str(round(QFRS/oper.parsum(floorRS, 'area'), 2))
        if CV == True:
            Res['Conv power']['Floor'] = str(round(alpha['Floor'] * oper.parsum(floorRS, 'area') * (floorRS[0].TRS - temp_res_list['Tra']), 2))
            Res['Conv flux']['Floor'] = str(round(float(Res['Conv power']['Floor'])/oper.parsum(floorRS, 'area'), 2))
        else:
            Res['Conv power']['Floor'] = '0'
            Res['Conv flux']['Floor'] = '0'
        Res['Add power']['Floor'] = '0'
        Res['Total power']['Floor'] = str(round(float(Res['RS power']['Floor']) + float( Res['Conv power']['Floor']), 2))
        Res['Total flux']['Floor'] = str(round(float(Res['RS flux']['Floor']) + float( Res['Conv flux']['Floor']), 2))
    else:
        Res['RS flux']['Floor'] = '0'
        Res['RS power']['Floor'] = '0'
        Res['Conv power']['Floor'] = '0'
        Res['Conv flux']['Floor'] = '0'
        Res['Add power']['Floor'] = '0'
        Res['Total power']['Floor'] = '0'
        Res['Total flux']['Floor'] = '0'
    #Walls RS
    for i in range(1,5,1):       
        if len(wallRS[i-1]) != 0:
            QWRS = 0
            for wallnum in range(1,5,1):
                wn = str(wallnum)
                if wallnum != i:
                    QWRS += (sig * wtwr[wn + str(i)]['FW' + wn +'W' + str(i) + 'RS'] *(wallRS[i-1][0].TRS**4 - temp_res_list['Twi' + wn]**4))/(oper.eps(wallRS[i-1][0].eps, wall[wallnum-1].eps))
                    if len(wallOp[wallnum-1]) != 0 :
                        for opnum in range(len(wallOp[wallnum-1])):
                            on = str(opnum+1)
                            QWRS += (sig * wtor[str(i) + wn]['FW' + str(i) +'RSW' + wn + 'Op' + on] *(wallRS[i-1][0].TRS**4 - temp_res_list['Tw' + wn + 'Op' + on]**4))/(oper.eps(wallRS[i-1][0].eps, wallOp[wallnum-1][opnum].eps))
            QWRS += (sig * ftwr['f' + str(i)]['FFWRS'] *(wallRS[i-1][0].TRS**4 - temp_res_list['Tfi']**4))/(oper.eps(wallRS[i-1][0].eps, floor.eps)) 
            QWRS += (sig * ctwr['c' + str(i)]['FCWRS'] *(wallRS[i-1][0].TRS**4 - temp_res_list['Tci']**4))/(oper.eps(wallRS[i-1][0].eps, ceiling.eps))
            Res['RS power']['Wall ' +str(i)] = str(round(QWRS, 2))
            Res['RS flux']['Wall ' +str(i)] = str(round(QWRS/oper.parsum(wallRS[i-1], 'area'), 2))
            if CV == True:
                Res['Conv power']['Wall ' +str(i)] = str(round(alpha['Wall ' + str(i)] * oper.area(i, wall, wallRS, wallOp) * (temp_res_list['Twi' + str(i)] - temp_res_list['Tra']), 2))
                Res['Conv flux']['Wall ' +str(i)] = str(round(float(Res['Conv power']['Wall ' +str(i)])/oper.parsum(wallRS[i-1], 'area'), 2))
            else:
                Res['Conv power']['Wall ' +str(i)] = '0'
                Res['Conv flux']['Wall ' +str(i)] = '0'
            Res['Add power']['Wall ' +str(i)] = '0'
            Res['Total power']['Wall ' +str(i)] = str(round(float(Res['RS power']['Wall ' +str(i)]) + float( Res['Conv power']['Wall ' +str(i)]), 2))
            Res['Total flux']['Wall ' +str(i)] = str(round(float(Res['RS flux']['Wall ' +str(i)]) + float( Res['Conv flux']['Wall ' +str(i)]), 2))
        else:
            Res['RS power']['Wall ' +str(i)] = '0'
            Res['RS flux']['Wall ' +str(i)] = '0'
            Res['Conv power']['Wall ' +str(i)] = '0'
            Res['Conv flux']['Wall ' +str(i)] = '0'
            Res['Add power']['Wall ' +str(i)] = '0'
            Res['Total power']['Wall ' +str(i)] = '0'
            Res['Total flux']['Wall ' +str(i)] = '0'
        if len(wallOp[i-1]) !=0:
            for k in range(len(wallOp[i-1])):
                Res['RS power']['Wall ' +str(i) + ' Window/Door ' + str(k+1)] = '0'
                Res['RS flux']['Wall ' +str(i) + ' Window/Door ' + str(k+1)] = '0'
                Res['Conv power']['Wall ' +str(i) + ' Window/Door ' + str(k+1)] = '0'
                Res['Conv flux']['Wall ' +str(i) + ' Window/Door ' + str(k+1)] = '0'
                Res['Add power']['Wall ' +str(i) + ' Window/Door ' + str(k+1)] = '0'
                Res['Total power']['Wall ' +str(i) + ' Window/Door ' + str(k+1)] = '0'
                Res['Total flux']['Wall ' +str(i) + ' Window/Door ' + str(k+1)] = '0'
    

 

    Res['RS flux']= dict(sorted(Res['RS flux'].items()))
    Res['RS power']= dict(sorted(Res['RS power'].items()))
    Res['Conv power']= dict(sorted(Res['Conv power'].items()))
    Res['Conv flux']= dict(sorted(Res['Conv flux'].items()))
    Res['Add power']= dict(sorted(Res['Add power'].items()))
    Res['Total power']= dict(sorted(Res['Total power'].items()))
    Res['Total flux']= dict(sorted(Res['Total flux'].items()))

    Res['RS flux']['Room'] = '0' 
    Res['RS power']['Room'] = '0' 
    Res['Conv power']['Room'] = '0'
    Res['Conv flux']['Room'] = '0'
    Res['Total flux']['Room'] = '0'
    if insource != 0:
        Res['Add power']['Room'] = str(insource)
        Res['Total power']['Room'] = Res['Add power']['Room']
    else:
        Res['Add power']['Room'] = '0'
        Res['Total power']['Room'] = '0'
    


    #Summ
    SumHF = 0
    SumHP = 0
    SumCP = 0
    SumCF = 0
    SumAP = 0
    SumTP = 0
    SumTF = 0
    for key in Res['RS flux']:
        SumHF += float(Res['RS flux'][key])
    for key in Res['RS power']:
        SumHP += float(Res['RS power'][key])
    for key in Res['Conv power']:
        SumCP += float(Res['Conv power'][key])
    for key in Res['Conv flux']:
        SumCF += float(Res['Conv flux'][key])
    for key in Res['Add power']:
        SumAP += float(Res['Add power'][key])
    for key in Res['Total power']:
        SumTP += float(Res['Total power'][key])
    for key in Res['Total flux']:
        SumTF += float(Res['Total flux'][key])


    Res['RS power']['Total'] = str(round(SumHP, 2))
    Res['RS flux']['Total'] = str(round(SumHF, 2))    
    Res['Conv power']['Total'] = str(round(SumCP, 2))
    Res['Conv flux']['Total'] = str(round(SumCF, 2))
    Res['Add power']['Total'] = str(round(SumAP, 2))
    Res['Total power']['Total'] = str(round(SumTP, 2))
    Res['Total flux']['Total'] = str(round(SumTF, 2))
    return(Res)