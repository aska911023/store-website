# 檔案: styles.py
import streamlit as st

def load_landing_page_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Noto Sans TC', sans-serif;
            scroll-behavior: smooth;
            background-color: #f4f7f6;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* 導覽列 */
        .navbar {
            position: fixed; top: 0; left: 0; width: 100%;
            background: rgba(255, 255, 255, 0.95); padding: 15px 50px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); z-index: 9999;
            display: flex; justify-content: space-between; align-items: center;
            backdrop-filter: blur(10px);
        }
        .nav-logo { font-size: 1.5rem; font-weight: 800; color: #2563eb; text-decoration: none; }
        .nav-links a { margin-left: 30px; text-decoration: none; color: #333; font-weight: 500; transition: 0.3s; }
        .nav-btn { background: #2563eb; color: white !important; padding: 8px 20px; border-radius: 50px; }

        /* Hero */
        .hero-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e40af 100%);
            color: white; padding: 120px 20px 80px; text-align: center;
            border-radius: 0 0 50px 50px; margin-bottom: 50px;
            display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important;
        }
        .hero-title { font-size: 3.5rem; font-weight: 900; margin-bottom: 20px; text-shadow: 0 4px 10px rgba(0,0,0,0.3); width: 100%; max-width: 800px; }
        .hero-desc { font-size: 1.3rem; opacity: 0.9; line-height: 1.8; width: 100%; max-width: 800px; }
        
        /* 卡片 */
        .course-card {
            background: white; border-radius: 20px; padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            transition: all 0.3s ease; border: 1px solid #eee; height: 100%;
        }
        .card-badge { background: #dbeafe; color: #2563eb; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 15px; }
        .card-price { font-size: 2rem; font-weight: 800; color: #2563eb; margin: 15px 0; }
        .teacher-circle { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 5px solid white; box-shadow: 0 8px 20px rgba(0,0,0,0.1); margin: 0 auto 20px; display: block; }

        /* ============================================================
           [暴力修正] 強制 Radio Button 變成「方塊日曆格」
           ============================================================ */
        /* 1. 容器設定：橫向排列 + 自動換行 (Grid 效果的核心) */
        div[role="radiogroup"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: wrap !important; /* 這行最重要，讓它能換行 */
            gap: 10px !important;       /* 格子之間的間距 */
        }
        
        /* 2. 選項設定：變成方塊卡片 */
        div[role="radiogroup"] label {
            background-color: white !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 15px 5px !important;
            
            /* 強制大小：讓每個選項看起來像一個方塊 */
            flex: 0 0 calc(33.33% - 10px) !important; /* 一排強制 3 個 */
            min-width: 100px !important;
            
            text-align: center !important;
            justify-content: center !important;
            margin-right: 0px !important;
            transition: all 0.2s !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        }

        /* 3. 選中時的樣子：藍色背景 + 上浮效果 */
        div[role="radiogroup"] label[data-checked="true"] {
            background-color: #eff6ff !important;
            border-color: #2563eb !important;
            color: #2563eb !important;
            font-weight: 900 !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
            transform: translateY(-3px) !important;
        }

        /* 4. 滑鼠移過去 */
        div[role="radiogroup"] label:hover {
            border-color: #93c5fd !important;
        }

        /* 5. 絕對隱藏原本的圓點點 */
        div[role="radiogroup"] label > div:first-child {
            display: none !important;
        }
        
        /* 標題與按鈕 */
        .stButton button { width: 100%; background: linear-gradient(90deg, #2563eb, #3b82f6); color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 600; font-size: 1.1rem; transition: 0.3s; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3); }
        .stButton button:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4); }
        .section-title { text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; color: #1e293b; }
        .section-subtitle { text-align: center; color: #64748b; margin-bottom: 3rem; font-size: 1.1rem; }
        
        /* 表單標題裝飾 */
        .form-header {
            font-size: 1.0rem; font-weight: 800; color: #334155; 
            margin-top: 20px; margin-bottom: 10px; 
            border-left: 4px solid #2563eb; padding-left: 10px;
            background: #f8fafc; padding: 8px; border-radius: 0 8px 8px 0;
        }

        /* Navbar HTML */
        <div class="navbar">
            <a href="#" class="nav-logo">AI Future Lab.</a>
            <div class="nav-links">
                <a href="#about">課程進化</a>
                <a href="#courses">熱門班級</a>
                <a href="#teachers">導師介紹</a>
                <a href="#booking" class="nav-btn">立即預約</a>
            </div>
        </div>
    """, unsafe_allow_html=True)