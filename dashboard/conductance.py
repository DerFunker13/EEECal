# kappa in S/m , Material

conductance_table = [
    (2.38e7,"Aluminum"),
    (1.00e-2,"Carbon (graphite)"),
    (5.96e7,"Copper"),
    (1.00e-12,"Glass"),
    (3.50e7,"Gold"),   
    (1.02e7,"Iron"),
    (6.30e7,"Silver"),
    (1.00e-15,"Teflon"),
    (1.00e-6,"Water (distilled)"),
    (1.00e-4,"Water (tap)"),
]

def find_conductance(material_name):
    for value, name in conductance_table:
        if name.lower() == material_name.lower():
            return value
    return None  # Not found

#print(find_conductance("Copper"))