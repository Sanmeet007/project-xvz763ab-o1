from typing import Optional, List
from abc import abstractmethod, ABC
from ..data.models import Drug, Location


class AbstractStore(ABC):
    @abstractmethod
    def _fetch_from_api(self, drug_name: str, location: Location) -> dict:
        pass

    @abstractmethod
    def get_drug_matches(self, drug_name: str, location: Location) -> List[Drug]:
        pass
