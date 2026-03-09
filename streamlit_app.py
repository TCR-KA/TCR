import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم السيبراني (Neon Dark Theme) ---
st.set_page_config(page_title="TCR - Cyber Scan", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    /* الخلفية والخطوط العامة */
    .main { background-color: #050505; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تصميم البطاقات والحاويات */
    .stApp { background-color: #050505; }
    .status-card { 
        background: rgba(15, 15, 15, 0.9); 
        border: 1px solid #bc13fe; 
        box-shadow: 0 0 15px #bc13fe; 
        padding: 25px; border-radius: 15px; 
        margin-bottom: 25px;
    }
    
    /* نصوص النيون */
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .neon-blue { color: #3d5afe; text-shadow: 0 0 10px #3d5afe; font-weight: bold; }
    
    /* الأزرار السيبرانية */
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 4em; 
        background: linear-gradient(45deg, #bc13fe, #3d5afe); 
        color: white; border: none; font-weight: bold; font-size: 18px;
        transition: 0.4s; text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover { box-shadow: 0 0 25px #bc13fe; transform: scale(1.02); }

    /* جداول النيون */
    .stDataFrame { border: 1px solid #3d5afe !important; border-radius: 10px; }
    h1, h2, h3 { color: #bc13fe !important; text-shadow: 0 0 8px #bc13fe; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. المحرك المالي TCR ---
def analyze_stock_deep(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        financials = ticker.financials
        cf = ticker.cashflow
        
        # استخراج مؤشرات لينش (النمو)
        peg = info.get('pegRatio', 999)
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100
        debt_equity = info.get('debtToEquity', 999) / 100
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)
        fcf = cf.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cf.index else 0
        net_inc = financials.loc['Net Income Common Stock Holders'].iloc[0] if 'Net Income Common Stock Holders' in financials.index else 1
        fcf_quality = fcf / net_inc if net_inc > 0 else 0

        # استخراج مؤشرات بافيت (القيمة)
        pe = info.get('trailingPE', 999)
        payout = info.get('payoutRatio', 0) * 100

        # فلاتر TCR الصارمة
        lynch_pass = (peg < 1.0 and 20 <= eps_g <= 50 and debt_equity < 0.35 and net_cash > 0 and fcf_quality > 1.0)
        buffett_pass = (pe <= 15 and 20 <= payout <= 60 and debt_equity < 0.50)

        res = {
            "Symbol": symbol, "Name": info.get('longName', 'N/A'),
            "Type": "🚀 GROWTH" if lynch_pass else ("💰 VALUE" if buffett_pass else "FAIL"),
            "PEG": peg, "EPS_G": eps_g, "D_E": debt_equity, "Net_Cash": net_cash,
            "FCF_Q": fcf_quality, "PE": pe, "Payout": payout
        }
        return res, "OK"
    except:
        return None, "Error"

# --- 3. واجهة التحكم والبحث ---
st.markdown("<h1>🔮 TCR: THE CYBER SCANNER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #3d5afe;'>رادار فحص القوائم المالية للسوق السعودي - نسخة النيون</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
total_view = col1.empty()
match_view = col2.empty()
debt_view = col3.empty()
growth_view = col4.empty()

start_btn = st.button("إطلاق المسح السيبراني ⚡")

if start_btn:
    found = []
    scanned, matches, d_fail, g_fail = 0, 0, 0, 0
    
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{c}.SR" for r in ranges for code_range in ranges for c in code_range]
    all_codes = list(dict.fromkeys(all_codes)) # إزالة التكرار

    live_status = st.empty()

    for sym in all_codes:
        scanned += 1
        with live_status.container():
            st.markdown(f"""
            <div class="status-card">
                <h3 class="neon-purple">🔍 تحليل الهدف: {sym}</h3>
                <p>مراجعة تدفق النقد السنوي | فحص جودة الأرباح التشغيلية | اختبار الملاءة المالية</p>
                <div style="display: flex; justify-content: space-around;">
                    <span class="neon-blue">PEG: SCANNING</span>
                    <span class="neon-blue">DEBT: CHECKING</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        data, status = analyze_stock_deep(sym)
        
        if data:
            if data['D_E'] > 0.5: d_fail += 1
            if not (20 <= data['EPS_G'] <= 50): g_fail += 1
            
            if data['Type'] != "FAIL":
                matches += 1
                found.append(data)
                st.toast(f"🎯 تم صيد فرصة ذهبية: {sym}", icon="🔥")

        # تحديث العدادات الحية بلمسة نيون
        total_view.markdown(f"<div class='stMetric'><p>الممسوح</p><h2 class='neon-blue'>{scanned}</h2></div>", unsafe_allow_html=True)
        match_view.markdown(f"<div class='stMetric'><p>الفرص</p><h2 class='neon-purple'>{matches}</h2></div>", unsafe_allow_html=True)
        debt_view.markdown(f"<div class='stMetric'><p>استبعاد (ديون)</p><h2 style='color: #ff4b2b;'>{d_fail}</h2></div>", unsafe_allow_html=True)
        growth_view.markdown(f"<div class='stMetric'><p>استبعاد (نمو)</p><h2 style='color: #ff4b2b;'>{g_fail}</h2></div>", unsafe_allow_html=True)
        
        time.sleep(0.01)

    live_status.empty()
    if found:
        st.markdown("<h2 class='neon-purple'>🏆 القائمة الذهبية المكتشفة</h2>", unsafe_allow_html=True)
        df = pd.DataFrame(found).drop(columns=['Type'])
        st.dataframe(df.style.set_properties(**{'background-color': '#050505', 'color': '#bc13fe', 'border-color': '#3d5afe'}))
    else:
        st.error("📉 لم يتم العثور على فرص تطابق المعايير الصارمة اليوم.")
