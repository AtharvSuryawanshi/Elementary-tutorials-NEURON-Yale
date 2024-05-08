COMMENT 
HH model demo mod file
This demo file is directly taken from the course MB208 IISc and all credit goes to the creators. 
----------------------
This is s demo file to learn the structure of mod files. The language is called NMODL.
In every section comments will be made like this to describe the section.
ENDCOMMENT

TITLE hh membrane demo
COMMENT
TITLE is an optional feature. It says what the mod file contains
ENDCOMMENT

COMMENT
Units:
This section helps in checking consistency of units. 
It checks with the units database in nrn library which contains all the units.
Here these units are redefined to its shorter versions like mV for millivolt 
ENDCOMMENT
UNITS{
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}

COMMENT
    Neuron:
    Here we mention the keywork which is used to call any variable within the modfile
    When a name is mentioned as a suffix, a varible in mod file is called in neuron in the format variable_name

    The current i that the mod file deals with (current passing through pas channels) are not associated with any specific ionic species.
    This is so because their ionic charge has not much of a significance here. For specific ions, USEION is used to specify the ion
    USEION is used in the format: eg- USEION na READ ena WRITE ina

    The varibles are either RANGE or GLOBAL variables. 
    RANGE is a variable whose value changes with length so different compartments can havev different values of the variable.
    GLOBAL variables have the constant every where in the section.
    GLOBAL is the default for all variables so RANGE variables have to be specifically mentioned.
    Here we mention only range varaibles that are within the control of mod file. for example v is also a range variable but independent of mod file so not decalred here.
ENDCOMMENT
NEURON{
    SUFFIX hhdemo
    USEION na READ ena WRITE ina
    USEION k READ ek WRITE ik
    NONSPECIFIC_CURRENT il
    RANGE gnabar, gkbar, gl, ena, gna, gk
    GLOBAL minf, hinf, ninf, mtau, htau, ntau
}

COMMENT
    Parameter:
    Variables whose values are defined by users come in PARAMETER block.
    Also the variables that are going to remain constant throughout the simulation
    examples are g, e, g_na, g_k, etc

    var = value (unit)  <min,max> *min max only restricts the value in gui. Within the neuron file itself the min max values have no hold.
ENDCOMMENT
PARAMETER{
    gnabar = 0.12   (S/cm2) <0,1e9>
    gkbar = 0.036   (S/cm2) <0,1e9>
    gl = 0.0003   (S/cm2) <0,1e9>
    el = -54.3  (mV)
}

COMMENT
    Assigned:
    This block contains variables that are given values not owned by the mod file and the variables that occupy the lefthandside of the equations.
    The non-owned variables are majorly 5 - v, t, celsius, diam, area
    lefthandside variables like i. These variables are RANGE by default
ENDCOMMENT
ASSIGNED{
    v   (mV)
    celsius (degC)
    ena (mV)    :The values of ena and ek could change over the course of the simulation. So, they are not included in the paramter block
    ek  (mV)
    gna (S/cm2)
    gk  (S/cm2)
    ina (mA/cm2)
    ik  (mA/cm2)
    il  (mA/cm2)
    minf    hinf   ninf
    mtau    (ms)    htau    (ms)    ntau    (ms)
}

COMMENT
    State:
    This is where we mention the variables which whose differential equations will be solved in this mmod file.
    Variables like v and i which exist outside of this mod file is not mentioned. Only the state variables exclusive to this mod file.
ENDCOMMENT
STATE{
    m h n
}

COMMENT
    Initial:
    This block contains the inital values of the state variable. 
ENDCOMMENT
INITIAL{
    rates(v)    :The initial values are to be determined by running this procedure, whichis described in the procedure block.
    m = minf
    h = hinf
    n = ninf
}

COMMENT
    Procedure:
    This block contains procedures or functions to determine the values of some paramters or constants.
    separate procedure blocks for separate procedures.
ENDCOMMENT
PROCEDURE rates(v(mV)){
    LOCAL alpha, beta, sum, q10
    q10 = 3^((celsius - 6.3)/10) :Factor which adjusts for the temperature. The model is currently for 6.3deg so chaange in temperature is accounted for by this variable
    
    :m
    alpha = 0.1*vtrap(-(v + 40),10) :vtrap function is described later
    beta = 4*exp(-(v + 65)/18)
    sum = alpha + beta
    mtau = 1/(q10*sum)
    minf = alpha/sum

    :h
    alpha = 0.07*exp(-(v + 65)/20)
    beta = 1 / (exp(-(v + 35)/10) + 1)
    sum = alpha + beta
    htau = 1/(q10*sum)
    hinf = alpha/sum

    :n
    alpha = 0.01*vtrap(-(v + 55),10)
    beta = 0.125*exp(-(v + 65)/80)
    sum = alpha + beta
    ntau = 1/(q10*sum)
    ninf = alpha/sum
}   

COMMENT
    Function:
    Function is for numerical values. Procedure is more general
ENDCOMMENT
FUNCTION vtrap(x,y){
    if (fabs(x/y) < 1e-6){
        vtrap = y*(1 - x/y/2)
    }else{
        vtrap = x/(exp(x/y) - 1)
    }
}

COMMENT
Kinetics:
This block helps encode the reactions in a very simple manner. 
For a system C-a(v)->O and O-b(v)->C, where C and O are differnet states with a(v) and b(v) rate constants.
STATE{ c o }
KINETICS scheme1{
    ~ c <-> o (a(v),b(v))
}
ENDCOMMENT

COMMENT
    Breakpoint:
    Contains the equations of the mechanism.
ENDCOMMENT
BREAKPOINT{
    SOLVE states METHOD cnexp :When there are differnetial equations to solve. The diff eqns are given in derivative block
    :'states' is derivative block containing the equations. 'cnexp' is the method used to solve them.
    gna = gnabar*m*m*m*h
    gk = gkbar*n*n*n*n
    ina = gna*(v - ena)
    ik = gk*(v - ek)
    il = gl*(v - el)
}

COMMENT
    Derivative:
    This block contains the differential equations that needs to be solved.
ENDCOMMENT
DERIVATIVE states{
    rates(v)
    m' = (minf - m)/mtau
    h' = (hinf - h)/htau
    n' = (ninf - n)/ntau
}
