#!/usr/bin/env python3
"""Test script for API endpoints (Python)
Run after starting the server: python test_api.py
Requires: requests (pip install requests)
"""
import requests, uuid, time
base = 'http://127.0.0.1:8000'
# small wait to allow server start
time.sleep(1)
with requests.Session() as s:
    email = f"testuser-{uuid.uuid4()}@example.com"
    print('Registering', email)
    register = s.post(f"{base}/api/kayit", json={"ad_soyad":"Test User","email":email,"sifre":"TestPass123"})
    print('REGISTER:', register.status_code, register.text)
    login = s.post(f"{base}/api/giris", json={"email":email,"sifre":"TestPass123"})
    print('LOGIN:', login.status_code, login.text)
    print('Cookies:', s.cookies.get_dict())
    profile = s.get(f"{base}/api/profil")
    print('PROFILE:', profile.status_code, profile.text)
