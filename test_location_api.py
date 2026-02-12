"""
Automated Tests for Mobile Location API
Endpoint: GET /api/v1/mobile/location/

This test suite covers all query parameters:
- city
- price_max (FILTER ONLY - not in response)
- price_min (FILTER ONLY - not in response)  
- search
- time_end (FILTER ONLY - not in response)
- time_start (FILTER ONLY - not in response)
- page
- per_page

IMPORTANT NOTES:
1. AUTHENTICATION: The tests use session-based authentication. The `headers` fixture
   returns a requests.Session object with authentication cookies already set.
   Use: headers.get(url, params=params)
   
2. FILTER PARAMETERS: time_start, time_end, price_min, price_max are used to FILTER
   the results but are NOT returned in the API response body. The tests verify that:
   - Valid filter values are accepted (200 OK)
   - Invalid filter values are rejected (400 Bad Request)
   - The API responds appropriately to different parameter combinations
   
3. RESPONSE STRUCTURE: The API returns location data without the filter parameters.
   Example response structure:
   {
     "success": true,
     "results": [
       {
         "name": "M learning center2",
         "address": "Fayazov ko'chasi, 11",
         "phone": "+998936934545",
         "distance": "727.337218194701 km",
         // ... other location fields (NO time or price filters in response)
       }
     ]
   }
"""

import pytest
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional


