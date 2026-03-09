import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم السيبراني المتقدم (TCR Lab UI) ---
st.set_page_config(page_title="TCR Financial Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #bc13fe; }
    .stApp { background-color: #050505; }
    .step-box { 
        background: #111; border: 1px solid #bc13fe; 
        padding: 10px; border-radius: 8px; margin: 5px 0;
        box-shadow: 0 0 5px #bc13fe; font-size: 14px;
    }
    .neon-text { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .fail-text { color: #ff4b2b; text-shadow: 0 0 5px #ff4b2b; }
    .pass-text { color: #00ff41; text-shadow: 0 0 5px #00ff41; }
    .header-box { border-bottom: 2px solid #bc13fe; padding-bottom: 10px; margin-bottom: 20px; text-align: center; }
    .stButton>button { background: linear-gradient(45deg, #bc13fe, #3d5afe); color: white; border: none; font-weight: bold; width: 100%; height: 3em; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك التحليل التشخيصي (Diagnostic Engine) ---
def tcr_diagnostic_scan(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        financials = ticker.financials
        
        # استخراج البيانات
        peg = info.get('pegRatio', 999)
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100
        debt_equity = info.get('debtToEquity', 999) / 100
        pe = info.get('trailingPE', 999)
        payout = info.get('payoutRatio', 0) * 100
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)
        
        # مراجعة التدفق النقدي (FCF Quality)
        fcf = ticker.cashflow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in ticker.cashflow.index else 0
        net_inc = financials.loc['Net Income Common Stock Holders'].iloc[0] if 'Net Income Common Stock Holders' in financials.index else 1
        fcf_quality = fcf / net_inc if net_inc > 0 else 0

        # سجل النتائج
        steps = [
            {"name": "PEG (Lynch)", "val": peg, "limit": "< 1.0", "pass": peg < 1.0, "reason": f"PEG {peg} مرتفع" if peg >= 1.0 else "مثالي"},
            {"name": "نمو EPS", "val": f"{eps_g:.1f}%", "limit": "20-50%", "pass": 20 <= eps_g <= 50, "reason": f"نمو {eps_g:.1f}% خارج النطاق"},
            {"name": "الديون/الملكية", "val": debt_equity, "limit": "< 0.35", "pass": debt_equity < 0.35, "reason": f"ديون {debt_equity:.2f} مرتفعة"},
            {"name": "جودة FCF", "val": round(fcf_quality, 2), "limit": "> 1.0", "pass": fcf_quality > 1.0, "reason": "سيولة ضعيفة"},
            {"name": "مكرر P/E", "val": pe, "limit": "< 15", "pass": pe <= 15, "reason": f"سعر عالٍ {pe}"},
            {"name": "نسبة التوزيع", "val": f"{payout:.1f}%", "limit": "20-60%", "pass": 20 <= payout <= 60, "reason": "توزيع غير متزن"},
            {"name": "النقد الصافي", "val": f"{net_cash:,.0f}", "limit": "> 0", "pass": net_cash > 0, "reason": "ديون أكبر من الكاش"}
        ]

        # التقييم النهائي
        lynch_match = all(s['pass'] for s in steps[:4])
        buffett_match = all(s['pass'] for s in steps[4:])
        
        final_status = "🚀 نمو ذهبي" if lynch_match else ("💰 عوائد بافيت" if buffett_match else "❌ لم يجتز")
        
        return {
            "name": info.get('longName', symbol),
            "steps": steps,
            "final": final_status
        }
    except: return None

# --- 3. واجهة العرض (Dashboard) ---
st.markdown("<div class='header-box'><h1 class='neon-text'>🔮 TCR FINANCIAL LABORATORY</h1></div>", unsafe_allow_html=True)

col_ctrl, col_view = st.columns([1, 2])

with col_ctrl:
    st.markdown("### 🛠️ غرفة التحكم")
    start_btn = st.button("إطلاق المسح التشخيصي ⚡")
    st.markdown("---")
    st.write("📖 **دليل المؤشرات:**")
    st.caption("PEG: يقيس السعر مقابل النمو.\nEPS: نمو أرباح الشركة السنوي.\nD/E: نسبة الديون مقابل حقوق الملاك.")

if start_btn:
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{c}.SR" for r in ranges for c in r]
    
    found_stocks = []
    
    for sym in all_codes:
        result = tcr_diagnostic_scan(sym)
        if result:
            with col_view:
                # خانة اسم الشركة الحالية
                st.markdown(f"#### 🔍 فحص: <span class='neon-text'>{result['name']} ({sym})</span>", unsafe_allow_html=True)
                
                # عرض المؤشرات بخانات منفصلة
                for s in result['steps']:
                    status_class = "pass-text" if s['pass'] else "fail-text"
                    icon = "✅" if s['pass'] else "❌"
                    
                    st.markdown(f"""
                    <div class='step-box'>
                        <span style='width:120px; display:inline-block;'><b>{s['name']}</b></span> | 
                        المعيار: {s['limit']} | 
                        الفعلي: {s['val']} | 
                        <span class='{status_class}'>{icon} {s['reason'] if not s['pass'] else 'مطابق'}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # التقييم النهائي
                final_color = "#00ff41" if result['final'] != "❌ لم يجتز" else "#ff4b2b"
                st.markdown(f"### التقييم النهائي: <span style='color:{final_color}'>{result['final']}</span>", unsafe_allow_html=True)
                st.markdown("---")
                
                if result['final'] != "❌ لم يجتز":
                    found_stocks.append(result)
                    st.balloons()
            
            time.sleep(0.05)
