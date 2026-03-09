import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم السيبراني المتقدم (إصلاح الفريمات والألوان) ---
st.set_page_config(page_title="TCR Global Sector Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stApp { background-color: #050505; }
    
    /* فريم الفائزين المحكم */
    .winner-box {
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        min-height: 250px;
        max-height: 400px;
        overflow-y: auto; /* إضافة سكرول داخلي إذا كثرت الشركات */
        display: block;
    }
    .value-border { border: 2px solid #00ff41 !important; box-shadow: 0 0 15px rgba(0, 255, 65, 0.2); }
    .growth-border { border: 2px solid #bc13fe !important; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); }

    /* العناوين داخل الفريمات */
    .inner-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 1px solid #333;
        display: block;
    }

    /* نصوص الشركات - الحفاظ على الألوان الأصلية */
    .stock-tag {
        padding: 8px;
        margin-bottom: 5px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 5px;
        font-size: 0.9rem;
        line-height: 1.4;
        word-wrap: break-word;
    }
    .v-color { color: #00ff41 !important; }
    .g-color { color: #bc13fe !important; }

    .neon-text { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. قاعدة بيانات تاسي الشاملة (21 قطاع) ---
TASI_2026_SECTORS = {
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1080.SR", "1020.SR", "1030.SR", "1060.SR", "1140.SR", "1111.SR"],
    "الطاقة": ["2222.SR", "2223.SR", "2310.SR", "2030.SR", "2381.SR", "2082.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "2002.SR", "2380.SR", "2250.SR", "2290.SR", "2330.SR", "3001.SR", "3002.SR", "3003.SR", "3004.SR", "3005.SR", "3010.SR", "3020.SR", "3030.SR", "3040.SR", "3050.SR", "3060.SR", "3080.SR", "3090.SR", "3091.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR", "7040.SR"],
    "التأمين": ["8010.SR", "8200.SR", "8210.SR", "8230.SR", "8240.SR", "8250.SR", "8260.SR", "8270.SR", "8280.SR", "8300.SR", "8310.SR", "8311.SR", "8312.SR", "8120.SR", "8150.SR", "8160.SR", "8170.SR", "8180.SR", "8190.SR"],
    "الرعاية الصحية": ["4001.SR", "4004.SR", "4005.SR", "4009.SR", "4013.SR", "2060.SR", "4011.SR"],
    "الخدمات التقنية": ["7200.SR", "7201.SR", "7202.SR", "7203.SR"],
    "المرافق العامة": ["2080.SR", "2083.SR", "4080.SR"],
    "النقل": ["4030.SR", "4031.SR", "4040.SR", "4110.SR", "4260.SR", "4261.SR"],
    "إدارة العقارات": ["4020.SR", "4150.SR", "4180.SR", "4190.SR", "4250.SR", "4300.SR", "4310.SR", "4321.SR"],
    "تجزئة الأغذية": ["4006.SR", "4160.SR", "4161.SR", "4162.SR"],
    "إنتاج الأغذية": ["2270.SR", "2280.SR", "6001.SR", "2100.SR", "2170.SR", "2281.SR", "2282.SR"],
    "تجزئة السلع": ["4008.SR", "4192.SR", "4240.SR", "4002.SR", "4004.SR", "4005.SR"],
    "السلع الرأسمالية": ["1301.SR", "1304.SR", "1320.SR", "2230.SR", "1214.SR", "2140.SR", "2300.SR", "2370.SR"],
    "الخدمات التجارية": ["1831.SR", "4071.SR", "4072.SR", "1832.SR"],
    "الخدمات الاستهلاكية": ["1810.SR", "4170.SR", "4290.SR", "6002.SR", "6004.SR"],
    "الإعلام والترفيه": ["4070.SR", "4210.SR", "4211.SR"],
    "السلع طويلة الأجل": ["1213.SR", "2340.SR", "4050.SR", "4141.SR"],
    "الأدوية": ["2070.SR", "4012.SR"],
    "الصناديق العقارية (REITs)": ["4330.SR", "4335.SR", "4340.SR", "4342.SR", "4344.SR", "4345.SR", "4346.SR", "4347.SR", "4348.SR"],
    "الاستثمار والتمويل": ["4081.SR", "4280.SR", "1170.SR"]
}

# --- 3. محرك الفحص الذكي ---
def perform_deep_audit(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('shortName', symbol)
        pe = info.get('trailingPE', 999)
        dy = info.get('dividendYield', 0) * 100
        roe = info.get('returnOnEquity', 0) * 100
        de = info.get('debtToEquity', 999) / 100

        # شروط الفوز الصارمة
        is_val = (pe <= 20 and dy >= 3.0)
        is_gro = (roe >= 15 and de <= 0.6)
        
        return {"name": name, "sym": symbol, "v": is_val, "g": is_gro}
    except: return None

# --- 4. بناء الواجهة ---
st.markdown("<h1 class='neon-text'>🔮 TCR GLOBAL SECTOR LABORATORY v3.0</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🛰️ التحكم")
    sector_choice = st.selectbox("اختر القطاع المستهدف:", list(TASI_2026_SECTORS.keys()))
    scan = st.button("إطلاق المسح الشامل ⚡", use_container_width=True)

if scan:
    v_winners, g_winners = [], []
    progress = st.progress(0)
    
    # حلقة المسح
    for idx, sym in enumerate(TASI_2026_SECTORS[sector_choice]):
        res = perform_deep_audit(sym)
        if res:
            if res['v']: v_winners.append(f"🏆 {res['name']} ({res['sym']})")
            if res['g']: g_winners.append(f"🚀 {res['name']} ({res['sym']})")
        progress.progress((idx + 1) / len(TASI_2026_SECTORS[sector_choice]))

    # عرض النتائج النهائية (الفائزون فقط داخل الفريمات)
    st.markdown("### 🏆 قائمة الفائزين (الفرص الذهبية)")
    col1, col2 = st.columns(2)

    with col1:
        v_html = "".join([f"<div class='stock-tag v-color'>{w}</div>" for w in v_winners]) if v_winners else "<div style='color:#555;'>لا توجد فرص مطابقة حالياً</div>"
        st.markdown(f"""
            <div class='winner-box value-border'>
                <div class='inner-title v-color'>💎 نخبة القيمة</div>
                {v_html}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        g_html = "".join([f"<div class='stock-tag g-color'>{w}</div>" for w in g_winners]) if g_winners else "<div style='color:#555;'>لا توجد فرص مطابقة حالياً</div>"
        st.markdown(f"""
            <div class='winner-box growth-border'>
                <div class='inner-title g-color'>🔥 صواريخ النمو</div>
                {g_html}
            </div>
        """, unsafe_allow_html=True)
    
    st.balloons()
