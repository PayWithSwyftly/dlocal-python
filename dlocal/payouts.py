import uuid

from dlocal.client import DLocalClient


class DLPayout(DLocalClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.external_id = str(uuid.uuid4())
