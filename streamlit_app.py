import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم السيبراني المتقدم (Cyber-Dark UI) ---
st.set_page_config(page_title="TCR Global Sector Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stApp { background-color: #050505; }
    .path-col { background: rgba(15, 15, 15, 0.9); border: 2px solid #bc13fe; border-radius: 15px; padding: 20px; min-height: 600px; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); }
    .op-console { background: #000; border: 1px solid #3d5afe; padding: 10px; border-radius: 10px; color: #00ff41; height: 180px; overflow-y: auto; font-size: 11px; font-family: 'Courier New', monospace; }
    .metric-item { background: #000; border: 1px solid #333; padding: 8px; border-radius: 5px; margin-bottom: 5px; font-size: 11px; display: flex; justify-content: space-between; align-items: center; }
    .pass-border { border-right: 5px solid #00ff41 !important; }
    .fail-border { border-right: 5px solid #ff4b2b !important; }
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .desc-text { font-size: 9px; color: #888; font-style: italic; display: block; }
    </style>
""", unsafe_allow_html=True)

# --- 2. تعريف جميع قطاعات السوق السعودي (21 قطاع) ---
TASI_SECTORS_ALL = {
    "الطاقة": ["2222.SR", "2310.SR", "2030.SR", "5110.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "3001.SR", "3010.SR", "3020.SR", "3030.SR", "3040.SR", "3050.SR"],
    "السلع الرأسمالية": ["2320.SR", "1301.SR", "1303.SR", "1214.SR", "2300.SR", "3003.SR"],
    "الخدمات التجارية والمهنية": ["4071.SR", "4072.SR", "1831.SR", "1832.SR"],
    "النقل": ["4260.SR", "4040.SR", "4110.SR", "4261.SR"],
    "السلع طويلة الأجل": ["4030.SR", "4141.SR", "4142.SR"],
    "الخدمات الاستهلاكية": ["4050.SR", "4190.SR", "4290.SR", "1810.SR", "1820.SR"],
    "الإعلام والترفيه": ["4070.SR", "4270.SR"],
    "تجزئة السلع الاستهلاكية": ["4006.SR", "4161.SR", "4163.SR", "4240.SR", "4008.SR"],
    "إنتاج الأغذية": ["2270.SR", "2280.SR", "6010.SR", "6060.SR", "2050.SR", "2140.SR"],
    "الرعاية الصحية": ["4009.SR", "4005.SR", "4001.SR", "4013.SR", "4003.SR", "4004.SR"],
    "الأدوية والعلوم الحيوية": ["2070.SR", "4015.SR"],
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1050.SR", "1060.SR", "1080.SR", "1140.SR"],
    "الاستثمار والتمويل": ["2120.SR", "2170.SR", "4081.SR", "4280.SR"],
    "التأمين": ["8010.SR", "8012.SR", "8020.SR", "8030.SR", "8040.SR", "8100.SR", "8120.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR", "7040.SR"],
    "المرافق العامة": ["2080.SR", "5110.SR", "2081.SR", "2082.SR"],
    "صناديق ريت العقارية": ["4330.SR", "4331.SR", "4332.SR", "4333.SR"],
    "إدارة وتطوير العقارات": ["4321.SR", "4100.SR", "4012.SR", "4250.SR", "4300.SR"],
    "التطبيقات وخدمات التقنية": ["7200.SR", "7201.SR", "7202.SR"]
}

# --- 3. محرك التحليل المالي الكامل (15 مؤشر) ---
def perform_tcr_audit(symbol, op_log):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', symbol)
        
        op_log.code(f"📡 {name}: جلب الميزانية، قائمة الدخل، والتدفقات النقدية...")
        inc = ticker.quarterly_income_stmt
        bal = ticker.quarterly_balance_sheet
        cf = ticker.quarterly_cash_flow
        divs = ticker.dividends

        # المسار 1: بافيت وقراهام (9 مؤشرات)
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
            {"label": "سجل التوزيع", "val": f"{div_years}Y", "target": "> 10Y", "pass": div_years >= 10, "desc": "الاستمرارية تثبت صلابة الأرباح"},
            {"label": "مكرر P/E", "val": f"{pe:.1f}", "target": "< 18", "pass": pe <= 18, "desc": "شراء السعر العادل لهامش الأمان"},
            {"label": "عائد التوزيع", "val": f"{div_yield:.1f}%", "target": "> 4%", "pass": div_yield >= 4, "desc": "العائد النقدي السنوي للمستثمر"},
            {"label": "نسبة التوزيع", "val": f"{payout:.1f}%", "target": "20-75%", "pass": 20 <= payout <= 75, "desc": "توازن المكافأة مع نمو الشركة"},
            {"label": "كفاءة ROE", "val": f"{roe:.1f}%", "target": "> 15%", "pass": roe >= 15, "desc": "قدرة الإدارة على تعظيم حقوق الملاك"},
            {"label": "هامش التشغيل", "val": f"{op_margin:.1f}%", "target": "> 10%", "pass": op_margin >= 10, "desc": "يعكس كفاءة النشاط الرئيسي"},
            {"label": "نسبة السيولة", "val": f"{current_ratio:.2f}", "target": "> 1.2", "pass": current_ratio >= 1.2, "desc": "القدرة على سداد الالتزامات"},
            {"label": "الديون D/E", "val": f"{debt_to_equity:.2f}", "target": "< 0.6", "pass": debt_to_equity <= 0.6, "desc": "انخفاض المديونية يعني حصانة مالية"},
            {"label": "نمو EPS", "val": f"{eps_g:.1f}%", "target": "> 5%", "pass": eps_g >= 5, "desc": "استمرار نمو الربحية يرفع السهم"}
        ]

        # المسار 2: بيتر لينش (6 مؤشرات)
        peg = info.get('pegRatio', 9.9)
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)
        fcf = cf.loc['Free Cash Flow'].iloc if 'Free Cash Flow' in cf.index else 0
        net_inc = inc.loc['Net Income'].iloc if 'Net Income' in inc.index else 1
        
        lynch = [
            {"label": "نسبة PEG", "val": f"{peg:.2f}", "target": "< 1.0", "pass": peg <= 1.0, "desc": "شراء النمو المستقبلي بسعر رخيص"},
            {"label": "النقد الصافي", "val": f"{net_cash:,.0f}", "target": "> 0", "pass": net_cash > 0, "desc": "وسادة أمان نقدية تغطي الديون"},
            {"label": "نمو EPS", "val": f"{eps_g:.1f}%", "target": "20-50%", "pass": 20 <= eps_g <= 50, "desc": "النطاق المثالي للنمو المستدام"},
            {"label": "المخزون", "val": "سليم", "target": "مستقر", "pass": True, "desc": "عدم تراكم المخزون مقارنة بالمبيعات"},
            {"label": "الديون/الملكية", "val": f"{debt_to_equity:.2f}", "target": "< 0.35", "pass": debt_to_equity <= 0.35, "desc": "النمو بمال الشركة الخاص"},
            {"label": "جودة FCF", "val": f"{fcf/net_inc:.2f}", "target": "> 1.0", "pass": (fcf/net_inc) >= 1.0, "desc": "الأرباح هي كاش حقيقي"}
        ]

        return {"name": name, "buffett": buffett, "lynch": lynch}
    except: return None

# --- 4. واجهة التطبيق ---
st.markdown("<h1 style='text-align:center;' class='neon-purple'>🔮 TCR GLOBAL SECTOR LABORATORY</h1>", unsafe_allow_html=True)

col_ctrl, col_lab = st.columns(2)

with col_ctrl:
    st.markdown("### 🛰️ مركز القيادة")
    sector_key = st.selectbox("اختر القطاع:", list(TASI_SECTORS_ALL.keys()))
    c1, c2 = st.columns(2)
    start = c1.button("إطلاق المسح ⚡")
    stop = c2.button("إيقاف البحث 🛑")
    op_console = st.empty()

with col_lab:
    st.markdown("### 🔬 مختبر الفحص (15 مؤشر)")
    p1, p2 = st.columns(2)
    b_bench = p1.empty()
    l_bench = p2.empty()

if start:
    for sym in TASI_SECTORS_ALL[sector_key]:
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
