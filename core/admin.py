from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import Province, District, Ward, Location, Station, TideMeasurement, User, Policy,Station
from datetime import datetime, timedelta
import pandas as pd

# Đăng ký các model cơ bản
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Ward)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Policy)
admin.site.register(Station)

class TideMeasurementResource(resources.ModelResource):
    station = fields.Field(
        column_name='station',
        attribute='station',
        widget=ForeignKeyWidget(Station, 'station_name')
    )
    measurement_date = fields.Field(
        column_name='measurement_date',
        attribute='measurement_date'
    )

    def before_import(self, dataset, **kwargs):
        """
        Hàm xử lý toàn bộ dataset trước khi import.
        """
        df = dataset.df  # Dataset được chuyển thành pandas DataFrame

        # Gán tên cột chuẩn
        expected_columns = [
            'station', 'measurement_date',
            'peak_level_1', 'peak_time_1', 'peak_level_2', 'peak_time_2',
            'low_level_1', 'low_time_1', 'low_level_2', 'low_time_2'
        ]
        df.columns = expected_columns[:len(df.columns)]

        # Ffill station nếu thiếu
        df['station'] = df['station'].ffill()

        # Xử lý measurement_date
        def chuan_hoa_ngay(x):
            if isinstance(x, str):
                parts = x.strip().split('/')
                if len(parts) == 2:
                    return f"{x}/2025"  # Bổ sung năm nếu chỉ có ngày/tháng
                return x
            return x

        df['measurement_date'] = df['measurement_date'].apply(chuan_hoa_ngay)
        df['measurement_date'] = pd.to_datetime(
            df['measurement_date'], format='%d/%m/%Y', errors='coerce'
        )
        df = df.dropna(subset=['measurement_date'])

        # Normalize time
        def normalize_time(t):
            try:
                if isinstance(t, str):
                    t = t.replace(',', '.').strip()
                    if ':' in t:
                        return pd.to_datetime(t, format="%H:%M").strftime("%H:%M:%S")
                    t = float(t)
                elif isinstance(t, (int, float)):
                    t = float(t)
                else:
                    return "00:00:00"

                hour = int(t)
                minute = int(round((t - hour) * 100))
                return f"{hour:02d}:{minute:02d}:00"
            except Exception:
                return "00:00:00"

        # Tạo DataFrame kết quả chuẩn hóa
        result = pd.DataFrame(columns=[
            'station', 'measurement_date', 'tide_type', 'water_level', 'time_of_occurrence'
        ])

        for idx, row in df.iterrows():
            station = row['station']
            date_str = row['measurement_date'].strftime("%Y-%m-%d")

            # PEAK
            for level, time in [(row['peak_level_1'], row['peak_time_1']), (row['peak_level_2'], row['peak_time_2'])]:
                if pd.notna(level) and pd.notna(time):
                    result.loc[len(result)] = [
                        station, date_str, 'PEAK', str(level).replace(',', '.'), normalize_time(time)
                    ]
            # LOW
            for level, time in [(row['low_level_1'], row['low_time_1']), (row['low_level_2'], row['low_time_2'])]:
                if pd.notna(level) and pd.notna(time):
                    result.loc[len(result)] = [
                        station, date_str, 'LOW', str(level).replace(',', '.'), normalize_time(time)
                    ]

        # Gán lại dataset.df để tiếp tục import
        dataset.df = result

    def before_import_row(self, row, **kwargs):
        """
        Xử lý measurement_date cho đúng format.
        """
        date_value = row.get('measurement_date')
        try:
            if isinstance(date_value, (int, float)) or str(date_value).isdigit():
                parsed_date = datetime(1899, 12, 30) + timedelta(days=int(float(date_value)))
            elif isinstance(date_value, datetime):
                parsed_date = date_value
            else:
                try:
                    parsed_date = datetime.strptime(date_value, "%Y-%m-%d")
                except ValueError:
                    parsed_date = datetime.strptime(date_value, "%m/%d/%Y")
            row['measurement_date'] = parsed_date.strftime("%Y-%m-%d")
        except Exception:
            raise Exception(f"Invalid date format for 'measurement_date': {date_value}")

    def before_save_instance(self, instance, row, **kwargs):
        # Ép measurement_date thành datetime.date
        instance.measurement_date = datetime.strptime(row['measurement_date'], "%Y-%m-%d").date()

    def get_instance(self, instance_loader, row):
        try:
            station = Station.objects.get(station_name=row.get('station'))
            date_value = row.get('measurement_date')
            time_value = row.get('time_of_occurrence')
            return TideMeasurement.objects.filter(
                station=station,
                measurement_date=date_value,
                time_of_occurrence=time_value
            ).first()
        except Station.DoesNotExist:
            raise Exception(f"Station '{row.get('station')}' does not exist!")

    class Meta:
        model = TideMeasurement
        import_id_fields = ['station', 'measurement_date', 'time_of_occurrence']
        fields = ('station', 'measurement_date', 'tide_type', 'water_level', 'time_of_occurrence')
        skip_unchanged = True
        report_skipped = True

# Admin giao diện cho TideMeasurement
@admin.register(TideMeasurement)
class TideMeasurementAdmin(ImportExportModelAdmin):
    resource_class = TideMeasurementResource
    list_display = ('station', 'measurement_date', 'tide_type', 'water_level', 'time_of_occurrence')
