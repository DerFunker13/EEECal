import addresources.conductance as cond
import numpy as np

#Skineffekt-Faktor in Näherung nach Harry Hertwig: Induktivitäten. Berlin: Verlag für Radio-Foto-Kinotechnik. 1954.

def hertwig_skineffekt(f,kappa,d):
    try:
        kappa_copper=cond.find_conductance("Copper")
        if(f==0):
            return 0.25
        f2=f*kappa/kappa_copper
        #print(f2)
        k=6.53
        delta_f=k/(np.sqrt(f2)*d*100) #*100: cm->m
        
        delta=min(0.25,delta_f)
        return delta
    except ValueError:
            return("Invalid input!")
    
print(hertwig_skineffekt(1000,59600000.0,1e-2))