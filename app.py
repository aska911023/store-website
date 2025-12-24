# 檔案: app.py
import streamlit as st
import styles
import db
import course_data 
from datetime import datetime, date

# --- 1. 頁面設定 ---
st.set_page_config(
    page_title="給家長的 AI 學習工作坊 | AI Future Lab", 
    page_icon="🌱", 
    layout="wide"
)

# --- 2. 參數設定 ---
MAX_CAPACITY = 8  # 滿班人數
MIN_CAPACITY = 4  # 開班門檻

# --- 3. 載入 CSS ---
styles.load_landing_page_css()
st.markdown("""
    <style>
    /* 確保所有大標題強制置中 */
    .section-title { text-align: center !important; margin-left: auto !important; margin-right: auto !important; }
    
    /* 狀態燈號樣式 */
    .status-badge { padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 0.95rem; margin-bottom: 10px; display: inline-block; letter-spacing: 1px; }
    .status-green { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; } 
    .status-orange { background-color: #ffedd5; color: #9a3412; border: 1px solid #fed7aa; } 
    .status-red { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
    
    /* 表單標題樣式 */
    .form-header {
        font-size: 1.1rem; font-weight: bold; color: #1e293b; 
        margin-top: 25px; margin-bottom: 15px; 
        border-left: 5px solid #2563eb; padding-left: 10px;
        background-color: #f8fafc; padding: 8px 10px; border-radius: 0 8px 8px 0;
    }

    /* 內容區塊優化 (用於 Why 與 課程介紹) */
    .content-box {
        background: white; border-radius: 15px; padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #eee; height: 100%;
    }
    .sub-title { font-size: 1.2rem; font-weight: bold; color: #2563eb; margin-bottom: 15px; display: block; }
    .list-item { margin-bottom: 8px; font-size: 1rem; color: #475569; display: block; }
    
    /* Tab 字體加大 */
    button[data-baseweb="tab"] { font-size: 1.1rem !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- [輔助函式] 日期顯示 ---
def get_date_display_string(date_str):
    """輸入 '1月3日'，輸出 '1月3日 (週六)'"""
    try:
        month = int(date_str.split("月")[0])
        day = int(date_str.split("月")[1].replace("日", ""))
        dt = date(2026, month, day)
        weekdays = ["(週一)", "(週二)", "(週三)", "(週四)", "(週五)", "(週六)", "(週日)"]
        return f"{date_str} {weekdays[dt.weekday()]}"
    except:
        return date_str

# --- 4. 價格計算邏輯 ---
def calculate_best_price(city, date_str, quantity):
    info = course_data.COURSE_DATA[city]
    prices = info["prices"]
    try:
        # date_str 進來時可能是 "1月3日 (週六)"，我們只取空白前的部分 "1月3日"
        clean_date_str = date_str.split(" ")[0]
        month = int(clean_date_str.split("月")[0])
        day = int(clean_date_str.split("月")[1].replace("日", ""))
        course_date = datetime(2026, month, day)
        today = datetime.now()
        days_diff = (course_date - today).days
    except:
        days_diff = 0 

    plan_name = "原價"
    unit_price = prices["原價"]
    is_discounted = False
    
    if quantity >= 2:
        if days_diff >= 14 and "早鳥團體報名" in prices:
            plan_name = "🔥 早鳥 + 雙人團報超優惠"
            unit_price = prices["早鳥團體報名"]
            is_discounted = True
        elif "團體報名" in prices:
            plan_name = "👫 雙人同行/團體優惠"
            unit_price = prices["團體報名"]
            is_discounted = True
        elif days_diff >= 14 and "寒假早鳥優惠" in prices:
            plan_name = "🐦 寒假早鳥優惠"
            unit_price = prices["寒假早鳥優惠"]
            is_discounted = True
        elif "寒假優惠" in prices:
            plan_name = "⛄ 寒假優惠"
            unit_price = prices["寒假優惠"]
            is_discounted = True
    elif days_diff >= 14 and "寒假早鳥優惠" in prices:
        plan_name = "🐦 寒假早鳥優惠 (早於兩週)"
        unit_price = prices["寒假早鳥優惠"]
        is_discounted = True
    elif "寒假優惠" in prices:
        plan_name = "⛄ 寒假優惠"
        unit_price = prices["寒假優惠"]
        is_discounted = True

    total_price = unit_price * quantity
    return plan_name, unit_price, total_price, is_discounted

# --- 5. 網站內容 ---

# === HERO ===
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">給家長的 AI 學習工作坊</div>
        <p class="hero-desc">
            孩子每天都在接觸 AI，但多數孩子不知道怎麼好好使用它。<br>
            這套工作坊不教寫程式，而是教孩子三件真正重要的事：<br>
            <b>怎麼思考、怎麼表達、怎麼與 AI 合作，而不是依賴 AI。</b>
        </p>
    </div>
""", unsafe_allow_html=True)

