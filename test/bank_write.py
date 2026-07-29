from ising_pkg import *
from decoding import *
from math import *

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

def bank_write(profiles, unit_group, bank_num):
    group_profiles = [] # pad with 0s until TERM_TOTAL_MAX
    for i in range(len(profiles)):
        terms = []
        group_profiles.append(terms)

    for i in unit_group:
        if ((i != -1)):
            group_profiles[i-1] = profiles[i-1]

    terms_hex_length = ceil(TERM_STRING_W / 4)

    with open(f"terms_{bank_num}.hex", "w") as f:
        for i in group_profiles:
            for j in i:
                f.write(f"{j:0{terms_hex_length}x}\n")

    group_indices = [] # pad with 0s until PBITS_PER_PLU_MAX
    for i in unit_group:
        index = 0
        group_indices.append(index)

    for i in range(len(unit_group)):
        if (unit_group[i] == -1):
            group_indices[i] = get_index(0, 0, 0, 0)
        else:
            group_indices[i] = get_index(1, unit_group[i]-1, get_profile_address(group_profiles, unit_group[i]-1), len(group_profiles[unit_group[i]-1]))

    indices_hex_length = ceil(INDEX_STRING_W / 4)

    with open(f"indices_{bank_num}.hex", "w") as f:
        for i in group_indices:
            f.write(f"{i:0{indices_hex_length}x}\n")

for i in range(pbits_per_color):
    bank_write(profiles, unit_groups[i], i)