from rest_framework import serializers
from .models import Circuit, Customer, Site


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'customer_name', 'city', 'state', 'address')


class CircuitSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Circuit
        fields = ('id', 'customer','circuit_id', 'mep_id', 'cir_az', 'cir_za')


class SiteSerializer(serializers.ModelSerializer):
    circuit = CircuitSerializer()

    class Meta:
        model = Site
        fields = ('id', 'circuit', 'ip', 'hw_version','ip_type')
