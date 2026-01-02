from typing import List
from .data.models import Drug, Location
from .stores.factory import StoreFactory
from .data.enums import AvailableMedStores


class MedicineSearchService:
    @staticmethod
    async def search(
        store: AvailableMedStores, drug_name: str, location: Location
    ) -> List[Drug]:
        store_instance = StoreFactory.get_store(store)
        return store_instance.get_drug_matches(drug_name, location)
