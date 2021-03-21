""" Serializers for the Transaction Logging API """
from rest_framework import serializers
from .models import TransactionRecord


class TransactionRecordSerializer(serializers.ModelSerializer):
    """ Serializer for TransactionRecord objects """

    class Meta:
        """ TransactionRecordSerializer Django Metadata """

        model = TransactionRecord
        fields = "__all__"