# === 為什麼適合 (Why) ===
st.markdown('<div id="about"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">🌱 為什麼這個工作坊適合現在的孩子？</div>', unsafe_allow_html=True)

col_why1, col_why2 = st.columns(2)
with col_why1:
    st.markdown("""
    <div class="content-box">
        <div class="sub-title">❌ 在台灣的學習環境中，許多孩子...</div>
        <li>習慣等標準答案</li>
        <li>不敢開口表達自己的想法</li>
        <li>面對新工具容易依賴或排斥</li>
        <li>使用 AI 時，不知道怎樣才算「用對」</li>
    </div>
    """, unsafe_allow_html=True)
with col_why2:
    st.markdown("""
    <div class="content-box" style="border-left: 5px solid #16a34a;">
        <div class="sub-title">✅ 這個工作坊的設計重點是...</div>
        <li>不害怕 AI，也不迷信 AI</li>
        <li>能清楚表達自己的想法</li>
        <li>知道「什麼時候該用 AI」</li>
        <li>知道「什麼時候該自己想」</li>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# === 課程介紹 (Courses) ===
st.markdown('<div id="courses"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">兩大分齡主題工作坊</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🧠 國中生 AI 探索 (12-15歲)", "🚀 高中生 AI 思考與應用 (15-18歲)"])

with tab1:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("""
        <div class="content-box">
            <div class="sub-title">👶 適合這樣的孩子</div>
            <li>第一次接觸 AI</li>
            <li>害羞、不太敢發言</li>
            <li>容易照指示做，但不習慣自己想</li>
            <li>對科技有好奇，但不知道怎麼開始</li>
            <hr>
            <div class="sub-title">🛠️ 孩子會做什麼？</div>
            <li>用生活化的方式認識 AI（不是技術課）</li>
            <li>學會怎麼「問問題」，讓 AI 聽懂自己</li>
            <li>把模糊的想法，慢慢說清楚</li>
            <li>和同齡孩子一起完成小任務</li>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="content-box" style="background:#f0f9ff; border-color:#bae6fd;">
            <div class="sub-title">👀 家長能看到的改變</div>
            <li>孩子比較敢表達自己的想法</li>
            <li>知道不是所有 AI 回答都要照單全收</li>
            <li>開始理解「想清楚再問」的重要性</li>
            <li>對學習產生更多主動感</li>
            <hr>
            <div class="sub-title">📌 工作坊形式</div>
            <li>時長：2–4 小時</li>
            <li>小班互動、小組合作</li>
            <li>無需任何 AI 或科技基礎</li>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("""
        <div class="content-box">
            <div class="sub-title">🧑‍🎓 適合這樣的孩子</div>
            <li>已經在用 AI（寫報告、整理資料）</li>
            <li>成績不差，但不確定未來方向</li>
            <li>容易「用 AI 很快完成」，但不確定有沒有真的學到</li>
            <li>想提升競爭力與思考能力</li>
            <hr>
            <div class="sub-title">🛠️ 孩子會學到什麼？</div>
            <li>了解 AI 的優點與限制</li>
            <li>學會把問題想清楚再交給 AI</li>
            <li>練習修正、判斷 AI 的回應</li>
            <li>與同學合作完成一個小型專題或想法</li>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="content-box" style="background:#fffbeb; border-color:#fde68a;">
            <div class="sub-title">👀 家長能看到的改變</div>
            <li>孩子不再只是「交給 AI 做」</li>
            <li>能解釋自己為什麼這樣用 AI</li>
            <li>對學習與未來多一份主動性</li>
            <li>使用 AI 時更有判斷力與責任感</li>
            <hr>
            <div class="sub-title">📌 工作坊形式</div>
            <li>時長：2–3 小時</li>
            <li>專題導向、小組討論</li>
            <li>不以考試或成績為導向</li>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# === 導師介紹 ===
st.markdown('<div id="teachers"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">特訓班導師</div>', unsafe_allow_html=True)
_, ct, _ = st.columns([1, 2, 1])
with ct:
    st.markdown("""
        <div class="course-card" style="text-align: center;">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Aska&backgroundColor=e5e7eb&clothing=hoodie" class="teacher-circle">
            <h2 style="color: #2563eb; margin-bottom: 5px;">Aska</h2>
            <p style="font-weight: bold; color: #64748b; margin-bottom: 15px;">AI 實戰教練 | 系統工程思維推廣者</p>
            <p style="color: #333; line-height: 1.8; text-align: left; padding: 0 20px;">
                嗨！我是 Aska。我不喜歡講空泛的理論，我只教你在未來世界存活的技能。<br><br>
                出身於工程背景，我習慣用<b>「系統化、邏輯化」</b>的方式來解決問題。
                在大學時期，我發現工程邏輯與 AI 操作有著驚人的相似之處——只要邏輯對了，工具就能發揮 100 倍的威力。<br><br>
                我比任何人都清楚學生在學習新科技時的痛點，因為我也曾經在那裡。
                在這個特訓班，我不會把你們當成學生，我會把你們當成未來的工程師與創造者，帶你們用最短的路徑，掌握 AI 的核心力量。
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# === 預約系統 (左右版面 + 方塊日曆 + 詳細資料) ===
st.markdown('<div id="booking"></div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="section-title">👉 歡迎家長洽詢與預約名額</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">每班僅限 {MAX_CAPACITY} 人，單場體驗或營隊形式，重視互動品質。</div>', unsafe_allow_html=True)

    # 外層容器 (左右留白)
    _, main_container, _ = st.columns([1, 10, 1]) 
    
    with main_container:
        st.markdown('<div class="course-card" style="border-top: 5px solid #2563eb;">', unsafe_allow_html=True)
        c_left, c_right = st.columns([1, 1], gap="large")
        
        # --- 左側：選課與日期 (方塊樣式) ---
        with c_left:
            st.subheader("1. 選擇方案")
            
            # 地點 (CSS會變方塊)
            city = st.radio("📍 上課地點", list(course_data.COURSE_DATA.keys()), label_visibility="collapsed")
            info = course_data.COURSE_DATA[city]
            st.write("") 
            # 身分 (CSS會變方塊)
            grade = st.radio("🎓 學員身分", ["國中生", "高中生"])
            
            st.write("")
            st.markdown("📅 **選擇日期**")
            
            # 1. 取得原始日期清單
            raw_dates = info["dates"][grade]
            # 2. 轉換成顯示格式 (含星期)
            display_dates = [get_date_display_string(d) for d in raw_dates]
            
            # 3. 顯示選單 (CSS 會讓它變方塊)
            selected_date_display = st.radio("選擇日期", display_dates, label_visibility="collapsed")
            
            # 4. [還原] 把選到的 "1月3日 (週六)" 變回 "1月3日" 給資料庫用
            selected_date = selected_date_display.split(" ")[0]
            
            # 庫存查詢 (用還原後的乾淨日期查)
            current_count = db.get_booking_count(city, grade, selected_date)
            remaining_seats = MAX_CAPACITY - current_count
            
            # 狀態顯示 (模糊化)
            st.write("")
            if current_count >= MAX_CAPACITY:
                st.markdown(f'<span class="status-badge status-red">🔴 已額滿 (候補中)</span>', unsafe_allow_html=True)
                is_full = True
            elif remaining_seats <= 3:
                st.markdown(f'<span class="status-badge status-orange">⚡ 即將額滿 | 最後席次</span>', unsafe_allow_html=True)
                is_full = False
            else:
                st.markdown(f'<span class="status-badge status-green">🔥 熱烈招生中</span>', unsafe_allow_html=True)
                is_full = False
            
            # 價格與人數
            if not is_full:
                st.write("")
                cq1, cq2 = st.columns([1, 2])
                with cq1:
                    max_select = remaining_seats if remaining_seats > 0 else 1
                    quantity = st.number_input("人數", min_value=1, max_value=max_select, value=1)
                with cq2:
                    st.caption("✨ 2人以上團購優惠")
                
                # 計算價格 (用還原後的日期算)
                plan_name, unit_price, total_price, is_discounted = calculate_best_price(city, selected_date, quantity)
                
                st.markdown(f"""
                    <div style="background:#f8fafc; padding:15px; border-radius:10px; margin-top:10px; text-align:center; border: 1px dashed #cbd5e1;">
                        <div style="color:#64748b; font-size:0.8rem;">每人 NT$ {unit_price:,}</div>
                        <div style="font-size:2.2rem; font-weight:800; color:#2563eb;">NT$ {total_price:,}</div>
                        <div style="color:#dc2626; font-size:0.9rem; font-weight:bold;">{plan_name}</div>
                    </div>
                """, unsafe_allow_html=True)

        # --- 右側：填寫資料 (含Line/多學生) ---
        with c_right:
            st.subheader("2. 填寫資料")
            
            if not is_full:
                with st.form("booking_form"):
                    st.markdown('<div class="form-header">家長 / 聯絡人資料</div>', unsafe_allow_html=True)
                    name = st.text_input("聯絡人姓名", placeholder="請輸入真實姓名")
                    phone = st.text_input("聯絡電話", placeholder="09xx-xxx-xxx")
                    line_id = st.text_input("Line ID", placeholder="方便建立班級群組與聯繫")
                    email = st.text_input("電子信箱", placeholder="用於寄送繳費通知")
                    
                    student_names = []
                    student_ages = []
                    student_genders = []
                    student_schools = []
                    
                    for i in range(quantity):
                        st.markdown(f'<div class="form-header">第 {i+1} 位學員</div>', unsafe_allow_html=True)
                        s_name = st.text_input(f"姓名 ({i+1})", key=f"sn{i}")
                        c_age, c_gen = st.columns(2)
                        with c_age: s_age = st.text_input(f"年紀 ({i+1})", key=f"sa{i}")
                        with c_gen: s_gender = st.radio(f"性別 ({i+1})", ["男", "女"], horizontal=True, key=f"sg{i}")
                        s_school = st.text_input(f"學校 ({i+1})", key=f"ss{i}")
                        
                        student_names.append(s_name)
                        student_ages.append(s_age)
                        student_genders.append(s_gender)
                        student_schools.append(s_school)

                    st.write("")
                    submit = st.form_submit_button("🚀 確認送出報名")
                    
                    if submit:
                        if not name or not phone or not line_id:
                            st.error("請填寫完整聯絡資料")
                        elif any([not s for s in student_names]):
                            st.error("請填寫學員姓名")
                        else:
                            # 組合字串存入 DB
                            s_names_str = ", ".join(student_names)
                            s_ages_str = ", ".join(student_ages)
                            s_genders_str = ", ".join(student_genders)
                            s_schools_str = ", ".join(student_schools)

                            success = db.create_booking(
                                name, phone, city, grade, selected_date, plan_name, total_price, email, quantity,
                                line_id, s_names_str, s_ages_str, s_genders_str, s_schools_str
                            )
                            if success:
                                st.balloons()
                                st.success(f"報名成功！已保留 {quantity} 位名額。")
            else:
                st.warning("⚠️ 本場次已額滿")
                with st.form("waiting_list"):
                    st.text_input("Email 加入候補")
                    if st.form_submit_button("加入"): st.success("已加入候補")

        st.markdown('</div>', unsafe_allow_html=True)

# === FAQ ===
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="section-title" style="font-size:2rem;">🤔 常見家長問題</div>', unsafe_allow_html=True)
qa1, qa2 = st.columns(2)
with qa1:
    with st.expander("Q: 這會不會讓孩子更依賴 AI？"): st.write("A: 相反地，孩子會學到「什麼時候不該用 AI」，以及如何判斷 AI 的限制。我們的重點是培養主動思考。")
    with st.expander("Q: 孩子不擅長科技，適合嗎？"): st.write("A: 非常適合。本工作坊重點在「思考與表達」，不是技術操作課，無需程式基礎。")
with qa2:
    with st.expander("Q: 這對升學有幫助嗎？"): st.write("A: 有間接幫助。孩子會培養未來學習與思考的底層能力（提問力、組織力），這些是面試與專題製作的核心能力。")
    with st.expander("Q: 退費規定？"): st.write("A: 開課前 7 天申請可全額退費；開課前 3 天內（含當日）恕不退費，但可保留名額至下一梯次。")

# Footer
st.markdown("<div style='text-align:center; padding:40px; color:#999; margin-top:50px;'>© 2026 AI Future Lab.</div>", unsafe_allow_html=True)