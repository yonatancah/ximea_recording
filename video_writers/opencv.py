from __future__ import annotations

from typing import Literal

import cv2
from numpy.typing import NDArray

from .base_writer import BaseVideoWriter


class OpenCVVideoWriter(BaseVideoWriter):

    def __init__(self, writer: cv2.VideoWriter) -> None:
        self._writer: cv2.VideoWriter = writer
        self._isclosed = False

    @classmethod
    def open(cls, fname: str, frame_rate: int, frame_width: int, frame_height: int, fourcc: Literal["FMP4"] = "FMP4") -> OpenCVVideoWriter:
        return OpenCVVideoWriter(
            writer=cv2.VideoWriter(
                fname,
                cv2.VideoWriter_fourcc(*fourcc),
                frame_rate,
                (frame_width, frame_height),
            ),
        )

    def write(self, frame: NDArray) -> None:
        self._writer.write(frame)

    def close(self) -> None:
        self._writer.release()
        self._isclosed = True

    @property
    def is_closed(self) -> bool:
        return self._isclosed

    def __enter__(self) -> OpenCVVideoWriter:
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()



if __name__ == '__main__':
    import numpy as np

    # Set properties
    shape = (100, 150, 3)
    fname = "test_vid.avi"
    frame_rate = 30
    fourcc = "FMP4"

    # Generate Video File with those properties
    with OpenCVVideoWriter.open(fname=fname, frame_rate=frame_rate, frame_width=shape[1], frame_height=shape[0], fourcc=fourcc) as writer:
        for _ in range(300):
            frame = np.random.randint(0, 255, size=shape, dtype=np.uint8)
            writer.write(frame=frame)
    assert writer.is_closed

    # Check that the written Video File's properties are correct
    cap = cv2.VideoCapture(fname)
    observed_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    assert observed_width == shape[1]

    observed_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    assert observed_height == shape[0]

    observed_frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    assert observed_frame_rate == frame_rate

    fourcc_code = int(cap.get(cv2.CAP_PROP_FOURCC))
    observed_fourcc = "".join([chr((fourcc_code >> 8 * i) & 0xFF) for i in range(4)])
    assert observed_fourcc == fourcc, f"Wanted: {fourcc}; Observed: {observed_fourcc}"

    