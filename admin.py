# 檔案: admin.py
import streamlit as st
import pandas as pd
import db

st.set_page_config(page_title="後台管理系統", layout="wide")

def check_password():
    """簡單的密碼保護，避免閒雜人等看到個資"""
    def password_entered():
        if st.session_state["password"] == "aska2026": # 設定你的後台密碼
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 不儲存密碼
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 第一次進入，顯示輸入框
        st.text_input("請輸入管理員密碼", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # 密碼錯誤
        st.text_input("請輸入管理員密碼", type="password", on_change=password_entered, key="password")
        st.error("😕 密碼錯誤")
        return False
    else:
        # 密碼正確
        return True

if check_password():
    st.title("📊 特訓班報名管理後台")
    
    # 1. 讀取資料
    data = db.get_all_bookings()
    
    if data:
        df = pd.DataFrame(data)
        
        # 2. 關鍵指標 (KPI)
        col1, col2, col3 = st.columns(3)
        total_income = df['total_price'].sum()
        total_students = df['quantity'].sum()
        
        col1.metric("💰 總營收", f"NT$ {total_income:,}")
        col2.metric("👥 總報名人數", f"{total_students} 人")
        col3.metric("📝 訂單數", f"{len(df)} 筆")
        
        st.markdown("---")
        
        # 3. 詳細報表
        st.subheader("報名明細")
        
        # 整理一下欄位順序，比較好讀
        display_df = df[['name', 'phone', 'city', 'grade', 'course_date', 'quantity', 'total_price', 'plan_name', 'created_at']]
        st.dataframe(display_df, use_container_width=True)
        
        # 4. 下載功能 (給會計用)
        csv = display_df.to_csv(index=False).encode('utf-8-sig') # utf-8-sig 解決 Excel 中文亂碼
        st.download_button(
            "📥 下載 Excel 報表 (CSV)",
            csv,
            "bookings_report.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.info("目前尚無報名資料")