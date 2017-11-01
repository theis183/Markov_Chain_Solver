from fractions import Fraction
from fractions import gcd
from functools import reduce

def lcm(x):   
    def lcm(a, b):
        return (a * b) // gcd(a, b)
    return reduce(lcm, x, 1)

'''since markov chains can substitute ie.
1/2 p1 can be substituted with 1/2 * (values of p1)
when this return the same element that is being checked
this term can be removed by multiplying by the inverse of
the compliment'''
def markov(tran, i, m, n):
    for j in range(0, n):
        if m[i][j] != 0 and j in tran:
            factor=m[i][j]
            m[i][j]=0
            temp0=[x * factor for x in m[j]]
            temp=[temp0, m[i]]
            m[i]=[sum(x) for x in zip(*temp)]
            if m[i][i]!=0:
                recp=(1-m[i][i])**(-1)
                m[i][i]=0
                m[i]=[x*recp for x in m[i]]
                

def answer(m):
    term=[]
    tran=[]
    n=len(m)
    for i in range(0, n): #remove self returning
        if m[i][i]!= 0:
            m[i][i] = 0
    for i in range(0, n): #sorts into transient or terminal states
        for j in range(0, n):
            if m[i][j]!=0:
                tran.append(i)
                break
            elif j==n-1:
                term.append(i)
    for i in range(0, len(m)): #turns number into fraction
        denom=sum(m[i])
        for j in range(0, len(m[i])):
            if m[i][j]!=0:
                m[i][j]=Fraction(m[i][j],denom)
    found=False
    while found==False: #runs till m[0] has no trans elements
        found=True
        for i in range(0, n):
            if i in tran:
                markov(tran, i, m, n) #see markov function
        for i in range(0, n):
            if m[0][i] != 0 and i in tran:
                found=False
    solution=[]
    for i in range(0, n): #extracts the terminal elements only
        if i in term:
            solution.append(m[0][i])
    denom=[]
    for frac in solution: 
        denom.append(frac.denominator)
    g=lcm(denom)
    solution=[int(x.numerator * (g / x.denominator)) for x in solution]
    solution.append(g)
    if len(tran)==0 or 0 not in tran: #edge case
        solution=[1,1]
    return(solution)
        
