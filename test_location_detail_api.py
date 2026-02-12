"""
Automated Tests for Mobile Location Detail API
Endpoint: GET /api/v1/mobile/location/{id}/

This test suite covers the location detail endpoint that returns
full information about a specific location including:
- Basic info (name, phone, description, address)
- Courses with pricing
- Working days/hours schedule
- Gallery images
- Distance
"""

import pytest
import requests
from typing import Dict


class TestLocationDetailAPI:
    """Test suite for location detail endpoint"""
    
    BASE_URL = "https://api.qa.2plus6.uz/api/v1/mobile/location"
    
    # Test location IDs based on the example
    VALID_LOCATION_ID = 4  # "Toshkent Test" from your example
    
    @pytest.fixture(scope="class")
    def auth_session(self):
        """Get authentication session for API requests"""
        # Step 1: Request OTP
        login_url = "https://api.qa.2plus6.uz/api/v1/users/mobile/auth/login/"
        phone = "+998990660699"
        
        response = requests.post(
            login_url,
            json={"phone": phone},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            pytest.fail(f"Login failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        if not result.get("success"):
            pytest.fail(f"Login failed: {result}")
        
        secret_code = result["result"]["secret_code"]
        
        # Step 2: Confirm OTP
        confirm_url = "https://api.qa.2plus6.uz/api/v1/users/mobile/auth/login/confirm/"
        confirm_response = requests.post(
            confirm_url,
            json={
                "phone": phone,
                "otp": "111111",
                "secret_code": secret_code
            },
            headers={"Content-Type": "application/json"}
        )
        
        if confirm_response.status_code != 200:
            pytest.fail(f"Confirm failed with status {confirm_response.status_code}")
        
        # Create a session with cookies
        session = requests.Session()
        session.cookies.update(confirm_response.cookies)
        session.headers.update({
            "accept": "application/json",
            "Content-Type": "application/json"
        })
        
        return session
    
    @pytest.fixture
    def headers(self, auth_session):
        """Create headers with authentication - returns session"""
        return auth_session
    
    # ==================== BASIC ENDPOINT TESTS ====================
    
    def test_get_valid_location_detail(self, headers):
        """Test getting details for a valid location ID"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "result" in data
    
    def test_location_detail_response_structure(self, headers):
        """Test that location detail has correct structure"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        result = data["result"]
        
        # Check required fields
        assert "name" in result
        assert "phone" in result
        assert "address" in result
        assert "courses" in result
        assert "working_days" in result
        assert "galleries" in result
        assert "distance" in result
    
    def test_invalid_location_id(self, headers):
        """Test with non-existent location ID"""
        url = f"{self.BASE_URL}/99999/"
        response = headers.get(url)
        
        assert response.status_code in [404, 400]
    
    def test_negative_location_id(self, headers):
        """Test with negative location ID"""
        url = f"{self.BASE_URL}/-1/"
        response = headers.get(url)
        
        assert response.status_code in [404, 400]
    
    def test_zero_location_id(self, headers):
        """Test with zero location ID"""
        url = f"{self.BASE_URL}/0/"
        response = headers.get(url)
        
        assert response.status_code in [404, 400]
    
    def test_string_location_id(self, headers):
        """Test with string instead of integer ID"""
        url = f"{self.BASE_URL}/invalid/"
        response = headers.get(url)
        
        assert response.status_code in [404, 400]
    
    # ==================== ADDRESS FIELD TESTS ====================
    
    def test_address_field_structure(self, headers):
        """Test address field contains required data"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        address = data["result"]["address"]
        
        assert "longitude" in address
        assert "latitude" in address
        assert "address_line" in address
        
        # Validate coordinate types
        assert isinstance(address["longitude"], (int, float))
        assert isinstance(address["latitude"], (int, float))
        assert isinstance(address["address_line"], str)
    
    def test_address_coordinates_valid_range(self, headers):
        """Test that coordinates are in valid geographic range"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        address = data["result"]["address"]
        
        # Valid latitude: -90 to 90
        assert -90 <= address["latitude"] <= 90
        
        # Valid longitude: -180 to 180
        assert -180 <= address["longitude"] <= 180
    
    # ==================== COURSES FIELD TESTS ====================
    
    def test_courses_field_is_array(self, headers):
        """Test courses field is an array"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        courses = data["result"]["courses"]
        
        assert isinstance(courses, list)
    
    def test_course_structure(self, headers):
        """Test each course has required fields"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        courses = data["result"]["courses"]
        
        if len(courses) > 0:
            course = courses[0]
            assert "id" in course
            assert "name" in course
            assert "name_uz" in course
            assert "name_ru" in course
            assert "month_payment" in course
            
            # Validate types
            assert isinstance(course["id"], int)
            assert isinstance(course["month_payment"], (int, float))
    
    def test_course_payment_is_positive(self, headers):
        """Test course payment amounts are positive or zero"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        courses = data["result"]["courses"]
        
        for course in courses:
            assert course["month_payment"] >= 0
    
    # ==================== WORKING DAYS TESTS ====================
    
    def test_working_days_field_is_array(self, headers):
        """Test working_days field is an array"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        working_days = data["result"]["working_days"]
        
        assert isinstance(working_days, list)
    
    def test_working_days_has_7_days(self, headers):
        """Test working_days contains all 7 days of week"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        working_days = data["result"]["working_days"]
        
        # Should have 7 days (Monday=1 to Sunday=7)
        assert len(working_days) == 7
        
        # Check all days 1-7 are present
        days = [day["day"] for day in working_days]
        assert sorted(days) == [1, 2, 3, 4, 5, 6, 7]
    
    def test_working_day_structure(self, headers):
        """Test each working day has required fields"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        working_days = data["result"]["working_days"]
        
        for day_info in working_days:
            assert "id" in day_info
            assert "day" in day_info
            assert "is_working_day" in day_info
            assert "open_at" in day_info
            assert "close_at" in day_info
            
            # Validate types
            assert isinstance(day_info["day"], int)
            assert isinstance(day_info["is_working_day"], bool)
            assert 1 <= day_info["day"] <= 7
    
    def test_working_day_time_format(self, headers):
        """Test working hours are in HH:MM:SS format"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        working_days = data["result"]["working_days"]
        
        import re
        time_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')
        
        for day_info in working_days:
            assert time_pattern.match(day_info["open_at"])
            assert time_pattern.match(day_info["close_at"])
    
    def test_non_working_day_hours(self, headers):
        """Test non-working days have 00:00:00 hours"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        working_days = data["result"]["working_days"]
        
        for day_info in working_days:
            if not day_info["is_working_day"]:
                # Non-working days should have 00:00:00
                assert day_info["open_at"] == "00:00:00"
                assert day_info["close_at"] == "00:00:00"
    
    # ==================== GALLERIES TESTS ====================
    
    def test_galleries_field_is_array(self, headers):
        """Test galleries field is an array"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        galleries = data["result"]["galleries"]
        
        assert isinstance(galleries, list)
    
    def test_gallery_structure(self, headers):
        """Test each gallery item has required fields"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        galleries = data["result"]["galleries"]
        
        if len(galleries) > 0:
            gallery = galleries[0]
            assert "is_main" in gallery
            assert "file_url" in gallery
            
            # Validate types
            assert isinstance(gallery["is_main"], bool)
            assert isinstance(gallery["file_url"], str)
    
    def test_gallery_url_format(self, headers):
        """Test gallery URLs are valid"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        galleries = data["result"]["galleries"]
        
        for gallery in galleries:
            # Should start with http:// or https://
            assert gallery["file_url"].startswith(("http://", "https://"))
    
    def test_has_main_gallery_image(self, headers):
        """Test there is at least one main gallery image"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        galleries = data["result"]["galleries"]
        
        if len(galleries) > 0:
            main_images = [g for g in galleries if g["is_main"]]
            # Should have at least one main image
            assert len(main_images) >= 1
    
    # ==================== DISTANCE FIELD TESTS ====================
    
    def test_distance_field_exists(self, headers):
        """Test distance field is present"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        result = data["result"]
        
        assert "distance" in result
    
    def test_distance_is_numeric(self, headers):
        """Test distance is a numeric value"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        distance = data["result"]["distance"]
        
        assert isinstance(distance, (int, float))
    
    def test_distance_is_non_negative(self, headers):
        """Test distance is not negative"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        distance = data["result"]["distance"]
        
        assert distance >= 0
    
    # ==================== AUTHENTICATION TESTS ====================
    
    def test_detail_without_auth(self):
        """Test accessing location detail without authentication"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = requests.get(url)
        
        assert response.status_code in [401, 403]
    
    def test_detail_with_invalid_auth(self):
        """Test with invalid authentication token"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        headers_dict = {
            "accept": "application/json",
            "Authorization": "Bearer invalid_token"
        }
        response = requests.get(url, headers=headers_dict)
        
        assert response.status_code in [401, 403]
    
    # ==================== PHONE FIELD TESTS ====================
    
    def test_phone_format(self, headers):
        """Test phone number format"""
        url = f"{self.BASE_URL}/{self.VALID_LOCATION_ID}/"
        response = headers.get(url)
        
        assert response.status_code == 200
        data = response.json()
        phone = data["result"]["phone"]
        
        # Should start with + and contain only digits after that
        assert phone.startswith("+")
        assert phone[1:].replace(" ", "").isdigit() or phone[1:].isdigit()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])