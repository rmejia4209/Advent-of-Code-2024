def Bron_Kerbosch(R, P, X, network):
    if not P and not X:
        parties.add(tuple(sorted(R)))  # Found a maximal clique
        return

    pivot = next(iter(P | X))  # Choose a pivot vertex from P ∪ X

    for v in P - network[pivot]:  # Explore vertices not adjacent to pivot
        Bron_Kerbosch(R | {v}, P & network[v], X & network[v], network)
        P.remove(v)
        X.add(v)

# Example graph (adjacency list)
network = {
    'ka': {'tb', 'tc'},
    'tb': {'ka', 'cg', 'tc'},
    'tc': {'ka', 'kh', 'co', 'tb'},
    'kh': {'tc', 'ta'},
    'ta': {'kh'},
    'cg': {'tb', 'de'},
    'de': {'cg'},
    'co': {'tc'}
}

# Initial sets
P = set(network.keys())  # All vertices
X = set()  # Initially empty set for excluded vertices
R = set()  # Initially empty set for the current clique
parties = set()  # To store the maximal cliques

Bron_Kerbosch(R, P, X, network)

# Print maximal cliques
print("Maximal cliques:", parties)
