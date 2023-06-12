
resource_num = 4
accepts_cero = False
destination_num = 4
caso = 'min'

asig_options = [x for x in range(resource_num + 1)] if accepts_cero else [x for x in range(1,resource_num + 1)]

destinations = []
for destNum in range(destination_num):
    dest = {}
    for op in asig_options:
        dest[op] = int(input(f'Ingrese beneficio para opcion {op}: '))
    destinations.append(dest)






print(resource_num)
print(destinations)