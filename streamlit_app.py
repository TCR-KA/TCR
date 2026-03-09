import streamlit as st
import yfinance as yf
import pandas as pd
import time
import plotly.graph_objects as go

# --- 1. واجهة المختبر السيبراني (Cyber-Black & Purple) ---
st.set_page_config(page_title="TCR - Sector Master", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #bc13fe; }
    .stApp { background-color: #050505; }
    .neon-card { border: 2px solid #bc13fe; border-radius: 15px; padding: 25px; background: rgba(10, 10, 10, 0.9); box-shadow: 0 0 20px rgba(188, 19, 254, 0.3); }
    .stButton>button { background: linear-gradient(45deg, #bc13fe, #3d5afe); color: white; font-weight: bold; border-radius: 10px; height: 3.5em; width: 100%; border: none; }
    .op-log { background: #000; border-left: 3px solid #3d5afe; padding: 10px; font-family: monospace; color: #00ff41; font-size: 11px; height: 200px; overflow-y: auto; }
    </style>
""", unsafe_allow_html=True)

# --- 2. تعريف قطاعات السوق السعودي (2026 TASI Sectors) ---
TASI_SECTORS = {
    "الطاقة": ["2222.SR", "2310.SR", "2030.SR", "5110.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "3001.SR", "3010.SR", "3020.SR"],
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1050.SR", "1060.SR", "1080.SR", "1140.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR", "7040.SR"],
    "الرعاية الصحية": ["4009.SR", "4005.SR", "4001.SR", "4013.SR", "4003.SR"],
    "إنتاج الأغذية": ["2270.SR", "2280.SR", "6010.SR", "6060.SR"],
    "السلع الرأسمالية": ["2320.SR", "1301.SR", "1303.SR", "1214.SR"],
    "النقل": ["4260.SR", "4040.SR", "4110.SR"],
    "الاستثمار والتمويل": ["2120.SR", "2170.SR", "4081.SR"],
    "تجزئة الأغذية": ["4006.SR", "4161.SR", "4163.SR"],
    "الخدمات التجارية والمهنية": ["4071.SR", "4072.SR", "1831.SR"],
    "المرافق العامة": ["2080.SR", "5110.SR", "2081.SR"],
    "التطوير العقاري": ["4020.SR", "4150.SR", "4250.SR", "4300.SR"],
    "إدارة وتطوير العقارات": ["4321.SR", "4100.SR", "4012.SR"]
}

# --- 3. محرك التحليل المالي المزدوج (Manual Calculations) ---
def deep_tcr_scan(symbol, log):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', symbol)
        
        # المرحلة 1: جمع البيانات المالية الخام
        log.write(f"⚙️ {name}: جلب الميزانية وقائمة الدخل السنوية...")
        financials = ticker.financials
        balance = ticker.balance_sheet
        
        # 1. معايير بيتر لينش (نمو)
        peg = info.get('pegRatio', 99)
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100
        debt_equity = info.get('debtToEquity', 999) / 100
        net_cash = (info.get('totalCash', 0) - info.get('totalDebt', 0))
        
        lynch_pass = (peg < 1.0 and 20 <= eps_g <= 50 and debt_equity < 0.35 and net_cash > 0)
        
        # 2. معايير بافيت (عوائد)
        pe = info.get('trailingPE', 99)
        payout = info.get('payoutRatio', 0) * 100
        
        buffett_pass = (pe <= 15 and 20 <= payout <= 60 and debt_equity < 0.50)

        # التقييم
        result_type = "🚀 نمو (Lynch)" if lynch_pass else ("💰 عوائد (Buffett)" if buffett_pass else "FAIL")
        
        return {
            "symbol": symbol, "name": name, "type": result_type,
            "peg": peg, "eps_g": eps_g, "debt": debt_equity, "pe": pe, "payout": payout,
            "status": "PASS" if result_type != "FAIL" else "FAIL"
        }
    except: return None

# --- 4. واجهة التطبيق التفاعلية ---
st.markdown("<h1 style='text-align:center; color:#bc13fe;'>🔮 TCR ULTIMATE: SECTOR ANALYZER</h1>", unsafe_allow_html=True)

col_ctrl, col_lab = st.columns([1, 2])

with col_ctrl:
    st.markdown("### 🛰️ مركز التحكم")
    sector_choice = st.selectbox("اختر القطاع للفحص:", ["كامل السوق"] + list(TASI_SECTORS.keys()))
    
    c1, c2 = st.columns(2)
    start_btn = c1.button("إطلاق المسح ⚡")
    stop_btn = c2.button("إيقاف البحث 🛑")
    
    st.markdown("📖 **سجل العمليات الحية:**")
    op_log = st.empty()

with col_lab:
    st.markdown("### 🔬 مختبر الفحص الحي")
    live_bench = st.empty()

results_area = st.container()

if start_btn:
    # تحديد الشركات بناءً على الخيار
    target_symbols = []
    if sector_choice == "كامل السوق":
        for s_list in TASI_SECTORS.values(): target_symbols.extend(s_list)
    else:
        target_symbols = TASI_SECTORS[sector_choice]
    
    found_stocks = []
    for idx, sym in enumerate(target_symbols):
        if stop_btn: break
        
        log_txt = f"🔍 يتم الآن تحليل: {sym}..."
        op_log.markdown(f"<div class='op-log'>{log_txt}</div>", unsafe_allow_html=True)
        
        res = deep_tcr_scan(sym, st)
        if res:
            # عرض عملية الفحص بخانات منفصلة
            with live_bench.container():
                st.markdown(f"""
                <div class='neon-card'>
                    <h3>الشركة: {res['name']} ({res['symbol']})</h3>
                    <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px;'>
                        <div><b>PEG:</b> {res['peg']}</div>
                        <div><b>P/E:</b> {res['pe']}</div>
                        <div><b>Debt/Equity:</b> {res['debt']}</div>
                    </div>
                    <hr>
                    <div style='color:{"#00ff41" if res["status"]=="PASS" else "#ff4b2b"}'>التقييم: {res['type']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            if res["status"] == "PASS":
                found_stocks.append(res)
        time.sleep(0.1)

    st.markdown("---")
    if found_stocks:
        st.success(f"🎯 تم العثور على {len(found_stocks)} فرص ذهبية!")
        st.table(pd.DataFrame(found_stocks))
