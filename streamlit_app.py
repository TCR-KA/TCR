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
    .path-col { background: rgba(15, 15, 15, 0.9); border: 2px solid #bc13fe; border-radius: 15px; padding: 20px; min-height: 450px; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); }
    .op-console { background: #000; border: 1px solid #3d5afe; padding: 15px; border-radius: 10px; font-family: 'Courier New', monospace; color: #00ff41; height: 250px; overflow-y: auto; font-size: 12px; }
    .elite-card { background: #111; border: 2px solid #00ff41; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 0 20px rgba(0, 255, 65, 0.2); }
    .metric-item { background: #000; border: 1px solid #333; padding: 8px; border-radius: 5px; margin-bottom: 5px; font-size: 12px; }
    .pass { color: #00ff41; font-weight: bold; }
    .fail { color: #ff4b2b; font-weight: bold; }
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. تعريف جميع قطاعات السوق السعودي (21 قطاع) ---
ALL_TASI_SECTORS = {
    "الطاقة": ["2222.SR", "2310.SR", "2030.SR", "5110.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "3001.SR", "3010.SR", "3020.SR", "3030.SR", "3040.SR", "3050.SR"],
    "السلع الرأسمالية": ["2320.SR", "1301.SR", "1303.SR", "1214.SR", "2300.SR", "3003.SR"],
    "الخدمات التجارية والمهنية": ["4071.SR", "4072.SR", "1831.SR", "1832.SR"],
    "النقل": ["4260.SR", "4040.SR", "4110.SR", "4261.SR"],
    "السلع طويلة الاجل": ["4030.SR", "4141.SR", "4142.SR"],
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
    "الصناديق العقارية المتداولة (REITs)": ["4330.SR", "4331.SR", "4332.SR", "4333.SR"],
    "إدارة وتطوير العقارات": ["4321.SR", "4100.SR", "4012.SR", "4250.SR", "4300.SR"],
    "التطبيقات وخدمات التقنية": ["7200.SR", "7201.SR", "7202.SR"]
}

# --- 3. محرك التحليل المالي والعمليات ---
def perform_tcr_vanguard_audit(symbol, op_log):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', symbol)
        
        # سجل العمليات (Command Center)
        op_log.code(f"📡 {name}: استدعاء القوائم المالية الربعية...")
        inc = ticker.quarterly_income_stmt
        bal = ticker.quarterly_balance_sheet
        cf = ticker.quarterly_cash_flow
        
        op_log.code(f"⚙️ {name}: حساب نسب المديونية وملاءة رأس المال...")
        debt_eq = info.get('debtToEquity', 999) / 100
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)

        # أ. مدرسة القيمة (بافيت وقراهام)
        op_log.code(f"⚖️ {name}: تقييم مكرر الربحية P/E وسياسة التوزيعات...")
        pe = info.get('trailingPE', 99)
        div_yield = info.get('dividendYield', 0) * 100
        roe = info.get('returnOnEquity', 0) * 100
        payout = info.get('payoutRatio', 0) * 100
        
        b_metrics = [
            {"label": "مكرر P/E", "val": f"{pe:.1f}", "pass": pe < 18},
            {"label": "عائد التوزيع", "val": f"{div_yield:.1f}%", "pass": div_yield > 4},
            {"label": "ROE (العائد على الملكية)", "val": f"{roe:.1f}%", "pass": roe > 15},
            {"label": "نسبة التوزيع Payout", "val": f"{payout:.1f}%", "pass": 20 <= payout <= 75}
        ]

        # ب. مدرسة النمو (بيتر لينش)
        op_log.code(f"🚀 {name}: فحص مؤشر PEG وجودة التدفق النقدي الحر...")
        peg = info.get('pegRatio', 9.9)
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100
        # جودة FCF
        fcf = cf.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cf.index else 0
        net_inc = inc.loc['Net Income'].iloc[0] if 'Net Income' in inc.index else 1
        fcf_q = fcf / net_inc if net_inc > 0 else 0

        l_metrics = [
            {"label": "نسبة PEG", "val": f"{peg:.2f}", "pass": peg < 1.0},
            {"label": "نمو EPS (ربعي)", "val": f"{eps_g:.1f}%", "pass": 20 <= eps_g <= 50},
            {"label": "الديون/الملكية", "val": f"{debt_eq:.2f}", "pass": debt_eq < 0.35},
            {"label": "النقد الصافي", "val": f"{net_cash:,.0f}", "pass": net_cash > 0}
        ]

        return {
            "name": name, "symbol": symbol, "b_audit": b_metrics, "l_audit": l_metrics,
            "is_b": all(m['pass'] for m in b_metrics), "is_l": all(m['pass'] for m in l_metrics)
        }
    except: return None

# --- 4. واجهة المختبر والتحكم ---
st.markdown("<h1 class='neon-purple' style='text-align:center;'>🔮 TCR GLOBAL SECTOR LABORATORY</h1>", unsafe_allow_html=True)

if 'run' not in st.session_state: st.session_state.run = False

col_ctrl, col_lab = st.columns([1, 2])

with col_ctrl:
    st.markdown("### 🛰️ مركز القيادة والتحكم")
    sector_key = st.selectbox("اختر القطاع المستهدف:", list(ALL_TASI_SECTORS.keys()))
    
    c1, c2 = st.columns(2)
    if c1.button("إطلاق الرادار ⚡"): st.session_state.run = True
    if c2.button("تجميد البحث 🛑"): st.session_state.run = False
    
    st.markdown("📟 **مركز العمليات الحية (Live Ops):**")
    op_console = st.empty()

with col_lab:
    st.markdown("### 🔬 المختبر التحليلي المنقسم")
    path_a, path_b = st.columns(2)
    b_bench = path_a.empty()
    l_bench = path_b.empty()

vault = st.container()

if st.session_state.run:
    targets = ALL_TASI_SECTORS[sector_key]
    for sym in targets:
        if not st.session_state.run: break
        
        res = perform_tcr_vanguard_audit(sym, op_console)
        if res:
            with b_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 💰 مدرسة القيمة: {res['name']}")
                for m in res['b_audit']:
                    st.markdown(f"<div class='metric-item'>{m['label']}: {m['val']} | <span class='{'pass' if m['pass'] else 'fail'}'>{'✅' if m['pass'] else '❌'}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with l_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 🚀 مدرسة النمو: {res['name']}")
                for m in res['l_audit']:
                    st.markdown(f"<div class='metric-item'>{m['label']}: {m['val']} | <span class='{'pass' if m['pass'] else 'fail'}'>{'✅' if m['pass'] else '❌'}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            if res['is_b'] or res['is_l']:
                with vault:
                    st.markdown(f"<div class='elite-card'>🏆 <b>فرصة نُخبة:</b> {res['name']} ({res['symbol']}) - النوع: {'نمو' if res['is_l'] else 'عوائد'}</div>", unsafe_allow_html=True)
            
            time.sleep(0.5)
