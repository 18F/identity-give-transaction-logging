""" Models for the Transaction Logging microservice """
from django.db import models
import uuid


class ServiceType(models.TextChoices):
    """ Service types for TransactionRecord objects """

    ATTRIBUTE_SERVICE = "ATTRIBUTE SERVICE"
    DOCUMENT_SERVICE = "DOCUMENT SERVICE"
    PHONE_SERVICE = "PHONE SERVICE"
    PROOFING_SERVICE = "PROOFING SERVICE"
    SENSOR_SERVICE = "SENSOR SERVICE"


class TransactionRecord(models.Model):
    """ TransactionRecord objects hold information representing a single enrollment record """

    service_type = models.CharField(
        max_length=20,
        choices=ServiceType.choices,
    )

    # The validation provider. e.g. USPS, Idemia
    provider = models.CharField(max_length=60)

    # The CSP that sent the request. e.g. login.gov
    csp = models.CharField(max_length=60)

    # The result of the transaction. e.g. match, no match, unknown
    result = models.CharField(max_length=60)

    # The unique identifier for this record. Services that need to look up
    # and modify existing records with additional data should store this
    # value themselves.
    record_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cost = models.DecimalField(decimal_places=3, max_digits=8)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """ TransactionRecord Django Metadata """

        ordering = ["creation_date"]

    @property
    def uuid(self):
        """ Allow reading string representations of the uuid """
        return str(self.record_uuid)

    def __str__(self):
        return f"{self.record_uuid}: {self.result}"
