import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. هندسة الواجهة (Advanced UI Engineering) ---
st.set_page_config(page_title="TCR Professional Lab", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* تصميم الخلفية والخطوط */
    .main { background-color: #050505; color: #E0E0E0; font-family: 'Inter', sans-serif; }
    .stApp { background-color: #050505; }
    
    /* حاوية المفاعل المركزي (Test Bench) */
    .reactor-container {
        background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
        border: 2px solid #bc13fe;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 30px rgba(188, 19, 254, 0.2);
        margin-bottom: 40px;
        text-align: center;
    }

    /* خانات المؤشرات (Test Tubes) */
    .test-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 15px;
        margin-top: 25px;
    }
    .test-tube {
        background: #000;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 15px;
        transition: 0.3s;
    }
    .tube-pass { border-color: #00ff41; box-shadow: 0 0 10px rgba(0, 255, 65, 0.3); }
    .tube-fail { border-color: #ff4b2b; box-shadow: 0 0 10px rgba(255, 75, 43, 0.3); }

    /* نصوص النيون */
    .neon-title { color: #bc13fe; text-shadow: 0 0 15px #bc13fe; font-size: 45px; font-weight: 900; }
    .company-name { color: #58A6FF; font-size: 28px; font-weight: bold; margin-bottom: 5px; }
    
    /* أزرار التحكم */
    .stButton>button {
        background: linear-gradient(90deg, #bc13fe, #3d5afe);
        color: white; border: none; border-radius: 50px;
        height: 4em; font-weight: bold; letter-spacing: 2px;
        transition: 0.4s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #bc13fe; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التحليل المالي (The Logic Core) ---
def run_tcr_logic(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', symbol)
        
        # استخراج المعايير
        metrics = [
            {"label": "PEG (Growth)", "val": info.get('pegRatio', 9.9), "target": "< 1.0", "key": "peg"},
            {"label": "EPS Growth", "val": info.get('earningsQuarterlyGrowth', 0) * 100, "target": "20-50%", "key": "eps"},
            {"label": "P/E Ratio", "val": info.get('trailingPE', 99), "target": "< 15", "key": "pe"},
            {"label": "Debt/Equity", "val": info.get('debtToEquity', 999)/100, "target": "< 0.35", "key": "debt"},
            {"label": "Payout Ratio", "val": info.get('payoutRatio', 0)*100, "target": "20-60%", "key": "payout"},
            {"label": "Net Cash", "val": (info.get('totalCash', 0) - info.get('totalDebt', 0))/1e6, "target": "> 0", "key": "cash"},
            {"label": "FCF Quality", "val": info.get('freeCashflow', 0)/info.get('netIncomeToCommon', 1) if info.get('netIncomeToCommon',0)>0 else 0, "target": "> 1.0", "key": "fcf"}
        ]

        # اختبار كل مؤشر
        results = []
        for m in metrics:
            passed = False
            reason = ""
            v = m['val']
            if m['key'] == "peg": passed = v < 1.0; reason = "High Value"
            elif m['key'] == "eps": passed = 20 <= v <= 50; reason = "Unstable"
            elif m['key'] == "pe": passed = v <= 15; reason = "Overpriced"
            elif m['key'] == "debt": passed = v < 0.35; reason = "High Debt"
            elif m['key'] == "payout": passed = 20 <= v <= 60; reason = "Imbalanced"
            elif m['key'] == "cash": passed = v > 0; reason = "Negative Cash"
            elif m['key'] == "fcf": passed = v > 1.0; reason = "Low Liquidity"
            
            results.append({**m, "passed": passed, "reason": reason})

        all_passed = all(r['passed'] for r in results)
        return {"name": name, "symbol": symbol, "checks": results, "final": all_passed}
    except: return None

# --- 3. بناء الواجهة الرسومية ---
st.markdown("<h1 class='neon-title'>TCR LABORATORY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>PREMIUM STOCK CRAWLER & FINANCIAL RANKER</p>", unsafe_allow_html=True)

# غرفة العمليات (Placeholder)
bench = st.empty()

# الأرشيف السفلي
st.markdown("### 🏺 THE ELITE VAULT (الفرص المكتشفة)")
vault = st.container()

if st.button("START EXPERIMENT (إطلاق الفحص)"):
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{c}.SR" for r in ranges for c in r]
    
    found_count = 0
    for sym in all_codes:
        res = run_tcr_logic(sym)
        if res:
            # تحديث المفاعل المركزي
            with bench.container():
                st.markdown(f"""
                <div class="reactor-container">
                    <div class="company-name">{res['name']}</div>
                    <div style="color:#bc13fe; font-weight:bold; letter-spacing:3px;">ANALYZING: {res['symbol']}</div>
                    <div class="test-grid">
                        {' '.join([f'''
                            <div class="test-tube {'tube-pass' if c['passed'] else 'tube-fail'}">
                                <div style="font-size:11px; color:#888;">{c['label']}</div>
                                <div style="font-size:16px; font-weight:bold; color:{'#00ff41' if c['passed'] else '#ff4b2b'};">{c['val'] if isinstance(c['val'], str) else round(c['val'],2)}</div>
                                <div style="font-size:10px;">{icon if (icon := '✅ OK' if c['passed'] else '❌ ' + c['reason']) else ''}</div>
                            </div>
                        ''' for c in res['checks']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # حفظ في الأرشيف إذا نجح السهم
            if res['final']:
                found_count += 1
                with vault:
                    st.success(f"🏆 نُخبة: {res['name']} ({res['symbol']})")
                    st.json(res['checks']) # عرض البيانات بشكل منظم
            
            time.sleep(0.01)
