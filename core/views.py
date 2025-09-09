from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import requests
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import (
    Province, District, Ward, Location, Station, TideMeasurement, User,  Policy, Category, Article, MiniAppOption
)
from .serializers import (
    ProvinceSerializer, DistrictSerializer, WardSerializer, LocationSerializer, 
    StationSerializer, TideMeasurementSerializer, UserSerializer, PolicySerializer, 
    TideSyncSerializer,CategorySerializer, ArticleSerializer, MiniAppOptionSerializer
)
from .zalo_api import (
    get_user_location, check_oa_follow_status, request_location_permission,
    get_location_token, get_location_with_token, check_location_error
)
from django.db.models import Q
from datetime import datetime
import pytz
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter
from .pagination import OptionalLimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.utils.timezone import localtime
class ArticleBulkDeleteView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])  # 👈 Lấy list id từ body
        if not ids or not isinstance(ids, list):
            return Response({"detail": "Vui lòng cung cấp danh sách ID cần xóa."}, status=status.HTTP_400_BAD_REQUEST)
        articles = Article.objects.filter(id__in=ids)
        deleted_count = articles.count()
        articles.delete()
        return Response({"detail": f"Đã xóa {deleted_count} bài viết."}, status=status.HTTP_200_OK)
class ArticleDetailBySlugView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('-createdAt')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'name', 'createdAt']
    ordering_fields = ['createdAt', 'name']
    ordering = ['-createdAt']
    pagination_class = OptionalLimitOffsetPagination
class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all().order_by('-createdAt')
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'title', 'category', 'createdAt']
    ordering_fields = ['createdAt', 'title']
    ordering = ['-createdAt']
    pagination_class = OptionalLimitOffsetPagination
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id', None)
        show_all = self.request.query_params.get('show_all', 'false').lower() == 'true'
        if not show_all:
            now = timezone.now()
            queryset = queryset.filter(postAt__lte=now)
        if category_id:
            queryset = queryset.filter(category=category_id)
        return queryset
class ArticleRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
class MiniAppOptionListCreateView(generics.ListCreateAPIView):
    queryset = MiniAppOption.objects.all()
    serializer_class = MiniAppOptionSerializer
    permission_classes = [IsAuthenticated]
class MiniAppOptionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MiniAppOption.objects.all()
    serializer_class = MiniAppOptionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
