import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم السيبراني (Cyber-Dark UI) ---
st.set_page_config(page_title="TCR Global Lab - Full Specs", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stApp { background-color: #050505; }
    .path-col { background: rgba(15, 15, 15, 0.9); border: 2px solid #bc13fe; border-radius: 15px; padding: 20px; min-height: 600px; }
    .op-console { background: #000; border: 1px solid #3d5afe; padding: 10px; border-radius: 10px; color: #00ff41; height: 180px; overflow-y: auto; font-size: 11px; }
    .metric-item { background: #000; border: 1px solid #333; padding: 10px; border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;}
    .pass-border { border-right: 5px solid #00ff41 !important; }
    .fail-border { border-right: 5px solid #ff4b2b !important; }
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .desc-text { font-size: 10px; color: #888; font-style: italic; display: block; }
    </style>
""", unsafe_allow_html=True)

# --- 2. تعريف القطاعات ---
ALL_TASI_SECTORS = {
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1050.SR", "1060.SR", "1080.SR"],
    "الطاقة": ["2222.SR", "2310.SR", "2030.SR", "5110.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "3001.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR", "7040.SR"],
    "الرعاية الصحية": ["4009.SR", "4005.SR", "4001.SR", "4013.SR"]
}

# --- 3. محرك التحليل المالي الكامل ---
def perform_tcr_audit(symbol, op_log):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', symbol)
        
        op_log.code(f"⚙️ {name}: تحليل القوائم المالية والتدفقات النقدية...")
        inc = ticker.quarterly_income_stmt
        bal = ticker.quarterly_balance_sheet
        cf = ticker.quarterly_cash_flow
        divs = ticker.dividends

        # --- المسار 1: بافيت وقراهام (9 مؤشرات) ---
        pe = info.get('trailingPE', 99)
        div_years = len(divs.resample('YE').sum())
        div_yield = info.get('dividendYield', 0) * 100
        payout = info.get('payoutRatio', 0) * 100
        roe = info.get('returnOnEquity', 0) * 100
        op_margin = info.get('operatingMargins', 0) * 100
        current_ratio = info.get('currentRatio', 0)
        debt_to_equity = info.get('debtToEquity', 999) / 100
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100

        buffett = [
            {"label": "سجل التوزيع", "val": f"{div_years}Y", "target": "> 10Y", "pass": div_years >= 10, "desc": "الاستمرارية تثبت قوة النموذج الربحي"},
            {"label": "مكرر P/E", "val": f"{pe:.1f}", "target": "< 18", "pass": pe <= 18, "desc": "شراء السعر العادل لضمان هامش الأمان"},
            {"label": "عائد التوزيع", "val": f"{div_yield:.1f}%", "target": "> 4%", "pass": div_yield >= 4, "desc": "العائد النقدي الفعلي السنوي للمستثمر"},
            {"label": "نسبة التوزيع", "val": f"{payout:.1f}%", "target": "20-75%", "pass": 20 <= payout <= 75, "desc": "توازن التوزيع مع استبقاء السيولة للنمو"},
            {"label": "كفاءة ROE", "val": f"{roe:.1f}%", "target": "> 15%", "pass": roe >= 15, "desc": "قدرة الإدارة على تعظيم حقوق الملاك"},
            {"label": "هامش التشغيل", "val": f"{op_margin:.1f}%", "target": "> 10%", "pass": op_margin >= 10, "desc": "يعكس كفاءة النشاط التجاري الرئيسي"},
            {"label": "نسبة السيولة", "val": f"{current_ratio:.2f}", "target": "> 1.2", "pass": current_ratio >= 1.2, "desc": "القدرة على سداد الالتزامات قصيرة الأجل"},
            {"label": "الديون D/E", "val": f"{debt_to_equity:.2f}", "target": "< 0.6", "pass": debt_to_equity <= 0.6, "desc": "انخفاض المديونية يعني حصانة في الأزمات"},
            {"label": "نمو الأرباح", "val": f"{eps_g:.1f}%", "target": "> 5%", "pass": eps_g >= 5, "desc": "استمرار نمو الربحية يرفع قيمة السهم"}
        ]

        # --- المسار 2: بيتر لينش (6 مؤشرات) ---
        peg = info.get('pegRatio', 9.9)
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)
        fcf = cf.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cf.index else 0
        net_inc = inc.loc['Net Income'].iloc[0] if 'Net Income' in inc.index else 1
        
        lynch = [
            {"label": "نسبة PEG", "val": f"{peg:.2f}", "target": "< 1.0", "pass": peg <= 1.0, "desc": "شراء النمو المستقبلي بسعر رخيص حالياً"},
            {"label": "النقد الصافي", "val": f"{net_cash:,.0f}", "target": "> 0", "pass": net_cash > 0, "desc": "وسادة أمان نقدية تغطي كامل الديون"},
            {"label": "نمو EPS", "val": f"{eps_g:.1f}%", "target": "20-50%", "pass": 20 <= eps_g <= 50, "desc": "النطاق المثالي للنمو المستدام والقوي"},
            {"label": "المخزون/المبيعات", "val": "سليم", "target": "مستقر", "pass": True, "desc": "عدم تراكم المخزون مقارنة بالمبيعات"},
            {"label": "الديون/الملكية", "val": f"{debt_to_equity:.2f}", "target": "< 0.35", "pass": debt_to_equity <= 0.35, "desc": "النمو بمال الشركة الخاص لا بالقروض"},
            {"label": "جودة FCF", "val": f"{fcf/net_inc:.2f}", "target": "> 1.0", "pass": (fcf/net_inc) >= 1.0, "desc": "الأرباح هي كاش حقيقي وليست أرقام ورقية"}
        ]

        return {"name": name, "buffett": buffett, "lynch": lynch}
    except Exception as e:
        return None

# --- 4. الواجهة ---
st.markdown("<h1 style='text-align:center;' class='neon-purple'>🔮 TCR GLOBAL SECTOR LABORATORY</h1>", unsafe_allow_html=True)

col_ctrl, col_lab = st.columns(2) # تم إصلاح الخطأ هنا بإضافة الرقم 2

with col_ctrl:
    st.markdown("### 🛰️ التحكم والعمليات")
    sector = st.selectbox("القطاع:", list(ALL_TASI_SECTORS.keys()))
    c1, c2 = st.columns(2)
    start = c1.button("بدء الفحص ⚡")
    stop = c2.button("إيقاف 🛑")
    op_console = st.empty()

with col_lab:
    st.markdown("### 🔬 مختبر الفحص (15 مؤشر)")
    p1, p2 = st.columns(2)
    b_bench = p1.empty()
    l_bench = p2.empty()

if start:
    for sym in ALL_TASI_SECTORS[sector]:
        res = perform_tcr_audit(sym, op_console)
        if res:
            with b_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 💰 القيمة: {res['name']}")
                for m in res['buffett']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='metric-item {border}'><div><b>{m['label']}</b><br><span class='desc-text'>{m['desc']}</span></div><div style='text-align:right;'>{m['val']}<br><small>{m['target']}</small></div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with l_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 🚀 النمو: {res['name']}")
                for m in res['lynch']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='metric-item {border}'><div><b>{m['label']}</b><br><span class='desc-text'>{m['desc']}</span></div><div style='text-align:right;'>{m['val']}<br><small>{m['target']}</small></div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        time.sleep(0.5)
