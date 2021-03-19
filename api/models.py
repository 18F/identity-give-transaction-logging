""" Models for the Transaction Logging microservice """
import uuid
from django.db import models


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
    provider = models.CharField(max_length=16)

    # The CSP that sent the request. e.g. login.gov. NOTE that this value is the value
    # stored as the custom_id in the KONG gateway microservice.
    csp = models.CharField(max_length=16)

    # The result of the transaction. True=Match, False=NoMatch, Null/None=Unknown/N/A
    result = models.BooleanField(null=True, blank=True, default=None)

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
