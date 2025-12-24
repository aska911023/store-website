import streamlit as st
import styles
import db
import course_data 
from datetime import datetime, timedelta

# --- 1. 頁面設定 ---
st.set_page_config(
    page_title="2026 AI 冬令營 | AI Future Lab", 
    page_icon="🚀", 
    layout="wide"
)

# --- 2. 參數設定 (庫存管理) ---
MAX_CAPACITY = 8  # 滿班人數
MIN_CAPACITY = 4  # 開班門檻

# --- 3. 載入 CSS 與強制置中設定 ---
styles.load_landing_page_css()
st.markdown("""
    <style>
    /* 強制置中設定 */
    .hero-section {
        display: flex !important; flex-direction: column !important;
        align-items: center !important; justify-content: center !important; text-align: center !important;
    }
    .hero-title, .hero-desc {
        width: 100%; max-width: 800px; margin-left: auto !important; margin-right: auto !important;
    }
    .section-title { text-align: center !important; }
    
    /* 狀態燈號樣式 */
    .status-badge {
        padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; margin-bottom: 10px; display: inline-block;
    }
    .status-green { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; } 
    .status-orange { background-color: #ffedd5; color: #9a3412; border: 1px solid #fed7aa; } 
    .status-red { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }   
    </style>
""", unsafe_allow_html=True)

# --- 4. 價格計算邏輯 ---
def calculate_best_price(city, date_str, quantity):
    info = course_data.COURSE_DATA[city]
    prices = info["prices"]
    
    try:
        month = int(date_str.split("月")[0])
        day = int(date_str.split("月")[1].replace("日", ""))
        course_date = datetime(2026, month, day)
        today = datetime.now()
        days_diff = (course_date - today).days
    except:
        days_diff = 0 

    plan_name = "原價"
    unit_price = prices["原價"]
    is_discounted = False
    
    # 邏輯: 2人以上即算團體
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


# --- 5. 網站內容開始 ---

# === HERO SECTION ===
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">啟動孩子的 AI 超能力</div>
        <p class="hero-desc">
            2026 寒假最強檔！專為國高中生打造的「生成式 AI 實戰特訓班」。<br>
            這不只是學程式，這是一場關於「思維升級」的進化。<br>
            用工程師的腦袋，駕馭最強大的 AI 工具。🚀
        </p>
    </div>
""", unsafe_allow_html=True)

# === 學員進化論 (取代舊的特色介紹) ===
st.markdown('<div id="about"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">參加特訓班，你將獲得的三大進化</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">AI 時代，我們不教死背硬記，我們教你如何「讓電腦幫你工作」</div>', unsafe_allow_html=True)

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("""
    <div class="course-card" style="text-align:center;">
        <div style="font-size:3rem; margin-bottom:15px;">🧠</div>
        <h3>從「解題者」進化為「提問者」</h3>
        <p style="color:#666;">AI 時代最缺的不是答案，而是「好問題」。我們用工程邏輯訓練你的 Prompt 技巧，精準指揮 AI 產出你要的結果。</p>
    </div>
    """, unsafe_allow_html=True)
with col_f2:
    st.markdown("""
    <div class="course-card" style="text-align:center;">
        <div style="font-size:3rem; margin-bottom:15px;">⚙️</div>
        <h3>從「單點思考」進化為「系統思維」</h3>
        <p style="color:#666;">結合工程背景的嚴謹邏輯，教你如何拆解複雜任務，將 AI 變成你的私人助理，學習效率提升 10 倍。</p>
    </div>
    """, unsafe_allow_html=True)
with col_f3:
    st.markdown("""
    <div class="course-card" style="text-align:center;">
        <div style="font-size:3rem; margin-bottom:15px;">🎨</div>
        <h3>從「消費者」進化為「創造者」</h3>
        <p style="color:#666;">不需要深厚的繪畫或程式底子，只要有想法，我們教你用 AI 工具把腦中的創意瞬間具象化，產出屬於你的作品。</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# === 熱門場次展示 ===
st.markdown('<div id="courses"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">熱門開課場次</div>', unsafe_allow_html=True)

col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    st.markdown("""
    <div class="course-card">
        <span class="card-badge">台北市 Taipei</span>
        <h3>AI 全能實戰班</h3>
        <p style="color:#666; font-size:0.9rem;">對象：國中生 / 高中生</p>
        <hr style="border:0; border-top:1px dashed #ddd; margin:15px 0;">
        <div class="card-features">
            <li>📅 下午 13:30 - 17:00</li>
            <li>📍 台北市區優質教室</li>
            <li>💻 需自備筆電</li>
        </div>
        <div class="card-price">NT$ 4,000 <span style="font-size:1rem; color:#999; font-weight:normal;">起</span></div>
    </div>
    """, unsafe_allow_html=True)
