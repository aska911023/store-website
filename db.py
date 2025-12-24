# 檔案: db.py
import streamlit as st
import requests

def get_config():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        if not url.endswith("/"): url += "/"
        api_url = f"{url}rest/v1"
        return api_url, key
    except Exception as e:
        st.error(f"設定讀取失敗: {e}")
        return None, None

def get_headers(key):
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

# [更新] 支援 Line ID 與 詳細學生資料
def create_booking(name, phone, city, grade, date, plan_name, total_price, email="", quantity=1, 
                   line_id="", s_names="", s_ages="", s_genders="", s_schools=""):
    base_url, key = get_config()
    if not base_url: return False

    url = f"{base_url}/bookings"
    headers = get_headers(key)
    
    data = {
        "name": name,
        "phone": phone,
        "email": email,
        "line_id": line_id,          # 新增
        "city": city,
        "grade": grade,
        "course_date": date,
        "plan_name": plan_name,
        "total_price": total_price,
        "quantity": quantity,
        "student_names": s_names,    # 新增
        "student_ages": s_ages,      # 新增
        "student_genders": s_genders,# 新增
        "student_schools": s_schools # 新增
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"寫入失敗: {response.text}")
            st.error(f"寫入失敗 (Code {response.status_code})")
            return False
    except Exception as e:
        print(f"連線錯誤: {e}")
        return False

def get_booking_count(city, grade, date):
    base_url, key = get_config()
    if not base_url: return 0
    url = f"{base_url}/bookings"
    headers = get_headers(key)
    params = {"select": "quantity", "city": f"eq.{city}", "grade": f"eq.{grade}", "course_date": f"eq.{date}"}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return sum([item.get('quantity', 0) for item in data])
        else: return 0
    except: return 0

def get_all_bookings():
    base_url, key = get_config()
    if not base_url: return []
    url = f"{base_url}/bookings"
    headers = get_headers(key)
    params = {"order": "created_at.desc"}
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json() if response.status_code == 200 else []
    except: return []