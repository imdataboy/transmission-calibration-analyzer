from pathlib import Path
from asammdf import MDF

class MF4Reader:

    def __init__(self, fpath: str):
        self.fpath = Path(fpath)
        self.mdf = None

    def _ensure_open(self):
        if self.mdf is None:
            raise RuntimeError("MF4 file must be opened before accessing data")

    def open(self):
        if not self.fpath.exists():
            raise FileNotFoundError(
                f"File '{self.fpath}' does not exist."
            )
        self.mdf = MDF(self.fpath)

    def list_channels(self):
        self._ensure_open()
        return list(self.mdf.channels_db.keys())

    def get_signal(self, channel_name: str):

        self._ensure_open()

        if channel_name not in self.mdf.channels_db.keys():
            raise ValueError(
                f"Channel '{channel_name}' not found in {self.fpath.name}"
            )
        return self.mdf.get(channel_name)


    