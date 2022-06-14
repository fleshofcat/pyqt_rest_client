from pyqt_rest_client.request import endpoint


def find_pet_by_status(status: str):
    return endpoint(list, ["pet", "findByStatus"], {"status": status})
