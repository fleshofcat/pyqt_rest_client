from typing import List

from pyqt_rest_client import endpoint
from usage_example.dataclasses.pet import Pet


def find_pet_by_status(status: str):
    return endpoint(List[Pet], ["pet", "findByStatus"], {"status": status})
