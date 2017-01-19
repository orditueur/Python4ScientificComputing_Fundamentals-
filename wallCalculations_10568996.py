# In this file you are defining a module including the wallResistanceCal function
#this function receives the input information with the same format as that of assignemnt 4.
#material_library={}

materialLibrary={
    "outSideSurfaceSummer":{"RValue":0.044},
    "outSideSurfaceWinter":{"RValue":0.030},
    "insideSurface":{"RValue":0.12},
    "airSpace-13mm":{"RValue":0.16,"length-mm":13},
    "airSpace-20mm":{"RValue":0.17,"length-mm":20},
    "airSpace-40mm":{"RValue":0.16,"length-mm":40},
    "airSpace-90mm":{"RValue":0.16,"length-mm":90},
    "insulation-glassFiber-25mm":{"RValue":0.7,"length-mm":25},
    "insulation-mineralFiberBatt-25mm":{"RValue":0.66,"length-mm":25},
    "insulation-urethaneRigidFoam-25mm":{"RValue":0.98,"length-mm":25},
    "stucco-25mm":{"RValue":0.037,"length-mm":25},
    "faceBrick-100mm":{"RValue":0.075,"length-mm":100},
    "commonBrick-100mm":{"RValue":0.12,"length-mm":100},
    "steelSiding":{"RValue":0.0},
    "slag-13mm":{"RValue":0.067,"length-mm":13},
    "wood-25mm":{"RValue":0.22,"length-mm":25},
    "woodStud-90mm":{"RValue":0.63,"length-mm":90},
    "woodStud-140mm":{"RValue":0.63,"length-mm":140},
    "clayTile-100mm":{"RValue":0.18,"length-mm":100},
    "acousticTile":{"RValue":0.32},
    "asphaltShingleRoofing":{"RValue":0.077},
    "buildingPaper":{"RValue":0.011},
    "concreteBlockLightweight-100mm":{"RValue":0.27,"length-mm":100},
    "concreteBlockHeavyweight-100mm":{"RValue":0.13,"length-mm":100},
    "plaster-13mm":{"RValue":0.079,"length-mm":13},
    "woodFiberboard-13mm":{"RValue":0.23,"length-mm":13},
    "plywood-13mm":{"RValue":0.11,"length-mm":13},
    "concreteBlockLightweight-200mm":{"RValue":1.17,"length-mm":200},
    "concreteBlockHeavyweight-200mm":{"RValue":0.12,"length-mm":200},
    "cementMortar-13mm":{"RValue":0.018,"length-mm":13},
    "woodBevelLappedSiding-13x200mm":{"RValue":0.14,"length1-mm":13,"length1-mm":200},
    }
    
