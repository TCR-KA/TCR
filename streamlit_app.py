import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم البصري (Vanguard Cyber UI) ---
st.set_page_config(page_title="TCR Vanguard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #e0e0e0; }
    .stApp { background-color: #050505; }
    
    /* لوحة التحكم الرئيسية */
    .dashboard-panel {
        background: rgba(20, 20, 20, 0.95);
        border: 2px solid #bc13fe;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 40px rgba(188, 19, 254, 0.15);
    }
    
    /* خانات المؤشرات (Scanner Cells) */
    .indicator-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    .indicator-cell {
        background: #000;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        transition: 0.5s;
    }
    .cell-pass { border-color: #00ff41; box-shadow: 0 0 15px rgba(0, 255, 65, 0.2); }
    .cell-fail { border-color: #ff4b2b; box-shadow: 0 0 15px rgba(255, 75, 43, 0.2); }
    
    /* نصوص النيون */
    .neon-text { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .desc-text { font-size: 11px; color: #888; margin-top: 5px; }
    
    /* الأزرار */
    .stButton>button {
        background: linear-gradient(90deg, #bc13fe, #3d5afe);
        border: none; color: white; font-weight: bold; border-radius: 50px;
        height: 3.5em; letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك الفحص والتحليل (The Core) ---
def tcr_vanguard_scan(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', 'Unknown Entity')
        
        # مصفوفة المعايير
        criteria = [
            {"id": "PEG", "label": "مؤشر النمو (PEG)", "target": "< 1.0", "desc": "يقيس سعر السهم مقابل نمو أرباحه المتوقع.", "val": info.get('pegRatio', 9.9)},
            {"id": "EPS", "label": "نمو الأرباح (EPS)", "target": "20%-50%", "desc": "النمو السنوي المستدام للأرباح التشغيلية.", "val": info.get('earningsQuarterlyGrowth', 0) * 100},
            {"id": "PE", "label": "مكرر الربحية (P/E)", "target": "< 15", "desc": "تقييم السعر العادل بناءً على الأرباح الحالية.", "val": info.get('trailingPE', 99)},
            {"id": "DEBT", "label": "نسبة الديون (D/E)", "target": "< 0.35", "desc": "قوة الملاءة المالية وعدم الاعتماد على القروض.", "val": info.get('debtToEquity', 999) / 100},
            {"id": "CASH", "label": "النقد الصافي (Net Cash)", "target": "> 0", "desc": "توفر سيولة كاش تغطي كامل إجمالي الديون.", "val": info.get('totalCash', 0) - info.get('totalDebt', 0)}
        ]

        results = []
        for c in criteria:
            passed = False
            reason = ""
            v = c['val']
            if c['id'] == "PEG": passed = v < 1.0; reason = f"PEG {v:.2f} عالٍ"
            elif c['id'] == "EPS": passed = 20 <= v <= 50; reason = f"نمو {v:.1f}% غير مثالي"
            elif c['id'] == "PE": passed = v <= 15; reason = f"P/E {v:.1f} متضخم"
            elif c['id'] == "DEBT": passed = v < 0.35; reason = f"ديون {v:.2f} مرتفعة"
            elif c['id'] == "CASH": passed = v > 0; reason = "الديون > الكاش"
            
            results.append({**c, "passed": passed, "reason": reason if not passed else "✅ مطابق"})

        is_elite = all(r['passed'] for r in results)
        return {"name": name, "symbol": symbol, "checks": results, "elite": is_elite}
    except: return None

# --- 3. بناء لوحة البيانات ---
st.markdown("<h1 style='text-align:center; color:#bc13fe;'>🛡️ TCR VANGUARD SYSTEM</h1>", unsafe_allow_html=True)

# لوحة الفحص الثابتة (Placeholder)
scanner_placeholder = st.empty()

# الأرشيف (الفرص الذهبية)
st.markdown("### 🏺 THE ELITE VAULT")
vault = st.container()

if st.button("إطلاق فحص الحماية المالية ⚡"):
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_symbols = [f"{c}.SR" for r in ranges for c in r]
    
    for sym in all_symbols:
        res = tcr_vanguard_scan(sym)
        if res:
            with scanner_placeholder.container():
                st.markdown(f"""
                <div class="dashboard-panel">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h2 style="color:#58A6FF; margin:0;">{res['name']}</h2>
                        <span class="neon-text" style="font-size:20px;">SYMBOL: {res['symbol']}</span>
                    </div>
                    <div class="indicator-grid">
                        {' '.join([f'''
                            <div class="indicator-cell {'cell-pass' if c['passed'] else 'cell-fail'}">
                                <div style="font-size:12px; font-weight:bold;">{c['label']}</div>
                                <div style="font-size:20px; font-weight:900; color:{'#00ff41' if c['passed'] else '#ff4b2b'}; margin:5px 0;">{c['val'] if isinstance(c['val'], str) else round(c['val'],2)}</div>
                                <div style="font-size:11px; color:#aaa;">المعيار: {c['target']}</div>
                                <div style="font-size:10px; margin-top:5px; color:{'#00ff41' if c['passed'] else '#ff4b2b'};">{c['reason']}</div>
                                <div class="desc-text">{c['desc']}</div>
                            </div>
                        ''' for c in res['checks']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if res['elite']:
                with vault:
                    st.success(f"🏆 نُخبة: {res['name']} ({res['symbol']})")
                    st.json(res['checks'])
            
            time.sleep(0.01)
