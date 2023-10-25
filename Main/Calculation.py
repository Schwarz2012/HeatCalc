from scipy.optimize import fsolve
from numpy import full
import Operations as oper #Additional operations and equations
import Classes_list as Classes #Classes list for walls, oppenings and radiant surfaces
from View_factor_calculation import VF_wall_ceiling as VFWC #View factor calculations analytic equations
from View_factor_calculation import VF_wall_floor as VFWF #View factor calculations analytic equations
from View_factor_calculation import VF_wall_wall as VFWW #View factor calculations analytic equations
from View_factor_calculation import VF_wall_op_wall as VFWoW #View factor calculations analytic equations
from View_factor_calculation import VF_floor_ceiling as VFFC #View factor calculations analytic equations
from View_factor_convertation import VF_ceiling_to_walls_result as VFWCr #Result convertation of view factors from ceiling to walls
from View_factor_convertation import VF_floor_to_walls_result as VFWFr #Result convertation of view factors from floor to walls
from View_factor_convertation import VF_walls_to_walls_result as VFWWr #Result convertation of view factors from floor to walls
from View_factor_convertation import VF_walls_to_openings_result as VFWOpr
from Equation_configurate import Wall_equations as weq
from Equation_configurate import Variables_list as vl
from Equation_configurate import Floor_equation as feq
from Equation_configurate import Ceiling_equation as ceq
from Equation_configurate import Heat_balance_equation as hbeq
from Equation_configurate import Openings_equations as opeq
from Results import TempResults as Tres
from Results import QResults as Qres
from Results import LossResults as Lres
from Results import TempInit as TIres

from time import time




