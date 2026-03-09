import streamlit as st
import yfinance as yf
import pandas as pd
import time
import plotly.graph_objects as go

# --- 1. هندسة الواجهة السيبرانية (Dashboard UI) ---
st.set_page_config(page_title="TCR Ultimate Dashboard", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS مخصص تماماً ليطابق الصورة
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #ffffff; font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0b0e14; }
    
    /* تصميم البطاقات الزجاجية المتطورة */
    .card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        height: 100%;
    }
    
    /* شريط المسح العلوي */
    .scanner-bar {
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
        border-bottom: 2px solid #bc13fe;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .neon-blue { color: #3d5afe; text-shadow: 0 0 10px #3d5afe; font-weight: bold; }
    
    /* الأزرار الاحترافية */
    .stButton>button {
        background: linear-gradient(45deg, #bc13fe, #3d5afe);
        color: white; border: none; border-radius: 8px;
        height: 3.5em; font-weight: bold; width: 100%;
        text-transform: uppercase; letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك الرسوم التفاعلية (Interactive Gauges) ---
def create_gauge(title, value, min_val, max_val, target):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title, 'font': {'size': 14, 'color': "#bc13fe"}},
        gauge = {
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "#3d5afe"},
            'bar': {'color': "#bc13fe"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#3d5afe",
            'steps': [{'range': [min_val, target], 'color': 'rgba(0, 255, 136, 0.1)'}],
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "#ffffff"}, height=200, margin=dict(l=20, r=20, t=30, b=20))
    return fig

# --- 3. محرك التحليل والبحث المتسلسل ---
def run_deep_scan(symbol):
    try:
        start_time = time.time()
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', symbol)
        
        # استخراج المعايير الـ 7 الصارمة
        metrics = {
            "PEG": info.get('pegRatio', 9.9),
            "EPS_G": info.get('earningsQuarterlyGrowth', 0) * 100,
            "PE": info.get('trailingPE', 99),
            "DEBT": info.get('debtToEquity', 999) / 100,
            "PAYOUT": info.get('payoutRatio', 0) * 100,
            "NET_CASH": (info.get('totalCash', 0) - info.get('totalDebt', 0)) / 1e6,
            "FCF": info.get('freeCashflow', 0) / info.get('netIncomeToCommon', 1) if info.get('netIncomeToCommon', 0) > 0 else 0
        }
        
        duration = time.time() - start_time
        return {"name": name, "symbol": symbol, "metrics": metrics, "time": f"{duration:.2f}s"}
    except: return None

# --- 4. بناء لوحة التحكم التفاعلية ---
st.markdown("<h1 style='text-align:center; color:#bc13fe; text-shadow:0 0 15px #bc13fe;'>🛡️ TCR ULTIMATE VANGUARD</h1>", unsafe_allow_html=True)

# شريط الحالة العلوي (الثابت)
scanner_header = st.empty()

# تقسيم الشاشة (المربعات المنفصلة)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 🛰️ رادار التحليل الحي")
    analysis_grid = st.empty() # هنا تظهر البطاقات والرسوم

with col_right:
    st.markdown("### 🏺 أرشيف النخبة")
    elite_vault = st.container()

if st.button("LAUNCH SYSTEM SCAN (بدء المسح الشامل)"):
    # نطاقات تاسي الكاملة
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_symbols = [f"{c}.SR" for r in ranges for c in r]
    
    found_elite = []
    
    for sym in all_symbols:
        # 1. تحديث شريط الحالة (الوقت والبدء)
        scanner_header.markdown(f"""
            <div class="scanner-bar">
                <span class="neon-blue">جاري الفحص الآن:</span> 
                <span style="font-size:20px; color:#fff;"> {sym} </span> | 
                <span class="neon-purple">الحالة: مراجعة القوائم المالية...</span>
            </div>
        """, unsafe_allow_html=True)
        
        result = run_deep_scan(sym)
        
        if result:
            m = result['metrics']
            # 2. تحديث لوحة الرسوم والبطاقات (تفاعلية حية)
            with analysis_grid.container():
                st.markdown(f"#### 🏷️ الشركة الحالية: {result['name']} | تم التحليل في: {result['time']}")
                
                c1, c2, c3 = st.columns(3)
                # رسم بياني تفاعلي لكل مؤشر
                c1.plotly_chart(create_gauge("PEG Ratio", m['PEG'], 0, 3, 1), use_container_width=True)
                c2.plotly_chart(create_gauge("EPS Growth %", m['EPS_G'], -50, 100, 20), use_container_width=True)
                c3.plotly_chart(create_gauge("P/E Ratio", m['PE'], 0, 50, 15), use_container_width=True)
                
                # بطاقات البيانات الإضافية
                st.markdown(f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 10px; margin-top: 20px;">
                    <div class="card"><small>الديون/الملكية</small><br><b class="neon-blue">{m['DEBT']:.2f}</b></div>
                    <div class="card"><small>نسبة التوزيع</small><br><b class="neon-blue">{m['PAYOUT']:.1f}%</b></div>
                    <div class="card"><small>صافي النقد (مليون)</small><br><b class="neon-blue">{m['NET_CASH']:,.1f}</b></div>
                    <div class="card"><small>جودة السيولة</small><br><b class="neon-blue">{m['FCF']:.2f}</b></div>
                </div>
                """, unsafe_allow_html=True)

            # 3. اختبار النخبة (لينش وبافيت)
            is_elite = (m['PEG'] < 1.0 and 20 <= m['EPS_G'] <= 50 and m['DEBT'] < 0.35 and m['PE'] <= 15)
            
            if is_elite:
                found_elite.append(result)
                with elite_vault:
                    st.success(f"🏆 {result['name']} ({result['symbol']})")
        
        time.sleep(0.01) # سرعة الفحص المتطورة

