import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم السيبراني (Cyber-Black & Neon Purple) ---
st.set_page_config(page_title="TCR - Automated Test Bench", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #bc13fe; }
    .stApp { background-color: #050505; }
    .test-bench { 
        background: #111; border: 2px solid #bc13fe; 
        padding: 20px; border-radius: 15px; box-shadow: 0 0 20px #bc13fe;
    }
    .neon-text { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-size: 20px; font-weight: bold; }
    .data-val { color: #3d5afe; font-family: 'Courier New', monospace; font-size: 18px; }
    .pass { color: #00ff41; text-shadow: 0 0 5px #00ff41; }
    .fail { color: #ff4b2b; text-shadow: 0 0 5px #ff4b2b; }
    .stButton>button { background: linear-gradient(45deg, #bc13fe, #3d5afe); color: white; border: none; font-weight: bold; height: 3.5em; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك الفحص التشخيصي لـ TCR ---
def perform_tcr_scan(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', symbol) # جلب الاسم الصريح للشركة
        
        # استخراج البيانات المالية
        peg = info.get('pegRatio', 9.9)
        pe = info.get('trailingPE', 99)
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100
        debt_eq = info.get('debtToEquity', 999) / 100
        payout = info.get('payoutRatio', 0) * 100
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)

        # هيكل الاختبارات (لينش + بافيت)
        tests = [
            {"label": "1. مكرر النمو PEG", "val": f"{peg:.2f}", "target": "< 1.0", "ok": peg < 1.0, "reason": "سعر مرتفع للنمو"},
            {"label": "2. نمو الأرباح EPS", "val": f"{eps_g:.1f}%", "target": "20-50%", "ok": 20 <= eps_g <= 50, "reason": "نمو غير مثالي"},
            {"label": "3. مكرر الربحية P/E", "val": f"{pe:.1f}", "target": "< 15", "ok": pe <= 15, "reason": "السهم متضخم"},
            {"label": "4. نسبة الديون D/E", "val": f"{debt_eq:.2f}", "target": "< 0.35", "ok": debt_eq < 0.35, "reason": "ديون مرتفعة"},
            {"label": "5. نسبة التوزيع", "val": f"{payout:.1f}%", "target": "20-60%", "ok": 20 <= payout <= 60, "reason": "توزيع غير متزن"},
            {"label": "6. النقد الصافي", "val": f"{net_cash:,.0f}", "target": "> 0", "ok": net_cash > 0, "reason": "سيولة ضعيفة"}
        ]
        
        all_passed = all(t['ok'] for t in tests)
        return {"name": name, "symbol": symbol, "tests": tests, "passed": all_passed}
    except: return None

# --- 3. واجهة المستخدم ---
st.markdown("<h1>🔮 TCR: CYBER TEST BENCH</h1>", unsafe_allow_html=True)

# القسم العلوي: خط الفحص الحي
st.markdown("### 🔬 مختبر الفحص الفوري")
bench_placeholder = st.empty()

# القسم السفلي: قائمة النخبة (تظهر فقط عند النجاح)
st.markdown("---")
st.markdown("### 🏆 قائمة الفرص الذهبية المكتشفة")
results_container = st.container()

if st.button("إطلاق عملية المسح الآلي للسوق السعودي ⚡"):
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{c}.SR" for r in ranges for c in r]
    
    confirmed_opportunities = []

    for sym in all_codes:
        res = perform_tcr_scan(sym)
        if res:
            # تحديث شاشة الفحص الثابتة (تختفي وتظهر لكل شركة)
            with bench_placeholder.container():
                st.markdown(f"""
                <div class='test_bench'>
                    <div style='display:flex; justify-content:space-between;'>
                        <span class='neon-text'>الشركة الحالية: {res['name']}</span>
                        <span class='neon-text'>الرمز: {res['symbol']}</span>
                    </div>
                    <hr style='border-color:#bc13fe;'>
                    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;'>
                        {" ".join([f"<div><b>{t['label']}</b><br><span class='data-val'>{t['val']}</span><br><span class='{'pass' if t['ok'] else 'fail'}'>{'✅ مطابق' if t['ok'] else '❌ '+t['reason']}</span></div>" for t in res['tests']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # إذا نجحت الشركة، أضفها للقائمة السفلية للأبد
            if res['passed']:
                confirmed_opportunities.append(res)
                with results_container:
                    st.success(f"🎯 فرصة ذهبية مكتشفة: {res['name']} ({res['symbol']})")
                    st.write(pd.DataFrame([{t['label']: t['val'] for t in res['tests']}]))
            
            time.sleep(0.02) # سرعة الفحص