with col_c2:
    st.markdown("""
    <div class="course-card">
        <span class="card-badge" style="background:#fef3c7; color:#d97706;">新竹市 Hsinchu</span>
        <h3>AI 創客實戰班</h3>
        <p style="color:#666; font-size:0.9rem;">對象：國中生 / 高中生</p>
        <hr style="border:0; border-top:1px dashed #ddd; margin:15px 0;">
        <div class="card-features">
            <li>🔥 雙人成團享優惠</li>
            <li>📍 新竹市區科技中心</li>
            <li>🚀 含進階硬體實作</li>
        </div>
        <div class="card-price">NT$ 4,000 <span style="font-size:1rem; color:#999; font-weight:normal;">起</span></div>
    </div>
    """, unsafe_allow_html=True)
with col_c3:
    st.markdown("""
    <div class="course-card">
        <span class="card-badge" style="background:#dcfce7; color:#15803d;">台中市 Taichung</span>
        <h3>AI 未來領袖班</h3>
        <p style="color:#666; font-size:0.9rem;">對象：國中生 / 高中生</p>
        <hr style="border:0; border-top:1px dashed #ddd; margin:15px 0;">
        <div class="card-features">
            <li>🔥 雙人成團享優惠</li>
            <li>📍 台中市區創客基地</li>
            <li>🤝 重視團隊合作專案</li>
        </div>
        <div class="card-price">NT$ 4,000 <span style="font-size:1rem; color:#999; font-weight:normal;">起</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# === 導師介紹 (Aska) ===
st.markdown('<div id="teachers"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">特訓班導師</div>', unsafe_allow_html=True)

c_spacer1, c_teacher, c_spacer2 = st.columns([1, 2, 1])
with c_teacher:
    st.markdown("""
        <div class="course-card" style="text-align: center;">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Aska&backgroundColor=e5e7eb&clothing=hoodie" class="teacher-circle" style="margin: 0 auto 20px;">
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

# === 預約系統 (含庫存 & Email 修正) ===
st.markdown('<div id="booking"></div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="section-title">立即預約席次</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">每班僅限 {MAX_CAPACITY} 人，{MIN_CAPACITY} 人即開班，名額有限！</div>', unsafe_allow_html=True)

    bg_col1, bg_col2, bg_col3 = st.columns([1, 2, 1])
    
    with bg_col2:
        st.markdown('<div class="course-card" style="border-top: 5px solid #2563eb;">', unsafe_allow_html=True)
        
        # --- 1. 選擇場次 ---
        st.subheader("1. 選擇場次")
        city = st.selectbox("📍 選擇上課城市", list(course_data.COURSE_DATA.keys()))
        info = course_data.COURSE_DATA[city]
        
        c_grade, c_date = st.columns(2)
        with c_grade:
            grade = st.radio("🎓 學員身分", ["國中生", "高中生"], horizontal=True)
        with c_date:
            available_dates = info["dates"][grade]
            selected_date = st.selectbox("📅 選擇日期", available_dates)
        
        # --- 查詢名額 ---
        current_count = db.get_booking_count(city, grade, selected_date)
        remaining_seats = MAX_CAPACITY - current_count
        
        # --- 狀態顯示 ---
        st.write("---")
        st.markdown("**📊 目前班級狀態：**")
        
        if current_count >= MAX_CAPACITY:
            st.markdown(f'<span class="status-badge status-red">🔴 已額滿 (候補中)</span>', unsafe_allow_html=True)
            st.progress(1.0)
            is_full = True
        elif current_count >= MIN_CAPACITY:
            st.markdown(f'<span class="status-badge status-orange">🟠 確定開班 | 僅剩 {remaining_seats} 席</span>', unsafe_allow_html=True)
            st.progress(current_count / MAX_CAPACITY)
            is_full = False
        else:
            needed = MIN_CAPACITY - current_count
            st.markdown(f'<span class="status-badge status-green">🟢 招生中 | 尚缺 {needed} 人開班</span>', unsafe_allow_html=True)
            st.progress(current_count / MAX_CAPACITY)
            is_full = False

        st.caption(f"目前報名人數：{current_count} / 上限：{MAX_CAPACITY} 人")

        # --- 2. 選擇人數與結帳 ---
        if not is_full:
            st.subheader("2. 選擇人數")
            
            max_select = remaining_seats if remaining_seats > 0 else 1
            quantity = st.number_input("👥 報名人數 (2人以上享團體優惠)", min_value=1, max_value=max_select, value=1, step=1)
            
            plan_name, unit_price, total_price, is_discounted = calculate_best_price(city, selected_date, quantity)
            
            if is_discounted:
                st.success(f"🎉 太棒了！已套用優惠：**{plan_name}**")
            else:
                st.info(f"目前適用方案：{plan_name}")

            st.markdown(f"""
                <div style="background:#f8fafc; padding:20px; border-radius:10px; margin:15px 0; text-align:center; border: 1px dashed #cbd5e1;">
                    <div style="color:#64748b; font-size:0.9rem;">單價：NT$ {unit_price:,} x {quantity} 人</div>
                    <div style="font-size:2.5rem; font-weight:800; color:#2563eb;">NT$ {total_price:,}</div>
                    <div style="color:#dc2626; font-size:0.9rem; font-weight:bold;">
                        {'(包含早鳥優惠)' if '早鳥' in plan_name else ''} 
                        {'(包含團體折扣)' if '團體' in plan_name or '雙人' in plan_name else ''}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # --- 3. 填寫資料 ---
            st.subheader("3. 聯絡資料")
            with st.form("booking_form"):
                name = st.text_input("聯絡人姓名", placeholder="請輸入真實姓名")
                phone = st.text_input("聯絡電話", placeholder="09xx-xxx-xxx")
                email = st.text_input("電子信箱", placeholder="用於寄送繳費通知")
                
                st.write("")
                submit = st.form_submit_button("🚀 確認送出報名")
                
                if submit:
                    if not name or not phone:
                        st.error("請填寫完整資訊！")
                    else:
                        # [修正] 這裡要把 email 和 quantity 也傳進去！
                        success = db.create_booking(name, phone, city, grade, selected_date, plan_name, total_price, email, quantity)
                        if success:
                            st.balloons()
                            st.success(f"報名成功！我們已為您保留 {quantity} 個名額，確認信已寄至 {email}。")
        else:
            st.warning("⚠️ 本場次已額滿，請選擇其他日期或加入候補名單。")
            with st.form("waiting_list"):
                email_wait = st.text_input("輸入 Email 加入候補通知")
                wait_submit = st.form_submit_button("加入候補")
                if wait_submit:
                    st.success("已加入候補清單，有空位將優先通知您！")
        
        st.markdown('</div>', unsafe_allow_html=True)

# === 常見問題 (FAQ) ===
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="section-title" style="font-size:2rem;">常見問題 QA</div>', unsafe_allow_html=True)

faq_col1, faq_col2 = st.columns(2)
with faq_col1:
    with st.expander("Q: 課程適合什麼程度的學生？"):
        st.write("A: 我們的課程專為初學者設計，從零開始教起。但為了確保學習品質，建議學生具備基本的電腦打字能力。")
    with st.expander("Q: 課程有包含餐點嗎？"):
        st.write("A: 本課程為下午時段 (13:30-17:00) 的特訓班，**非全日營隊，故不提供午餐與點心**，請學員用過午餐後再來上課。")
    with st.expander("Q: 需要自備筆電嗎？"):
        st.write("A: 是的，建議攜帶筆記型電腦（Windows / Mac 皆可）以利保存作品回家複習。現場會提供電源插座與 Wi-Fi。")
    with st.expander("Q: 上課前需要先安裝軟體嗎？"):
        st.write("A: 報名成功後，我們會寄送「課前通知信」，裡面會有簡單的軟體安裝教學。若安裝遇到問題，開課當天助教也會協助處理。")

with faq_col2:
    with st.expander("Q: 團體報名需要所有人一起填寫嗎？"):
        st.write("A: 不需要。只要由一位代表在「報名人數」欄位選擇總人數，並填寫代表人的聯絡資料即可。後續我們會聯繫您確認每位學員的姓名。")
    with st.expander("Q: 家長可以陪同上課嗎？"):
        st.write("A: 為了培養孩子的獨立思考與團隊合作能力，家長僅需在接送時出現即可，課程中不開放旁聽。")
    with st.expander("Q: 報名後如何繳費？"):
        st.write("A: 送出報名表後，系統會自動發送確認信到您的信箱，信中會附上銀行匯款帳號。請於 3 日內完成匯款以保留名額。")
    with st.expander("Q: 如果臨時有事可以退費嗎？"):
        st.write("A: 開課前 7 天申請可全額退費；開課前 3 天申請可退費 50%；開課當天恕不退費，但可保留名額至下一梯次。")

# === 頁尾 (Footer) ===
st.markdown("""
    <div style="text-align:center; padding:40px; color:#94a3b8; font-size:0.9rem; border-top:1px solid #eee; margin-top:50px;">
        © 2026 AI Future Lab. All rights reserved.<br>
        打造未來的關鍵一步
    </div>
""", unsafe_allow_html=True)