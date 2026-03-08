import streamlit as st
import yfinance as yf
import pandas as pd
import time

# 1. إعدادات الواجهة الرسومية لنظام TCR
st.set_page_config(page_title="TCR - Tadawul Crawler & Ranker", page_icon="📈", layout="wide")

# تصميم بسيط واحترافي للواجهة
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1E88E5; color: white; font-weight: bold; }
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ نظام TCR لفلترة الأسهم السعودية")
st.info("هذا التطبيق يقوم بمسح السوق السعودي (TASI) للبحث عن فرص النمو (بيتر لينش) والعوائد (بافيت) وعرضها هنا مباشرة.")

# 2. القائمة الجانبية للتحكم في صرامة الفلاتر
with st.sidebar:
    st.header("⚙️ معايير التصفية")
    peg_limit = st.slider("الحد الأقصى لـ PEG", 0.1, 2.0, 1.0)
    pe_limit = st.slider("الحد الأقصى لـ P/E", 5, 40, 15)
    min_eps_growth = st.number_input("أدنى نمو للأرباح %", value=20)
    st.divider()
    st.caption("نظام TCR - تحليل آلي يعتمد على البيانات الحية.")

# 3. وظيفة التحليل المالي لكل سهم
def analyze_stock(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if 'currentPrice' not in info: return None
        
        # استخراج البيانات المالية الأساسية
        peg = info.get('pegRatio', 999)
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100
        pe = info.get('trailingPE', 999)
        debt_equity = info.get('debtToEquity', 999) / 100
        payout = info.get('payoutRatio', 0) * 100
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)

        # تطبيق معايير TCR (نمو أو عوائد)
        is_growth = (peg <= peg_limit and min_eps_growth <= eps_g <= 50 and debt_equity < 0.35)
        is_value = (pe <= pe_limit and 20 <= payout <= 60 and debt_equity <= 0.50)

        if is_growth or is_value:
            return {
                "الرمز": symbol,
                "الاسم": info.get('longName', 'N/A'),
                "السعر": f"{info.get('currentPrice')} ر.س",
                "التصنيف": "🚀 فرصة نمو" if is_growth else "💰 سهم عوائد",
                "P/E": round(pe, 2) if pe != 999 else "N/A",
                "PEG": peg if peg != 999 else "N/A",
                "الديون": round(debt_equity, 2),
                "النقد الصافي": f"{net_cash:,.0f} ر.س"
            }
    except:
        return None

# 4. زر التشغيل وعرض النتائج داخل التطبيق
if st.button("إطلاق رادار TCR لفحص السوق السعودي 🔍"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    found_stocks = []

    # نطاقات رموز تداول (TASI)
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{code}.SR" for r in ranges for code in r]
    
    total_count = len(all_codes)
    
    for idx, sym in enumerate(all_codes):
        status_text.text(f"يتم الآن فحص وتحليل السهم: {sym} ({idx+1}/{total_count})")
        res = analyze_stock(sym)
        if res:
            found_stocks.append(res)
        progress_bar.progress((idx + 1) / total_count)
        # تأخير بسيط لضمان استقرار جلب البيانات من Yahoo Finance
        if idx % 15 == 0: time.sleep(0.1)

    status_text.empty()
    st.markdown("---")
    
    if found_stocks:
        st.success(f"🎯 تم العثور على ({len(found_stocks)}) فرص تطابق معايير TCR اليوم!")
        df = pd.DataFrame(found_stocks)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ لا توجد شركات في السوق السعودي تطابق المعايير الصارمة حالياً.")
