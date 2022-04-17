from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from .models import (Customer, Policy, CustomerPurchases)
import json



class CustomerSerializer(serializers.ModelSerializer):
    """
    Class for serializing for customer.
    """
    class Meta:
        model = Customer
        fields = ["id", "customer_id", "customer_gender", "customer_marital_status", "customer_income_from_range", "customer_income_to_range", "created_at", "customer_region"]

class UpdateCustomerSerializer(serializers.ModelSerializer):
    """
    Class for serializing for update customer.
    """
    class Meta:
        model = Customer
        fields = ["id", "customer_id", "customer_gender", "customer_marital_status", "customer_income_from_range", "customer_income_to_range", "updated_at", "customer_region"]


class PolicySerializer(serializers.ModelSerializer):
    """
    Class for serializing for policy.
    """
    class Meta:
        model = Policy
        fields = ["id", "policy_id", "premium", "fuel", "vehical_segment", "bodily_injury_libility", "bodily_damage_libility", "personal_injury_protection","collision","comprehensive","created_at"]


class UpdatePolicySerializer(serializers.ModelSerializer):
    """
    Class for serializing for update policy.
    """
    class Meta:
        model = Policy
        fields = ["id", "policy_id", "premium", "fuel", "vehical_segment", "bodily_injury_libility", "bodily_damage_libility", "personal_injury_protection","collision","comprehensive","updated_at"]


class CustomerPurchaseSerializer(serializers.ModelSerializer):
    """
    Class for serializing for customer.
    """
    class Meta:
        model = CustomerPurchases
        fields = ["id", "customer_id", "policy_id", "purchased_date", "created_at"]



class PolicyListSerializer(serializers.ModelSerializer):
    policy_details = serializers.SerializerMethodField()
    customer_details = serializers.SerializerMethodField()

    class Meta:
        model = CustomerPurchases
        fields = ["id", "customer_id", "policy_id", "purchased_date", "created_at","customer_details","policy_details"]

    def get_policy_details(self, instance):
        get_policy = Policy.objects.filter(policy_id=instance.policy_id).values(
            "id", "policy_id", "premium", "fuel", "vehical_segment", "bodily_injury_libility", "bodily_damage_libility", "personal_injury_protection","collision","comprehensive","created_at"
        )
        return get_policy

    def get_customer_details(self, instance):
        get_customer = Customer.objects.filter(customer_id=instance.customer_id).values(
            "id", "customer_id", "customer_gender", "customer_marital_status", "customer_income_from_range", "customer_income_to_range", "created_at", "customer_region"
        )
        return get_customer



class PolicyReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerPurchases
        fields = ["id", "purchased_date"]
