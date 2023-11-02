from __future__ import annotations

from .base_writer import BaseTimestampWriter

import csv


class CSVTimestampWriter(BaseTimestampWriter):

    def __init__(self, writer, file) -> None:
        self._writer = writer
        self._file = file

    @classmethod
    def open(cls, fname: str) -> CSVTimestampWriter:
        file = open(fname, 'w', newline='')
        writer = csv.writer(file)
        field = ["timestamp", "corrected_timestamp"]
        writer.writerow(field)
        return CSVTimestampWriter(writer=writer, file=file)


    def write(self, timestamp: int, timestamp_correction: int = 0) -> None:
        self._writer.writerow([timestamp, timestamp + timestamp_correction])


    def close(self) -> None:
        self._file.close()



if __name__ == '__main__':
    writer = CSVTimestampWriter.open("test_timestamps.csv")

    for t in range(10):
        writer.write(timestamp=t(t, t*10))
    writer.close()
