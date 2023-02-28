import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.fixture
def success_get_data():
    return [
        {
            "username": "resplendent",
            "spentMoney": "451731.00",
            "gems": ["Сапфир", "Танзанит", "Рубин"],
        },
        {
            "username": "bellwether",
            "spentMoney": "217794.00",
            "gems": ["Сапфир", "Петерсит"],
        },
        {
            "username": "uvulaperfly117",
            "spentMoney": "120419.00",
            "gems": ["Танзанит", "Петерсит"],
        },
        {"username": "braggadocio", "spentMoney": "108957.00", "gems": ["Изумруд"]},
        {
            "username": "turophile",
            "spentMoney": "100132.00",
            "gems": ["Рубин", "Изумруд"],
        },
    ]


@pytest.mark.django_db
def test_get_deals(success_get_data, deals_csv, deals_csv_second, api_client):
    # first i should upload data
    client = api_client()
    with open(deals_csv, "r") as file:
        client.post(reverse("deal-list"), {"deals": file}, format="multipart")

    # get deals
    response = client.get(reverse("deal-list"))
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.json() == success_get_data

    # update csv
    client = api_client()
    with open(deals_csv_second, "r") as file:
        client.post(reverse("deal-list"), {"deals": file}, format="multipart")

    # get deals, data should be different
    response = client.get(reverse("deal-list"))
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.json() != success_get_data
