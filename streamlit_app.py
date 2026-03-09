import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- الإعدادات السيبرانية ---
st.set_page_config(page_title="TCR Cyber Scanner", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #050505; color: #bc13fe; }
    .stApp { background-color: #050505; }
    .neon-box { border: 1px solid #bc13fe; box-shadow: 0 0 15px #bc13fe; padding: 20px; border-radius: 15px; background: #000; }
    .stButton>button { background: linear-gradient(45deg, #bc13fe, #3d5afe); color: white; border: none; font-weight: bold; box-shadow: 0 0 10px #bc13fe; }
    h1, h2, h3 { color: #bc13fe !important; text-shadow: 0 0 10px #bc13fe; text-align: center; }
    </style>
""", unsafe_allow_html=True)

def deep_financial_check(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # سحب بيانات 4 سنوات
        hist_inc = ticker.financials 
        hist_bs = ticker.balance_sheet
        hist_cf = ticker.cashflow
        info = ticker.info

        if hist_inc.empty or 'Net Income' not in hist_inc.index: return None

        # 1. حساب متوسط النمو السنوي (3 سنوات) - بيتر لينش
        net_income_series = hist_inc.loc['Net Income Common Stock Holders']
        growth_rates = net_income_series.pct_change(periods=-1).dropna()
        avg_growth = growth_rates.mean() # يجب أن يكون 20-50%

        # 2. جودة الأرباح التشغيلية
        op_income = hist_inc.loc['Operating Income'].iloc[0]
        net_income_latest = net_income_series.iloc[0]
        op_quality = op_income / net_income_latest # يجب أن يكون > 0.85

        # 3. النقد الصافي والديون
        total_cash = info.get('totalCash', 0)
        total_debt = info.get('totalDebt', 0)
        net_cash = total_cash - total_debt
        debt_to_equity = info.get('debtToEquity', 999) / 100

        # 4. معايير بافيت (P/E & Payout)
        pe = info.get('trailingPE', 999)
        peg = info.get('pegRatio', 999)
        payout = info.get('payoutRatio', 0)

        # المنطق الصارم المشترك
        is_lynch = (0.20 <= avg_growth <= 0.50 and peg < 1.0 and debt_to_equity < 0.35 and net_cash > 0)
        is_buffett = (pe <= 15 and 0.20 <= payout <= 0.60 and debt_equity < 0.50)

        if is_lynch or is_buffett:
            return {
                "الرمز": symbol,
                "الشركة": info.get('longName', 'N/A'),
                "النمو السنوي": f"{avg_growth*100:.1f}%",
                "P/E": pe,
                "PEG": peg,
                "جودة الأرباح": "✅ تشغيلية" if op_quality > 0.85 else "⚠️ استثنائية",
                "النوع": "🚀 نمو (Lynch)" if is_lynch else "💰 قيمة (Buffett)"
            }
        return None
    except: return None

st.markdown("<h1>🔮 TCR: CYBER RADAR TASI</h1>", unsafe_allow_html=True)
if st.button("إطلاق المسح العميق ⚡"):
    found = []
    # نطاقات تاسي
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_symbols = [f"{c}.SR" for r in ranges for c in r]
    
    progress = st.progress(0)
    status = st.empty()
    
    for i, sym in enumerate(all_symbols):
        status.markdown(f"<div class='neon-box'>🔍 فحص الميزانيات التاريخية: {sym}</div>", unsafe_allow_html=True)
        res = deep_financial_check(sym)
        if res: found.append(res)
        progress.progress((i+1)/len(all_symbols))
        time.sleep(0.05)

    st.markdown("---")
    if found:
        st.success(f"🎯 تم العثور على {len(found)} فرص حقيقية")
        st.dataframe(pd.DataFrame(found))
    else:
        st.error("📉 لم يجتز أي سهم الفلتر الصارم لبيانات تداول اليوم.")