def calculation(self, results):
    # Geometry and phys parametres of structures, radiant surfaces and oppenings
    start = time()

    geomunits = self.unit_box.currentText()
    if geomunits == 'm':
        correct = 1
    elif geomunits == 'cm':
        correct = 0.01
    elif geomunits == 'mm':
        correct = 0.001
    tempunits = self.temp_box.currentText()
    if tempunits == 'K':
        tempcorrect = 273.15
    else:
        tempcorrect = 0



    #Initial data
    Tout = {}
    for key in self.construct_list:
        Tout[key] = float(results[key]['Tout']) - tempcorrect
    RL = float(results['Room']['RL']) * correct
    RW = float(results['Room']['RW']) * correct
    RH = float(results['Room']['RH']) * correct
    wall_name_list = ['Wall 1', 'Wall 2', 'Wall 3', 'Wall 4']
    alpha = {}
    if ('Adsource' in results['Room'].keys()) == False:
        CV = False
        alpha = {'Ceiling': 0, 'Floor': 0, 'Wall 1': 0, 'Wall 2': 0, 'Wall 3': 0, 'Wall 4': 0}
        insource = 0 #W
    else:
        CV = True
        for name in self.construct_list:
            alpha[name] = 1/float(results[name]['alpha'])
            insource = float(results['Room']['Adsource']) #W

    #Objects initiation from classes_list
    #region
    #Ceiling
    ceiling = Classes.Ceiling(results, correct, tempcorrect)
    #Ceiling RS objects
    ceilingRS = []
    for num in results['Ceiling']['RS']:
        ceilingRS.append(Classes.CeilingRS(results, num, correct, tempcorrect))
    #Floor
    floor = Classes.Floor(results, correct, tempcorrect)
    #Floor RS objects
    floorRS = []
    for num in results['Floor']['RS']:
        floorRS.append(Classes.FloorRS(results, num, correct, tempcorrect))
    #Walls
    wall = []
    for wall_name in wall_name_list:
        if (int(wall_name[-1]))%2 == 0: 
            wall.append(Classes.Walls(results, wall_name, RL, correct, tempcorrect))
        else:
            wall.append(Classes.Walls(results, wall_name, RW, correct, tempcorrect))
    #Walls RS objects
    wallRS = [[], [], [], []]
    for wall_name in wall_name_list:
        for num in results[wall_name]['RS']:
            if (int(wall_name[-1]))%2 == 0: 
                wallRS[int(wall_name[-1])-1].append(Classes.WallRS(results, wall_name, num, RL, correct, tempcorrect))
            else:
                wallRS[int(wall_name[-1])-1].append(Classes.WallRS(results, wall_name, num, RW, correct, tempcorrect)) 
    #Walls Op objects
    wallOp = [[], [], [], []]
    for wall_name in wall_name_list:
        for num in results[wall_name]['door']:
            if (int(wall_name[-1]))%2 == 0: 
                wallOp[int(wall_name[-1])-1].append(Classes.WallOp(results, wall_name, num, RL, correct, tempcorrect))
            else:
                wallOp[int(wall_name[-1])-1].append(Classes.WallOp(results, wall_name, num, RW, correct, tempcorrect)) 
    #endregion

    #View factors calculation
    #region
    #Walls to Walls
    wtw = {} 
    for j in range(1,5,1):
        for i in range(1, 5, 1):
            if i == j:
                continue
            elif abs(i-j) == 2:
                wtw[str(j) + str(i)] = VFWoW.WalltoOpWall(j, i, wall, wallRS, wallOp, RW, RL)
            else:
                wtw[str(j) + str(i)] = VFWW.WalltoWall(j, i, wall, wallRS, wallOp)
    #Ceiling to Wall 1,2,3,4
    ctw = {} 
    for i in range(1,5,1):
        ctw ['c' + str(i)] = VFWC.WalltoCeiling(i, wall, wallRS, wallOp, ceiling, ceilingRS)
    #Floor to Wall 1,2,3,4
    ftw = {} 
    for i in range(1,5,1):
        ftw ['f' + str(i)] = VFWF.WalltoFloor(i, wall, wallRS, wallOp, floor, floorRS)
    #Ceiling to Floor
    cf = VFFC.FloortoCeiling(ceiling, ceilingRS, floor, floorRS, RH)
    #endregion

    #View factors result convertation 
    #region 
    #Ceiling to floor
    cfr = {}
    #Ceiling area to floor area
    cfr['FCF'] = (cf['FCF'] - sum(cf['FCFRS']) ) - (sum(cf['FCRSF'])  - oper.merge(cf['FCRSFRS']))
    #Ceiling RS to floor
    cfr['FCRSF'] = sum(cf['FCRSF']) - oper.merge(cf['FCRSFRS'])
    #Floor RS to ceiling
    cfr['FCFRS'] = sum(cf['FCFRS']) - oper.merge(cf['FCRSFRS'])
    #Ceiling to walls
    ctwr = {}
    for i in range(1,5,1):
        ctwr['c' + str(i)] = VFWCr.ceilingtowall(i, ctw)
    #Floor to walls
    ftwr = {}
    for i in range(1,5,1):
        ftwr['f' + str(i)] = VFWFr.floortowall(i, ftw)
    ##Walls to walls
    wtwr = {}
    for i in range(1,5,1):
        for j in range(1,5,1):
            if i == j:
                continue
            else:
                wtwr[str(i) + str(j)] = VFWWr.walltowall(i, j, wallRS, wallOp, wtw)
    #Walls to Op
    wtor = {}
    for i in range(1,5,1):
        for j in range(1,5,1):
            if i == j:
                continue
            else:
                wtor[str(i) + str(j)] = VFWOpr.walltoopening(i, j, wallOp, wallRS, wtw)
    #print(wtwr)
    #endregion


    #Equation configurer
    #region
    #var = vl.variables(wallOp)
    Eq = []
    #Heat Balance equation
    Eq.append(hbeq.heatbaleq(ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, insource, alpha))
    #Wall equations
    for i in range(1,5,1):
        Eq.append(weq.walleq(i, ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, ctwr, ftwr, wtwr, wtor, alpha))
    #Floor equation
    Eq.append(feq.flooreq(ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, cfr, ftwr, alpha))
    #Ceiling equation
    Eq.append(ceq.ceilingeq(ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, cfr, ctwr, alpha)) 
    #Windows equations
    for i in range(1,5,1):
        for j in range(len(wallOp[i-1])):
            Eq.append(opeq.openingeq(i, j+1, ceiling, ceilingRS, floor, floorRS, wall, wallRS, wallOp, ctwr, ftwr, wtor, alpha))
    #endregion

    #Equations system formulation
    #region

    def eqsys(x):
        v = oper.varnum(vl.variables(wallOp))
        Eqc = Eq.copy()
        for j in range(len(Eqc)):
            for i in range(len(v)):
                Eqc[j] = Eqc[j].subs(v[i],x[i])
        return(Eqc)
    #endregion

    #Calculation
    #region
    sol = []
    x = full((len(oper.varnum(vl.variables(wallOp)))), 263)
    sol = fsolve(eqsys,x)

    #endregion

    #Results
    #region
    Results = {}
    Results['Temperatures'] = Tres.results(sol, ceilingRS, floorRS, wallRS, wallOp, ceiling, floor, wall, CV)
    Results['TemperaturesOut'] = TIres.results(Tout, wallOp, ceiling, ceilingRS, floor, floorRS, wall, wallRS)
    Results['Heat'] = Qres.results(sol, ceilingRS, floorRS, wallRS, wallOp, cfr, ctwr, ftwr, wtwr, wtor, ceiling, floor, wall, insource, alpha, CV)
    Results['Losses'] = Lres.results(sol, ceilingRS, floorRS, wallRS, wallOp, ceiling, floor, wall)
    Results['Solution time'] = str(round(time() - start, 3))
    return Results
    ##endregion
