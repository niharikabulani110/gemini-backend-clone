#!/usr/bin/env python3
"""
Simple test script to verify API endpoints
Run this after starting the server with: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth_flow():
    """Test the complete authentication flow"""
    print("Testing Authentication Flow...")
    
    # Test signup
    mobile_number = "+1234567890"
    signup_data = {"mobile_number": mobile_number, "password": "testpassword123"}
    
    print("1. Testing signup...")
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    print(f"   Signup response: {response.status_code} - {response.json()}")
    
    # Test send OTP
    print("2. Testing send OTP...")
    response = requests.post(f"{BASE_URL}/auth/send-otp", json={"mobile_number": mobile_number})
    print(f"   Send OTP response: {response.status_code} - {response.json()}")
    
    if response.status_code == 200:
        otp = response.json().get("otp")
        
        # Test verify OTP
        print("3. Testing verify OTP...")
        verify_data = {"mobile_number": mobile_number, "otp": otp}
        response = requests.post(f"{BASE_URL}/auth/verify-otp", json=verify_data)
        print(f"   Verify OTP response: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test user profile
            print("4. Testing user profile...")
            response = requests.get(f"{BASE_URL}/user/me", headers=headers)
            print(f"   User profile response: {response.status_code} - {response.json()}")
            
            # Test usage stats
            print("5. Testing usage stats...")
            response = requests.get(f"{BASE_URL}/user/usage", headers=headers)
            print(f"   Usage stats response: {response.status_code} - {response.json()}")
            
            return token, headers
    
    return None, None

def test_chatroom_flow(token, headers):
    """Test chatroom creation and messaging"""
    if not token:
        print("No token available, skipping chatroom tests")
        return
    
    print("\nTesting Chatroom Flow...")
    
    # Test create chatroom
    print("1. Testing create chatroom...")
    chatroom_data = {"name": "Test Chatroom"}
    response = requests.post(f"{BASE_URL}/chatroom/", json=chatroom_data, headers=headers)
    print(f"   Create chatroom response: {response.status_code} - {response.json()}")
    
    if response.status_code == 200:
        chatroom_id = response.json().get("id")
        
        # Test list chatrooms
        print("2. Testing list chatrooms...")
        response = requests.get(f"{BASE_URL}/chatroom/", headers=headers)
        print(f"   List chatrooms response: {response.status_code} - {response.json()}")
        
        # Test get specific chatroom
        print("3. Testing get specific chatroom...")
        response = requests.get(f"{BASE_URL}/chatroom/{chatroom_id}", headers=headers)
        print(f"   Get chatroom response: {response.status_code} - {response.json()}")
        
        # Test send message
        print("4. Testing send message...")
        message_data = {"content": "Hello, this is a test message!"}
        response = requests.post(f"{BASE_URL}/chatroom/{chatroom_id}/message", 
                               json=message_data, headers=headers)
        print(f"   Send message response: {response.status_code} - {response.json()}")

def test_subscription_flow(token, headers):
    """Test subscription endpoints"""
    if not token:
        print("No token available, skipping subscription tests")
        return
    
    print("\nTesting Subscription Flow...")
    
    # Test subscription status
    print("1. Testing subscription status...")
    response = requests.get(f"{BASE_URL}/subscription/status", headers=headers)
    print(f"   Subscription status response: {response.status_code} - {response.json()}")
    
    # Test start subscription (this will create a Stripe checkout session)
    print("2. Testing start subscription...")
    response = requests.post(f"{BASE_URL}/subscription/pro", headers=headers)
    print(f"   Start subscription response: {response.status_code} - {response.json()}")

def main():
    """Run all tests"""
    print("Starting API Tests...")
    print("=" * 50)
    
    try:
        # Test authentication flow
        token, headers = test_auth_flow()
        
        if token:
            # Test chatroom flow
            test_chatroom_flow(token, headers)
            
            # Test subscription flow
            test_subscription_flow(token, headers)
        
        print("\n" + "=" * 50)
        print("Tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 