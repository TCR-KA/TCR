import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم الهندسي الفاخر (UI Dashboard CSS) ---
st.set_page_config(page_title="TCR Ultimate Dashboard", layout="wide")

st.markdown("""
    <style>
    /* الخلفية العامة */
    .stApp {
        background-color: #0b0e14;
        background-image: radial-gradient(circle at 20% 20%, #1a1a2e 0%, #0b0e14 100%);
        color: #ffffff;
    }
    
    /* تصميم البطاقات (Cards) */
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: 0.3s;
    }
    
    /* تأثير التوهج عند النجاح */
    .card-pass { border: 1px solid #00ff88; box-shadow: 0 0 15px rgba(0, 255, 136, 0.2); }
    .card-fail { border: 1px solid #ff0055; box-shadow: 0 0 15px rgba(255, 0, 85, 0.2); }

    /* العناوين والقيم */
    .metric-label { font-size: 12px; color: #8a8a8a; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { font-size: 24px; font-weight: 900; margin: 10px 0; font-family: 'Monaco', monospace; }
    .status-text { font-size: 10px; font-weight: bold; }
    
    /* اسم الشركة الرئيسي */
    .company-header {
        background: linear-gradient(90deg, #bc13fe, #3d5afe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px; font-weight: 800; text-align: center;
    }
    
    /* تخصيص الأزرار */
    .stButton>button {
        background: linear-gradient(45deg, #bc13fe, #3d5afe);
        color: white; border: none; border-radius: 10px;
        height: 3.5em; font-weight: bold; width: 100%;
        box-shadow: 0 4px 15px rgba(188, 19, 254, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك الفحص والتشخيص ---
def run_tcr_ultimate_scan(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # استخراج البيانات السبعة
        metrics = [
            {"id": "PEG", "label": "مؤشر PEG", "target": "< 1.0", "val": info.get('pegRatio', 9.9), "desc": "سعر السهم مقابل النمو"},
            {"id": "EPS", "label": "نمو EPS", "target": "20-50%", "val": info.get('earningsQuarterlyGrowth', 0)*100, "desc": "نمو الأرباح التشغيلية"},
            {"id": "PE", "label": "مكرر P/E", "target": "< 15", "val": info.get('trailingPE', 99), "desc": "تقييم السعر العادل"},
            {"id": "DEBT", "label": "ديون D/E", "target": "< 0.35", "val": info.get('debtToEquity', 999)/100, "desc": "مستوى الأمان المالي"},
            {"id": "PAY", "label": "التوزيع %", "target": "20-60%", "val": info.get('payoutRatio', 0)*100, "desc": "اتزان توزيع الأرباح"},
            {"id": "CASH", "label": "صافي النقد", "target": "> 0", "val": (info.get('totalCash', 0)-info.get('totalDebt', 0))/1e6, "desc": "الكاش المتوفر بالمليون"},
            {"id": "FCF", "label": "جودة FCF", "target": "> 1.0", "val": info.get('freeCashflow', 0)/info.get('netIncomeToCommon', 1) if info.get('netIncomeToCommon',0)>0 else 0, "desc": "تحويل الربح لكاش حقيقي"}
        ]

        # اختبار المطابقة
        final_results = []
        for m in metrics:
            p = False
            if m['id']=="PEG": p = m['val'] < 1.0
            elif m['id']=="EPS": p = 20 <= m['val'] <= 50
            elif m['id']=="PE": p = m['val'] <= 15
            elif m['id']=="DEBT": p = m['val'] < 0.35
            elif m['id']=="PAY": p = 20 <= m['val'] <= 60
            elif m['id']=="CASH": p = m['val'] > 0
            elif m['id']=="FCF": p = m['val'] > 1.0
            final_results.append({**m, "passed": p})
            
        return {"name": info.get('longName', symbol), "symbol": symbol, "data": final_results, "elite": all(r['passed'] for r in final_results)}
    except: return None

# --- 3. بناء الواجهة التفاعلية ---
st.markdown("<div style='text-align:center;'><h1 style='color:#bc13fe; margin-bottom:0;'>TCR ULTIMATE</h1><p style='color:#888;'>PREMIUM FINANCIAL SCANNER UNIT</p></div>", unsafe_allow_html=True)

# مساحة الفحص النشطة
scanner_view = st.empty()

# قائمة النخبة (The Vault)
st.markdown("---")
st.markdown("### 🏺 THE ELITE VAULT")
vault = st.container()

if st.button("LAUNCH SCANNER (إطلاق الفحص)"):
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{c}.SR" for r in ranges for c in r]
    
    for sym in all_codes:
        res = run_tcr_ultimate_scan(sym)
        if res:
            with scanner_view.container():
                st.markdown(f"<div class='company-header'>{res['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center; color:#58A6FF;'>{res['symbol']} | مراجعة الميزانيات والنمو التشغيلي</p>", unsafe_allow_html=True)
                
                # عرض البطاقات بنظام Grid
                cols = st.columns(len(res['data']))
                for i, m in enumerate(res['data']):
                    status_class = "card-pass" if m['passed'] else "card-fail"
                    status_color = "#00ff88" if m['passed'] else "#ff0055"
                    
                    cols[i].markdown(f"""
                        <div class="card {status_class}">
                            <div class="metric-label">{m['label']}</div>
                            <div class="metric-value" style="color:{status_color};">{round(m['val'],2) if not isinstance(m['val'], str) else m['val']}</div>
                            <div class="status-text">{m['desc']}</div>
                            <div style="font-size:9px; margin-top:5px; color:#888;">Target: {m['target']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            if res['elite']:
                with vault:
                    st.success(f"🏆 نُخبة: {res['name']} ({res['symbol']})")
            
            time.sleep(0.01)
