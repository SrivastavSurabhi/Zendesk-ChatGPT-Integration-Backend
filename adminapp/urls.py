from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.Login.as_view(), name="login"),
    path('login/', views.Login.as_view(), name="login"),
    # path('admin_dashboard/', views.Login.as_view(), name="admin_dashboard"),
    path('logout/', views.logout_view, name="logout"),
    path('add_user/', views.AddUser.as_view(), name="add_user"),
    path('get_response/', views.GetResponse.as_view(), name="get_response"),
    path('get_yes_response/', views.GetYesResponse.as_view(), name="get_yes_response"),
    path('get_no_response/', views.GetNoResponse.as_view(), name="get_no_response"),
    path('get_instruct_response/', views.GetInstructResponse.as_view(), name="get_instruct_response"),
    path('get_moreinfo_response/', views.GetMoreInfoResponse.as_view(), name="get_moreinfo_response"),
    path('count_api_hit/', views.CountHits.as_view(), name="count_api_hit"),
    path('save_user/', views.SaveUser.as_view(), name="count_api_hit"),
    path('update_user_data/', views.UpdateUser.as_view(), name="update_user_data"),
    path('apihit_info/', views.APIHitsInfo.as_view(), name="apihit_info"),
    path('get_admin_data/<organizatin_id>', views.GetAdminData.as_view(), name="get_admin_data"),
    path('fetch_all_users/', views.FetchAllUsers.as_view(), name="fetch_all_users"),
    path('check_pricing/', views.CheckPricing.as_view(), name="check_pricing"),

    # path('accoun_owner/', views.AccountOwnerDashboard.as_view(), name="accoun_owner"),
    path('admin_dashboard/', views.AdminDashboard.as_view(), name="admin_dashboard"),
    path('update_config/', views.UpdateConfig.as_view(), name="update_config"),
    path('get_admin_settings/', views.AdminSettings.as_view(), name="get_admin_settings"),
    path('get_plans/', views.GetPlans.as_view(), name="get_plans"),
    path('get_users/', views.GetAllAccountOwners.as_view(), name="get_users"),
    path('get_users/<user_id>', views.GetAccountOwnerInfo.as_view(), name="get_userss"),

    path('fetch_user_token/', views.FetchUserToken.as_view(), name="fetch_user_token"),
    path('get_jwt_token/', views.GetJWTToken.as_view(), name="get_jwt_token"),
    path('get_jwt_token_by_id/', views.GetJWTTokenById.as_view(), name="get_jwt_token_by_id"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
