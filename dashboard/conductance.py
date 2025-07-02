# kappa in S/m , Material

conductance_table = [
    {5.96e7,"Copper"},
    {6.30e7,"Silver"},
    {1.02e7,"Iron"},
    {3.50e7,"Gold"},
    {1.00e-2,"Carbon (graphite)"},
    {1.00e-4,"Water (tap)"},
    {1.00e-6,"Distilled Water"},
    {1.00e-12,"Glass"},
    {1.00e-15,"Teflon"},
    {2.38e7,"Aluminum"},
]

def find_conductance(material_name):
    for value, name in conductance_table:
        if name.lower() == material_name.lower():
            return value
    return None  # Not found

#print(find_conductance("Copper"))