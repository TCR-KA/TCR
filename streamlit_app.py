import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. إعدادات الصفحة والتنسيق السيبراني المحسن ---
st.set_page_config(page_title="TCR Global Sector Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stApp { background-color: #050505; }
    /* إطار البطاقة الرئيسي */
    .sector-card { 
        background: #0f0f0f; 
        border: 1px solid #bc13fe; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 20px;
        overflow: hidden;
    }
    /* بطاقة المؤشر الصغيرة */
    .indicator-item { 
        background: #000; 
        border: 1px solid #222; 
        padding: 8px; 
        border-radius: 6px; 
        margin: 4px 0;
        font-size: 13px;
        line-height: 1.2;
    }
    .pass-tag { border-right: 4px solid #00ff41; }
    .fail-tag { border-right: 4px solid #ff4b2b; }
    
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; text-align: center; }
    
    /* خانة الفائزين (الفرص) */
    .winner-box { 
        background: #070707; 
        border: 2px solid #00ff41; 
        border-radius: 15px; 
        padding: 20px; 
        min-height: 150px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.1);
    }
    .winner-item {
        color: #00ff41;
        font-weight: bold;
        padding: 5px;
        border-bottom: 1px dashed #333;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. قاعدة البيانات الشاملة (جميع قطاعات تاسي) ---
TASI_2026_SECTORS = {
    "الطاقة": ["2222.SR", "2223.SR", "2310.SR", "2030.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "2002.SR", "2380.SR"],
    "السلع الرأسمالية": ["1301.SR", "1304.SR", "1320.SR", "2230.SR", "1214.SR"],
    "النقل": ["4030.SR", "4040.SR", "4110.SR", "4260.SR"],
    "الرعاية الصحية": ["4009.SR", "4005.SR", "4001.SR", "4013.SR"],
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1080.SR", "1020.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR"],
    "العقارات": ["4020.SR", "4150.SR", "4180.SR", "4250.SR"],
    "التجزئة": ["4002.SR", "4004.SR", "4006.SR", "4008.SR"],
    "التقنية": ["7200.SR", "7201.SR", "7202.SR"],
    "الاستثمار": ["4280.SR", "4190.SR", "2170.SR"]
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
        
        # استخراج البيانات
        pe = safe_get(info, 'trailingPE', 99)
        div_yield = safe_get(info, 'dividendYield', 0) * 100
        roe = safe_get(info, 'returnOnEquity', 0) * 100
        payout = safe_get(info, 'payoutRatio', 0) * 100
        debt_eq = safe_get(info, 'debtToEquity', 999) / 100
        peg = safe_get(info, 'pegRatio', 9.9)

        # مدرسة القيمة
        b_criteria = [
            {"label": "P/E Ratio", "val": f"{pe:.1f}", "pass": pe <= 20},
            {"label": "Yield", "val": f"{div_yield:.1f}%", "pass": div_yield >= 3},
            {"label": "ROE", "val": f"{roe:.1f}%", "pass": roe >= 12},
            {"label": "Payout", "val": f"{payout:.1f}%", "pass": 20 <= payout <= 80}
        ]

        # مدرسة النمو
        l_criteria = [
            {"label": "PEG Ratio", "val": f"{peg:.2f}", "pass": peg <= 1.2},
            {"label": "Debt/Equity", "val": f"{debt_eq:.2f}", "pass": debt_eq <= 0.5},
            {"label": "ROE", "val": f"{roe:.1f}%", "pass": roe >= 15}
        ]
        
        return {"name": name, "symbol": symbol, "buffett": b_criteria, "lynch": l_criteria}
    except: return None

# --- 4. واجهة التطبيق ---
st.markdown("<h1 class='neon-purple'>🔮 TCR GLOBAL SECTOR LABORATORY</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ التحكم")
    sector_choice = st.selectbox("اختر القطاع:", list(TASI_2026_SECTORS.keys()))
    scan_btn = st.button("إطلاق المسح الذكي ⚡", use_container_width=True)

# مساحات العرض
col_b, col_l = st.columns(2)
col_b.markdown("### 🏛️ مدرسة القيمة (بافيت)")
col_l.markdown("### 🚀 مدرسة النمو (لينش)")

st.divider()
st.markdown("## 🏆 قائمة الفائزين (الفرص الذهبية)")
win_b, win_l = st.columns(2)

if scan_btn:
    value_winners = []
    growth_winners = []

    for sym in TASI_2026_SECTORS[sector_choice]:
        res = perform_deep_audit(sym)
        if res:
            # عرض تفاصيل بافيت
            with col_b:
                with st.container():
                    st.markdown(f"<div class='sector-card'><b>{res['name']}</b>", unsafe_allow_html=True)
                    for m in res['buffett']:
                        tag = "pass-tag" if m['pass'] else "fail-tag"
                        st.markdown(f"<div class='indicator-item {tag}'>{m['label']}: {m['val']}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            # عرض تفاصيل لينش
            with col_l:
                with st.container():
                    st.markdown(f"<div class='sector-card'><b>{res['name']}</b>", unsafe_allow_html=True)
                    for m in res['lynch']:
                        tag = "pass-tag" if m['pass'] else "fail-tag"
                        st.markdown(f"<div class='indicator-item {tag}'>{m['label']}: {m['val']}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            # حساب الفائزين (يجب أن يجتاز جميع الشروط ليظهر في الأسفل)
            if all(m['pass'] for m in res['buffett']):
                value_winners.append(f"{res['name']} ({sym})")
            
            if all(m['pass'] for m in res['lynch']):
                growth_winners.append(f"{res['name']} ({sym})")

    # عرض الفائزين فقط في الخانات السفلية
    with win_b:
        st.markdown("<div class='winner-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#00ff41;'>💎 نخبة القيمة</h4>", unsafe_allow_html=True)
        if value_winners:
            for w in value_winners: st.markdown(f"<div class='winner-item'>🏆 {w}</div>", unsafe_allow_html=True)
        else: st.write("جاري البحث عن فرص...")
        st.markdown("</div>", unsafe_allow_html=True)

    with win_l:
        st.markdown("<div class='winner-box' style='border-color:#bc13fe;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#bc13fe;'>🔥 صواريخ النمو</h4>", unsafe_allow_html=True)
        if growth_winners:
            for w in growth_winners: st.markdown(f"<div class='winner-item' style='color:#bc13fe;'>🚀 {w}</div>", unsafe_allow_html=True)
        else: st.write("جاري البحث عن فرص...")
        st.markdown("</div>", unsafe_allow_html=True)
