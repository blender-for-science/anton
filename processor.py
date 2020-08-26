import bpy
import os
from scipy.sparse import csr_matrix, csc_matrix
from scipy.sparse.linalg import spsolve
from sklearn.neighbors import KDTree

from tqdm import tqdm
import numpy as np

#################################################
# FUNCTIONS FROM pyOptFEM
# -----------------------------------------------
# pyOptFEM is a Python module providing simple and efficient vectorized routines for
# assembling P1-Lagrange Finite Element matrices in 2D and 3D
#
# Read more about pyOptFEM: https://www.math.univ-paris13.fr/~cuvelier/software/docs/Software/FEM/pyOptFEM/0.0.7/html/index.html
# Source: https://github.com/gscarella/pyOptFEM
# License: https://github.com/gscarella/pyOptFEM/blob/master/LICENSE

# --------------------------------------------------------------------
# ATTRIBUTION NOTICE: This product includes software developed for the pyOptFEM project at (C) University Paris XIII, Galilee Institute, LAGA, France.
# pyOptFEM is a python software package for P_1-Lagrange Finite Element Methods in 3D. The project is maintained by F. Cuvelier, C. Japhet and G. Scarella. For Online Documentation and Download we refer to
# http://www.math.univ-paris13.fr/~cuvelier
# --------------------------------------------------------------------

def BuildIkVec(me,nq):
    nme=me.shape[1]
    I=np.ndarray(shape=(12,nme),dtype=np.int32)
    for i in range(0,4):
        I[3*i]=3*me[i]
        I[3*i+1]=3*me[i]+1
        I[3*i+2]=3*me[i]+2
    return I

def BuildIgJg3DP1VF(me,nq):
    nme=me.shape[1]
    I=BuildIkVec(me,nq)
    ii=(np.array(np.arange(0,12),dtype=np.int32,ndmin=2).T)*np.ones((1,12),dtype=np.int32)
    ii.shape = (144)

    Ig=np.ndarray(shape=(144,nme),dtype=np.int32)
    Jg=np.ndarray(shape=(144,nme),dtype=np.int32)

    for i in np.arange(0,12):
        for j in np.arange(0,12):
            Ig[12*i+j]=I[i]
            Jg[12*i+j]=I[j]

    return Ig.reshape((144*nme)),Jg.reshape((144*nme))

def ComputeGradientVecTr(q,me):
    nme=me.shape[1]
    q1=q[:,me[0]];q2=q[:,me[1]];q3=q[:,me[2]];q4=q[:,me[3]]
    D12=q1-q2;D13=q1-q3;D14=q1-q4
    D23=q2-q3;D24=q2-q4
    #D34=q3-q4;
    G=np.ndarray(shape=(4,3,nme))
    G[0,0] = D23[2]*D24[1] - D23[1]*D24[2]
    G[0,1] = D23[0]*D24[2] - D23[2]*D24[0]
    G[0,2] = D23[1]*D24[0] - D23[0]*D24[1]
    G[1,0] = D13[1]*D14[2] - D13[2]*D14[1]
    G[1,1] = D13[2]*D14[0] - D13[0]*D14[2]
    G[1,2] = D13[0]*D14[1] - D13[1]*D14[0]
    G[2,0] = D12[2]*D14[1] - D12[1]*D14[2]
    G[2,1] = D12[0]*D14[2] - D12[2]*D14[0]
    G[2,2] = D12[1]*D14[0] - D12[0]*D14[1]
    G[3,0] = D12[1]*D13[2] - D12[2]*D13[1]
    G[3,1] = D12[2]*D13[0] - D12[0]*D13[2]
    G[3,2] = D12[0]*D13[1] - D12[1]*D13[0]
    return G

