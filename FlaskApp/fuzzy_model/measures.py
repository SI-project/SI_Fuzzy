
def _general_form(a,b):
    r = a+b
    set_result = set(r)
    try:
        return len(a)/len(set_result)
    except:
        return 999999999

def accuracy (rr:list,ri:list):
    '''
        Medida de precicion
        RR: lista de documentos recuperados relevantes
        RI: lista de documentos recuperados irrelevantes
    '''
    
    return _general_form(rr,ri)

def relay(rr:list,nr:list):
    '''
        Medida de recobrado
        RR: lista de documentos recuperados relevantes
        NR: lista de documentos no recuperados relevantes
    '''
    return _general_form(rr,nr)

def f(p:int,r:int,beta):
    ''' 
        Permite analizar la precicion sobre el recobrado y viceversa
        p: precicion
        r: recobrado
        beta=1: igual peso o enfasis para la precision y el recobrado
        beta>1: mayor peso para la precision
        beta<1: mayor peso para el recobrado
    '''
    try:    
        square_beta = beta**2
        numerator = 1+ square_beta
        denominator = 1/p +square_beta/r

        return numerator/denominator
    except:
        return 99999
def f1(p:int, r:int):
    return f(p,r,1)

def fallout(ri:list,ni:list):
    '''
        Medida de fallout
        Ri: lista de documentos recuperados irrelevantes
        NI: lista de documentos no recuperados irrelevantes
    '''
    return _general_form(ri,ni)