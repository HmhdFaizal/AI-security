def calculate_risk(process_hits, network_hits):
    """
    Calculates risk score from 0 to 100
    """

    score = 0

    # Process behavior weight
    score += min(process_hits * 15, 60)

    # Network behavior weight
    score += min(network_hits * 20, 40)

    return min(score, 100)
