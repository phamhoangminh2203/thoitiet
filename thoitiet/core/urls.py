from django.urls import path
from .views import (
    ProvinceListView, ProvinceCreateView, ProvinceUpdateView, ProvinceDeleteView,
    DistrictListView, DistrictCreateView, DistrictUpdateView, DistrictDeleteView,
    WardListView, WardCreateView, WardUpdateView, WardDeleteView,
    LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView,
    StationListView, StationCreateView, StationUpdateView, StationDeleteView,
    TideMeasurementListView, TideMeasurementCreateView, TideMeasurementUpdateView, TideMeasurementDeleteView,
    UserDetailView, UserCreateView, UserUpdateView, UserDeleteView,
    ZaloLocationView, ZaloPhoneView, ZaloUserInfoView,
    PolicyListView, PolicyCreateView, PolicyUpdateView, PolicyDeleteView,LocationSearchView, 
    
)

urlpatterns = [
    path('provinces/', ProvinceListView.as_view(), name='province-list'),
    path('provinces/create/', ProvinceCreateView.as_view(), name='province-create'),
    path('provinces/update/', ProvinceUpdateView.as_view(), name='province-update'),
    path('provinces/delete/', ProvinceDeleteView.as_view(), name='province-delete'),
    path('districts/', DistrictListView.as_view(), name='district-list'),
    path('districts/create/', DistrictCreateView.as_view(), name='district-create'),
    path('districts/update/', DistrictUpdateView.as_view(), name='district-update'),
    path('districts/delete/', DistrictDeleteView.as_view(), name='district-delete'),
    path('wards/', WardListView.as_view(), name='ward-list'),
    path('wards/create/', WardCreateView.as_view(), name='ward-create'),
    path('wards/update/', WardUpdateView.as_view(), name='ward-update'),
    path('wards/delete/', WardDeleteView.as_view(), name='ward-delete'),
    path('location/', LocationListView.as_view(), name='location-list'),
    path('location/create/', LocationCreateView.as_view(), name='location-create'),
    path('location/update/', LocationUpdateView.as_view(), name='location-update'),
    path('location/delete/', LocationDeleteView.as_view(), name='location-delete'),
    path('locations/search/', LocationSearchView.as_view(), name='location-search'),
    path('tide/stations/', StationListView.as_view(), name='station-list'),
    path('tide/stations/create/', StationCreateView.as_view(), name='station-create'),
    path('tide/stations/update/', StationUpdateView.as_view(), name='station-update'),
    path('tide/stations/delete/', StationDeleteView.as_view(), name='station-delete'),
    path('tide/measurements/', TideMeasurementListView.as_view(), name='tide-measurement-list'),
    path('tide/measurements/create/', TideMeasurementCreateView.as_view(), name='tide-measurement-create'),
    path('tide/measurements/update/', TideMeasurementUpdateView.as_view(), name='tide-measurement-update'),
    path('tide/measurements/delete/', TideMeasurementDeleteView.as_view(), name='tide-measurement-delete'),
    
    path('users/', UserDetailView.as_view(), name='user-detail'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/delete/', UserDeleteView.as_view(), name='user-delete'),
   

    path('policies/', PolicyListView.as_view(), name='policy-list'),
    path('policies/create/', PolicyCreateView.as_view(), name='policy-create'),
    path('policies/update/', PolicyUpdateView.as_view(), name='policy-update'),
    path('policies/delete/', PolicyDeleteView.as_view(), name='policy-delete'),

    path('zalo/location/', ZaloLocationView.as_view(), name='zalo-location'),
    path('zalo/phone/', ZaloPhoneView.as_view(), name='zalo-phone'),
    path('zalo/user-info/', ZaloUserInfoView.as_view(), name='zalo-user-info'),
]