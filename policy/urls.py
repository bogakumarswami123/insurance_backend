from django.conf.urls import url
from .views import (AddPolicyAPIView,UpdatePolicyAPIView, GetPolicyListView, AddCustomerAPIView, CustomerPurchaseAPIView,
                    UpdateCustomerAPIView, GetPolicyReportView)


urlpatterns = [
    url('addPolicy', AddPolicyAPIView.as_view(), name='create-policy'),
    url('addCustomer', AddCustomerAPIView.as_view(), name='get-customer'),
    url('customerPurchase', CustomerPurchaseAPIView.as_view(), name='customer-purchase'),
    url('updatePolicy/(?P<pk>.+)', UpdatePolicyAPIView.as_view(), name='update-policy'),
    url('updateCustomer/(?P<pk>.+)', UpdateCustomerAPIView.as_view(), name='update-customer'),
    url('getPolicyList', GetPolicyListView.as_view(), name='get-policies'),
    url('getPolicyReport', GetPolicyReportView.as_view(), name='get-policy-report'),
]
