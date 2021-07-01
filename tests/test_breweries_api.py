import pytest
import requests

from conftest import BREWERIES_URL


def test_breweries_status_code():
    r = requests.get(BREWERIES_URL)
    assert r.status_code == 200


@pytest.mark.parametrize("city", ['Alameda', 'Moscow', 'Zelienople'])
def test_search_by_city(city):
    r = requests.get(url=BREWERIES_URL, params={'by_city': city})
    assert r.status_code == 200 and r.json()[0]["city"] == city


@pytest.mark.parametrize("brewery_type",
                         ['micro', 'nano', 'regional', 'brewpub', 'large', 'planning', 'bar', 'contract', 'proprietor',
                          'closed'])
def test_search_by_type(brewery_type):
    r = requests.get(url=BREWERIES_URL, params={'by_type': brewery_type})
    assert r.status_code == 200 and r.json()[0]["brewery_type"] == brewery_type


@pytest.mark.parametrize("per_page",
                         [1, 25, 50, ""],
                         ids=["min", "average", "max", "by_default"])
def test_numbers_per_page(per_page):
    r = requests.get(url=BREWERIES_URL, params={'per_page': per_page})
    assert r.status_code == 200 and len(r.json()) == per_page if per_page else 20


@pytest.mark.parametrize("brewery_id", ("0", "q", "-1"))
def test_negative_search_by_id(brewery_id):
    r = requests.get(BREWERIES_URL + brewery_id)
    assert (r.status_code == 404) and (r.json()["message"] == f"Couldn't find Brewery with 'id'={brewery_id}")


@pytest.mark.parametrize("brewery_id", (9094, 14677, 11767))
def test_positive_search_by_id(brewery_id):
    r = requests.get(BREWERIES_URL + str(brewery_id))
    assert (r.status_code == 200) and (r.json()["id"] == brewery_id)
