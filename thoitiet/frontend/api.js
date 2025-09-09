import { getLocation } from 'zmp-sdk/apis';

const BASE_URL = 'http://localhost:8000/api/';

async function apiRequest(method, endpoint, data = null, queryParams = {}) {
    try {
        const url = new URL(`${BASE_URL}${endpoint}`);
        if (method === 'GET' && Object.keys(queryParams).length) {
            url.search = new URLSearchParams(queryParams).toString();
        }

        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data && ['POST', 'PUT'].includes(method)) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Something went wrong');
        }

        return result;
    } catch (error) {
        console.error(`API Error: ${endpoint}`, error);
        alert(error.message || 'Đã xảy ra lỗi, vui lòng thử lại!');
        throw error;
    }
}

// Province APIs
async function getProvinces() {
    return apiRequest('GET', 'provinces/');
}

async function createProvince(data) {
    return apiRequest('POST', 'provinces/create/', {
        name: data.name,
    });
}

async function updateProvince(data) {
    return apiRequest('PUT', 'provinces/update/', {
        id: data.id,
        name: data.name,
    });
}

async function deleteProvince(provinceId) {
    return apiRequest('DELETE', 'provinces/delete/', null, { id: provinceId });
}

// District APIs
async function getDistricts(provinceId = null) {
    return apiRequest('GET', 'districts/', null, provinceId ? { province_id: provinceId } : {});
}

async function createDistrict(data) {
    return apiRequest('POST', 'districts/create/', {
        name: data.name,
        province_id: data.provinceId,
    });
}

async function updateDistrict(data) {
    return apiRequest('PUT', 'districts/update/', {
        id: data.id,
        name: data.name,
        province_id: data.provinceId,
    });
}

async function deleteDistrict(districtId) {
    return apiRequest('DELETE', 'districts/delete/', null, { id: districtId });
}

// Ward APIs
async function getWards(districtId = null) {
    return apiRequest('GET', 'wards/', null, districtId ? { district_id: districtId } : {});
}

async function createWard(data) {
    return apiRequest('POST', 'wards/create/', {
        name: data.name,
        district_id: data.districtId,
    });
}

async function updateWard(data) {
    return apiRequest('PUT', 'wards/update/', {
        id: data.id,
        name: data.name,
        district_id: data.districtId,
    });
}

async function deleteWard(wardId) {
    return apiRequest('DELETE', 'wards/delete/', null, { id: wardId });
}

// Location APIs
async function getLocations() {
    return apiRequest('GET', 'location/');
}

async function createLocation(data) {
    return apiRequest('POST', 'location/create/', {
        latitude: data.latitude,
        longitude: data.longitude,
        ward_id: data.wardId,
    });
}

async function updateLocation(data) {
    return apiRequest('PUT', 'location/update/', {
        location_id: data.locationId,
        latitude: data.latitude,
        longitude: data.longitude,
        ward_id: data.wardId,
    });
}

async function deleteLocation(locationId) {
    return apiRequest('DELETE', 'location/delete/', null, { location_id: locationId });
}

async function searchLocations(wardId) {
    return apiRequest('GET', 'locations/search/', null, { ward_id: wardId });
}

// Station APIs
async function getStations() {
    return apiRequest('GET', 'tide/stations/');
}

async function createStation(data) {
    return apiRequest('POST', 'tide/stations/create/', {
        station_name: data.stationName,
    });
}

async function updateStation(data) {
    return apiRequest('PUT', 'tide/stations/update/', {
        station_id: data.stationId,
        station_name: data.stationName,
    });
}

async function deleteStation(stationId) {
    return apiRequest('DELETE', 'tide/stations/delete/', null, { station_id: stationId });
}

// TideMeasurement APIs
async function getTideMeasurements(stationId, date) {
    return apiRequest('GET', 'tide/measurements/', null, {
        station_id: stationId,
        date,
    });
}

async function createTideMeasurement(data) {
    return apiRequest('POST', 'tide/measurements/create/', {
        station_id: data.stationId,
        measurement_date: data.date,
        tide_type: data.tideType,
        water_level: data.waterLevel,
        time_of_occurrence: data.time,
    });
}

async function updateTideMeasurement(data) {
    return apiRequest('PUT', 'tide/measurements/update/', {
        measurement_id: data.measurementId,
        station_id: data.stationId,
        measurement_date: data.date,
        tide_type: data.tideType,
        water_level: data.waterLevel,
        time_of_occurrence: data.time,
    });
}

