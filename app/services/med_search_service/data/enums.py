from enum import Enum


class AvailableMedStores(Enum):
    """
    Supported medicine stores.

    NETMEDS:
        Requires full location context including country, state, city, and pincode.

    PHARMEASY:
        Requires only pincode, passed via app_location_details cookie.
    """

    PHARMEASY = 0
    NETMEDS = 1

    @staticmethod
    def list_all():
        return [AvailableMedStores.PHARMEASY, AvailableMedStores.NETMEDS]
