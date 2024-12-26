from utils.utils import extract_data_to_list

Deltas = tuple[int, int, int, int]


def mix_num(secret_num: int, mix_in: int) -> int:
    """Returns the bitwise xor of the two numbers"""
    return secret_num ^ mix_in


def prune_secret(secret_num: int) -> int:
    """Returns the modulo 16777216 of the secret number"""
    return secret_num % 16777216


def gen_secret(num: int) -> int:
    """Generates a secret number based on the input"""

    num = prune_secret(mix_num(num, 64*num))
    num = prune_secret(mix_num(num, int(num/32)))
    return prune_secret(mix_num(num, 2048*num))


def get_2000th_secret(secret: int) -> int:
    """Returns the 2000th secret number generated from the given seed"""
    for _ in range(2000):
        secret = gen_secret(secret)
    return secret


def get_solution_1(seeds: list[int]) -> int:
    return sum([get_2000th_secret(seed) for seed in seeds])


def gen_prices(secret: int) -> list[int]:
    """Generates a list of 2000 prices"""
    prices = []
    for _ in range(2000):
        prices.append(int(str(secret)[-1]))
        secret = gen_secret(secret)
    return prices


def gen_delta_map(prices: list[int]) -> dict[Deltas, tuple[int, int]]:

    deltas = [
        prices[1] - prices[0],
        prices[2] - prices[1],
        prices[3] - prices[2],
        prices[4] - prices[3]
    ]
    delta_map = {tuple(deltas): prices[4]}
    for idx in range(5, len(prices)):
        deltas.pop(0)
        deltas.append(prices[idx] - prices[idx-1])
        new_sequence = tuple(deltas)
        if delta_map.get(new_sequence) is None:
            delta_map[new_sequence] = prices[idx]
    return delta_map


def get_solution_2(seeds: list[int]):
    """TODO"""

    delta_maps = []
    for seed in seeds:
        delta_maps.append(gen_delta_map(gen_prices(seed)))

    unique_deltas = set(
        [key for delta_map in delta_maps for key in delta_map.keys()]
    )

    banana_prices = []
    for unique_delta in unique_deltas:
        banana_prices.append(
            sum([delta_map.get(unique_delta, 0) for delta_map in delta_maps])
        )
    return max(banana_prices)


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    seeds = [int(num) for num in extract_data_to_list(22)]
    return get_solution_1(seeds), get_solution_2(seeds)