async function deleteTideMeasurement(measurementId) {
    return apiRequest('DELETE', 'tide/measurements/delete/', null, { measurement_id: measurementId });
}

async function syncTideData(data) {
    return apiRequest('POST', 'tide/sync/', {
        station_id: data.stationId,
        date: data.date,
    });
}

// User APIs
async function getUser(userId) {
    return apiRequest('GET', 'users/', null, { user_id: userId });
}

async function createUser(data) {
    return apiRequest('POST', 'users/create/', {
        user_id: data.userId,
        phone_number: data.phoneNumber,
        access_token: data.accessToken,
        full_name: data.fullName,
        email: data.email,
        avatar_url: data.avatarUrl,
        location_id: data.locationId,
        location_permission: data.locationPermission,
    });
}

async function updateUser(data) {
    return apiRequest('PUT', 'users/update/', {
        user_id: data.userId,
        phone_number: data.phoneNumber,
        full_name: data.fullName,
        email: data.email,
        avatar_url: data.avatarUrl,
        location_id: data.locationId,
        location_permission: data.locationPermission,
    });
}

async function deleteUser(userId) {
    return apiRequest('DELETE', 'users/delete/', null, { user_id: userId });
}

async function getUserNotifications(userId, limit = 50, offset = 0) {
    return apiRequest('GET', 'users/notifications/', null, {
        user_id: userId,
        limit,
        offset,
    });
}

// OAFollow APIs
async function createOAFollow(data) {
    return apiRequest('POST', 'zalo/oa/follows/create/', {
        user_id: data.userId,
        oa_id: data.oaId,
        follow_status: data.followStatus,
        followed_at: data.followedAt,
        source_app: data.sourceApp,
    });
}

async function getOAFollow(userId, oaId) {
    return apiRequest('GET', 'zalo/oa/follows/', null, { user_id: userId, oa_id: oaId });
}

async function updateOAFollow(data) {
    return apiRequest('PUT', 'zalo/oa/follows/update/', {
        follow_id: data.followId,
        follow_status: data.followStatus,
        source_app: data.sourceApp,
    });
}

async function deleteOAFollow(followId) {
    return apiRequest('DELETE', 'zalo/oa/follows/delete/', null, { follow_id: followId });
}

async function checkOAFollowStatus(userId, accessToken) {
    return apiRequest('GET', 'zalo/oa/followers/', null, {
        user_id: userId,
        access_token: accessToken,
    });
}

// ZNSNotification APIs
async function sendZNSNotification(data) {
    return apiRequest('POST', 'notifications/zns/create/', {
        user_id: data.userId,
        location_id: data.locationId,
        notification_type: data.notificationType,
        content: data.content,
    });
}

async function getZNSNotifications(userId, limit = 50, offset = 0) {
    return apiRequest('GET', 'notifications/zns/', null, {
        user_id: userId,
        limit,
        offset,
    });
}

async function deleteZNSNotification(notificationId) {
    return apiRequest('DELETE', 'notifications/zns/delete/', null, { notification_id: notificationId });
}

async function sendZNSBatch(data) {
    return apiRequest('POST', 'notifications/zns/batch/', {
        location_id: data.locationId,
        notification_type: data.notificationType,
        content: data.content,
    });
}

// LunarCalendar APIs
async function getLunarCalendar(solarDate) {
    return apiRequest('GET', 'calendar/lunar/', null, { solar_date: solarDate });
}

async function createLunarCalendar(data) {
    return apiRequest('POST', 'calendar/lunar/create/', {
        solar_date: data.solarDate,
        lunar_day: data.lunarDay,
        lunar_month: data.lunarMonth,
        lunar_year: data.lunarYear,
        is_leap_month: data.isLeapMonth,
        description: data.description,
    });
}

async function updateLunarCalendar(data) {
    return apiRequest('PUT', 'calendar/lunar/update/', {
        lunar_id: data.lunarId,
        solar_date: data.solarDate,
        lunar_day: data.lunarDay,
        lunar_month: data.lunarMonth,
        lunar_year: data.lunarYear,
        is_leap_month: data.isLeapMonth,
        description: data.description,
    });
}

async function deleteLunarCalendar(lunarId) {
    return apiRequest('DELETE', 'calendar/lunar/delete/', null, { lunar_id: lunarId });
}

async function syncLunarCalendar(data) {
    return apiRequest('POST', 'calendar/lunar/sync/', {
        start_date: data.startDate,
        end_date: data.endDate,
    });
}

// Policy APIs
async function getPolicies(policyType = null) {
    return apiRequest('GET', 'policies/', null, policyType ? { policy_type: policyType } : {});
}

