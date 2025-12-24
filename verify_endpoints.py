import requests
import sys

BASE_URL = "http://127.0.0.1:8000"
EMAIL = f"test_user_{sys.argv[1]}@example.com" if len(sys.argv) > 1 else "test_user_1@example.com"
PASSWORD = "password123"

def run_test():
    print(f"Testing with email: {EMAIL}")
    
    # 1. Register
    print("\n[1] Registering User...")
    reg_res = requests.post(f"{BASE_URL}/register", json={"email": EMAIL, "password": PASSWORD})
    print(f"Status: {reg_res.status_code}, Response: {reg_res.text}")
    if reg_res.status_code not in [200, 400]: # 400 if already exists is okay for re-runs
         print("Registration failed.")
         return

    # 2. Login
    print("\n[2] Logging in...")
    login_res = requests.post(f"{BASE_URL}/login", data={"username": EMAIL, "password": PASSWORD})
    if login_res.status_code != 200:
        print(f"Login failed: {login_res.text}")
        return
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful.")

    # 3. Setup Profile (Update)
    print("\n[3] Setting up Profile...")
    profile_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "age": 30,
        "phone": "+1234567890",
        "profile_photo": "https://example.com/alice.jpg"
    }
    update_res = requests.put(f"{BASE_URL}/users/me", json=profile_data, headers=headers)
    print(f"Status: {update_res.status_code}, Response: {update_res.json()}")
    
    # 4. Get Profile
    print("\n[4] Getting Profile...")
    get_res = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"Status: {get_res.status_code}, Response: {get_res.json()}")
    
    # 5. Create Server
    print("\n[5] Creating Server...")
    server_data = {
        "name": "Production Server",
        "ip_address": "192.168.1.100",
        "username": "admin",
        "port": 22,
        "status": "active"
    }
    create_srv_res = requests.post(f"{BASE_URL}/servers/", json=server_data, headers=headers)
    print(f"Status: {create_srv_res.status_code}, Response: {create_srv_res.text}")
    if create_srv_res.status_code == 200:
        server_id = create_srv_res.json()["id"]
        
        # 6. List Servers
        print("\n[6] Listing Servers...")
        list_res = requests.get(f"{BASE_URL}/servers/", headers=headers)
        print(f"Status: {list_res.status_code}, Count: {len(list_res.json())}")

        # 7. Update Server
        print("\n[7] Updating Server...")
        update_srv_res = requests.put(f"{BASE_URL}/servers/{server_id}", json={"status": "maintenance"}, headers=headers)
        print(f"Status: {update_srv_res.status_code}, Response: {update_srv_res.json()}")

        # 8. Delete Server
        print("\n[8] Deleting Server...")
        del_srv_res = requests.delete(f"{BASE_URL}/servers/{server_id}", headers=headers)
        print(f"Status: {del_srv_res.status_code}, Response: {del_srv_res.json()}")
    else:
        print("Skipping Server CRUD steps due to creation failure")

    # 9. Delete User
    print("\n[9] Deleting User Account...")
    del_user_res = requests.delete(f"{BASE_URL}/users/me", headers=headers)
    print(f"Status: {del_user_res.status_code}, Response: {del_user_res.json()}")

if __name__ == "__main__":
    run_test()
