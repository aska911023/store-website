# 檔案: styles.py
import streamlit as st

def load_landing_page_css():
    st.markdown("""
        <style>
        /* --- 全站基礎設定 --- */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Noto Sans TC', sans-serif;
            scroll-behavior: smooth;
            background-color: #f4f7f6; /* 很淡的灰藍色背景 */
        }
        
        /* 隱藏 Streamlit 預設選單 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* --- 1. 頂部導覽列 (Sticky Navbar) --- */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 50px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 9999;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(10px);
        }
        .nav-logo {
            font-size: 1.5rem;
            font-weight: 800;
            color: #2563eb;
            text-decoration: none;
        }
        .nav-links a {
            margin-left: 30px;
            text-decoration: none;
            color: #333;
            font-weight: 500;
            font-size: 1rem;
            transition: 0.3s;
        }
        .nav-links a:hover {
            color: #2563eb;
        }
        .nav-btn {
            background: #2563eb;
            color: white !important;
            padding: 8px 20px;
            border-radius: 50px;
        }

        /* --- 2. Hero 區塊 (首頁大圖) --- */
        .hero-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e40af 100%);
            color: white;
            padding: 120px 20px 80px; /* 上方留白給 Navbar */
            text-align: center;
            border-radius: 0 0 50px 50px;
            margin-bottom: 50px;
            position: relative;
            overflow: hidden;
        }
        .hero-title {
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 20px;
            text-shadow: 0 4px 10px rgba(0,0,0,0.3);
            background: -webkit-linear-gradient(#fff, #bfdbfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-desc {
            font-size: 1.3rem;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto 40px;
            line-height: 1.8;
        }
        
        /* --- 3. 課程卡片 (Card Design) --- */
        .course-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            border: 1px solid #eee;
            height: 100%;
            position: relative;
            overflow: hidden;
        }
        .course-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(37, 99, 235, 0.15);
            border-color: #bfdbfe;
        }
        .card-badge {
            background: #dbeafe;
            color: #2563eb;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 15px;
        }
        .card-price {
            font-size: 2rem;
            font-weight: 800;
            color: #2563eb;
            margin: 15px 0;
        }
        .card-features li {
            margin-bottom: 8px;
            color: #64748b;
            list-style-type: none;
        }
        
        /* --- 4. 講師圓形頭像 --- */
        .teacher-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 5px solid white;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            margin: 0 auto 20px;
            display: block;
        }

        /* --- 5. 按鈕優化 --- */
        .stButton button {
            width: 100%;
            background: linear-gradient(90deg, #2563eb, #3b82f6);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: 0.3s;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        }
        .stButton button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
        }
        
        /* --- 標題裝飾 --- */
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            color: #1e293b;
        }
        .section-subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 3rem;
            font-size: 1.1rem;
        }
        </style>
        
        <div class="navbar">
            <a href="#" class="nav-logo">AI Future Lab.</a>
            <div class="nav-links">
                <a href="#about">課程特色</a>
                <a href="#courses">熱門班級</a>
                <a href="#teachers">師資陣容</a>
                <a href="#booking" class="nav-btn">立即預約</a>
            </div>
        </div>
    """, unsafe_allow_html=True)