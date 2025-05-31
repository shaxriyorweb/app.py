def calculate_throughput(num_nodes, avg_distance):
    """
    Oddiy o'tkazuvchanlik hisoblash:
    O'tkazuvchanlik tarmoq zichligi va masofaga bog'liq.
    """
    base_throughput = 100  # Mbps asosiy o'tkazuvchanlik
    throughput = base_throughput / (1 + 0.05 * avg_distance) * (1 - 0.01 * num_nodes)
    return max(throughput, 1)  # Minimal 1 Mbps

def calculate_latency(num_nodes, avg_distance):
    """
    Kechikish hisoblash:
    Kechikish masofa va tugunlar soniga bog'liq.
    """
    base_latency = 20  # ms minimal kechikish
    latency = base_latency + 2 * avg_distance + 1.5 * num_nodes
    return latency

def calculate_coverage(num_nodes, avg_distance):
    """
    Qoplash hududi hisoblash:
    Tugunlar soni va o'rtacha masofaga bog'liq
    """
    area_per_node = 3.14 * (avg_distance ** 2)
    total_coverage = area_per_node * num_nodes * 0.8  # 80% samaradorlik
    return total_coverage
