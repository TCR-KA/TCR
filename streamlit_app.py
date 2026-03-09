import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم السيبراني المطور (Grid System للبطاقات) ---
st.set_page_config(page_title="TCR Global Sector Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stApp { background-color: #050505; }
    
    /* فريم الفائزين */
    .winner-box {
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        min-height: 300px;
        max-height: 600px;
        overflow-y: auto;
    }
    .value-border { border: 2px solid #00ff41 !important; box-shadow: 0 0 15px rgba(0, 255, 65, 0.2); }
    .growth-border { border: 2px solid #bc13fe !important; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); }

    /* بطاقة البيانات داخل الفريم */
    .stock-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 12px;
        border-left: 4px solid;
    }
    .v-card { border-left-color: #00ff41; }
    .g-card { border-left-color: #bc13fe; }

    .card-header { font-weight: bold; font-size: 1rem; margin-bottom: 5px; display: block; }
    .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 0.85rem; }
    
    .v-color { color: #00ff41 !important; }
    .g-color { color: #bc13fe !important; }
    .label { color: #888; }
    </style>
""", unsafe_allow_html=True)

# --- 2. قاعدة بيانات تاسي الشاملة ---
TASI_2026_SECTORS = {
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1080.SR", "1020.SR", "1030.SR", "1060.SR"],
    "الطاقة": ["2222.SR", "2223.SR", "2310.SR", "2030.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "2002.SR", "2380.SR", "3001.SR", "3010.SR"],
    "الرعاية الصحية": ["4001.SR", "4005.SR", "4009.SR", "4013.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR", "7040.SR"],
    "العقارات": ["4020.SR", "4150.SR", "4300.SR", "4330.SR"],
    "التقنية": ["7200.SR", "7201.SR", "7202.SR"]
}

def safe_get(info, key, default=0):
    val = info.get(key)
    return val if val is not None else default

# --- 3. محرك الفحص الذكي (مع استخراج الأرقام) ---
def perform_deep_audit(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('shortName', symbol)
        
        # جلب المؤشرات الحقيقية
        pe = safe_get(info, 'trailingPE', 999)
        dy = safe_get(info, 'dividendYield', 0) * 100
        roe = safe_get(info, 'returnOnEquity', 0) * 100
        de = safe_get(info, 'debtToEquity', 999) / 100
        peg = safe_get(info, 'pegRatio', 9.9)

        # شروط الفوز
        is_val = (pe <= 22 and dy >= 2.5)
        is_gro = (roe >= 15 and de <= 0.6)
        
        return {
            "name": name, "sym": symbol, "v": is_val, "g": is_gro,
            "data": {"pe": pe, "dy": dy, "roe": roe, "de": de, "peg": peg}
        }
    except: return None

# --- 4. بناء الواجهة ---
st.markdown("<h1 style='color:#bc13fe; text-align:center;'>🔮 TCR SECTOR LAB: METRICS EDITION</h1>", unsafe_allow_html=True)

with st.sidebar:
    sector_choice = st.selectbox("🎯 اختر القطاع:", list(TASI_2026_SECTORS.keys()))
    scan = st.button("إطلاق المسح واستخراج البيانات ⚡", use_container_width=True)

if scan:
    v_winners, g_winners = [], []
    bar = st.progress(0)
    
    for i, sym in enumerate(TASI_2026_SECTORS[sector_choice]):
        res = perform_deep_audit(sym)
        if res:
            if res['v']: v_winners.append(res)
            if res['g']: g_winners.append(res)
        bar.progress((i + 1) / len(TASI_2026_SECTORS[sector_choice]))

    st.markdown("### 🏆 قائمة الفائزين مع المؤشرات")
    col1, col2 = st.columns(2)

    # خانة مدرسة القيمة
    with col1:
        st.markdown("<div class='winner-box value-border'>", unsafe_allow_html=True)
        st.markdown("<div class='inner-title v-color'>💎 نخبة القيمة</div>", unsafe_allow_html=True)
        if v_winners:
            for w in v_winners:
                st.markdown(f"""
                    <div class='stock-card v-card'>
                        <span class='card-header v-color'>🏆 {w['name']} ({w['sym']})</span>
                        <div class='metrics-grid'>
                            <span><span class='label'>P/E:</span> {w['data']['pe']:.1f}</span>
                            <span><span class='label'>Yield:</span> {w['data']['dy']:.1f}%</span>
                            <span><span class='label'>ROE:</span> {w['data']['roe']:.1f}%</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else: st.write("لا توجد فرص مطابقة")
        st.markdown("</div>", unsafe_allow_html=True)

    # خانة مدرسة النمو
    with col2:
        st.markdown("<div class='winner-box growth-border'>", unsafe_allow_html=True)
        st.markdown("<div class='inner-title g-color'>🔥 صواريخ النمو</div>", unsafe_allow_html=True)
        if g_winners:
            for w in g_winners:
                st.markdown(f"""
                    <div class='stock-card g-card'>
                        <span class='card-header g-color'>🚀 {w['name']} ({w['sym']})</span>
                        <div class='metrics-grid'>
                            <span><span class='label'>ROE:</span> {w['data']['roe']:.1f}%</span>
                            <span><span class='label'>D/E:</span> {w['data']['de']:.2f}</span>
                            <span><span class='label'>PEG:</span> {w['data']['peg']:.2f}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else: st.write("لا توجد فرص مطابقة")
        st.markdown("</div>", unsafe_allow_html=True)
