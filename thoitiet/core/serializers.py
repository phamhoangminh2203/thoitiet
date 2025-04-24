from rest_framework import serializers
from .models import (
    Province, District, Ward, Location, Station, TideMeasurement, User, Policy
)
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['province_id', 'name']

class DistrictSerializer(serializers.ModelSerializer):
    province_id = serializers.IntegerField(source='province.province_id', read_only=True)

    class Meta:
        model = District
        fields = ['district_id', 'name', 'province_id']

class WardSerializer(serializers.ModelSerializer):
    district_id = serializers.IntegerField(source='district.district_id', read_only=True)

    class Meta:
        model = Ward
        fields = ['ward_id', 'name', 'district_id']

class LocationSerializer(serializers.ModelSerializer):
    ward_id = serializers.IntegerField(write_only=True, required=False)
    ward = WardSerializer(read_only=True)

    class Meta:
        model = Location
        fields = ['location_id', 'latitude', 'longitude', 'ward_id', 'ward']

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['station_id', 'station_name']

class TideMeasurementSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='station.station_name', read_only=True)

    class Meta:
        model = TideMeasurement
        fields = [
            'measurement_id', 'station_id', 'station_name', 'measurement_date',
            'tide_type', 'water_level', 'time_of_occurrence'
        ]

class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'user_id', 'phone_number', 'access_token', 'full_name', 'email',
            'avatar_url', 'location', 'location_id', 'location_permission'
        ]


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['policy_id',  'title', 'content', 'updated_at']

class TideSyncSerializer(serializers.Serializer):
    station_id = serializers.IntegerField()
    date = serializers.DateField()


