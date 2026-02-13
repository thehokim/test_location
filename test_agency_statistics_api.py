import pytest
import requests
from datetime import datetime, timedelta
from typing import Dict, List


class TestAgencyStatisticsAPI:
    """Test suite for agency statistics endpoints"""
    
    BASE_URL = "https://api.qa.2plus6.uz/api/v1/statistics/agency"
    
    LANGUAGE_IDS = {
        "English": 1,
        "German": 4,
        "French": 3,
        "Japanese": 6,
        "Korean": 7,
        "Chinese": 5
    }
    
    CITY_IDS = {
        "Tashkent": 1,
        "Jizzakh": 2,
        "Sirdaryo": 3,
        "Bukhara": 4,
        "Fergana": 5,
        "Navoiy": 6,
        "Karakalpakstan": 8,
        "Namangan": 9,
        "Samarqand": 10,
        "Tashkent_Region": 12,
        "Surxondaryo": 170,
        "Andijon": 347,
        "Xorazm": 348,
        "Qashqadaryo": 349
    }
    
    DISTRICT_IDS = [17, 21, 237, 238, 239, 240, 241, 242, 243, 244]
    
    @pytest.fixture(scope="class")
    def auth_session(self):
        """Get authentication session for agency API"""
        login_url = "https://api.qa.2plus6.uz/api/v1/agency/auth/login/"
        
        credentials = {
            "username": "yiaadmin@2plus6.uz",
            "password": "_b#1mv5^X2T0"
        }
        
        response = requests.post(
            login_url,
            json=credentials,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            pytest.fail(f"Login failed with status {response.status_code}: {response.text}")
        
        session = requests.Session()
        session.cookies.update(response.cookies)
        session.headers.update({
            "accept": "application/json",
            "Content-Type": "application/json"
        })
        
        return session
    
    @pytest.fixture
    def session(self, auth_session):
        """Return authenticated session"""
        return auth_session
    
    
    def test_application_learning_center_card(self, session):
        """Test application learning center card endpoint"""
        url = f"{self.BASE_URL}/application-learning-center/card/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data or isinstance(data, (dict, list))
    
    def test_application_learning_center_company_card(self, session):
        """Test application learning center company card endpoint"""
        url = f"{self.BASE_URL}/application-learning-center/company/card/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data or isinstance(data, (dict, list))
    
    def test_application_student_card(self, session):
        """Test application student card endpoint"""
        url = f"{self.BASE_URL}/application-student/card/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data or isinstance(data, (dict, list))
    
    def test_student_card(self, session):
        """Test student card endpoint"""
        url = f"{self.BASE_URL}/student/card/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data or isinstance(data, (dict, list))
    
    def test_learning_center_city_no_params(self, session):
        """Test learning center city statistics without parameters"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
    
    def test_learning_center_city_with_single_city(self, session):
        """Test with single city parameter"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"city": self.CITY_IDS["Tashkent"]}
        response = session.get(url, params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
    
    def test_learning_center_city_with_district(self, session):
        """Test with city and district parameters"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "district": 17
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_learning_center_city_with_languages(self, session):
        """Test with languages parameter"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "languages": [1, 3, 4]  
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_learning_center_city_with_dates(self, session):
        """Test with start_date and end_date"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {
            "start_date": "2026-01-01",
            "end_date": "2026-12-31"
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_learning_center_city_all_params(self, session):
        """Test with all parameters combined"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "district": 17,
            "languages": [1, 3],
            "start_date": "2026-01-01",
            "end_date": "2026-12-31"
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_learning_center_city_invalid_city(self, session):
        """Test with invalid city ID"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"city": 99999}
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400, 404]
    
    def test_learning_center_city_multiple_languages(self, session):
        """Test with multiple language IDs"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {
            "languages": [1, 3, 4, 5, 6, 7]  
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    
    def test_learning_center_district_no_params(self, session):
        """Test learning center district statistics without parameters"""
        url = f"{self.BASE_URL}/learning-center-statistic/district/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
    
    def test_learning_center_district_with_city(self, session):
        """Test district endpoint with city parameter"""
        url = f"{self.BASE_URL}/learning-center-statistic/district/"
        params = {"city": self.CITY_IDS["Tashkent"]}
        response = session.get(url, params=params)
        
        assert response.status_code == 200
    
    def test_learning_center_district_with_district(self, session):
        """Test with specific district"""
        url = f"{self.BASE_URL}/learning-center-statistic/district/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "district": 17
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_learning_center_district_with_languages(self, session):
        """Test district with languages filter"""
        url = f"{self.BASE_URL}/learning-center-statistic/district/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "languages": [1, 4]  
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_learning_center_district_all_params(self, session):
        """Test district with all parameters"""
        url = f"{self.BASE_URL}/learning-center-statistic/district/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "district": 17,
            "languages": [1],
            "start_date": "2026-01-01",
            "end_date": "2026-12-31"
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_learning_center_neighbor_no_params(self, session):
        """Test learning center neighbor/neighbourhood statistics"""
        url = f"{self.BASE_URL}/learning-center-statistic/neighbor/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
    
    def test_learning_center_neighbor_with_city(self, session):
        """Test neighbor endpoint with city"""
        url = f"{self.BASE_URL}/learning-center-statistic/neighbor/"
        params = {"city": self.CITY_IDS["Tashkent"]}
        response = session.get(url, params=params)
        
        assert response.status_code == 200
    
    def test_learning_center_neighbor_with_district(self, session):
        """Test neighbor with city and district"""
        url = f"{self.BASE_URL}/learning-center-statistic/neighbor/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "district": 17
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_learning_center_neighbor_with_languages(self, session):
        """Test neighbor with languages"""
        url = f"{self.BASE_URL}/learning-center-statistic/neighbor/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "languages": [1, 3, 4]
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_learning_center_neighbor_all_params(self, session):
        """Test neighbor with all parameters"""
        url = f"{self.BASE_URL}/learning-center-statistic/neighbor/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "district": 17,
            "languages": [1, 4],
            "start_date": "2026-01-01",
            "end_date": "2026-12-31"
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_student_age_city_no_params(self, session):
        """Test student age statistics by city"""
        url = f"{self.BASE_URL}/student-statistic/age/city/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
    
    def test_student_age_city_with_city(self, session):
        """Test student age city with city parameter"""
        url = f"{self.BASE_URL}/student-statistic/age/city/"
        params = {"city": self.CITY_IDS["Tashkent"]}
        response = session.get(url, params=params)
        
        assert response.status_code == 200
    
    def test_student_age_city_with_languages(self, session):
        """Test student age city with languages"""
        url = f"{self.BASE_URL}/student-statistic/age/city/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "languages": [1, 3, 4]
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_student_age_city_all_params(self, session):
        """Test student age city with all parameters"""
        url = f"{self.BASE_URL}/student-statistic/age/city/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "district": 17,
            "languages": [1],
            "start_date": "2026-01-01",
            "end_date": "2026-12-31"
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_student_age_district_no_params(self, session):
        """Test student age statistics by district"""
        url = f"{self.BASE_URL}/student-statistic/age/district/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
    
    def test_student_age_district_with_params(self, session):
        """Test student age district with parameters"""
        url = f"{self.BASE_URL}/student-statistic/age/district/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "district": 17
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_student_age_district_with_languages(self, session):
        """Test student age district with languages"""
        url = f"{self.BASE_URL}/student-statistic/age/district/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "languages": [1, 4]
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_student_age_neighbourhood_no_params(self, session):
        """Test student age statistics by neighbourhood"""
        url = f"{self.BASE_URL}/student-statistic/age/neighbourhood/"
        response = session.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))
    
    def test_student_age_neighbourhood_with_params(self, session):
        """Test student age neighbourhood with parameters"""
        url = f"{self.BASE_URL}/student-statistic/age/neighbourhood/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "district": 17
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_student_age_neighbourhood_with_languages(self, session):
        """Test student age neighbourhood with languages"""
        url = f"{self.BASE_URL}/student-statistic/age/neighbourhood/"
        params = {
            "city": self.CITY_IDS["Tashkent"],
            "languages": [1, 3, 4, 5]
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]

    
    def test_languages_single_english(self, session):
        """Test with single English language"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"languages": [1]}  
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_languages_multiple(self, session):
        """Test with multiple languages"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"languages": [1, 3, 4, 5, 6, 7]}  
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_languages_invalid_id(self, session):
        """Test with invalid language ID"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"languages": [999]}
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_languages_empty_array(self, session):
        """Test with empty languages array"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"languages": []}
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_city_tashkent(self, session):
        """Test with Tashkent city"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"city": 1}
        response = session.get(url, params=params)
        
        assert response.status_code == 200
    
    def test_city_multiple_regions(self, session):
        """Test with different city IDs"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        
        for city_name, city_id in list(self.CITY_IDS.items())[:5]:
            params = {"city": city_id}
            response = session.get(url, params=params)
            assert response.status_code == 200
    
    def test_city_invalid(self, session):
        """Test with invalid city ID"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"city": 99999}
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400, 404]
    
    def test_city_negative(self, session):
        """Test with negative city ID"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"city": -1}
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_city_zero(self, session):
        """Test with zero city ID"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"city": 0}
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_district_valid(self, session):
        """Test with valid district ID"""
        url = f"{self.BASE_URL}/learning-center-statistic/district/"
        params = {
            "city": 1,
            "district": 17
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_district_without_city(self, session):
        """Test district without city parameter"""
        url = f"{self.BASE_URL}/learning-center-statistic/district/"
        params = {"district": 17}
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_district_invalid(self, session):
        """Test with invalid district ID"""
        url = f"{self.BASE_URL}/learning-center-statistic/district/"
        params = {
            "city": 1,
            "district": 99999
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400, 404]
    
    def test_dates_valid_range(self, session):
        """Test with valid date range"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {
            "start_date": "2026-01-01",
            "end_date": "2026-12-31"
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_dates_start_only(self, session):
        """Test with only start_date"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"start_date": "2026-01-01"}
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_dates_end_only(self, session):
        """Test with only end_date"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {"end_date": "2026-12-31"}
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_dates_invalid_format(self, session):
        """Test with invalid date format"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {
            "start_date": "invalid-date",
            "end_date": "2026-12-31"
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_dates_start_after_end(self, session):
        """Test when start_date is after end_date"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        params = {
            "start_date": "2026-12-31",
            "end_date": "2026-01-01"
        }
        response = session.get(url, params=params)
        
        assert response.status_code in [200, 400]
    
    def test_without_authentication(self):
        """Test accessing endpoint without authentication"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        response = requests.get(url)
        
        assert response.status_code in [401, 403]
    
    def test_invalid_session(self):
        """Test with invalid session"""
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        headers = {"Cookie": "sessionid=invalid_session_token"}
        response = requests.get(url, headers=headers)
        
        assert response.status_code in [401, 403]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])