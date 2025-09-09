from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.utils import timezone
from django.conf import settings

from .models import (
    Province, District, Ward, Location, Station, TideMeasurement, User,  Policy
)
from .serializers import (
    ProvinceSerializer, DistrictSerializer, WardSerializer, LocationSerializer, 
    StationSerializer, TideMeasurementSerializer, UserSerializer, PolicySerializer, 
    TideSyncSerializer
)
from .zalo_api import (
    get_user_location, check_oa_follow_status, request_location_permission,
    get_location_token, get_location_with_token, check_location_error
)
from django.db.models import Q
from datetime import datetime
import pytz
from rest_framework.exceptions import APIException


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
        # Lấy token, user_id, access_token từ body của Mini App
        token = request.data.get('token')
        user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')

        if not (token and user_id and access_token):
            return Response(
                {"error": "token, user_id, and access_token are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Gọi Zalo Open API để lấy dữ liệu vị trí
            location_data = self.get_data_from_zalo(token, access_token)

            # Xác thực dữ liệu vị trí
            if not (location_data.get("latitude") and location_data.get("longitude")):
                raise Exception("Location data not found in response")

            location_result = {
                "provider": location_data.get("provider"),
                "latitude": location_data.get("latitude"),
                "longitude": location_data.get("longitude"),
                "timestamp": location_data.get("timestamp")
            }

            # Trả về dữ liệu mà không lưu
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
        # Lấy token, user_id, access_token từ body của Mini App
        token = request.data.get('token')
        user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')

        if not (token and user_id and access_token):
            return Response(
                {"error": "token, user_id, and access_token are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Gọi Zalo Open API để lấy dữ liệu số điện thoại
            phone_data = self.get_data_from_zalo(token, access_token)

            # Xác thực dữ liệu số điện thoại
            phone_number = phone_data.get("number")
            if not phone_number:
                raise Exception("Phone number not found in response")

            # Lưu hoặc cập nhật thông tin người dùng
            user, created = User.objects.get_or_create(
                user_id=user_id,
                defaults={
                    "phone_number": phone_number,
                    "access_token": access_token,
                    "full_name": "",  # Để trống vì không có thông tin
                    "location_permission": False,
                    "created_at": timezone.now(),
                }
            )

            if not created:
                # Nếu người dùng đã tồn tại, cập nhật các trường cần thiết
                user.phone_number = phone_number
                user.access_token = access_token
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
        # URL của Zalo Open API
        zalo_api_url = "https://graph.zalo.me/v2.0/me/info"

        # Lấy secret_key từ biến môi trường
        secret_key = settings.SECRET_KEY
        if not secret_key:
            raise Exception("SECRET_KEY is not configured")

        # Tham số yêu cầu
        headers = {
            "access_token": access_token,
            "code": token,
            "secret_key": secret_key
        }

        # Gửi yêu cầu GET tới Zalo Open API
        response = requests.get(zalo_api_url, headers=headers)

        # Kiểm tra phản hồi từ Zalo
        if response.status_code != 200:
            raise Exception(f"Zalo API error: {response.status_code}")

        # Trích xuất dữ liệu từ phản hồi
        response_data = response.json()
        if response_data.get("error") != 0:
            raise Exception(f"Zalo API error: {response_data.get('message', 'Unknown error')} (Code: {response_data.get('error')})")

        return response_data.get("data", {})

class ZaloUserInfoView(APIView):
    def post(self, request):
        # Lấy user_id và access_token từ body của Mini App
        user_id = request.data.get('user_id')
        access_token = request.data.get('access_token')
        user_info = request.data.get('user_info')  # Dữ liệu từ getUserInfo()

        if not (user_id and access_token and user_info):
            return Response(
                {"error": "user_id, access_token, and user_info are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Trích xuất thông tin từ user_info
            name = user_info.get("name", "")
            avatar = user_info.get("avatar", "")

            # Lưu hoặc cập nhật thông tin người dùng
            user, created = User.objects.get_or_create(
                user_id=user_id,
                defaults={
                    "phone_number": "",  # Để trống nếu chưa có
                    "access_token": access_token,
                    "full_name": name,
                    "avatar_url": avatar,
                    "location_permission": False,
                    "created_at": timezone.now(),
                }
            )

            if not created:
                # Nếu người dùng đã tồn tại, cập nhật các trường cần thiết
                user.access_token = access_token
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