class ProvinceListView(APIView):
    def get(self, request):
        try:
            provinces = Province.objects.all()
            serializer = ProvinceSerializer(provinces, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ProvinceCreateView(APIView):
    def post(self, request):
        try:
            serializer = ProvinceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "SUCCESS",
                    "province_id": serializer.data['province_id']
                }, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ProvinceUpdateView(APIView):
    def put(self, request):
        try:
            province_id = request.data.get('province_id')
            if not province_id:
                return Response({"error": "province_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            province = Province.objects.get(province_id=province_id)
            serializer = ProvinceSerializer(province, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "SUCCESS",
                    "province_id": serializer.data['province_id']
                }, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Province.DoesNotExist:
            return Response({"error": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ProvinceDeleteView(APIView):
    def delete(self, request):
        try:
            province_id = request.query_params.get('province_id')
            if not province_id:
                return Response({"error": "province_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            province = Province.objects.get(province_id=province_id)
            province.delete()
            return Response({
                "status": "SUCCESS",
                "province_id": int(province_id)
            }, status=status.HTTP_200_OK)
        except Province.DoesNotExist:
            return Response({"error": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class DistrictListView(APIView):
    def get(self, request):
        try:
            province_id = request.query_params.get('province_id')
            districts = District.objects.all()
            if province_id:
                districts = districts.filter(province__province_id=province_id)
            serializer = DistrictSerializer(districts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class DistrictCreateView(APIView):
    def post(self, request):
        try:
            serializer = DistrictSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "SUCCESS",
                    "district_id": serializer.data['district_id']
                }, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class DistrictUpdateView(APIView):
    def put(self, request):
        try:
            district_id = request.data.get('district_id')
            if not district_id:
                return Response({"error": "district_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            district = District.objects.get(district_id=district_id)
            serializer = DistrictSerializer(district, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "SUCCESS",
                    "district_id": serializer.data['district_id']
                }, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except District.DoesNotExist:
            return Response({"error": "District not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class DistrictDeleteView(APIView):
    def delete(self, request):
        try:
            district_id = request.query_params.get('district_id')
            if not district_id:
                return Response({"error": "district_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            district = District.objects.get(district_id=district_id)
            district.delete()
            return Response({
                "status": "SUCCESS",
                "district_id": int(district_id)
            }, status=status.HTTP_200_OK)
        except District.DoesNotExist:
            return Response({"error": "District not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class WardListView(APIView):
    def get(self, request):
        try:
            district_id = request.query_params.get('district_id')
            wards = Ward.objects.all()
            if district_id:
                wards = wards.filter(district__district_id=district_id)
            serializer = WardSerializer(wards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class WardCreateView(APIView):
    def post(self, request):
        try:
            serializer = WardSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "SUCCESS",
                    "ward_id": serializer.data['ward_id']
                }, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class WardUpdateView(APIView):
    def put(self, request):
        try:
            ward_id = request.data.get('ward_id')
            if not ward_id:
                return Response({"error": "ward_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            ward = Ward.objects.get(ward_id=ward_id)
            serializer = WardSerializer(ward, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "SUCCESS",
                    "ward_id": serializer.data['ward_id']
                }, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Ward.DoesNotExist:
            return Response({"error": "Ward not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class WardDeleteView(APIView):
    def delete(self, request):
        try:
            ward_id = request.query_params.get('ward_id')
            if not ward_id:
                return Response({"error": "ward_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            ward = Ward.objects.get(ward_id=ward_id)
            ward.delete()
            return Response({
                "status": "SUCCESS",
                "ward_id": int(ward_id)
            }, status=status.HTTP_200_OK)
        except Ward.DoesNotExist:
            return Response({"error": "Ward not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LocationListView(APIView):
    def get(self, request):
        try:
            locations = Location.objects.all()
            serializer = LocationSerializer(locations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LocationCreateView(APIView):
    def post(self, request):
        try:
            serializer = LocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "SUCCESS",
                    "location_id": serializer.data['location_id']
                }, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LocationUpdateView(APIView):
    def put(self, request):
        try:
            location_id = request.data.get('location_id')
            if not location_id:
                return Response({"error": "location_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            location = Location.objects.get(location_id=location_id)
            serializer = LocationSerializer(location, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "SUCCESS",
                    "location_id": serializer.data['location_id']
                }, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LocationDeleteView(APIView):
    def delete(self, request):
        try:
            location_id = request.query_params.get('location_id')
            if not location_id:
                return Response({"error": "location_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            location = Location.objects.get(location_id=location_id)
            location.delete()
            return Response({
                "status": "SUCCESS",
                "location_id": int(location_id)
            }, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class StationListView(APIView):
    def get(self, request):
        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)
class StationCreateView(APIView):
    def post(self, request):
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "SUCCESS",
                "station_id": serializer.data['station_id']
            }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class StationUpdateView(APIView):
    def put(self, request):
        try:
            station = Station.objects.get(station_id=request.data.get('station_id'))
        except Station.DoesNotExist:
            return Response({"error": "Station not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StationSerializer(station, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "SUCCESS",
                "station_id": serializer.data['station_id']
            })
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class StationDeleteView(APIView):
    def delete(self, request):
        station_id = request.query_params.get('station_id')
        try:
            station = Station.objects.get(station_id=station_id)
            station.delete()
            return Response({
                "status": "SUCCESS",
                "station_id": int(station_id)
            })
        except Station.DoesNotExist:
            return Response({"error": "Station not found"}, status=status.HTTP_404_NOT_FOUND)
class TideMeasurementListView(APIView):
    def get(self, request):
        station_id = request.query_params.get('station_id')
        date = request.query_params.get('date')
        if not (station_id and date):
            return Response({"error": "station_id and date are required"}, status=status.HTTP_400_BAD_REQUEST)
        measurements = TideMeasurement.objects.filter(station_id=station_id, measurement_date=date)
        serializer = TideMeasurementSerializer(measurements, many=True)
        return Response(serializer.data)
class TideMeasurementLast10DaysView(APIView):
    def get(self, request):
        station_id = request.query_params.get('station_id')
        if not station_id:
            return Response({"error": "station_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        today = timezone.now().date()
        ten_days_ago = today - timedelta(days=10)
        measurements = TideMeasurement.objects.filter(
            station_id=station_id,
            measurement_date__gte=ten_days_ago  
        ).order_by('-measurement_date') 
        serializer = TideMeasurementSerializer(measurements, many=True)
        return Response(serializer.data)
class TideMeasurementCreateView(APIView):
    def post(self, request):
        serializer = TideMeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "SUCCESS",
                "measurement_id": serializer.data['measurement_id']
            }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class TideMeasurementUpdateView(APIView):
    def put(self, request):
        try:
            measurement = TideMeasurement.objects.get(measurement_id=request.data.get('measurement_id'))
        except TideMeasurement.DoesNotExist:
            return Response({"error": "Measurement not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TideMeasurementSerializer(measurement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "SUCCESS",
                "measurement_id": serializer.data['measurement_id']
            })
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class TideMeasurementDeleteView(APIView):
    def delete(self, request):
        measurement_id = request.query_params.get('measurement_id')
        try:
            measurement = TideMeasurement.objects.get(measurement_id=measurement_id)
            measurement.delete()
            return Response({
                "status": "SUCCESS",
                "measurement_id": int(measurement_id)
            })
        except TideMeasurement.DoesNotExist:
            return Response({"error": "Measurement not found"}, status=status.HTTP_404_NOT_FOUND)
class UserDetailView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "SUCCESS",
                "user_id": serializer.data['user_id']
            }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class UserUpdateView(APIView):
    def put(self, request):
        try:
            user = User.objects.get(user_id=request.data.get('user_id'))
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "SUCCESS",
                "user_id": serializer.data['user_id']
            })
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class UserDeleteView(APIView):
    def delete(self, request):
        user_id = request.query_params.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
            user.delete()
            return Response({
                "status": "SUCCESS",
                "user_id": user_id
            })
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
class PolicyListView(APIView):
    def get(self, request):
        policies = Policy.objects.all()
        serializer = PolicySerializer(policies, many=True)
        return Response(serializer.data)
class PolicyCreateView(APIView):
    def post(self, request):
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "SUCCESS",
                "policy_id": serializer.data['policy_id']
            }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class PolicyUpdateView(APIView):
    def put(self, request):
        try:
            policy = Policy.objects.get(policy_id=request.data.get('policy_id'))
        except Policy.DoesNotExist:
            return Response({"error": "Policy not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PolicySerializer(policy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "SUCCESS",
                "policy_id": serializer.data['policy_id']
            })
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class PolicyDeleteView(APIView):
    def delete(self, request):
        policy_id = request.query_params.get('policy_id')
        try:
            policy = Policy.objects.get(policy_id=policy_id)
            policy.delete()
            return Response({
                "status": "SUCCESS",
                "policy_id": int(policy_id)
            })
        except Policy.DoesNotExist:
            return Response({"error": "Policy not found"}, status=status.HTTP_404_NOT_FOUND)
class LocationSearchView(APIView):
    def get(self, request):
        ward_id = request.query_params.get('ward_id')
        if not ward_id:
            return Response({"error": "ward_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        locations = Location.objects.filter(ward_id=ward_id)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
class ZaloLocationView(APIView):
    def post(self, request):
        token = request.data.get('token')
        user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')
        if not (token and user_id and access_token):
            return Response(
                {"error": "token, user_id, and access_token are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            location_data = self.get_data_from_zalo(token, access_token)
            if not (location_data.get("latitude") and location_data.get("longitude")):
                raise Exception("Location data not found in response")

            location_result = {
                "provider": location_data.get("provider"),
                "latitude": location_data.get("latitude"),
                "longitude": location_data.get("longitude"),
                "timestamp": location_data.get("timestamp")
            }
            return Response(
                {
                    "status": "SUCCESS",
                    "location": location_result
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve location: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    def get_data_from_zalo(self, token, access_token):
        zalo_api_url = "https://graph.zalo.me/v2.0/me/info"
        secret_key = settings.SECRET_KEY
        if not secret_key:
            raise Exception("SECRET_KEY is not configured")
        headers = {
            "access_token": access_token,
            "code": token,
            "secret_key": secret_key
        }
        response = requests.get(zalo_api_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Zalo API error: {response.status_code}")
        response_data = response.json()
        if response_data.get("error") != 0:
            raise Exception(f"Zalo API error: {response_data.get('message', 'Unknown error')} (Code: {response_data.get('error')})")
        return response_data.get("data", {})
    
class ZaloPhoneView(APIView):
    def post(self, request):
        token = request.data.get('token')
        user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')
        if not (token and user_id and access_token):
            return Response(
                {"error": "token, user_id, and access_token are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            phone_data = self.get_data_from_zalo(token, access_token)
            phone_number = phone_data.get("number")
            if not phone_number:
                raise Exception("Phone number not found in response")
            user, created = User.objects.get_or_create(
                user_id=user_id,
                defaults={
                    "phone_number": phone_number,
                    "full_name": "",  
                    "location_permission": False,
                    "created_at": timezone.now(),
                }
            )
            if not created:
                user.phone_number = phone_number
                user.save()
            return Response(
                {
                    "status": "SUCCESS",
                    "phone_number": phone_number
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve phone number: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    def get_data_from_zalo(self, token, access_token):
        zalo_api_url = "https://graph.zalo.me/v2.0/me/info"
        secret_key = settings.SECRET_KEY
        if not secret_key:
            raise Exception("SECRET_KEY is not configured")
        headers = {
            "access_token": access_token,
            "code": token,
            "secret_key": secret_key
        }
        response = requests.get(zalo_api_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Zalo API error: {response.status_code}")
        response_data = response.json()
        if response_data.get("error") != 0:
            raise Exception(f"Zalo API error: {response_data.get('message', 'Unknown error')} (Code: {response_data.get('error')})")
        return response_data.get("data", {})
class ZaloUserInfoView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')  
        user_info = request.data.get('user_info')  
        if not (user_id and access_token and user_info):
            return Response(
                {"error": "user_id, access_token, and user_info are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            
            name = user_info.get("name", "")
            avatar = user_info.get("avatar", "")
            user, created = User.objects.get_or_create(
                user_id=user_id,
                defaults={
                    "phone_number": "",  
                    "full_name": name,
                    "avatar_url": avatar,
                    "location_permission": False,
                    "created_at": timezone.now(),
                }
            )

            if not created:
                user.full_name = name
                user.avatar_url = avatar
                user.save()

            return Response(
                {
                    "status": "SUCCESS",
                    "user_info": {
                        "user_id": user_id,
                        "full_name": name,
                        "avatar_url": avatar
                    }
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to process user info: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class Map4DReverseGeocodeView(APIView):
    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        if not lat or not lng:
            return Response({"error": "lat and lng are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            api_key = "3815de3fd2c9832724d9b975b5efdbea"
            url = f"https://api.map4d.vn/sdk/v2/geocode?key={api_key}&location={lat},{lng}"
            response = requests.get(url)
            data = response.json()
            if "result" not in data or len(data["result"]) == 0:
                return Response({"error": "No result found"}, status=status.HTTP_404_NOT_FOUND)
            address_components = data["result"][0].get("addressComponents", [])
            result = {}
            for comp in address_components:
                types = comp.get("types", [])
                if "admin_level_4" in types:
                    result["ward"] = comp.get("name")
                elif "admin_level_3" in types:
                    result["district"] = comp.get("name")
                elif "admin_level_2" in types:
                    result["province"] = comp.get("name")

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ZaloBasicInfoView(APIView):
    def post(self, request):
        data = request.data
        zalo_id = data.get("id")
        id_by_oa = data.get("idByOA")
        name = data.get("name", "")
        avatar = data.get("avatar", "")
        phone_number = data.get("phone_number", "")

        if not (zalo_id and id_by_oa):
            return Response(
                {"error": "Missing 'id' or 'idByOA'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user, created = User.objects.get_or_create(
            user_id=zalo_id,
            defaults={
                "idByOA": id_by_oa,
                "full_name": name,
                "avatar_url": avatar,
                "phone_number": phone_number,
                "created_at": timezone.now(),
            }
        )

        if not created:
            user.idByOA = id_by_oa
            user.full_name = name
            user.avatar_url = avatar
            user.phone_number = phone_number
            user.save()

        return Response({
            "status": "SUCCESS",
            "user_id": zalo_id,
            "idByOA": id_by_oa,
            "name": name,
            "avatar_url": avatar,
            "phone_number": phone_number,
        }, status=status.HTTP_200_OK)
   