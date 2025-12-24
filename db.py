# 檔案: db.py
import streamlit as st
import requests
import json

# --- 1. 設定工具 ---
def get_config():
    """從 secrets.toml 讀取設定"""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        # Supabase 的資料庫 API 網址通常是 專案網址 + /rest/v1
        # 這裡做一個自動修正，確保網址格式正確
        if not url.endswith("/"):
            url += "/"
        api_url = f"{url}rest/v1"
        return api_url, key
    except Exception as e:
        st.error(f"讀取設定失敗: {e}")
        return None, None

def get_headers(key):
    """產生通用的請求標頭"""
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation" # 讓 Supabase 回傳寫入後的資料
    }

# --- 2. 寫入報名資料 (Create) ---
def create_booking(name, phone, city, grade, date, plan_name, total_price, email="", quantity=1):
    """
    使用 Requests 直接呼叫 API，避免 SDK 的編碼問題
    """
    base_url, key = get_config()
    if not base_url or not key:
        return False

    url = f"{base_url}/bookings"
    headers = get_headers(key)
    
    data = {
        "name": name,
        "phone": phone,
        "email": email,
        "city": city,
        "grade": grade,
        "course_date": date,
        "plan_name": plan_name,
        "total_price": total_price,
        "quantity": quantity
    }

    try:
        # 使用 requests.post 自動處理中文編碼
        response = requests.post(url, headers=headers, json=data)
        
        # 檢查是否成功 (201 Created)
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"寫入失敗 (Status {response.status_code}): {response.text}")
            st.error(f"報名失敗，伺服器回應錯誤：{response.status_code}")
            return False
            
    except Exception as e:
        print(f"連線錯誤: {e}")
        st.error("網路連線發生問題，請稍後再試。")
        return False

# --- 3. 查詢目前人數 (Read) ---
def get_booking_count(city, grade, date):
    """
    查詢某場次的已報名總人數
    """
    base_url, key = get_config()
    if not base_url or not key:
        return 0

    url = f"{base_url}/bookings"
    headers = get_headers(key)
    
    # Supabase (PostgREST) 的查詢語法
    params = {
        "select": "quantity",
        "city": f"eq.{city}",         # eq. 代表 equal (等於)
        "grade": f"eq.{grade}",
        "course_date": f"eq.{date}"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            # 累加所有訂單的人數
            total = sum([item.get('quantity', 0) for item in data])
            return total
        else:
            print(f"查詢失敗: {response.text}")
            return 0
            
    except Exception as e:
        print(f"查詢錯誤: {e}")
        return 0

# --- 4. 讀取所有資料 (給 Admin 後台用) ---
def get_all_bookings():
    """撈取所有報名資料"""
    base_url, key = get_config()
    if not base_url: return []

    url = f"{base_url}/bookings"
    headers = get_headers(key)
    
    # 依照建立時間排序 (desc)
    params = {
        "order": "created_at.desc"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"讀取資料失敗: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"連線錯誤: {e}")
        return []