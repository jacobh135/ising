from ising_pkg import *

def twos_comp(value, width):
    return (value & ((1 << width) - 1))

def get_term(type, weight, j_index, k_index):
    term_type = twos_comp(type, 2)
    term_weight = twos_comp(weight, TERM_WEIGHT_W)
    term_pbit_j_index = twos_comp(j_index, PBIT_INDEX_W)
    term_pbit_k_index = twos_comp(k_index, PBIT_INDEX_W)

    term = (
        (term_type << 2*PBIT_INDEX_W + TERM_WEIGHT_W) |
        (term_weight << 2*PBIT_INDEX_W) |
        (term_pbit_j_index << PBIT_INDEX_W) |
        (term_pbit_k_index)
    )
    return term

def is_related(relationships, color_groups, pbit, color):
    for k in color_groups[color]:
        if pbit in relationships[k-1]:
            return True
    return False

pbits_total = 6
pbits_per_color = 10

# index starts at 1
H_weights = {
    (1): 0,
    (2): 2,
    (3): 1,
    (4): 0,
    (5): -1,
    (6): 0
}

J_weights = {
    (1,2): -3,
    (1,3): -1,
    (1,4): 2,
    (1,5): 2,
    (2,3): 0,
    (2,4): 2,
    (2,5): -1,
    (3,4): 0,
    (3,5): 3,
    (4,5): -2
}

K_weights = {
    (1,2,3): -1,
    (1,2,4): -1,
    (1,2,5): -1,
    (1,3,4): -2,
    (1,3,5): 0,
    (1,4,5): 1,
    (2,3,4): -1,
    (2,3,5): 0,
    (2,4,5): 0,
    (3,4,5): -1
}

profiles = []
for i in range(pbits_total):
    terms = []
    profiles.append(terms)

for key, value in K_weights.items():
    if (value != 0):
        for i in range(3):
            if (i == 0):
                j = 1
                k = 2
            elif (i == 1):
                j = 0
                k = 2
            else:
                j = 0
                k = 1

            term = get_term(2, value, key[j]-1, key[k]-1)
            
            profiles[key[i]-1].append(term)

for key, value in J_weights.items():
    if (value != 0):
        for i in range(2):
            if (i == 0):
                j = 1
            else:
                j = 0
                
            term = get_term(1, value, key[j]-1, 0)

            profiles[key[i]-1].append(term)

for key, value in H_weights.items():
    if (value != 0):
        term = get_term(0, value, 0, 0)

        profiles[key-1].append(term)

for i in range(len(profiles)):
    if not (profiles[i]):
        term = get_term(0, 0, 0, 0)

        profiles[i].append(term)

relationships = []
for i in range(pbits_total):
    related = []
    relationships.append(related)

for key, value in K_weights.items():
    if (value != 0):
        for i in range(3):
            if (i == 0):
                j = 1
                k = 2
            elif (i == 1):
                j = 0
                k = 2
            else:
                j = 0
                k = 1

            if not key[j] in relationships[key[i]-1]:
                relationships[key[i]-1].append(key[j])
            if not key[k] in relationships[key[i]-1]:
                relationships[key[i]-1].append(key[k])

for key, value in J_weights.items():
    if (value != 0):
        for i in range(2):
            if (i == 0):
                j = 1
            else:
                j = 0

            if not key[j] in relationships[key[i]-1]:
                relationships[key[i]-1].append(key[j])

color_groups = []

for i in range(len(relationships)):
    # can sort by term number here

    added = False
    j = 0
    while (not added) and j < len(color_groups):
        if (not is_related(relationships, color_groups, i+1, j) and (len(color_groups[j]) < pbits_per_color)):
            color_groups[j].append(i+1)
            added = 1
        else:
            j += 1
    if not added:
        color = [i+1]
        color_groups.append(color)

print(color_groups)

colors_per_group = len(color_groups)

unit_groups = []
for i in range(pbits_per_color):
    group = []
    for j in range(colors_per_group):
        group.append(-1)

    unit_groups.append(group)

for i in range(len(color_groups)):
    for j in range(len(color_groups[i])):
        unit_groups[j][i] = color_groups[i][j]

print(unit_groups)

# ensure total terms in a group is less than term max