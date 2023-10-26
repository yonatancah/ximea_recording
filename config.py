from __future__ import annotations
from pathlib import Path

from typing import NamedTuple

from camera import CameraSettings
from yaml import load, CLoader

## Program Configuration


class ConfigData(NamedTuple):
    """
    The Configuration data for the application.
    """
    cam_ids: list[str]
    cam_settings: CameraSettings
    

    @classmethod
    def from_yaml(cls, fname: str) -> ConfigData:
        """
        Reads in data from a yaml file (e.g. "config.yaml")
        """

        # Read configuration yaml file
        data = load(Path(fname).open(), Loader=CLoader)

        # Extract main fields of the config file
        settings = data['camera-settings']
        cam_ids = data['camera-ids']

        # Construct ConfigData data structure
        config = ConfigData(
            cam_ids=cam_ids,
            cam_settings=CameraSettings(
                exposure_usec=settings['exposure'],
                frame_rate=settings['frame_rate'],
                white_balance_auto=settings['auto-white_balance'],
                image_format=settings['image-format'],
                bit_depth=settings['bit-depth']
            )
        )
        return config






if __name__ == '__main__':
    
    config = ConfigData.from_yaml('config.yaml')
    print(config)