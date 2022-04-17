from django.db import models
from django.utils import timezone




class Customer(models.Model):
    """
    Class for creating model for customer.
    """

    Gender_Choices = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    customer_id = models.IntegerField(null=False, blank=False, unique=True)
    customer_gender = models.TextField(null=True, blank=False, choices=Gender_Choices)
    customer_marital_status =  models.TextField(null=True, blank=False)
    customer_income_from_range = models.TextField(null=True, blank=False)
    customer_income_to_range = models.TextField(null=True, blank=False)
    customer_region =  models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)



class Policy(models.Model):
    """
    Class for creating model for policy.
    """

    policy_id = models.IntegerField(null=False, blank=False, unique=True)
    premium = models.IntegerField(null=True, blank=False)
    fuel =  models.TextField(null=True, blank=False)
    vehical_segment = models.TextField(null=True, blank=False)
    bodily_injury_libility = models.IntegerField(null=True, blank=False)
    bodily_damage_libility = models.IntegerField(null=True, blank=False)
    personal_injury_protection = models.IntegerField(null=True, blank=False)
    collision = models.IntegerField(null=True, blank=False)
    comprehensive = models.IntegerField(null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

class CustomerPurchases(models.Model):
    """
    Class for creating model for customer policy purchases.
    """
    policy_id = models.IntegerField(null=False, blank=False)
    customer_id = models.IntegerField(null=False, blank=False)
    purchased_date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)