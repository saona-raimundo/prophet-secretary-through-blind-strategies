# Optmization solver
# 
# Reference API
# https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustconstr.html

from detailed_performance import detailed_performance
import numpy as np
from scipy.optimize import minimize

m = 30


# Bounds
# lower <= x <= upper   

from scipy.optimize import Bounds
lower = np.full(m, 1e-10)
upper = np.full(m, 1 - 1e-10)
bounds = Bounds(lower, upper)

# Linear constraints
# increasing alpha
# c <= A x <= b

from scipy.optimize import LinearConstraint
c = np.full(m-1, -np.inf)
A = [[-1 * (i == j) + 1 * (i == j - 1) for j in range(m)] for i in range(m-1)]
b = np.full(m-1, 0) 
linear_constraint = LinearConstraint(A, c, b)

# Optimization problem

# Initial value
alpha0 = np.linspace(0.55, 0.05, num=m)
# Function to minimize
def fun(alpha):
    return -np.min(detailed_performance(alpha))
# Compute minimization
res = minimize(fun, alpha0, method='trust-constr',
    constraints=[linear_constraint],
    options={
        'verbose': 3, 
        'maxiter': 2000, # default 1000
        'gtol': 1e-50, # default 1e-8
        'xtol': 1e-50, # default 1e-8
        'barrier_tol': 1e-50, # default 1e-8
    }, 
    bounds=bounds)

# Report result

print(res)
print(np.min(detailed_performance(res.x)))

# Some experimental results
    
    # alpha 
    # performance

    # [0.72369543, 0.64226064, 0.58769284, 0.54562721, 0.51225859,
    #    0.48459988, 0.46056567, 0.43960941, 0.42032546, 0.40283973,
    #    0.38672948, 0.3716508 , 0.35765868, 0.34459633, 0.33236537,
    #    0.31715066, 0.30242103, 0.2879849 , 0.27324156, 0.25748757,
    #    0.24034747, 0.22235207, 0.20414479, 0.1855729 , 0.16639905,
    #    0.14631284, 0.12484141, 0.10117722, 0.07358793, 0.03649029] 
    # 0.6682670938073006
    
    # [0.74563438, 0.65509097, 0.5956051 , 0.54837587, 0.50970638,
    #    0.47696111, 0.44848823, 0.42316269, 0.40018369, 0.38738087,
    #    0.37639742, 0.36630308, 0.35671755, 0.3481476 , 0.33269121,
    #    0.3178706 , 0.3032794 , 0.2888033 , 0.27367471, 0.25836997,
    #    0.24277429, 0.22673822, 0.21009635, 0.1926313 , 0.17408305,
    #    0.15409213, 0.13216475, 0.10743496, 0.07876431, 0.04100157] 
    # 0.6675791644950522
    
    # [0.72241383, 0.64132521, 0.58638382, 0.54465525, 0.51083185,
    #    0.48253277, 0.45816543, 0.43665956, 0.41752443, 0.40021008,
    #    0.38445254, 0.37008241, 0.35679807, 0.34086704, 0.32573318,
    #    0.31134425, 0.29759731, 0.28428215, 0.27137004, 0.258793  ,
    #    0.24656899, 0.23460191, 0.21490543, 0.19482806, 0.17408551,
    #    0.15242167, 0.12946182, 0.10439072, 0.07559736, 0.03796015] 
    # 0.6677718716944624
    
    # [0.72330608, 0.64352342, 0.58995907, 0.5490439 , 0.51564802,
    #    0.48725508, 0.46244133, 0.44031947, 0.42029573, 0.40195089,
    #    0.38497511, 0.36913247, 0.35433267, 0.34034803, 0.32706784,
    #    0.31440062, 0.30226907, 0.28821375, 0.27459647, 0.2613897 ,
    #    0.24271562, 0.22395042, 0.205072  , 0.1858517 , 0.16609424,
    #    0.14551633, 0.12366791, 0.09973132, 0.07185998, 0.03471215] 
    # 0.6683453198850813
    
    # [0.73088247, 0.64728024, 0.5905843 , 0.54690972, 0.5121255 ,
    #    0.48318737, 0.45836084, 0.43640322, 0.41673529, 0.39910151,
    #    0.38313396, 0.36841816, 0.35463798, 0.34192615, 0.33001295,
    #    0.31667341, 0.30384813, 0.28955402, 0.27405804, 0.2581746 ,
    #    0.24026949, 0.22200931, 0.20363255, 0.18500573, 0.16594442,
    #    0.14625332, 0.12555283, 0.10325394, 0.07812557, 0.04656071] 
    # 0.6680461420330217
    
    # [0.73893968, 0.64434168, 0.58480161, 0.53869582, 0.50270844,
    #    0.47306925, 0.45042111, 0.43077154, 0.41323084, 0.39726484,
    #    0.3827544 , 0.36922685, 0.35649349, 0.34443508, 0.3316864 ,
    #    0.31721168, 0.30297507, 0.28859577, 0.27318622, 0.2575347 ,
    #    0.24169288, 0.2256185 , 0.20920915, 0.19225314, 0.17463547,
    #    0.15583728, 0.1353647 , 0.11247984, 0.08555998, 0.05085876] 
    # 0.6672715271153086
    
    # [0.72415396, 0.65028453, 0.59310701, 0.54947008, 0.51160574,
    #    0.48031465, 0.45456811, 0.43309757, 0.41475892, 0.39865762,
    #    0.38414138, 0.37072823, 0.35805588, 0.345838  , 0.33382368,
    #    0.31859215, 0.30326725, 0.28826348, 0.27305961, 0.25754141,
    #    0.24181697, 0.22547304, 0.20827237, 0.18992247, 0.1700711 ,
    #    0.14833399, 0.12441609, 0.09830483, 0.06856294, 0.03578367] 
    # 0.6681904421593717
    
    # [0.72407053, 0.64397759, 0.58827444, 0.54599951, 0.51202039,
    #    0.48344469, 0.45941024, 0.43828841, 0.41901649, 0.40155561,
    #    0.38532784, 0.37019188, 0.35599739, 0.3426052 , 0.3299015 ,
    #    0.31778729, 0.30223632, 0.28699443, 0.27196446, 0.25695988,
    #    0.24014673, 0.22309978, 0.20567374, 0.18769918, 0.16894294,
    #    0.14908918, 0.12765407, 0.10378471, 0.07569712, 0.04009888] 
    # 0.668069652667508
    
    # [0.67699182, 0.66490484, 0.60158186, 0.55614734, 0.52010464,
    #    0.49025544, 0.46484012, 0.4424727 , 0.4224104 , 0.40415579,
    #    0.3874404 , 0.37196344, 0.35793043, 0.34318325, 0.32944535,
    #    0.31320542, 0.29739753, 0.28191541, 0.26670487, 0.25143146,
    #    0.23601253, 0.22021746, 0.20378073, 0.18680571, 0.16867315,
    #    0.14915083, 0.12761786, 0.10292822, 0.07331355, 0.03333235] 
    # 0.6684561705990512

    # [0.73470981, 0.64016774, 0.5836485 , 0.54111827, 0.50779049,
    #    0.48015017, 0.45635485, 0.43530098, 0.41629283, 0.39885004,
    #    0.38262812, 0.36737409, 0.35288684, 0.33900537, 0.325594  ,
    #    0.31254526, 0.29914608, 0.28484207, 0.27050712, 0.25603515,
    #    0.24131508, 0.22621961, 0.21060051, 0.19427063, 0.17697997,
    #    0.15837484, 0.13791548, 0.11466933, 0.08671899, 0.04895757] 
    # 0.6673010074464397