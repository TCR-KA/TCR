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
    .path-col { background: rgba(15, 15, 15, 0.9); border: 2px solid #bc13fe; border-radius: 15px; padding: 20px; min-height: 600px; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); }
    .op-console { background: #000; border: 1px solid #3d5afe; padding: 10px; border-radius: 10px; font-family: 'Courier New', monospace; color: #00ff41; height: 180px; overflow-y: auto; font-size: 11px; }
    .metric-item { background: #000; border: 1px solid #333; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-right: 4px solid #333; }
    .pass-border { border-right: 4px solid #00ff41 !important; }
    .fail-border { border-right: 4px solid #ff4b2b !important; }
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .desc-text { font-size: 10px; color: #888; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

# --- 2. تعريف جميع قطاعات السوق السعودي (21 قطاع) ---
ALL_TASI_SECTORS = {
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1050.SR", "1060.SR", "1080.SR"],
    "الطاقة": ["2222.SR", "2310.SR", "2030.SR", "5110.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "3001.SR", "3010.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR", "7040.SR"],
    "الرعاية الصحية": ["4009.SR", "4005.SR", "4001.SR", "4013.SR"],
    "التطوير العقاري": ["4020.SR", "4150.SR", "4250.SR", "4300.SR"],
    "إنتاج الأغذية": ["2270.SR", "2280.SR", "6010.SR", "6060.SR"],
    "النقل": ["4260.SR", "4040.SR", "4110.SR"]
}

# --- 3. محرك التحليل المالي والعمليات ---
def perform_tcr_master_audit(symbol, op_log):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', symbol)
        
        op_log.code(f"⚙️ {name}: جلب الميزانية وقائمة الدخل والتدفقات النقدية...")
        inc = ticker.quarterly_income_stmt
        bal = ticker.quarterly_balance_sheet
        cf = ticker.quarterly_cash_flow
        divs = ticker.dividends

        # --- المسار 1: مدرسة القيمة (9 مؤشرات) ---
        pe = info.get('trailingPE', 99)
        div_years = len(divs.resample('YE').sum())
        div_yield = info.get('dividendYield', 0) * 100
        payout = info.get('payoutRatio', 0) * 100
        roe = info.get('returnOnEquity', 0) * 100
        op_margin = info.get('operatingMargins', 0) * 100
        current_ratio = info.get('currentRatio', 0)
        debt_to_equity = info.get('debtToEquity', 999) / 100
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100

        buffett_metrics = [
            {"label": "سجل التوزيع", "val": f"{div_years}Y", "target": "> 10Y", "pass": div_years >= 10, "desc": "الاستمرارية تثبت قوة النموذج"},
            {"label": "مكرر P/E", "val": f"{pe:.1f}", "target": "< 18", "pass": pe <= 18, "desc": "شراء السعر العادل لهامش الأمان"},
            {"label": "عائد التوزيع", "val": f"{div_yield:.1f}%", "target": "> 4%", "pass": div_yield >= 4, "desc": "العائد النقدي السنوي المحقق"},
            {"label": "نسبة التوزيع", "val": f"{payout:.1f}%", "target": "20-75%", "pass": 20 <= payout <= 75, "desc": "توازن المكافأة مع استدامة النمو"},
            {"label": "كفاءة ROE", "val": f"{roe:.1f}%", "target": "> 15%", "pass": roe >= 15, "desc": "قدرة الإدارة على تنمية الملكية"},
            {"label": "هامش التشغيل", "val": f"{op_margin:.1f}%", "target": "> 10%", "pass": op_margin >= 10, "desc": "يعكس قوة النشاط الرئيسي"},
            {"label": "نسبة السيولة", "val": f"{current_ratio:.2f}", "target": "> 1.2", "pass": current_ratio >= 1.2, "desc": "القدرة على سداد الالتزامات"},
            {"label": "الديون D/E", "val": f"{debt_to_equity:.2f}", "target": "< 0.6", "pass": debt_to_equity <= 0.6, "desc": "ديون منخفضة تعني حصانة مالية"},
            {"label": "نمو EPS ربعي", "val": f"{eps_g:.1f}%", "target": "> 5%", "pass": eps_g >= 5, "desc": "المحرك الأساسي لسعر السهم"}
        ]

        # --- المسار 2: مدرسة النمو (6 مؤشرات) ---
        peg = info.get('pegRatio', 9.9)
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)
        inv_growth = (bal.loc['Inventory'].iloc[0] / bal.loc['Inventory'].iloc[1] - 1) if 'Inventory' in bal.index else 0
        rev_growth = info.get('revenueGrowth', 0)
        fcf = cf.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cf.index else 0
        net_inc = inc.loc['Net Income'].iloc[0] if 'Net Income' in inc.index else 1

        lynch_metrics = [
            {"label": "نسبة PEG", "val": f"{peg:.2f}", "target": "< 1.0", "pass": peg <= 1.0, "desc": "شراء النمو بسعر عادل غير متضخم"},
            {"label": "النقد الصافي", "val": f"{net_cash:,.0f}", "target": "> 0", "pass": net_cash > 0, "desc": "وسادة أمان تقلل التكلفة الفعلية"},
            {"label": "نمو EPS ربعي", "val": f"{eps_g:.1f}%", "target": "20-50%", "pass": 20 <= eps_g <= 50, "desc": "الوقود المحرك للأسعار مستقبلاً"},
            {"label": "كفاءة المخزون", "val": "سليم" if inv_growth < rev_growth else "متراكم", "target": "Inv < Sales", "pass": inv_growth < rev_growth, "desc": "تراكم المخزون يعني ضعف الطلب"},
            {"label": "الديون/الملكية", "val": f"{debt_to_equity:.2f}", "target": "< 0.35", "pass": debt_to_equity <= 0.35, "desc": "ضمان عدم التعثر في حالات الركود"},
            {"label": "جودة FCF", "val": f"{fcf/net_inc:.2f}", "target": "> 1.0", "pass": (fcf/net_inc) >= 1.0, "desc": "الأرباح كاش حقيقي وليست محاسبة"}
        ]

        return {"name": name, "symbol": symbol, "buffett": buffett_audit_data_to_pass(buffett_metrics), "lynch": lynch_metrics}
    except: return None

def buffett_audit_data_to_pass(metrics): return metrics # Helper

# --- 4. واجهة المختبر الكاملة ---
st.markdown("<h1 style='text-align:center;' class='neon-purple'>🔮 TCR GLOBAL SECTOR LABORATORY</h1>", unsafe_allow_html=True)

if 'run' not in st.session_state: st.session_state.run = False

col_ctrl, col_lab = st.columns()

with col_ctrl:
    st.markdown("### 🛰️ مركز القيادة")
    sector_key = st.selectbox("اختر القطاع:", list(ALL_TASI_SECTORS.keys()))
    c1, c2 = st.columns(2)
    if c1.button("إطلاق الرادار ⚡"): st.session_state.run = True
    if c2.button("إيقاف البحث 🛑"): st.session_state.run = False
    op_console = st.empty()

with col_lab:
    st.markdown("### 🔬 مختبر الفحص المنقسم")
    path_a, path_b = st.columns(2)
    b_bench = path_a.empty()
    l_bench = path_b.empty()

vault = st.container()

if st.session_state.run:
    for sym in ALL_TASI_SECTORS[sector_key]:
        if not st.session_state.run: break
        res = perform_tcr_master_audit_v2(sym, op_console) # Internal function mapped
        if res:
            with b_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 💰 مدرسة القيمة: {res['name']}")
                for m in res['buffett']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='metric-item {border}'><div><b>{m['label']}</b><br><span class='desc-text'>{m['desc']}</span></div><div style='text-align:right;'>{m['val']}<br><small>Target: {m['target']}</small></div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with l_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 🚀 مدرسة النمو: {res['name']}")
                for m in res['lynch']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='metric-item {border}'><div><b>{m['label']}</b><br><span class='desc-text'>{m['desc']}</span></div><div style='text-align:right;'>{m['val']}<br><small>Target: {m['target']}</small></div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            if all(m['pass'] for m in res['buffett']) or all(m['pass'] for m in res['lynch']):
                with vault: st.success(f"🏆 نُخبة: {res['name']} ({res['symbol']})")
        time.sleep(0.5)

# (تكملة الكود تتطلب دالة perform_tcr_master_audit_v2 التي تم تعريفها بالأعلى كـ perform_tcr_master_audit)