def wallResistanceCalc(Wall_structure,method):
    #"""documentation"""
    pass
    
    if method=="A": 
        
        #Resistance prime
        Rprime={}
        
        for i in range(0,len(Wall_structure)):
            for j in range(0,len(Wall_structure[i])):
                #Conv
                if Wall_structure[i][j]["type"]=="conv":
                    if Wall_structure[i][j].has_key("ID"):
                        if "hconv" in Wall_structure[i][j].keys():
                            hconv=Wall_structure[i][j]["hconv"]
                            Rprime[Wall_structure[i][j]["name"]] = 1/(hconv)
                        else:
                            Rprime[Wall_structure[i][j]["name"]]=materialLibrary[Wall_structure[i][j]["ID"]]["RValue"]
                    else:
                        hconv=Wall_structure[i][j]["hconv"]
                        Rprime[Wall_structure[i][j]["name"]] = 1/(hconv)
                else:#Cond
                    if "materialID" in Wall_structure[i][j].keys():
                        if Wall_structure[i][j]["materialID"] in materialLibrary.keys():
                            if "length" in Wall_structure[i][j].keys():
                                length = Wall_structure[i][j]["length"]
                                if length != "None" or length!=None:
                                    originalLength=materialLibrary[Wall_structure[i][j]["materialID"]]["length-mm"]*0.001
                                    originalR = materialLibrary[Wall_structure[i][j]["materialID"]]["RValue"]
                                    Rprime[Wall_structure[i][j]["name"]]= length/originalLength*originalR/(Wall_structure[i][j]["areaPercentage"])
                            else:
                                originalR = materialLibrary[Wall_structure[i][j]["materialID"]]["RValue"]
                                Rprime[Wall_structure[i][j]["name"]]=originalR/(Wall_structure[i][j]["areaPercentage"])
                        else:
                            print "I don't know this material"           
                    else:#use k
                        length=Wall_structure[i][j]["length"]
                        k=Wall_structure[i][j]["k"]
                        Rprime[Wall_structure[i][j]["name"]] = length/(k*Wall_structure[i][j]["areaPercentage"])
        
        
        
            
        #Resistances
        RnameSerie=[]
        RnamePar=[]
        Rserie={}
        Rpar={}
        RMidMin1=float(0)
        Rmid = float(0)            
        Rfinal = float(0)
        
        for i in range(0,len(Wall_structure)):
            if i==0: #in serie
                RnameSerie=Wall_structure[i][:]
                #Rfinal prep
                for j in range(0,len(RnameSerie)):
                    Rserie[Wall_structure[i][j]["name"]]=Rprime[Wall_structure[i][j]["name"]]
                    Rfinal = Rfinal+ Rprime.get(Wall_structure[i][j]["name"])
            
            else: #in //
                RnamePar=Wall_structure[i][:]
                for j in range(0,len(RnamePar)):
                    Rpar[Wall_structure[i][j]["name"]]=Rprime[Wall_structure[i][j]["name"]]
                    #Calcul the inverse of Rmid
                    RMidMin1=RMidMin1+1/Rprime.get(Wall_structure[i][j]["name"])
                    if RMidMin1 !=0:
                        Rmid = 1/RMidMin1
                    else:
                        print "error, divide by 0"
        #Rfinal
        Rfinal = Rfinal + Rmid
        
        Wall_calculation_output={"Rfinal":Rfinal,"Rmid":Rmid,"Rserie":Rserie,"Rparallel":Rpar}
        
    elif method=="B":
        #Resistances
        Rfinal = float(0)
        Rserie ={}
        Rpar1={}
        Rpar2={}
        RserieInt =[0,0]
        Rpar = {}
        
        for i in range(0,len(Wall_structure)):
            if i==0:
                Rserie=Rpar1
            else:
                Rserie=Rpar2
            for j in range(0,len(Wall_structure[i])):
                if Wall_structure[i][j]["type"]=="conv":#conv
                    if "ID" in Wall_structure[i][j].keys():
                        if "hconv" in Wall_structure[i][j].keys():
                            hconv=Wall_structure[i][j]["hconv"]
                            Rserie[Wall_structure[i][j]["name"]] = 1/(hconv)
                        else:
                                Rserie[Wall_structure[i][j]["name"]]=materialLibrary[Wall_structure[i][j]["ID"]]["RValue"]
                    else:
                        hconv=Wall_structure[i][j]["hconv"]
                        Rserie[Wall_structure[i][j]["name"]] = 1/(hconv)
                else:
                    if "materialID" in Wall_structure[i][j].keys():
                        if "length" in Wall_structure[i][j].keys():
                            length = Wall_structure[i][j]["length"]
                            if length != "None" or length!=None:
                                originalLength=materialLibrary[Wall_structure[i][j]["materialID"]]["length-mm"]*0.001
                                originalR = materialLibrary[Wall_structure[i][j]["materialID"]]["RValue"]
                                Rserie[Wall_structure[i][j]["name"]]= length/originalLength*originalR/(Wall_structure[i][j]["areaPercentage"])
                        else:
                            originalR = materialLibrary[Wall_structure[i][j]["materialID"]]["RValue"]
                            Rserie[Wall_structure[i][j]["name"]]=originalR/(Wall_structure[i][j]["areaPercentage"])              
                    else:#use k
                        length=Wall_structure[i][j]["length"]
                        k=Wall_structure[i][j]["k"]
                        Rserie[Wall_structure[i][j]["name"]] = length/(k*Wall_structure[i][j]["areaPercentage"])
                
                #Rfinal prep
                RserieInt[i] = RserieInt[i]+ Rserie.get(Wall_structure[i][j]["name"])
                
        Rfinal =RserieInt[1]*RserieInt[0]/(RserieInt[1]+RserieInt[0])
        Wall_calculation_output={"Rfinal":Rfinal,"Rpar1":Rpar1,"Rpar2":Rpar2,"Rserie":Rserie}
    else:
        print "I don't know this method, no calculation is done sorry!"
    
    return Wall_calculation_output