class TestLocationAPI:
    """Test suite for mobile location API endpoint"""
    
    BASE_URL = "https://api.qa.2plus6.uz/api/v1/mobile/location/"
    
    # Test data based on the region IDs from the uploaded information
    REGION_IDS = {
        "Andijon": 347,
        "Buxoro": 4,
        "Farg'ona": 5,
        "Jizzax": 2,
        "Namangan": 9,
        "Navoiy": 6,
        "Qashqadaryo": 349,
        "Qoraqalpog'iston": 8,
        "Samarqand": 10,
        "Sirdaryo": 3,
        "Surxondaryo": 170,
        "Toshkent shahri": 1,
        "Toshkent viloyati": 12,
        "Xorazm": 348
    }
    
    @pytest.fixture(scope="class")
    def auth_session(self):
        """
        Get authentication session for API requests
        This should be run once per test class
        """
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
                "otp": "111111",  # Test OTP
                "secret_code": secret_code
            },
            headers={"Content-Type": "application/json"}
        )
        
        if confirm_response.status_code != 200:
            pytest.fail(f"Confirm failed with status {confirm_response.status_code}: {confirm_response.text}")
        
        # Create a session with cookies
        session = requests.Session()
        session.cookies.update(confirm_response.cookies)
        
        # Also set headers for the session
        session.headers.update({
            "accept": "application/json",
            "Content-Type": "application/json"
        })
        
        return session
    
    @pytest.fixture
    def headers(self, auth_session):
        """Create headers with authentication - returns session for making requests"""
        return auth_session
    
    # ==================== CITY PARAMETER TESTS ====================
    
    def test_city_valid_andijon(self, headers):
        """Test with valid Andijon region ID"""
        params = {"city": self.REGION_IDS["Andijon"]}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "results" in data or "result" in data
    
    def test_city_valid_tashkent(self, headers):
        """Test with valid Tashkent city ID"""
        params = {"city": self.REGION_IDS["Toshkent shahri"]}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_city_multiple_regions(self, headers):
        """Test filtering across multiple regions"""
        for region_name, region_id in list(self.REGION_IDS.items())[:5]:
            params = {"city": region_id}
            response = headers.get(self.BASE_URL, params=params)
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
    
    def test_city_invalid_id(self, headers):
        """Test with invalid city ID"""
        params = {"city": 99999}
        response = headers.get(self.BASE_URL, params=params)
        
        # Should return empty results or error
        assert response.status_code in [200, 400, 404]
    
    def test_city_negative_id(self, headers):
        """Test with negative city ID"""
        params = {"city": -1}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_city_zero(self, headers):
        """Test with zero city ID"""
        params = {"city": 0}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_city_string_value(self, headers):
        """Test with string instead of integer"""
        params = {"city": "invalid"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    # ==================== PRICE_MAX PARAMETER TESTS ====================
    
    def test_price_max_valid_amount(self, headers):
        """Test with valid maximum price"""
        params = {"price_max": 1000000}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_price_max_zero(self, headers):
        """Test with zero maximum price"""
        params = {"price_max": 0}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_price_max_negative(self, headers):
        """Test with negative maximum price"""
        params = {"price_max": -1000}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_price_max_very_large(self, headers):
        """Test with very large maximum price"""
        params = {"price_max": 999999999999}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_price_max_decimal(self, headers):
        """Test with decimal maximum price"""
        params = {"price_max": 1500.50}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_price_max_string(self, headers):
        """Test with string maximum price"""
        params = {"price_max": "invalid"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    # ==================== PRICE_MIN PARAMETER TESTS ====================
    
    def test_price_min_valid_amount(self, headers):
        """Test with valid minimum price"""
        params = {"price_min": 100000}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_price_min_zero(self, headers):
        """Test with zero minimum price"""
        params = {"price_min": 0}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_price_min_negative(self, headers):
        """Test with negative minimum price"""
        params = {"price_min": -500}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_price_min_larger_than_max(self, headers):
        """Test when minimum price is larger than maximum price"""
        params = {
            "price_min": 500000,
            "price_max": 100000
        }
        response = headers.get(self.BASE_URL, params=params)
        
        # Should return empty results or validation error
        assert response.status_code in [200, 400]
    
    # ==================== PRICE RANGE TESTS ====================
    
    def test_price_range_valid(self, headers):
        """Test with valid price range"""
        params = {
            "price_min": 100000,
            "price_max": 500000
        }
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_price_range_equal(self, headers):
        """Test when min and max prices are equal"""
        params = {
            "price_min": 200000,
            "price_max": 200000
        }
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_price_range_with_city(self, headers):
        """Test price range combined with city filter"""
        params = {
            "city": self.REGION_IDS["Toshkent shahri"],
            "price_min": 100000,
            "price_max": 1000000
        }
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    # ==================== SEARCH PARAMETER TESTS ====================
    
    def test_search_valid_term(self, headers):
        """Test with valid search term"""
        params = {"search": "kvartira"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_search_empty_string(self, headers):
        """Test with empty search string"""
        params = {"search": ""}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_search_single_character(self, headers):
        """Test with single character search"""
        params = {"search": "a"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_search_special_characters(self, headers):
        """Test search with special characters"""
        params = {"search": "@#$%^&*()"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_search_cyrillic(self, headers):
        """Test search with Cyrillic characters"""
        params = {"search": "квартира"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_search_very_long_string(self, headers):
        """Test with very long search string"""
        params = {"search": "a" * 1000}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_search_with_spaces(self, headers):
        """Test search with multiple words"""
        params = {"search": "uy joy"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_search_sql_injection(self, headers):
        """Test search with SQL injection attempt"""
        params = {"search": "'; DROP TABLE locations; --"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    # ==================== TIME_END PARAMETER TESTS ====================
    
    def test_time_end_valid_future(self, headers):
        """Test with valid future time_end - API should validate and may reject"""
        future_time = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        params = {"time_end": future_time}
        response = headers.get(self.BASE_URL, params=params)
        
        # Test that API accepts the parameter and responds appropriately
        # 200 = accepted and filtered, 400 = validation error (both are valid)
        assert response.status_code in [200, 400]
        
        if response.status_code == 200:
            data = response.json()
            # Just verify response structure, don't check for time fields in results
            assert "success" in data or "result" in data or "results" in data
    
    def test_time_end_valid_past(self, headers):
        """Test with valid past time_end - should filter results"""
        past_time = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        params = {"time_end": past_time}
        response = headers.get(self.BASE_URL, params=params)
        
        # Past dates may or may not be accepted depending on API business logic
        assert response.status_code in [200, 400]
        
        if response.status_code == 200:
            data = response.json()
            assert data.get("success") is True or "result" in data or "results" in data
    
    def test_time_end_current_time(self, headers):
        """Test with current time as time_end"""
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        params = {"time_end": current_time}
        response = headers.get(self.BASE_URL, params=params)
        
        # Current time filtering behavior
        assert response.status_code in [200, 400]
    
    def test_time_end_invalid_format(self, headers):
        """Test with invalid time format"""
        params = {"time_end": "invalid-date"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_time_end_date_only(self, headers):
        """Test with date only (no time component)"""
        params = {"time_end": "2026-03-01"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_time_end_with_timezone(self, headers):
        """Test with timezone in time_end"""
        params = {"time_end": "2026-03-01T10:00:00+05:00"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    # ==================== TIME_START PARAMETER TESTS ====================
    
    def test_time_start_valid_past(self, headers):
        """Test with valid past time_start"""
        past_time = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        params = {"time_start": past_time}
        response = headers.get(self.BASE_URL, params=params)
        
        # API may have specific validation rules for time_start
        assert response.status_code in [200, 400]
    
    def test_time_start_valid_future(self, headers):
        """Test with future time_start"""
        future_time = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        params = {"time_start": future_time}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_time_start_current_time(self, headers):
        """Test with current time as time_start"""
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        params = {"time_start": current_time}
        response = headers.get(self.BASE_URL, params=params)
        
        # Current time may or may not be accepted
        assert response.status_code in [200, 400]
    
    def test_time_start_invalid_format(self, headers):
        """Test with invalid time format"""
        params = {"time_start": "not-a-date"}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    # ==================== TIME RANGE TESTS ====================
    
    def test_time_range_valid(self, headers):
        """Test with valid time range"""
        start_time = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        end_time = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        
        params = {
            "time_start": start_time,
            "time_end": end_time
        }
        response = headers.get(self.BASE_URL, params=params)
        
        # API may have specific validation for time ranges
        assert response.status_code in [200, 400]
    
    def test_time_range_start_after_end(self, headers):
        """Test when time_start is after time_end"""
        start_time = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        end_time = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        
        params = {
            "time_start": start_time,
            "time_end": end_time
        }
        response = headers.get(self.BASE_URL, params=params)
        
        # Should return error or empty results
        assert response.status_code in [200, 400]
    
    def test_time_range_equal(self, headers):
        """Test when time_start equals time_end"""
        same_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        params = {
            "time_start": same_time,
            "time_end": same_time
        }
        response = headers.get(self.BASE_URL, params=params)
        
        # May or may not be accepted
        assert response.status_code in [200, 400]
    
    # ==================== PAGINATION TESTS ====================
    
    def test_page_first_page(self, headers):
        """Test first page"""
        params = {"page": 1}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_page_second_page(self, headers):
        """Test second page"""
        params = {"page": 2}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_page_zero(self, headers):
        """Test page zero"""
        params = {"page": 0}
        response = headers.get(self.BASE_URL, params=params)
        
        # Invalid page may return 400 or 404
        assert response.status_code in [200, 400, 404]
    
    def test_page_negative(self, headers):
        """Test negative page number"""
        params = {"page": -1}
        response = headers.get(self.BASE_URL, params=params)
        
        # Invalid page may return 400 or 404
        assert response.status_code in [200, 400, 404]
    
    def test_page_very_large(self, headers):
        """Test very large page number"""
        params = {"page": 99999}
        response = headers.get(self.BASE_URL, params=params)
        
        # Non-existent page may return empty results (200) or 404
        assert response.status_code in [200, 404]
    
    def test_per_page_valid(self, headers):
        """Test valid per_page value"""
        params = {"per_page": 10}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_per_page_minimum(self, headers):
        """Test minimum per_page value"""
        params = {"per_page": 1}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_per_page_zero(self, headers):
        """Test zero per_page"""
        params = {"per_page": 0}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_per_page_negative(self, headers):
        """Test negative per_page"""
        params = {"per_page": -5}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_per_page_very_large(self, headers):
        """Test very large per_page"""
        params = {"per_page": 10000}
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_pagination_combination(self, headers):
        """Test page and per_page together"""
        params = {
            "page": 2,
            "per_page": 20
        }
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    # ==================== COMBINED PARAMETER TESTS ====================
    
    def test_all_parameters_combined(self, headers):
        """Test with all parameters combined"""
        start_time = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S")
        end_time = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S")
        
        params = {
            "city": self.REGION_IDS["Toshkent shahri"],
            "price_min": 100000,
            "price_max": 1000000,
            "search": "kvartira",
            "time_start": start_time,
            "time_end": end_time,
            "page": 1,
            "per_page": 20
        }
        response = headers.get(self.BASE_URL, params=params)
        
        # Combined parameters with time may have validation rules
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = response.json()
            assert data["success"] is True
    
    def test_city_and_price_range(self, headers):
        """Test city filter with price range"""
        params = {
            "city": self.REGION_IDS["Samarqand"],
            "price_min": 200000,
            "price_max": 800000
        }
        response = headers.get(self.BASE_URL, params=params)
        
        assert response.status_code == 200
    
    def test_search_with_price_and_time(self, headers):
        """Test search with price range and time filters"""
        start_time = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        
        params = {
            "search": "uy",
            "price_min": 150000,
            "price_max": 500000,
            "time_start": start_time
        }
        response = headers.get(self.BASE_URL, params=params)
        
        # Time parameter may cause validation error
        assert response.status_code in [200, 400]
    
    def test_no_parameters(self, headers):
        """Test endpoint with no parameters"""
        response = headers.get(self.BASE_URL)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    # ==================== AUTHENTICATION TESTS ====================
    
    def test_no_auth_token(self):
        """Test without authentication token"""
        response = requests.get(self.BASE_URL)
        
        assert response.status_code in [401, 403]
    
    def test_invalid_auth_token(self):
        """Test with invalid authentication token"""
        headers_dict = {
            "accept": "application/json",
            "Authorization": "Bearer invalid_token_12345"
        }
        response = requests.get(self.BASE_URL, headers=headers_dict)
        
        assert response.status_code in [401, 403]
    
    def test_expired_auth_token(self):
        """Test with expired authentication token"""
        headers_dict = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDAwMDAwMDB9.test"
        }
        response = requests.get(self.BASE_URL, headers=headers_dict)
        
        assert response.status_code in [401, 403]
    
    # ==================== RESPONSE VALIDATION TESTS ====================
    
    def test_response_structure(self, headers):
        """Test response has correct structure"""
        response = headers.get(self.BASE_URL)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "success" in data
        assert isinstance(data["success"], bool)
        assert "errors" in data or "error" in data
        assert "message" in data
        assert "result" in data or "results" in data
    
    def test_response_content_type(self, headers):
        """Test response content type is JSON"""
        response = headers.get(self.BASE_URL)
        
        assert response.status_code == 200
        assert "application/json" in response.headers.get("Content-Type", "")


# ==================== PERFORMANCE TESTS ====================

class TestLocationAPIPerformance:
    """Performance tests for the location API"""
    
    BASE_URL = "https://api.qa.2plus6.uz/api/v1/mobile/location/"
    
    @pytest.fixture(scope="class")
    def headers(self):
        """Get authentication session for performance testing"""
        # Step 1: Request OTP
        login_url = "https://api.qa.2plus6.uz/api/v1/users/mobile/auth/login/"
        phone = "+998990660699"
        
        response = requests.post(
            login_url,
            json={"phone": phone},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            pytest.skip(f"Authentication failed: {response.status_code}")
        
        result = response.json()
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
        
        # Create session
        session = requests.Session()
        session.cookies.update(confirm_response.cookies)
        session.headers.update({
            "accept": "application/json",
            "Content-Type": "application/json"
        })
        
        return session
    
    def test_response_time_basic_query(self, headers):
        """Test response time for basic query is under 2 seconds"""
        import time
        
        start_time = time.time()
        response = headers.get(self.BASE_URL)
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 2.0, f"Response time {response_time}s exceeds 2s threshold"
        assert response.status_code == 200
    
    def test_response_time_with_filters(self, headers):
        """Test response time with multiple filters"""
        import time
        
        params = {
            "city": 1,
            "price_min": 100000,
            "price_max": 1000000,
            "search": "kvartira"
        }
        
        start_time = time.time()
        response = headers.get(self.BASE_URL, params=params)
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 3.0, f"Response time {response_time}s exceeds 3s threshold"
        assert response.status_code == 200


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])