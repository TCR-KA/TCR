import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. إعداد واجهة المختبر الفاخرة ---
st.set_page_config(page_title="TCR Financial Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #ffffff; }
    .op-log { 
        background-color: #000; border: 1px solid #bc13fe; padding: 15px; 
        border-radius: 10px; height: 300px; overflow-y: auto; 
        font-family: 'Courier New', monospace; font-size: 13px; color: #00ff41;
    }
    .status-card { background: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .stButton>button { background: linear-gradient(45deg, #bc13fe, #3d5afe); color: white; border: none; font-weight: bold; width: 100%; height: 3.5em; }
    </style>
""", unsafe_allow_html=True)

# --- 2. المحرك المالي العميق (Deep Analysis Engine) ---
def deep_tcr_analysis(symbol, log_placeholder):
    try:
        ticker = yf.Ticker(symbol)
        
        # المرحلة 1: جمع البيانات الخام
        log_placeholder.markdown(f"📡 `[{symbol}]` جاري جلب القوائم المالية التاريخية (4 سنوات)...")
        income_stmt = ticker.quarterly_income_stmt
        balance_sheet = ticker.quarterly_balance_sheet
        cash_flow = ticker.quarterly_cashflow
        info = ticker.info

        if income_stmt.empty or balance_sheet.empty:
            log_placeholder.markdown(f"⚠️ `[{symbol}]` بيانات غير مكتملة. تخطي.")
            return None

        # المرحلة 2: تحليل نمو بيتر لينش (Peter Lynch)
        log_placeholder.markdown(f"🔍 `[{symbol}]` جاري فحص معايير النمو (بيتر لينش)...")
        op_inc = income_stmt.loc['Operating Income']
        growth = op_inc.pct_change(periods=-1).mean() # متوسط النمو التشغيلي
        peg = info.get('pegRatio', 99)
        debt_to_equity = info.get('debtToEquity', 999) / 100
        
        is_growth = (peg < 1.0 and 0.20 <= growth <= 0.50 and debt_to_equity < 0.35)
        
        # المرحلة 3: تحليل عوائد وارن بافيت (Warren Buffett)
        log_placeholder.markdown(f"💰 `[{symbol}]` جاري فحص معايير العوائد والقيمة (وارن بافيت)...")
        pe = info.get('trailingPE', 99)
        payout = info.get('payoutRatio', 0)
        # فحص استمرارية التوزيعات
        div_history = ticker.dividends
        has_consistent_div = len(div_history.resample('YE').sum()) >= 5
        
        is_value = (pe <= 15 and 0.20 <= payout <= 0.60 and debt_to_equity <= 0.50)

        # المرحلة 4: تقييم النتيجة
        final_type = "🚀 نمو (Lynch)" if is_growth else ("💎 عوائد (Buffett)" if is_value else None)
        
        if final_type:
            log_placeholder.markdown(f"✅ `[{symbol}]` تطابق السهم مع فئة: {final_type}")
        else:
            log_placeholder.markdown(f"❌ `[{symbol}]` لم يطابق المعايير الصارمة.")

        return {
            "الرمز": symbol, "الاسم": info.get('longName', 'N/A'),
            "النوع": final_type, "P/E": pe, "PEG": peg, "نمو": f"{growth*100:.1f}%",
            "ديون": debt_to_equity, "توزيع": f"{payout*100:.1f}%"
        }
    except Exception as e:
        log_placeholder.markdown(f"🛑 `[{symbol}]` خطأ أثناء التحليل: {str(e)}")
        return None

# --- 3. بناء لوحة القيادة ---
st.title("🛡️ نظام TCR: مختبر تحليل الأسهم السعودية")
st.markdown("---")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("⚙️ التحكم والعمليات")
    start_btn = st.button("إطلاق المسح العميق ⚡")
    st.write("📖 **صندوق العمليات الحية:**")
    log_area = st.empty()
    log_content = ""

with col_right:
    st.subheader("🏆 النتائج النهائية (النخبة)")
    results_area = st.container()

if start_btn:
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{c}.SR" for r in ranges for c in r]
    
    found_stocks = []
    
    for sym in all_codes:
        # تحديث صندوق العمليات
        res = deep_tcr_analysis(sym, log_area)
        if res and res["النوع"]:
            found_stocks.append(res)
            with results_area:
                st.success(f"🎯 فرصة مكتشفة: {res['الاسم']} ({res['الرمز']})")
                st.write(pd.DataFrame([res]))
        
        time.sleep(0.1) # سرعة معتدلة لملاحظة العمليات
