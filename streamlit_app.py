import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. إعدادات الصفحة وتصحيح الفريمات ---
st.set_page_config(page_title="TCR Global Sector Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stApp { background-color: #050505; }
    
    /* الفريمات السفلية (قائمة الفائزين) */
    .winner-container {
        border-radius: 15px;
        padding: 20px;
        margin-top: 10px;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .value-frame { border: 2px solid #00ff41; box-shadow: 0 0 15px rgba(0, 255, 65, 0.2); }
    .growth-frame { border: 2px solid #bc13fe; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); }

    /* عناوين الخانات السفلية داخل الفريم */
    .frame-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* الشركات الفائزة - الحفاظ على الألوان الأصلية */
    .winner-item {
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        font-size: 14px;
        word-wrap: break-word; /* لمنع خروج النص */
    }
    .value-text { color: #00ff41 !important; font-weight: bold; }
    .growth-text { color: #bc13fe !important; font-weight: bold; }

    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. قاعدة بيانات القطاعات (تأكد من الرموز) ---
TASI_2026_SECTORS = {
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR"],
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR"],
    "الطاقة": ["2222.SR", "2223.SR", "2310.SR"],
    "الرعاية الصحية": ["4009.SR", "4005.SR", "4001.SR"]
}

def safe_get(info, key, default=0):
    val = info.get(key)
    return val if val is not None else default

# --- 3. محرك الفحص المالي ---
def perform_deep_audit(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('shortName', symbol)
        
        # مؤشرات الفحص
        pe = safe_get(info, 'trailingPE', 99)
        div_yield = safe_get(info, 'dividendYield', 0) * 100
        roe = safe_get(info, 'returnOnEquity', 0) * 100
        debt_eq = safe_get(info, 'debtToEquity', 999) / 100

        # شروط الفوز
        is_value = (pe <= 22 and div_yield >= 2.5)
        is_growth = (roe >= 15 and debt_eq <= 0.6)
        
        return {"name": name, "symbol": symbol, "is_value": is_value, "is_growth": is_growth}
    except: return None

# --- 4. بناء الواجهة ---
st.markdown("<h1 class='neon-purple'>🔮 TCR GLOBAL SECTOR LABORATORY</h1>", unsafe_allow_html=True)

with st.sidebar:
    sector_choice = st.selectbox("اختر القطاع:", list(TASI_2026_SECTORS.keys()))
    scan_btn = st.button("إطلاق المسح الذكي ⚡", use_container_width=True)

# قسم الفائزين (الفرص الذهبية)
st.markdown("### 🏆 قائمة الفائزين (الفرص الذهبية)")
win_col1, win_col2 = st.columns(2)

# تعريف مسبق للخانات الفارغة
value_placeholder = win_col1.empty()
growth_placeholder = win_col2.empty()

if scan_btn:
    v_winners = []
    g_winners = []

    for sym in TASI_2026_SECTORS[sector_choice]:
        res = perform_deep_audit(sym)
        if res:
            if res['is_value']: v_winners.append(f"🏆 {res['name']} ({res['symbol']})")
            if res['is_growth']: g_winners.append(f"🚀 {res['name']} ({res['symbol']})")

    # تحديث خانة مدرسة القيمة
    with value_placeholder.container():
        content = "".join() if v_winners else "<div style='color:#555;'>جاري البحث...</div>"
        st.markdown(f"""
            <div class='winner-container value-frame'>
                <div class='frame-title' style='color:#00ff41;'>💎 نخبة القيمة</div>
                {content}
            </div>
        """, unsafe_allow_html=True)

    # تحديث خانة مدرسة النمو
    with growth_placeholder.container():
        content = "".join() if g_winners else "<div style='color:#555;'>جاري البحث...</div>"
        st.markdown(f"""
            <div class='winner-container growth-frame'>
                <div class='frame-title' style='color:#bc13fe;'>🔥 صواريخ النمو</div>
                {content}
            </div>
        """, unsafe_allow_html=True)
