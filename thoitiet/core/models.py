from django.db import models
from django.utils import timezone


class Province(models.Model):
    province_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'provinces'

    def __str__(self):
        return self.name

class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        db_table = 'districts'

    def __str__(self):
        return self.name

class Ward(models.Model):
    ward_id = models.AutoField(primary_key=True)  # ✅ sửa từ wards_id → ward_id
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='wards')

    class Meta:
        db_table = 'wards'

    def __str__(self):
        return self.name

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    ward = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.SET_NULL, related_name='locations')

    class Meta:
        db_table = 'locations'
        unique_together = ('latitude', 'longitude')

    def __str__(self):
        return f"({self.latitude}, {self.longitude}) - Ward: {self.ward.name if self.ward else 'N/A'}"


class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'station'

    def __str__(self):
        return self.station_name

class TideMeasurement(models.Model):
    class TideType(models.TextChoices):
        PEAK = 'PEAK', 'Đỉnh triều'
        LOW = 'LOW', 'Chân triều'

    measurement_id = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    measurement_date = models.DateField()
    tide_type = models.CharField(max_length=4, choices=TideType.choices)
    water_level = models.FloatField()
    time_of_occurrence = models.TimeField()

    class Meta:
        db_table = 'tide_measurement'

    def __str__(self):
        return f"{self.station.station_name} - {self.measurement_date} - {self.tide_type}"

class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    phone_number = models.CharField(max_length=20)
    access_token = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    location_permission = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'users'  # Tên bảng (điều chỉnh nếu tên bảng thực tế khác)

    def __str__(self):
        return self.user_id


class Policy(models.Model):
    policy_id = models.AutoField(primary_key=True)
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'policies'

    def __str__(self):
        return self.title