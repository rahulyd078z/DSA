def allocate_energy(hour, demands, sources):
    # Filter available sources for the given hour
    available = [s for s in sources if s['available_start'] <= hour <= s['available_end']]
    
    # Cheapest first allocated
    available.sort(key=lambda x: x['cost'])

    # Initialize allocation and remaining capacities
    allocation = {d: {s['type']: 0 for s in available} for d in demands}
    remaining_capacity = {s['type']: s['capacity'] for s in available}
    total_cost = 0

    # Allocate energy greedily
    for source in available:
        s_type = source['type']
        cost = source['cost']

        for district in demands:
            if remaining_capacity[s_type] > 0 and demands[district] > 0:
                alloc = min(remaining_capacity[s_type], demands[district])
                allocation[district][s_type] += alloc
                remaining_capacity[s_type] -= alloc
                demands[district] -= alloc
                total_cost += alloc * cost

    # Check if all demands are met and calculate percent met
    percent_met = {d: 100 for d in allocation}

    return allocation, total_cost, percent_met


# Sample test case
demands = {'A': 20, 'B': 15, 'C': 25}
sources = [
    {'type': 'Solar', 'capacity': 50, 'cost': 1.0, 'available_start': 6, 'available_end': 18},
    {'type': 'Hydro', 'capacity': 40, 'cost': 1.5, 'available_start': 0, 'available_end': 24}
]

allocation, total_cost, percent_met = allocate_energy(6, demands.copy(), sources)

print("Allocation:", allocation)
print("Total Cost:", total_cost)
print("Percent Met:", percent_met)
