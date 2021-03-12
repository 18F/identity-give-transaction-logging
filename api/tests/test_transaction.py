""" CRUD tests for TransactionRecord """
import string
import random
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import ServiceType


def generate_random_transaction_data() -> dict:
    """ Helper to generate transaction data """
    return {
        "service_type": random.choice(list(ServiceType)),
        "provider": random.choice(["idemia", "usps"]),
        "csp": "login.gov",
        "cost": random.randrange(0, 200) / 100,
        "result": random.choice(["fail", "pass"]),
    }


class TransactionRecordCRUDTest(APITestCase):
    """ Test crud operations on TransactionRecord objects """

    def test_create_transaction_succeed(self):
        url = reverse("transactionrecord-list")
        record = generate_random_transaction_data()
        response = self.client.post(url, record)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_transaction_fail(self):
        url = reverse("transactionrecord-list")
        response = self.client.post(url, None)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_read_transaction_succeed(self):
        url = reverse("transactionrecord-list")
        record = generate_random_transaction_data()
        response = self.client.post(url, record)

        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        get_response = self.client.get(url)

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_read_transaction_fail(self):
        url = reverse("transactionrecord-detail", args=["invalid"])
        get_response = self.client.get(url)

        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_transaction_succeed(self):
        url = reverse("transactionrecord-list")
        record = generate_random_transaction_data()
        response = self.client.post(url, record)

        new_result = "".join(random.choices(string.ascii_lowercase, k=10))
        record["result"] = new_result
        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        put_response = self.client.put(url, record)

        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.json()["result"], new_result)

    def test_update_transaction_fail(self):
        url = reverse("transactionrecord-list")
        record = generate_random_transaction_data()
        response = self.client.post(url, record)

        new_result = "".join(random.choices(string.ascii_lowercase, k=10))
        record["service_type"] = new_result
        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        put_response = self.client.put(url, record)

        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_transaction_fail(self):
        url = reverse("transactionrecord-list")
        record = generate_random_transaction_data()
        response = self.client.post(url, record)

        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        get_response = self.client.delete(url)

        self.assertEqual(get_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
