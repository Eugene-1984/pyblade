__all__ = [
    'human_to_float'
]

HUMAN_TO_FLOAT = {
    'K': 'e3',
    'M': 'e6',
    'G': 'e9'
}


def human_to_float(human: str) -> float:
    if isinstance(human, str):
        for suffix, replacement in HUMAN_TO_FLOAT.items():
            if suffix in human:
                human = human.replace(suffix, replacement)
                break

    return float(human)
