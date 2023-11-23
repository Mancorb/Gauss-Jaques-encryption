from methods import *
from copy import deepcopy
from time import perf_counter
import numpy as np

def step1(kn,I, b, r_counter):
    """Obtain all the equations from the matrix

    Args:
        kn (list): list of the matrix's values
        I (list): matrix with only ones and zeros where the inverse will be
        b (int): maximum number of values to use in encryption
        r_counter (int): row counter to skip to the rwo where this process takes place

    Returns:
        list: list of equation values
    """
    #b = p x q + r
    #Make each operation e.g: 89=33(2)+23 -> 33=23(1) + 10
    #obtains p,q,r
    
    iterations = [getFirstEquation(kn,I,b,r_counter)]
    counter = 0

    while iterations[-1][0]!=1:
        iterations.append(getEquation(iterations[-1]))
        counter += 1

    #returns p,q,r,b
    return iterations


#[p=33, q=2, r=23, b=89]
def step2(iterations,k,I,r_counter):
    """Retuns the multiplier to affect he original matrix

    Args:
        iterations (list): list of all the inicial equations before processing
        k (list): original matrix
        I (list): matrix with only 1s and 0s
        r_counter (int): counter to see in which row the process is tacking place

    Returns:
        int: multiplier to use in step 3
    """
    #part one
    #obtain the first equation
    p,q,r,b = iterations[0]
    #dictionary to store the equivalence of a value 
    b = Number(b)
    p = Number(p*-1,q)
    #r=b+(p(q))*-1
    equivalence = {r:[b,p]}#dictionary of equations to store

    if len(iterations) == 1:
        iteration = deepcopy(iterations[0])
        e,r = EquationIteration(iteration,equivalence)

    elif len(iterations) > 1:
    
        equations = deepcopy(iterations [1:-1])
        #-----------------------------------
        #Part two
        for iteration in equations:
            e,r = EquationIteration(iteration,equivalence)
            
            #Store new equation to the dictionary
            equivalence[r] = dissolve(e)
    
        #----------------------------------
        #part three last equation (just replicate part two but without adding to the dictionary and look for X based on the pivot)
        e,r = EquationIteration(equations[-1],equivalence)

    #find row pivot and return the multiplier
    for i in e:
        if i.value == k[r_counter][r_counter]:
            if I[r_counter][r_counter]:
                return i.multiplier     


def step3(K,I,X,B,r_counter):
    #Use the x[r_counter] as reference for multiplications but tot eh process first on x[r_counter]
    #R1 = r1 * X  % B
    #R2 = R1*-R2[r_counter]+R2
    #R3 = R1*-R3[r_counter]+R3

    #FIRST
    #Change I
    I_main_row =I[r_counter] = P3_first_process(I,r_counter,B,X)
    
    #Change K
    K_main_row = K[r_counter] = P3_first_process(K,r_counter,B,X)

    #go for each row
    temp = deepcopy(K)

    K = P3_second_process(K,r_counter,K_main_row,B)    
    #Change I
    I = P3_second_process(I,r_counter,I_main_row,B,temp)

    return K,I


def start(K=None,I=None,b=None,show=False):
    #create the matrix
    if not K:
        K = [[33,17,60],[50,28,72],[26,86,41]]
    if not I:
        I = [[1,0,0],[0,1,0],[0,0,1]]
    if not b:
        b = 89

    if show:
        showResults((K,I))

    for row_counter in range(len(K)):
        #row_counter = 0
        it = step1(K,I, b, row_counter)
        X = step2(it,K,I,row_counter)
        K,I = step3(K,I,X,b,row_counter)

    if show:
        showResults((K,I))

def make_I(length):
    I = []
    counter = 0
    for i in range(length):
        temp = []
        for j in range(length):
            if j == counter:
                temp.append(1)
            else:
                temp.append(0)
        I.append(temp)
        counter +=1
    return I

if __name__ == "__main__":
    n = 8 #maximum funccionality with only 7 so far
    K = np.random.randint(low=0, high=100, size=(n, n)).tolist()
    I = make_I(n)

    t1_start = perf_counter() 
    start(K,I,b=89,show=True)
    t1_stop = perf_counter()

