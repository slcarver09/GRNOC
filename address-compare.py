import pandas as pd
from rapidfuzz import fuzz, process

# Load CSVs
pops = pd.read_csv("pops.csv")
ciena = pd.read_csv("Ciena Site IDs.csv")

# Normalize addresses
def normalize_address(row, street_col, city_col, state_col):
    addr = f"{row[street_col]} {row[city_col]} {row[state_col]}".lower()
    return (addr
        .replace('street', 'st')
        .replace('road', 'rd')
        .replace('avenue', 'ave')
        .replace('northwest', 'nw')
        .replace('northeast', 'ne')
        .replace('.', '')
        .replace(',', '')
        .strip()
    )

pops["norm_addr"] = pops.apply(lambda x: normalize_address(x, "Shipping Street", "City", "State"), axis=1)
ciena["norm_addr"] = ciena.apply(lambda x: normalize_address(x, "Address 1", "City", "State"), axis=1)

# Match each POP to the closest Ciena site
matches = []
for _, pop in pops.iterrows():
    match, score, idx = process.extractOne(
        pop["norm_addr"],
        ciena["norm_addr"],
        scorer=fuzz.token_sort_ratio
    )
    best = ciena.loc[idx]
    matches.append({
        "POP Code": pop["Code"],
        "POP Address": pop["Shipping Street"],
        "Matched Ciena": best["Address 1"],
        "Ciena Site ID": best["Site ID"],
        "Similarity": score
    })

results = pd.DataFrame(matches)
results.to_csv("pop_to_ciena_matches.csv", index=False)
