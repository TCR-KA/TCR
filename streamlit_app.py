import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. الإعدادات الجمالية (Dark Mode & UI) ---
st.set_page_config(page_title="TCR - Lynch & Buffett Master", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #E0E0E0; }
    .stMetric { background-color: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 10px; }
    .status-card { padding: 20px; border-radius: 12px; background-color: #161B22; border: 2px solid #30363D; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .match-tag { color: #2ecc71; font-weight: bold; }
    .fail-tag { color: #e74c3c; font-weight: bold; }
    h1, h2, h3 { color: #58A6FF !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك التحليل العميق لـ TCR ---
def analyze_stock_deep(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        financials = ticker.financials
        cf = ticker.cashflow
        
        if financials.empty or 'Operating Income' not in financials.index:
            return None, "بيانات مالية ناقصة"

        # --- حساب مؤشرات بيتر لينش (النمو 🚀) ---
        peg = info.get('pegRatio', 999)
        # نمو EPS (مقارنة ربعية تشغيلية)
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100
        # الديون / الملكية
        debt_equity = info.get('debtToEquity', 999) / 100
        # النقد الصافي
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)
        # جودة الأرباح FCF vs Net Income
        fcf = cf.loc['Free Cash Flow'].iloc if 'Free Cash Flow' in cf.index else 0
        net_inc = financials.loc['Net Income Common Stock Holders'].iloc
        fcf_quality = fcf / net_inc if net_inc > 0 else 0

        # --- حساب مؤشرات بافيت (القيمة 💰) ---
        pe = info.get('trailingPE', 999)
        payout = info.get('payoutRatio', 0) * 100
        
        # اختبارات المطابقة
        lynch_pass = (peg < 1.0 and 20 <= eps_g <= 50 and debt_equity < 0.35 and net_cash > 0 and fcf_quality > 1.0)
        buffett_pass = (pe <= 15 and 20 <= payout <= 60 and debt_equity < 0.50)

        res = {
            "Symbol": symbol,
            "Name": info.get('longName', 'N/A'),
            "Type": "🚀 نمو صارم" if lynch_pass else ("💰 عوائد ذهبية" if buffett_pass else "فشل"),
            "PEG": peg, "EPS_G": eps_g, "D_E": debt_equity, "Net_Cash": net_cash,
            "FCF_Q": fcf_quality, "PE": pe, "Payout": payout
        }
        return res, "OK"
    except:
        return None, "خطأ فني"

# --- 3. الواجهة الرئيسية ---
st.title("🛡️ نظام TCR: رادار بافيت ولينش")
st.markdown("<p style='text-align: center;'>فحص القوائم المالية لـ 200+ شركة سعودية لحظة بلحظة</p>", unsafe_allow_html=True)

# عدادات علوية
c1, c2, c3, c4 = st.columns(4)
total_scanned = c1.empty()
matches_found = c2.empty()
failed_debt = c3.empty()
failed_growth = c4.empty()

start_btn = st.button("إطلاق رادار TCR التشغيلي ⚡")

if start_btn:
    found = []
    # إحصائيات حية
    cnt, m_cnt, d_fail, g_fail = 0, 0, 0, 0
    
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{c}.SR" for r in ranges for c in r]
    
    status_box = st.empty()
    
    for sym in all_codes:
        cnt += 1
        with status_box.container():
            st.markdown(f"""
            <div class="status-card">
                <h4>🔍 يتم الآن تحليل: <span style='color:#58A6FF'>{sym}</span></h4>
                <p>مراجعة: PEG | الديون | التدفق النقدي | مكرر الربحية</p>
            </div>
            """, unsafe_allow_html=True)
        
        data, status = analyze_stock_deep(sym)
        
        if data:
            # تحديث عدادات الفشل (للعلم فقط)
            if data['D_E'] > 0.5: d_fail += 1
            if not (20 <= data['EPS_G'] <= 50): g_fail += 1
            
            if data['Type'] != "فشل":
                found.append(data)
                m_cnt += 1
                st.toast(f"🎯 تم صيد فرصة: {sym}", icon="✅")
        
        # تحديث الأرقام الحية
        total_scanned.metric("تم فحصه", cnt)
        matches_found.metric("فرص مكتشفة", m_cnt, delta_color="normal")
        failed_debt.metric("فشل (ديون)", d_fail)
        failed_growth.metric("فشل (نمو)", g_fail)
        
        time.sleep(0.05)

    status_box.empty()
    st.markdown("---")
    if found:
        st.header("🏆 القائمة الذهبية المكتشفة")
        df = pd.DataFrame(found).drop(columns=['Type'])
        st.dataframe(df.style.background_gradient(cmap='Blues'), use_container_width=True)
    else:
        st.error("📉 لا يوجد أي سهم حالياً يجمع بين أمان بافيت ونمو بيتر لينش الصارم.")