def ElemStiffElasMatBa3DP1Vec(nme,q,me,volumes,la,mu):
    """
    Computes all the element elastic stiffness  matrices :math:`\mathbb{K}^e(T_k)` for :math:`k\in\{0,\hdots,\nme-1\}`
    in local *alternate* basis.

    :param nme: number of mesh elements,
    :type nme: int
    :param q: mesh vertices,
    :type q: ``(3,nq)`` *numpy* array of floats
    :param me: mesh connectivity,
    :type me: ``(4,nme)`` *numpy* array of integers
    :param volumes: volumes of all the mesh elements.
    :type volumes: ``(nme,)`` *numpy* array of floats
    :param la: the  :math:`\\lambda` Lame parameter,
    :type la: float
    :param mu: the  :math:`\\mu` Lame parameter.
    :type mu: float
    :returns: a ``(144*nme,)`` *numpy* array of floats.
    """
    ndf2=144;
    G=ComputeGradientVecTr(q,me)

    coef=6*np.sqrt(volumes)
    for il in range(0,4):
        for i in range(0,3):
            G[il,i]=G[il,i]/coef

    #Kg=zeros((ndf2,nme))
    Kg=np.ndarray(shape=(ndf2,nme))
    T1=G[0,0]**2
    T2=G[0,1]**2
    T3=G[0,2]**2
    C=mu*(T1+ T2 + T3)
    Kg[0] =(la + mu)*T1 + C
    Kg[13]=(la + mu)*T2 + C
    Kg[26]=(la + mu)*T3 + C

    T1=G[1,0]**2
    T2=G[1,1]**2
    T3=G[1,2]**2
    C=mu*(T1+ T2 + T3)
    Kg[39]=(la + mu)*T1 + C
    Kg[52]=(la + mu)*T2 + C
    Kg[65]=(la + mu)*T3 + C

    T1=G[2,0]**2
    T2=G[2,1]**2
    T3=G[2,2]**2
    C=mu*(T1+ T2 + T3)
    Kg[78]=(la + mu)*T1 + C
    Kg[91]=(la + mu)*T2 + C
    Kg[104]=(la + mu)*T3 + C

    T1=G[3,0]**2
    T2=G[3,1]**2
    T3=G[3,2]**2
    C=mu*(T1+ T2 + T3)
    Kg[117]=(la + mu)*T1 + C
    Kg[130]=(la + mu)*T2 + C
    Kg[143]=(la + mu)*T3 + C

    Kg[1]=Kg[12]=(la+mu)*G[0,0]*G[0,1]
    Kg[2]=Kg[24]=(la+mu)*G[0,0]*G[0,2]

    T1=G[0,0]*G[1,0]
    T2=G[0,1]*G[1,1]
    T3=G[0,2]*G[1,2]
    C=mu*(T1+ T2 + T3)
    Kg[3] =Kg[36]=(la + mu)*T1 + C
    Kg[16]=Kg[49]=(la + mu)*T2 + C
    Kg[29]=Kg[62]=(la + mu)*T3 + C

    T1=G[0,0]*G[1,1]
    T2=G[0,1]*G[1,0]
    Kg[4] =Kg[48]=la*T1+mu*T2
    Kg[15]=Kg[37]=la*T2+mu*T1

    T1=G[0,0]*G[1,2]
    T2=G[0,2]*G[1,0]
    Kg[5] =Kg[60]=la*T1+mu*T2
    Kg[27]=Kg[38]=la*T2+mu*T1

    T1=G[0,0]*G[2,0]
    T2=G[0,1]*G[2,1]
    T3=G[0,2]*G[2,2]
    C=mu*(T1+ T2 + T3)
    Kg[6] =Kg[72]=(la + mu)*T1 + C
    Kg[19]=Kg[85]=(la + mu)*T2 + C
    Kg[32]=Kg[98]=(la + mu)*T3 + C

    T1=G[0,0]*G[2,1]
    T2=G[0,1]*G[2,0]
    Kg[7] =Kg[84]= la*T1+mu*T2
    Kg[18]=Kg[73]= la*T2+mu*T1

    T1=G[0,0]*G[2,2]
    T2=G[0,2]*G[2,0]
    Kg[8] =Kg[96]= la*T1+mu*T2
    Kg[30]=Kg[74]= la*T2+mu*T1

    T1=G[0,0]*G[3,0]
    T2=G[0,1]*G[3,1]
    T3=G[0,2]*G[3,2]
    C=mu*(T1+ T2 + T3)
    Kg[9]=Kg[108]=(la + mu)*T1 + C
    Kg[22]=Kg[121]=(la + mu)*T2 + C
    Kg[35]=Kg[134]=(la + mu)*T3 + C

    T1=G[0,0]*G[3,1]
    T2=G[0,1]*G[3,0]
    Kg[10]=Kg[120]= la*T1+mu*T2
    Kg[21]=Kg[109]= la*T2+mu*T1

    T1=G[0,0]*G[3,2]
    T2=G[0,2]*G[3,0]
    Kg[11]=Kg[132]= la*T1+mu*T2
    Kg[33]=Kg[110]= la*T2+mu*T1

    Kg[14]=Kg[25]=(la+mu)*G[0,1]*G[0,2]

    T1=G[0,1]*G[1,2]
    T2=G[0,2]*G[1,1]
    Kg[17]=Kg[61]= la*T1+mu*T2
    Kg[28]=Kg[50]= la*T2+mu*T1

    T1=G[0,1]*G[2,2]
    T2=G[0,2]*G[2,1]
    Kg[20]=Kg[97]= la*T1+mu*T2
    Kg[31]=Kg[86]= la*T2+mu*T1

    T1=G[0,1]*G[3,2]
    T2=G[0,2]*G[3,1]
    Kg[23]=Kg[133]= la*T1+mu*T2
    Kg[34]=Kg[122]= la*T2+mu*T1

    Kg[40]=Kg[51]= (la+mu)*G[1,0]*G[1,1]
    Kg[41]=Kg[63]= (la+mu)*G[1,0]*G[1,2]

    T1=G[1,0]*G[2,0]
    T2=G[1,1]*G[2,1]
    T3=G[1,2]*G[2,2]
    C=mu*(T1+ T2 + T3)
    Kg[42]=Kg[75]=(la + mu)*T1 + C
    Kg[55]=Kg[88]=(la + mu)*T2 + C
    Kg[68]=Kg[101]=(la + mu)*T3 + C

    T1=G[1,0]*G[2,1]
    T2=G[1,1]*G[2,0]
    Kg[43]=Kg[87]= la*T1+mu*T2
    Kg[54]=Kg[76]= la*T2+mu*T1

    T1=G[1,0]*G[2,2]
    T2=G[1,2]*G[2,0]
    Kg[44]=Kg[99]= la*T1+mu*T2
    Kg[66]=Kg[77]= la*T2+mu*T1

    T1=G[1,0]*G[3,0]
    T2=G[1,1]*G[3,1]
    T3=G[1,2]*G[3,2]
    C=mu*(T1+ T2 + T3)
    Kg[45]=Kg[111]=(la + mu)*T1 + C
    Kg[58]=Kg[124]=(la + mu)*T2 + C
    Kg[71]=Kg[137]=(la + mu)*T3 + C

    T1=G[1,0]*G[3,1]
    T2=G[1,1]*G[3,0]
    Kg[46]=Kg[123]= la*T1+mu*T2
    Kg[57]=Kg[112]= la*T2+mu*T1

    T1=G[1,0]*G[3,2]
    T2=G[1,2]*G[3,0]
    Kg[47]=Kg[135]= la*T1+mu*T2
    Kg[69]=Kg[113]= la*T2+mu*T1

    Kg[53]=Kg[64]= (la+mu)*G[1,1]*G[1,2]

    T1=G[1,1]*G[2,2]
    T2=G[1,2]*G[2,1]
    Kg[56]=Kg[100]= la*T1+mu*T2
    Kg[67]=Kg[89]= la*T2+mu*T1

    T1=G[1,1]*G[3,2]
    T2=G[1,2]*G[3,1]
    Kg[59]=Kg[136]= la*T1+mu*T2
    Kg[70]=Kg[125]= la*T2+mu*T1

    Kg[79]=Kg[90]=(la+mu)*G[2,0]*G[2,1]

    Kg[80]=Kg[102]=(la+mu)*G[2,0]*G[2,2]

    T1=G[2,0]*G[3,0]
    T2=G[2,1]*G[3,1]
    T3=G[2,2]*G[3,2]
    C=mu*(T1+ T2 + T3)

    Kg[81] =Kg[114]=(la + mu)*T1 + C
    Kg[94] =Kg[127]=(la + mu)*T2 + C
    Kg[107]=Kg[140]=(la + mu)*T3 + C
    #
    T1=G[2,0]*G[3,1]
    T2=G[2,1]*G[3,0]
    Kg[82]=Kg[126]= la*T1+mu*T2
    Kg[93]=Kg[115]= la*T2+mu*T1

    T1=G[2,0]*G[3,2]
    T2=G[2,2]*G[3,0]
    Kg[83] =Kg[138]= la*T1+mu*T2
    Kg[105]=Kg[116]= la*T2+mu*T1

    Kg[92]=Kg[103]=(la+mu)*G[2,1]*G[2,2]

    T1=G[2,1]*G[3,2]
    T2=G[2,2]*G[3,1]
    Kg[95] = Kg[139]=la*T1+mu*T2
    Kg[106]= Kg[128]=la*T2+mu*T1

    Kg[118]=Kg[129]=(la + mu)*G[3,0]*G[3,1]
    Kg[119]=Kg[141]=(la + mu)*G[3,0]*G[3,2]
    Kg[131]=Kg[142]=(la + mu)*G[3,1]*G[3,2]

    # return Kg.reshape((ndf2*nme))
    return Kg.T

