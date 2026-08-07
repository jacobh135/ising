from ising_pkg import *
from weights import *

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

def is_related(relationships, color, pbit):
    for k in color:
        if pbit in relationships[k-1]:
            return True
    return False

pbits_total = PBIT_NUM_MAX
pbits_per_color = PLU_COUNT
colors_per_group = PBITS_PER_PLU_MAX

# create list of profiles

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

longest = 0
for i in profiles:
    if (len(i)) > longest:
        longest = len(i)
print(longest, " terms")

# create list of relationships

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

# create color groupings
color_groups = []

pbits = []
for i in range(pbits_total):
    pbits.append(i+1)

pbits_sorted = sorted(pbits, key=lambda i: len(profiles[i-1]), reverse=True)

for i in pbits_sorted:
    added = False
    j = 0
    while (not added) and j < len(color_groups):
        if (not is_related(relationships, color_groups[j], i) and (len(color_groups[j]) < pbits_per_color)):
            color_groups[j].append(i)
            added = 1
        else:
            j += 1
    if not added:
        color = [i]
        color_groups.append(color)

print(len(color_groups), " colors")

# create unit groupings 

unit_groups = []
for i in range(pbits_per_color):
    group = []
    for j in range(colors_per_group):
        group.append(-1)

    unit_groups.append(group)

for i in range(len(color_groups)):
    for j in range(len(color_groups[i])):
        unit_groups[j][i] = color_groups[i][j]