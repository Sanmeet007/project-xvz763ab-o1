from .base import AbstractStore
from typing import List, Optional
from ..data.models import Drug, Location
import requests


class PharmEasyStore(AbstractStore):
    BASE_PRODUCT_URL = "https://pharmeasy.in/online-medicine-order"

    def _fetch_from_api(self, drug_name: str, location: Location) -> dict:
        url = f"https://pharmeasy.in/api/search/search/?intent_id&page=1&q={drug_name}"

        cookies = {"X-Pincode": location.pincode or ""}
        response = requests.get(url, cookies=cookies, timeout=10)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _extract_image(product: dict) -> Optional[str]:
        """
        Priority:
        1. damImages[0].url (high-res)
        2. image (thumbnail)
        """
        dam_images = product.get("damImages") or []
        if dam_images and isinstance(dam_images, list):
            first_image = dam_images[0]
            if isinstance(first_image, dict):
                return first_image.get("url")

        return product.get("image")

    @classmethod
    def _extract_url(cls, product: dict) -> Optional[str]:
        """
        Builds PharmEasy product page URL.
        """
        slug = (
            product.get("slug")
            or product.get("productSlug")
            or product.get("seoSlug")
        )

        if slug:
            return f"{cls.BASE_PRODUCT_URL}/{slug}"

        return None

    def get_drug_matches(self, drug_name: str, location: Location) -> List[Drug]:
        api_response = self._fetch_from_api(drug_name, location)

        results: List[Drug] = []
        products = api_response.get("data", {}).get("products", [])

        for product in products:
            # entityType 2 = medicine
            if product.get("entityType") != 2:
                continue

            availability = product.get("productAvailabilityFlags", {}).get(
                "isAvailable", False
            )

            results.append(
                Drug(
                    name=product.get("name"),
                    description=product.get("subtitleText"),
                    molecule=product.get("moleculeName"),
                    manufacturer=product.get("manufacturer"),
                    mrp=float(product["mrpDecimal"]) if product.get("mrpDecimal") else None,
                    sale_price=(
                        float(product["salePriceDecimal"])
                        if product.get("salePriceDecimal")
                        else None
                    ),
                    discount_percent=(
                        float(product["discountPercent"])
                        if product.get("discountPercent")
                        else None
                    ),
                    available=bool(availability),
                    rx_required=bool(product.get("isRxRequired")),
                    image=self._extract_image(product),
                    url=self._extract_url(product),  # type: ignore
                )
            )

        return results