# ------------------------------------------------
# FUNCTIONS FROM pyOptFEM
##################################################

class Anton_OT_Operator(bpy.types.Operator):
    bl_idname = 'anton.process'
    bl_label = 'Anton_Processor'
    bl_description = 'Start Optimization'

    material_library = {'Steel-28Mn6': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S690MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PA6-Generic': {'POISSON': 0.39, 'YOUNGS': 2930.0},
                        'Steel-X39CrMo17-1': {'POISSON': 0.3, 'YOUNGS': 213000.0},
                        'Steel-S335N': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-3C22': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PET-Generic': {'POISSON': 0.36, 'YOUNGS': 3150.0},
                        'Steel-1C35': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-2C10': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJL-300': {'POISSON': 0.3, 'YOUNGS': 125000.0},
                        'Steel-C30E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-34CrNiMo6': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-1C60': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S380MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Glass-Generic': {'POISSON': 0.22, 'YOUNGS': 72000.0},
                        'Steel-E295-GC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C15': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-G20Mn5': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-St-E-380': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S500MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C60E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S335JO': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-E360-GC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C25E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-3C35': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Acrylic-Glass-Generic': {'POISSON': 0.38, 'YOUNGS': 2550.0},
                        'Steel-E360': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMW-450-7': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-S235JO': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PTFE-Generic': {'POISSON': 0.46, 'YOUNGS': 564.0},
                        'Steel-EN-GJL-150': {'POISSON': 0.3, 'YOUNGS': 95000.0},
                        'Steel-X6CrNiTi18-10': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'Steel-G260': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C50E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMB-650-2': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-G300': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMB-550-4': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-St-37-2K': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PVC-Generic': {'POISSON': 0.38, 'YOUNGS': 2800.0},
                        'Steel-EN-GJMW-360-12': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Wood-Generic': {'POISSON': 0.05, 'YOUNGS': 12000.0},
                        'Steel-St-E-460': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PP-Generic': {'POISSON': 0.44, 'YOUNGS': 1470.0},
                        'Steel-G30Mn5': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMW-400-5': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-S275N': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMW-350-4': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-C10': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJL-200': {'POISSON': 0.3, 'YOUNGS': 105000.0},
                        'Steel-30CrNiMo8': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJL-100': {'POISSON': 0.3, 'YOUNGS': 88000.0},
                        'Steel-EN-GJL-350': {'POISSON': 0.3, 'YOUNGS': 135000.0},
                        'AlMgSi1F31': {'POISSON': 0.3, 'YOUNGS': 70000.0},
                        'Concrete-Generic': {'POISSON': 0.17, 'YOUNGS': 32000.0},
                        'Steel-S420N': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-3C15': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMB-350-10': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Reinforcement-FIB-B500': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJS-800-1': {'POISSON': 0.3, 'YOUNGS': 180000.0},
                        'Steel-S355J2G3': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-G16Mn5': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-G230': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'AlZn4-5Mg1F35': {'POISSON': 0.3, 'YOUNGS': 70000.0},
                        'Steel-20NiCrMo2': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-E295': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S235JR': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJS-500-7': {'POISSON': 0.3, 'YOUNGS': 170000.0},
                        'PLA-Generic': {'POISSON': 0.36, 'YOUNGS': 3640.0},
                        'Steel-3V45': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Aluminum-6061-T6': {'POISSON': 0.33, 'YOUNGS': 69000.0},
                        'ABS-Generic': {'POISSON': 0.37, 'YOUNGS': 2300.0},
                        'Steel-17CrNiMo6': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJS-400-15': {'POISSON': 0.3, 'YOUNGS': 167000.0},
                        'Steel-St-E-315': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-E335': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S185': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-Generic': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'Steel-S420MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S275JR': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-X3CrNiMo13-14': {'POISSON': 0.3, 'YOUNGS': 216000.0},
                        'Steel-C40E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-X5CrNiMo17-12-2': {'POISSON': 0.3, 'YOUNGS': 180000.0},
                        'Steel-C22E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-E335-GC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S260NC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S275JO': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-1C22': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C55E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-36NiCrMo16': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-36CrNiMo4': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S335JR': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'CalculiX-Steel': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJS-600-3': {'POISSON': 0.3, 'YOUNGS': 177000.0},
                        'Steel-X2CrNiMoN17-13-3': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'Steel-S235JRG1': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S460N': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S460MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S550MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-15CrNi6': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Concrete-EN-C35_45': {'POISSON': 0.17, 'YOUNGS': 32000.0},
                        'Steel-St-E-255': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJL-250': {'POISSON': 0.3, 'YOUNGS': 115000.0},
                        'Steel-S340MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-St-E-500': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-1C45': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-X5CrNi18-10': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'AlMg3F24': {'POISSON': 0.3, 'YOUNGS': 70000.0},
                        'Steel-G200': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-X2CrNiN24-4': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'Steel-EN-GJS-700-2': {'POISSON': 0.3, 'YOUNGS': 180000.0}}

    def execute(self, context):

        scene = context.scene
        if scene.anton.defined:
            nodes = np.load(os.path.join(scene.anton.workspace_path, scene.anton.filename+'.nodes.npy'))
            elements = np.load(os.path.join(scene.anton.workspace_path, scene.anton.filename+'.elements.npy'))
            fixed = np.load(os.path.join(scene.anton.workspace_path, scene.anton.filename+'.fixed.npy'))
            no_design_nodes = np.load(os.path.join(scene.anton.workspace_path, scene.anton.filename+'.nds.npy'))
            youngs = self.material_library[scene.anton.material]['YOUNGS']
            poisson = self.material_library[scene.anton.material]['POISSON']

            load = scene.attributes['LOAD']
            no_design_set = np.array([], dtype=np.int)

            penalty = scene.anton.penalty_exponent
            volumina = scene.anton.volumina_ratio
            density_change = scene.anton.density_change
            convergence = 0.001
            n_neighbours = scene.anton.number_of_neighbours

            nq = len(nodes)
            nme = len(elements)
            ndofs = 3*nq
            dofs = np.arange(ndofs)

            for _node_id in no_design_nodes:
                no_design_set = np.append(no_design_set, np.where(elements==_node_id)[0])

            _temp_fixed = []
            fixed_elements = np.array([], dtype=np.int)
            for _node_id in fixed:
                _temp_fixed.extend([3*_node_id, 3*_node_id+1, 3*_node_id+2])
                fixed_elements = np.append(fixed_elements, np.where(elements==_node_id)[0])

            free = np.setdiff1d(dofs,_temp_fixed)
            F = np.zeros((ndofs, 1), dtype=np.float)

            forced_elements = np.array([], dtype=np.int)
            for _node_id in load.keys():
                forced_elements = np.append(forced_elements, np.where(elements==_node_id)[0])
                _id = 3*_node_id
                for _dim, value in enumerate(load[_node_id]):
                    F[_id + _dim] = value

            if scene.anton.include_fixed:
                no_design_set = np.append(no_design_set, fixed_elements)

            if scene.anton.include_forced:
                no_design_set = np.append(no_design_set, forced_elements)

            K = []

            densities = np.ones((nme, 1))
            displacement = np.zeros((ndofs,1), dtype=np.float)
            sensitivity = np.zeros((nme, 1))

            edofmat = np.array([np.arange(12)%3]*nme) + 3*elements[:, np.arange(12)//3]
            E0 = youngs
            Emin = scene.anton.emin

            ncoords = np.append(np.ones((nq, 1)), nodes, axis=1)[elements]
            element_centers = 0.25 * np.sum(ncoords[:, :, 1:], axis=1)
            np.save(os.path.join(scene.anton.workspace_path, scene.anton.filename+'.ecenters'), element_centers)

            distances, structure = KDTree(element_centers).query(element_centers, k=n_neighbours)
            distances = scene.anton.rmin - distances
            distances[distances<0] = 0.0

            distances_sum = np.sum(distances, axis=1)

            volumes = (1/6) * np.linalg.det(ncoords)
            np.save(os.path.join(scene.anton.workspace_path, scene.anton.filename+'.volumes'), volumes)

            Ig, Jg = BuildIgJg3DP1VF(elements.T, nq)
            Kg = ElemStiffElasMatBa3DP1Vec(nme, nodes.T, elements.T, volumes, 1, poisson)
            Ke = Kg.reshape(nme, 12, 12)
            pref = -1 * penalty * (E0 - Emin) * 0.5 * E0 * (1/volumes)

            for _step in tqdm(range(scene.anton.number_of_iterations)):
                E = Emin + (E0 - Emin)*(densities**penalty)
                modKg = (E * Kg).T
                K = csc_matrix((modKg.reshape((144*nme)),(Ig,Jg)),shape=(3*nq,3*nq))
                displacement[free, 0] = spsolve(K[free, :][:, free], F[free])

                Ue = displacement[edofmat]
                UeT = Ue.reshape((nme, 1, 12))
                sensitivity = np.matmul(np.matmul(UeT, Ke), Ue).reshape(nme)
                sensitivity = (pref * densities.reshape(nme)**(penalty - 1) * sensitivity).reshape(nme, 1)

                fsensdenom = densities.T[0] * distances_sum
                fsensdenom[fsensdenom<0.001] = 0.001
                fsensitivity = np.sum(densities[structure].reshape(nme, n_neighbours) * distances * sensitivity[structure].reshape(nme, n_neighbours), axis=1) / fsensdenom
                # fsensitivity.reshape(len(elements), 1)

                min_sens = 0.001
                max_sens = 1e9

                while((max_sens - min_sens)/(max_sens + min_sens) > convergence):
                    mid_sens = 0.5 * (max_sens + min_sens)

                    # DENSITY RULE
                    step_densities = np.maximum(
                                            0.0,
                                            np.maximum(
                                                densities - density_change,
                                                np.minimum(
                                                    1.0,
                                                    np.minimum(
                                                        densities + density_change,
                                                        densities * (-1 * (fsensitivity.reshape(len(elements), 1)/mid_sens))**0.5
                                                    )
                                        )))

                    if len(no_design_set) > 0:
                        step_densities[no_design_set] = 1.0

                    if np.mean(step_densities) - volumina > 0:
                        min_sens = mid_sens
                    else:
                        max_sens = mid_sens

                fdensities = np.sum(distances * step_densities[structure].reshape(nme, n_neighbours), axis=1)/distances_sum
                densities = fdensities.reshape(nme, 1)
                np.save(os.path.join(scene.anton.workspace_path, scene.anton.filename+'_i{}.densities'.format(_step+1)), densities)

            return {'FINISHED'}

        else:
            self.report({'ERROR'}, '.inp file missing in {}'.format(scene.anton.workspace_path))
            return {'CANCELLED'}


    @staticmethod
    def compute_Dmat(v):
        d_matrix = (1/((1+v)*(1-2*v))) * np.array([[1.0-v, v, v, 0.0, 0.0, 0.0],
                                                    [v, 1.0-v, v, 0.0, 0.0, 0.0],
                                                    [v, v, 1.0-v, 0.0, 0.0, 0.0],
                                                    [0.0, 0.0, 0.0, 0.5-v, 0.0, 0.0],
                                                    [0.0, 0.0, 0.0, 0.0, 0.5-v, 0.0],
                                                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.5-v]])
        return d_matrix