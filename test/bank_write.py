from ising_pkg import *
# from decoding import *
from math import *

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

def get_profile_address(profiles, index):
    count = 0
    for i in range(index):
        count += len(profiles[i])
    return count

def get_index(valid, i_index, profile_address, term_count):
    pbit_valid = twos_comp(valid, 1)
    pbit_i_index = twos_comp(i_index, PBIT_INDEX_W)
    pbit_profile_address = twos_comp(profile_address, PBIT_PROFILE_ADDRESS_W)
    pbit_term_count = twos_comp(term_count, PBIT_TERM_COUNT_W)

    index = (
        (pbit_valid << PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W + PBIT_INDEX_W) |
        (pbit_i_index << PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W) |
        (pbit_profile_address << PBIT_TERM_COUNT_W) |
        (pbit_term_count)
    )
    return index

# note that real pbits where h, j, and k are all 0 have a 1 zero term profile
# thus, it must be asserted that if valid=1, then term_count>=1
assigned_pbits = [1, -1, 5, -1, -1, 6]

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
for i in range(PBIT_NUM):
    terms = []
    profiles.append(terms)

for key, value in K_weights.items():
    if (value != 0):
        for i in range(3):
            if key[i] in assigned_pbits:
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
            if key[i] in assigned_pbits:
                if (i == 0):
                    j = 1
                else:
                    j = 0
                    
                term = get_term(1, value, key[j]-1, 0)

                profiles[key[i]-1].append(term)

for key, value in H_weights.items():
    if (value != 0):
        if key in assigned_pbits:
            term = get_term(0, value, 0, 0)

            profiles[key-1].append(term)

for i in assigned_pbits:
    if ((i != -1) and (not (profiles[i-1]))):
        term = get_term(0, 0, 0, 0)

        profiles[i-1].append(term)

terms_hex_length = ceil(TERM_STRING_W / 4)

with open("terms.hex", "w") as f:
    for i in profiles:
        for j in i:
            f.write(f"{j:0{terms_hex_length}x}\n")

indices = []

for i in assigned_pbits:
    if (i == -1):
        index = get_index(0, 0, 0, 0)
    else:
        index = get_index(1, i-1, get_profile_address(profiles, i-1), len(profiles[i-1]))

    indices.append(index)

indices_hex_length = ceil(INDEX_STRING_W / 4)

with open("indices.hex", "w") as f:
    for i in indices:
        f.write(f"{i:0{indices_hex_length}x}\n")