async function createPolicy(data) {
    return apiRequest('POST', 'policies/create/', {
        policy_type: data.policyType,
        title: data.title,
        content: data.content,
    });
}

async function updatePolicy(data) {
    return apiRequest('PUT', 'policies/update/', {
        policy_id: data.policyId,
        policy_type: data.policyType,
        title: data.title,
        content: data.content,
    });
}

async function deletePolicy(policyId) {
    return apiRequest('DELETE', 'policies/delete/', null, { policy_id: policyId });
}

// Zalo APIs
async function requestLocationPermission(userId, accessToken) {
    try {
        const response = await apiRequest('GET', 'zalo/location/permission/', null, {
            access_token: accessToken,
            user_id: userId,
        });
        if (response.status === 'pending') {
            alert('Yêu cầu cấp quyền vị trí đã được gửi. Vui lòng xác nhận!');
        }
        return response;
    } catch (error) {
        console.error('Location Permission Error:', error);
    }
}

async function getLocationToken(userId, accessToken) {
    try {
        const response = await apiRequest('GET', 'zalo/location/token/', null, {
            access_token: accessToken,
            user_id: userId,
        });
        return response.token;
    } catch (error) {
        console.error('Get Location Token Error:', error);
    }
}

async function getUserLocation(userId, accessToken) {
    try {
        const { token } = await getLocation({
            success: (data) => data,
            fail: (error) => {
                handleLocationError(error);
                throw new Error('Failed to get location');
            }
        });
        
        const response = await apiRequest('GET', 'zalo/location/', null, {
            access_token: accessToken,
            token,
            user_id: userId,
        });

        if (response.latitude && response.longitude) {
            alert('Vị trí của bạn đã được lưu!');
        }
        return response;
    } catch (error) {
        console.error('Get User Location Error:', error);
    }
}

async function checkLocationError(userId, accessToken) {
    try {
        const response = await apiRequest('GET', 'zalo/location/error/', null, {
            access_token: accessToken,
            user_id: userId,
        });
        if (response.status === 'denied') {
            alert(response.message);
        }
        return response;
    } catch (error) {
        console.error('Check Location Error:', error);
    }
}

function handleLocationError(error) {
    if (error.code === -201 || error.code === -202 || error.code === -2002) {
        alert('Bạn đã từ chối cấp quyền vị trí. Vui lòng bật quyền trong cài đặt Zalo.');
    } else {
        alert('Đã xảy ra lỗi khi lấy vị trí. Vui lòng thử lại.');
    }
}

async function requestUserLocation() {
    const userId = '12345'; // Lấy từ Zalo SDK
    const accessToken = 'your_access_token'; // Lấy từ Zalo SDK

    try {
        const permissionResponse = await requestLocationPermission(userId, accessToken);
        if (permissionResponse.status !== 'pending') {
            alert(permissionResponse.message);
            return;
        }

        const token = await getLocationToken(userId, accessToken);
        if (!token) {
            alert('Không thể lấy token vị trí.');
            return;
        }

        const location = await getUserLocation(userId, accessToken);
        if (location.latitude && location.longitude) {
            alert(`Vị trí: (${location.latitude}, ${location.longitude})`);
        }
    } catch (error) {
        const errorResponse = await checkLocationError(userId, accessToken);
        alert(errorResponse.message);
    }
}

function denyLocation() {
    alert('Bạn đã từ chối cấp quyền vị trí. Vui lòng bật quyền trong cài đặt Zalo.');
}

export {
    getProvinces, createProvince, updateProvince, deleteProvince,
    getDistricts, createDistrict, updateDistrict, deleteDistrict,
    getWards, createWard, updateWard, deleteWard,
    getLocations, createLocation, updateLocation, deleteLocation, searchLocations,
    getStations, createStation, updateStation, deleteStation,
    getTideMeasurements, createTideMeasurement, updateTideMeasurement, deleteTideMeasurement, syncTideData,
    getUser, createUser, updateUser, deleteUser, getUserNotifications,
    createOAFollow, getOAFollow, updateOAFollow, deleteOAFollow, checkOAFollowStatus,
    sendZNSNotification, getZNSNotifications, deleteZNSNotification, sendZNSBatch,
    getLunarCalendar, createLunarCalendar, updateLunarCalendar, deleteLunarCalendar, syncLunarCalendar,
    getPolicies, createPolicy, updatePolicy, deletePolicy,
    requestLocationPermission, getLocationToken, getUserLocation, checkLocationError, requestUserLocation, denyLocation
};