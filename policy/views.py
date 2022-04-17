import os
from django.db.models import Q
import datetime
import pytz
from datetime import datetime as dt,timedelta
from python_http_client import exceptions
from insurance_backend import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (GenericAPIView,
                                     UpdateAPIView,
                                     ListAPIView
                                     )
from policy.utils import (ResponseInfo,
                         CustomPagination
                         )
from utilities import messages
from dotenv import load_dotenv
import pandas as pd
import csv
import itertools
import copy
from datetime import datetime, date
from django.db.models import Count
from .serializers import (CustomerSerializer, PolicySerializer, CustomerPurchaseSerializer, PolicyListSerializer,UpdatePolicySerializer, UpdateCustomerSerializer,PolicyReportSerializer)
from .models import (Customer as CustomerModel, Policy as PolicyModel, CustomerPurchases as CustomerPurchasesModel)




def get_records():
    result_list = []
    with open('/home/sandeep/Downloads/Insurance_Client.csv', newline='') as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader]
        headers = data.pop(0)
        for i in data:
            empty_dict={}
            for item_index in range(0, len(i)):
                empty_dict[headers[item_index]] = i[item_index]
                if(headers[item_index] == 'Customer_Income group'):
                    empty_dict["customer_income_from_range"] = i[item_index].split("-")[0] if len(i[item_index].split("-")) > 0 else None
                    empty_dict["customer_income_to_range"] = i[item_index].split("-")[1] if len(i[item_index].split("-")) > 1 else None
                elif(headers[item_index] == "Date of Purchase"):
                    date_list = i[item_index].split("/")
                    purchased_date = date(2000,1,1)
                    if(len(date_list) == 3):
                        purchased_date = date(int(date_list[2]), int(date_list[0]), int(date_list[1]))  
                    empty_dict["Date of Purchase"] = purchased_date
            result_list.append(empty_dict)
    return result_list
        

class AddCustomerAPIView(GenericAPIView):
    """
    Class for creating API view for creating customers.
    """
    permission_classes = ()
    authentication_classes = ()

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(AddCustomerAPIView, self).__init__(**kwargs)


    def post(self, request):
        result_list = get_records()
        customers_list = list()
        for item in result_list:
            is_customer_exist = False
            for customer in customers_list:
                if(customer["Customer_id"] == item["Customer_id"]):
                    is_customer_exist = True
            
            if(is_customer_exist == False):
                customers_list.append(item)
        customer_count  = CustomerModel.objects.all().count()
        if customer_count == 0:
            for customer in customers_list:
                customer_item = {
                    "customer_id":customer.get("Customer_id"),
                    "customer_gender":customer.get("Customer_Gender"), 
                    "customer_marital_status": customer.get("Customer_Marital_status"), 
                    "customer_income_from_range": customer.get("customer_income_from_range"), 
                    "customer_income_to_range":customer.get("customer_income_to_range"),  
                    "customer_region": customer.get("Customer_Region")
                }
                customer_serialized = CustomerSerializer(data=customer_item)
                if customer_serialized.is_valid(raise_exception=True):
                    customer_serialized.save()
        self.response_format["data"] = None
        self.response_format["status_code"] = status.HTTP_201_CREATED
        self.response_format['message'] = "Success"
        return Response(self.response_format)


class AddPolicyAPIView(GenericAPIView):
    """
    Class for creating API view for creating policies.
    """

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(AddPolicyAPIView, self).__init__(**kwargs)

    def post(self, request):
        result_list = get_records()
        policy_list = list()
        for item in result_list:
            is_policy_exist = False
            for customer in policy_list:
                if(customer["Policy_id"] == item["Policy_id"]):
                    is_policy_exist = True
            
            if(is_policy_exist == False):
                policy_list.append(item)
        policy_count  = PolicyModel.objects.all().count()
        if policy_count == 0:
            for policy in policy_list:
                policy_item = {
                    "policy_id":policy.get("Policy_id"),
                    "premium":policy.get("Premium"),
                    "fuel" : policy.get("Fuel"),
                    "vehical_segment": policy.get("VEHICLE_SEGMENT"),
                    "bodily_injury_libility":policy.get("bodily injury liability"),
                    "bodily_damage_libility": policy.get(" property damage liability"),
                    "personal_injury_protection":policy.get(" personal injury protection"), 
                    "collision":policy.get(" collision"),
                    "comprehensive":policy.get(' comprehensive')
                }
                policy_serialized = PolicySerializer(data=policy_item)
                if policy_serialized.is_valid(raise_exception=True):
                    policy_serialized.save()
        self.response_format["data"] = None
        self.response_format["status_code"] = status.HTTP_201_CREATED
        self.response_format['message'] = "Success"
        return Response(self.response_format)


