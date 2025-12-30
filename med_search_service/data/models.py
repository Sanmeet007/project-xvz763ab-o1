from pydantic import BaseModel, Field
from typing import Optional
from urllib.parse import quote
import json


class Drug(BaseModel):
    url: str = Field(..., description="URL to the drug")

    name: str = Field(
        ..., description="Commercial name of the medicine as listed by the pharmacy"
    )

    description: Optional[str] = Field(
        None,
        description="Short description of the medicine including strength, form, and pack size",
    )

    molecule: Optional[str] = Field(
        None, description="Active pharmaceutical ingredient(s) present in the medicine"
    )

    manufacturer: Optional[str] = Field(
        None, description="Company that manufactures the medicine"
    )

    mrp: Optional[float] = Field(
        None,
        description="Maximum Retail Price (MRP) of the medicine before any discounts",
    )

    sale_price: Optional[float] = Field(
        None, description="Discounted selling price of the medicine currently offered"
    )

    discount_percent: Optional[float] = Field(
        None, description="Percentage discount applied on the MRP"
    )

    available: bool = Field(
        ...,
        description="Indicates whether the medicine is currently available for purchase",
    )

    rx_required: bool = Field(
        ...,
        description="Whether a valid doctor's prescription is required to purchase this medicine",
    )

    image: Optional[str] = Field(
        ..., description="Image of the drug available on the website"
    )

    def to_json(self) -> str:
        return self.model_dump_json()


class Location(BaseModel):
    country: str = Field(default="INDIA")
    country_iso_code: Optional[str] = Field(default="IN")
    pincode: Optional[str] = Field(default="160071")
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)

    def serialize(self):
        payload = {
            "country": self.country,
            "country_iso_code": self.country_iso_code,
            "pincode": self.pincode,
            "city": self.city,
            "state": self.state,
        }

        json_str = json.dumps(payload, separators=(",", ":"))
        return quote(json_str)

    def to_json(self):
        return self.model_dump_json()
