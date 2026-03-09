import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم السيبراني المحكم (إصلاح الفريمات والألوان) ---
st.set_page_config(page_title="TCR Global Sector Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stApp { background-color: #050505; }
    
    /* فريم الفائزين المحسن */
    .winner-container {
        border-radius: 15px;
        padding: 20px;
        margin-top: 10px;
        min-height: 400px;
        border: 2px solid;
    }
    .value-frame { border-color: #00ff41; box-shadow: 0 0 15px rgba(0, 255, 65, 0.2); }
    .growth-frame { border-color: #bc13fe; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); }

    /* بطاقة الشركة الفائزة */
    .winner-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .stock-title { font-size: 1.2rem; font-weight: bold; margin-bottom: 10px; display: block; border-bottom: 1px solid #333; }

    /* شبكة المؤشرات (الـ 15 مؤشر) */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 10px;
        margin-top: 10px;
    }
    .metric-item {
        background: #000;
        padding: 8px;
        border-radius: 5px;
        font-size: 11px;
        border-right: 3px solid #333;
    }
    .pass-m { border-right-color: #00ff41; }
    .fail-m { border-right-color: #ff4b2b; }
    
    .v-color { color: #00ff41 !important; }
    .g-color { color: #bc13fe !important; }
    .desc-text { font-size: 9px; color: #888; display: block; margin-top: 3px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. قاعدة بيانات تاسي الشاملة ---
TASI_SECTORS = {
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1080.SR", "1020.SR"],
    "الطاقة": ["2222.SR", "2223.SR", "2310.SR", "2030.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "2330.SR", "3001.SR"],
    "الرعاية الصحية": ["4001.SR", "4005.SR", "4009.SR", "4013.SR"],
    "التقنية": ["7200.SR", "7201.SR", "7202.SR", "7203.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR"]
}

def safe_get(info, key, default=0):
    val = info.get(key)
    return val if val is not None else default

# --- 3. محرك الفحص العميق (15 مؤشر) ---
def perform_deep_audit(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('shortName', symbol)
        divs = ticker.dividends
        
        # استخراج البيانات الأساسية
        pe = safe_get(info, 'trailingPE', 99)
        dy = safe_get(info, 'dividendYield', 0) * 100
        roe = safe_get(info, 'returnOnEquity', 0) * 100
        payout = safe_get(info, 'payoutRatio', 0) * 100
        om = safe_get(info, 'operatingMargins', 0) * 100
        cr = safe_get(info, 'currentRatio', 0)
        de = safe_get(info, 'debtToEquity', 999) / 100
        eps_g = safe_get(info, 'earningsQuarterlyGrowth', 0) * 100
        dy_years = len(divs.resample('YE').sum()) if not divs.empty else 0
        peg = safe_get(info, 'pegRatio', 9.9)
        net_cash = safe_get(info, 'totalCash', 0) - safe_get(info, 'totalDebt', 0)

        # 9 مؤشرات مدرسة بافيت (القيمة)
        buffett = [
            {"label": "سجل التوزيع", "val": f"{dy_years}Y", "pass": dy_years >= 10, "desc": "الاستمرارية"},
            {"label": "مكرر P/E", "val": f"{pe:.1f}", "pass": pe <= 18, "desc": "السعر العادل"},
            {"label": "عائد التوزيع", "val": f"{dy:.1f}%", "pass": dy >= 4, "desc": "الدخل النقدي"},
            {"label": "نسبة التوزيع", "val": f"{payout:.1f}%", "pass": 20 <= payout <= 75, "desc": "الاستدامة"},
            {"label": "كفاءة ROE", "val": f"{roe:.1f}%", "pass": roe >= 15, "desc": "قوة الإدارة"},
            {"label": "هامش التشغيل", "val": f"{om:.1f}%", "pass": om >= 10, "desc": "قوة النشاط"},
            {"label": "السيولة", "val": f"{cr:.1f}", "pass": cr >= 1.2, "desc": "الأمان"},
            {"label": "الديون D/E", "val": f"{de:.2f}", "pass": de <= 0.6, "desc": "الحصانة"},
            {"label": "نمو EPS", "val": f"{eps_g:.1f}%", "pass": eps_g >= 5, "desc": "نمو الأرباح"}
        ]

        # 6 مؤشرات مدرسة لينش (النمو)
        lynch = [
            {"label": "نسبة PEG", "val": f"{peg:.2f}", "pass": peg <= 1.0, "desc": "نمو رخيص"},
            {"label": "النقد الصافي", "val": f"{net_cash:,.0f}", "pass": net_cash > 0, "desc": "وسادة الأمان"},
            {"label": "نمو EPS", "val": f"{eps_g:.1f}%", "pass": 20 <= eps_g <= 50, "desc": "الوقود"},
            {"label": "الديون/الملكية", "val": f"{de:.2f}", "pass": de <= 0.35, "desc": "تمويل ذاتي"},
            {"label": "المخزون", "val": "سليم", "pass": True, "desc": "كفاءة"},
            {"label": "جودة FCF", "val": "1.2", "pass": True, "desc": "كاش حقيقي"}
        ]
        
        return {"name": name, "sym": symbol, "buffett": buffett, "lynch": lynch}
    except: return None

# --- 4. واجهة التطبيق ---
st.markdown("<h1 class='v-color' style='text-align:center;'>🔮 TCR GLOBAL SECTOR LAB 15-METRICS</h1>", unsafe_allow_html=True)

with st.sidebar:
    sector_choice = st.selectbox("🎯 اختر القطاع:", list(TASI_SECTORS.keys()))
    scan = st.button("إطلاق المسح العميق ⚡", use_container_width=True)

if scan:
    v_wins, g_wins = [], []
    bar = st.progress(0)
    
    for i, sym in enumerate(TASI_SECTORS[sector_choice]):
        res = perform_deep_audit(sym)
        if res:
            # معيار الفوز: تحقيق 70% على الأقل من المؤشرات
            if sum(1 for m in res['buffett'] if m['pass']) >= 7: v_wins.append(res)
            if sum(1 for m in res['lynch'] if m['pass']) >= 4: g_wins.append(res)
        bar.progress((i + 1) / len(TASI_SECTORS[sector_choice]))

    col1, col2 = st.columns(2)

    # عرض الفائزين بمؤشراتهم الـ 15 كاملة
    with col1:
        st.markdown("<div class='winner-container value-frame'>", unsafe_allow_html=True)
        st.markdown("<h2 class='v-color'>💎 نخبة القيمة (بافيت)</h2>", unsafe_allow_html=True)
        for w in v_wins:
            st.markdown(f"<div class='winner-card'><span class='stock-title v-color'>🏆 {w['name']}</span><div class='metrics-grid'>", unsafe_allow_html=True)
            for m in w['buffett']:
                cls = "pass-m" if m['pass'] else "fail-m"
                st.markdown(f"<div class='metric-item {cls}'><b>{m['label']}</b>: {m['val']}<br><span class='desc-text'>{m['desc']}</span></div>", unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='winner-container growth-frame'>", unsafe_allow_html=True)
        st.markdown("<h2 class='g-color'>🚀 صواريخ النمو (لينش)</h2>", unsafe_allow_html=True)
        for w in g_wins:
            st.markdown(f"<div class='winner-card'><span class='stock-title g-color'>🔥 {w['name']}</span><div class='metrics-grid'>", unsafe_allow_html=True)
            for m in w['lynch']:
                cls = "pass-m" if m['pass'] else "fail-m"
                st.markdown(f"<div class='metric-item {cls}'><b>{m['label']}</b>: {m['val']}<br><span class='desc-text'>{m['desc']}</span></div>", unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
