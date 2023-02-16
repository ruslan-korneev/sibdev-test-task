import pytest

from rest_framework.reverse import reverse
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("file_fixture", "expect_data_fixture", "status_code"),
    (
        ("deals_csv", None, status.HTTP_200_OK),
        (
            "deals_txt_invalid_data",
            None,
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "deals_csv_invalid_file_extension",
            "expect_fail_invalid_data",
            status.HTTP_400_BAD_REQUEST,
        ),
    ),
)
def test_deals_failed_uploading_disallowed_extension(
    file_fixture, expect_data_fixture, status_code, api_client, request
):
    filename = request.getfixturevalue(file_fixture)
    client = api_client()
    with open(filename, "r") as file:
        response = client.post(
            reverse("deal-list"), {"deals": file}, format="multipart"
        )
    assert response.status_code == status_code, response.data
    if expect_data_fixture:
        expect_data = request.getfixturevalue(expect_data_fixture)
        assert response.json() == expect_data, response.data
