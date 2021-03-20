""" CRUD tests for TransactionRecord """
import string
import random
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from api.models import ServiceType


def generate_random_transaction_data() -> dict:
    """ Helper to generate transaction data """
    return {
        "service_type": random.choice(list(ServiceType)),
        "provider": random.choice(["idemia", "usps"]),
        "csp": "login.gov",
        "cost": random.randrange(0, 200) / 100,
        "result": random.choice([True, False]),
    }


def post_new_record(client, transaction_record=None):
    """ POST a new transaction record """
    url = reverse("transactionrecord-list")
    if transaction_record is None:
        transaction_record = generate_random_transaction_data()
    return client.post(url, transaction_record, content_type="application/json")


class TransactionRecordCRUDTest(TestCase):
    """ Test crud operations on TransactionRecord objects """

    def test_create_transaction_succeed(self):
        """ Test that a transaction record can be created """
        response = post_new_record(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_transaction_fail(self):
        """ Test that bad request bodies are rejected """
        url = reverse("transactionrecord-list")
        response = self.client.post(url, None, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_transaction_succeed(self):
        """ Test that we can GET a previously created record """
        # Generate a record
        response = post_new_record(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Read the record
        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_read_transaction_fail(self):
        """ Test that GET with an invalid record id fails """
        url = reverse("transactionrecord-detail", args=["invalid"])
        get_response = self.client.get(url)

        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_transaction_succeed(self):
        """ Test that we can update the record result """
        # Generate a record
        response = post_new_record(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update the record result
        new_result = random.choice([True, False])
        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        patch_response = self.client.patch(
            url, data={"result": new_result}, content_type="application/json"
        )

        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()["result"], new_result)

    def test_update_transaction_fail(self):
        """ Test that malformed updates to a record are not allowed """
        # Generate a record
        response = post_new_record(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Attempt incorrect modification of the record
        new_service_type = "".join(random.choices(string.ascii_lowercase, k=10))
        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        patch_response = self.client.patch(
            url,
            data={"service_type": new_service_type},
            content_type="application/json",
        )

        self.assertEqual(patch_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_transaction_fail(self):
        """ Test that deleting a record is not possible """
        # Generate a record
        response = post_new_record(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        get_response = self.client.delete(url)
        self.assertEqual(get_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_no_result(self):
        """ Test that the value of 'result' is not True or False when omitted """
        record = generate_random_transaction_data()
        record["result"] = ""
        response = post_new_record(self.client, record)
        self.assertNotEqual(response.json()["result"], True)
        self.assertNotEqual(response.json()["result"], False)

    def test_modify_no_result_to_true(self):
        """ Test that updates to a record with result=None works as expected """
        record = generate_random_transaction_data()
        record["result"] = ""
        response = post_new_record(self.client, record)

        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        patch_response = self.client.patch(
            url, data={"result": True}, content_type="application/json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_result_default_value_empty_string(self):
        """ Test that None/Null is the default value for 'result' """
        record = generate_random_transaction_data()
        record["result"] = ""
        response = post_new_record(self.client, record)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.json()["result"])

    def test_result_default_value_when_explicit(self):
        record = generate_random_transaction_data()
        record["result"] = None
        response = post_new_record(self.client, record)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.json()["result"])

    def test_result_default_value_when_omitted(self):
        record = generate_random_transaction_data()
        del record["result"]
        response = post_new_record(self.client, record)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.json()["result"])

    def test_no_create_record_with_wrong_mediatype(self):
        record = generate_random_transaction_data()
        url = reverse("transactionrecord-list")

        # Explicitly try to use something other than "application/json"
        response = self.client.post(
            url, data=record, content_type="multipart/form-data"
        )

        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
