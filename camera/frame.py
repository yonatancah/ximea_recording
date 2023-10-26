from numpy.typing import NDArray


from typing import NamedTuple


class Frame(NamedTuple):
    timestamp: int
    image: NDArray