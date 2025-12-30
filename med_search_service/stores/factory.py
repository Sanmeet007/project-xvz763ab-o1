from ..data.enums import AvailableMedStores
from .netmeds import NetMedsStore
from .pharmeasy import PharmEasyStore
from .base import AbstractStore


class StoreFactory:
    _registry = {
        AvailableMedStores.PHARMEASY: PharmEasyStore,
        AvailableMedStores.NETMEDS: NetMedsStore,
    }

    @classmethod
    def get_store(cls, store: AvailableMedStores) -> AbstractStore:
        if store not in cls._registry:
            raise ValueError(f"Unsupported store: {store}")

        return cls._registry[store]()
