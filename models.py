import json
import urllib.parse
from datetime import date
from typing import Annotated

from pydantic import BeforeValidator, computed_field
from pydantic.dataclasses import dataclass

_BASE_UBER_DEEPLINK_URL = 'https://m.uber.com/looking'


def _parse_date(date_str: str) -> date:
    return date.strptime(date_str, '%d-%m-%Y')

Date = Annotated[date, BeforeValidator(_parse_date)]


@dataclass(frozen=True)
class Information:
    hangouts: list['Hangout']


@dataclass(frozen=True)
class Hangout:
    date: Date
    places: list['Place']


@dataclass(frozen=True)
class Place:
    tag: str
    name: str
    description: str
    description_symbol: str
    location: Location
    google_maps_url: str

    @computed_field
    def uber_deeplink(self) -> str:
        query_params = {
            'pickup': 'my_location',
            'drop[0]': json.dumps({
                'latitude': self.location.latitude,
                'longitude': self.location.longitude,
                'addressLine1': self.location.address,
            }, separators=(',', ':')),
        }

        encoded_params = urllib.parse.urlencode(
            query_params,
            quote_via=urllib.parse.quote,
            safe='[]',
        )

        return f'{_BASE_UBER_DEEPLINK_URL}?{encoded_params}'


@dataclass(frozen=True)
class Location:
    address: str
    latitude: float
    longitude: float
