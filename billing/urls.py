from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accoun_owner', views.AccountOwnerDashboard.as_view(), name="accoun_owner"),
    path('user_info/', views.AccountOwnerInfo.as_view(), name="accoun_owner"),
    path('checkout-session/', views.CheckOutSession.as_view(), name="checkout-session"),
    path('create-checkout-session/', views.CreateCheckOutSession.as_view(), name="create-checkout-session"),
    path('cancel-plan/', views.CancelPlan.as_view(), name="cancel-plan"),
    path('invoices/', views.Invoices.as_view(), name="invoices"),
    path('invoice-detail/', views.GetInvoiceDetail.as_view(), name="invoice-detail"),
    path('update_subs/', views.UpdateSubscription.as_view(), name="update_subs"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
