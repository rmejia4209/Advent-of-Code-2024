from utils.utils import extract_data_to_list


Network = dict[str, list[str]]
LAN_Party = tuple[str, ...]


def generate_network(connections: list[tuple[int, int]]) -> Network:
    """Generates a network for a given list of connections"""
    network = {}
    for node_1, node_2 in connections:
        network.setdefault(node_1, []).append(node_2)
        network.setdefault(node_2, []).append(node_1)
    return network


def get_matching_parties(network: Network) -> int:
    """Returns parties of 3 with at least one node that beings with t."""
    parties = set()
    for node, neighbors in network.items():
        if node[0] != 't':
            continue
        for i, neighbor in enumerate(neighbors):
            for j in range(len(neighbors)):
                if i == j:
                    continue
                if network[node][j] in network[neighbor]:
                    parties.add(
                        tuple(sorted([node] + [neighbor] + [network[node][j]]))
                    )
    return len(parties)


def get_maximal_cliques(network: Network) -> int:
    """Returns the maximal cliques using the Bron-Kerbosch algorithm"""
    parties = set()

    def Bron_Kerbosch(party: set[str], nodes: set[str], excluded: set[str]):
        """Bron-Kerbosch algorithm with pivoting"""
        if len(nodes) == 0 and len(excluded) == 0:
            parties.add(tuple(sorted(party)))
            return

        pivot = next(iter(nodes.union(excluded)))
        for vertex in nodes.difference(network[pivot]):
            Bron_Kerbosch(
                party.union({vertex}),
                nodes.intersection(network[vertex]),
                excluded.intersection(network[vertex])
            )
            nodes.remove(vertex)
            excluded.add(vertex)

    for node in network:
        network[node] = set(network[node])
    Bron_Kerbosch(set(), set(network.keys()), set())
    return parties


def get_largest_party(network: Network) -> str:
    """Returns a string of the largest party"""
    parties = get_maximal_cliques(network)
    largest_party = None
    for party in parties:
        if largest_party is None or len(largest_party) < len(party):
            largest_party = party
    return ','.join(largest_party)


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    connections = [
        tuple(nodes.split('-')) for nodes in extract_data_to_list(23)
    ]
    network = generate_network(connections)

    return get_matching_parties(network), get_largest_party(network)
