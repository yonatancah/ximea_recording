from typing import Literal, NamedTuple


class CameraSettings(NamedTuple):
    exposure_usec: int
    gain_analog: int
    frame_rate: int
    white_balance_auto: bool
    image_format: Literal['RGB', 'MONO', 'RAW']
    bit_depth: int