class CustomerPurchaseAPIView(GenericAPIView):
    """
    Class for creating API view for customer policy purchase.
    """

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(CustomerPurchaseAPIView, self).__init__(**kwargs)

    def post(self, request):
        result_list = get_records()
        count  = CustomerPurchasesModel.objects.all().count()
        if count == 0:
            for item in result_list:
                purchase_item = {
                    "policy_id":item.get("Policy_id"),
                    "customer_id":item.get("Customer_id"),
                    "purchased_date" : item.get("Date of Purchase")
                }
                purchase_serialized = CustomerPurchaseSerializer(data=purchase_item)
                if purchase_serialized.is_valid(raise_exception=True):
                    purchase_serialized.save()
        self.response_format["data"] = None
        self.response_format["status_code"] = status.HTTP_201_CREATED
        self.response_format['message'] = "Success"
        return Response(self.response_format)


class UpdatePolicyAPIView(UpdateAPIView):
    """
    Class for updating policy.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UpdatePolicySerializer

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UpdatePolicyAPIView, self).__init__(**kwargs)

    def get_queryset(self):
        id = self.kwargs['pk']
        return PolicyModel.objects.filter(id=id)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        policy_id = copy.copy(instance.policy_id)
        instance.policy_id = request.data["policy_id"]
        instance.premium = request.data["premium"]
        instance.fuel = request.data["fuel"]
        instance.vehical_segment = request.data["vehical_segment"]
        instance.bodily_injury_libility = request.data["bodily_injury_libility"]
        instance.bodily_damage_libility= request.data["bodily_damage_libility"]
        instance.personal_injury_protection = request.data["personal_injury_protection"]
        instance.collision = request.data["collision"]
        instance.comprehensive = request.data["comprehensive"]

        policy_serializer = self.get_serializer(instance, data=request.data)
        if policy_serializer.is_valid(raise_exception=True):
            self.partial_update(policy_serializer)
            CustomerPurchasesModel.objects.filter(policy_id=policy_id).update(policy_id=instance.policy_id)
            self.response_format["data"] = policy_serializer.data
        return Response(self.response_format)


class UpdateCustomerAPIView(UpdateAPIView):
    """
    Class for updating customer.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UpdateCustomerSerializer

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UpdateCustomerAPIView, self).__init__(**kwargs)

    def get_queryset(self):
        id = self.kwargs['pk']
        return CustomerModel.objects.filter(id=id)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        customer_id = copy.copy(instance.customer_id)
        instance.customer_id = request.data["customer_id"]
        instance.customer_gender = request.data["customer_gender"]
        instance.customer_marital_status = request.data["customer_marital_status"]
        instance.customer_income_from_range = request.data["customer_income_from_range"]
        instance.customer_income_to_range = request.data["customer_income_to_range"]
        instance.customer_region= request.data["customer_region"]

        customer_serializer = self.get_serializer(instance, data=request.data)
        if customer_serializer.is_valid(raise_exception=True):
            self.partial_update(customer_serializer)
            CustomerPurchasesModel.objects.filter(customer_id=customer_id).update(customer_id=instance.customer_id)
            self.response_format["data"] = customer_serializer.data
        return Response(self.response_format)



class GetPolicyListView(ListAPIView):
    """
    Class for creating API view for getting policies list.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = PolicyListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("policy_id","customer_id")

    def get_queryset(self):
        return CustomerPurchasesModel.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Function for getting all policies.
        """
        paginator = PageNumberPagination()
        paginator.page_size = 10

        purchased_policies_serialized = super().list(request, *args, **kwargs)

        result= paginator.paginate_queryset(purchased_policies_serialized.data, request)
        return CustomPagination.get_paginated_response(paginator, result)


class GetPolicyReportView(ListAPIView):
    """
    Class for creating API view for getting policies reports.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = PolicyReportSerializer
    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(GetPolicyReportView, self).__init__(**kwargs)
    def get_queryset(self):
        return   CustomerPurchasesModel.objects.all().values_list('purchased_date__year', 'purchased_date__month').annotate(Count('purchased_date__month')).order_by('purchased_date__year', 'purchased_date__month')

    def get(self, request, *args, **kwargs):
        """Count
        Function for getting all policies reports.
        """

        purchased_policies_serialized = CustomerPurchasesModel.objects.all().values('purchased_date__year', 'purchased_date__month').annotate(Count('purchased_date__month')).order_by('purchased_date__year', 'purchased_date__month')
        self.response_format["data"] = purchased_policies_serialized
        return Response(self.response_format)
