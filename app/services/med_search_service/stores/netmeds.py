from ..data.models import Drug, Location
from .base import AbstractStore
from typing import List, Optional
import requests


class NetMedsStore(AbstractStore):
    BASE_PRODUCT_URL = "https://www.netmeds.com/product"

    def _fetch_from_api(self, drug_name: str, location: Location) -> dict:
        app_location_details = location.serialize()

        url = (
            "https://www.netmeds.com/ext/search/application/api/v1.0/products"
            f"?filters=false&page_id=1&page_size=12&q={drug_name}"
        )

        cookies = {"app_location_details": app_location_details}
        response = requests.get(url, cookies=cookies, timeout=10)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _extract_image(item: dict) -> Optional[str]:
        """
        Priority:
        1. medias[0].url
        """
        medias = item.get("medias") or []
        if medias and isinstance(medias, list):
            first_media = medias[0]
            if isinstance(first_media, dict):
                return first_media.get("url")
        return None

    @classmethod
    def _extract_url(cls, item: dict) -> Optional[str]:
        """
        Builds Netmeds product page URL using slug.
        """
        slug = item.get("slug")

        # Fallback (rare but safe)
        if not slug:
            slug = (
                item.get("action", {})
                .get("page", {})
                .get("params", {})
                .get("slug", [None])[0]
            )

        if slug:
            return f"{cls.BASE_PRODUCT_URL}/{slug}"

        return None

    def get_drug_matches(self, drug_name: str, location: Location) -> List[Drug]:
        api_response = self._fetch_from_api(drug_name, location)

        drugs: List[Drug] = []
        items = api_response.get("items", [])

        for item in items:
            # Only medicine products
            if item.get("type") != "product":
                continue

            attrs = item.get("attributes", {})
            price = item.get("price", {})
            effective = price.get("effective", {})
            marked = price.get("marked", {})

            drugs.append(
                Drug(
                    name=item.get("name"),
                    description=attrs.get("mstar-packlabel"),
                    molecule=attrs.get("genericnamewithdosage")
                    or attrs.get("genericname"),
                    manufacturer=attrs.get("manufacturername"),
                    mrp=marked.get("min"),
                    sale_price=effective.get("min"),
                    discount_percent=attrs.get("mstar-discountpct"),
                    available=item.get("sellable", False),
                    rx_required=attrs.get("mstar-rxrequired") == "Rx required",
                    image=self._extract_image(item),
                    url=self._extract_url(item),  # type: ignore
                )
            )

        return drugs
