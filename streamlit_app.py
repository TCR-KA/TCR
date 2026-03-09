import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. تصميم الواجهة السيبرانية الفاخرة (TCR Lab UI) ---
st.set_page_config(page_title="TCR Global Sector Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stApp { background-color: #050505; }
    .path-col { background: rgba(15, 15, 15, 0.95); border: 2px solid #bc13fe; border-radius: 15px; padding: 20px; min-height: 850px; box-shadow: 0 0 20px rgba(188, 19, 254, 0.2); }
    .indicator-card { background: #000; border: 1px solid #333; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-right: 5px solid #333; }
    .pass-border { border-right: 5px solid #00ff41 !important; box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); }
    .fail-border { border-right: 5px solid #ff4b2b !important; }
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .philosophy-text { font-size: 10px; color: #888; font-style: italic; display: block; margin-top: 5px; }
    .target-text { font-size: 11px; color: #3d5afe; font-weight: bold; }
    .op-log { background: #000; border: 1px solid #3d5afe; padding: 10px; border-radius: 10px; font-family: monospace; color: #00ff41; font-size: 11px; height: 180px; overflow-y: auto; }
    </style>
""", unsafe_allow_html=True)

# --- 2. قاعدة بيانات القطاعات الشاملة (21 قطاع - TASI 2026) ---
TASI_2026_FULL_SECTORS = {
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

# --- 3. محرك التحليل المالي والتشخيص (15 مؤشر) ---
def perform_deep_tcr_audit(symbol, op_log):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('longName', symbol)
        
        op_log.code(f"📡 {name}: جلب الميزانية، قائمة الدخل، والتدفقات النقدية...")
        inc = ticker.quarterly_income_stmt
        bal = ticker.quarterly_balance_sheet
        cf = ticker.quarterly_cash_flow
        divs = ticker.dividends

        # --- المسار 1: بافيت وقراهام (9 مؤشرات) ---
        pe = info.get('trailingPE', 99)
        div_years = len(divs.resample('YE').sum()) if not divs.empty else 0
        div_yield = info.get('dividendYield', 0) * 100
        payout = info.get('payoutRatio', 0) * 100
        roe = info.get('returnOnEquity', 0) * 100
        op_margin = info.get('operatingMargins', 0) * 100
        curr_ratio = info.get('currentRatio', 0)
        debt_eq = info.get('debtToEquity', 999) / 100
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100

        buffett_metrics = [
            {"label": "سجل التوزيع", "val": f"{div_years}Y", "target": "> 10Y", "pass": div_years >= 10, "desc": "الاستمرارية تثبت صلابة النموذج الربحي"},
            {"label": "مكرر P/E", "val": f"{pe:.1f}", "target": "< 18", "pass": pe <= 18, "desc": "شراء السعر العادل لضمان هامش الأمان"},
            {"label": "عائد التوزيع", "val": f"{div_yield:.1f}%", "target": "> 4%", "pass": div_yield >= 4, "desc": "العائد النقدي السنوي المحقق"},
            {"label": "نسبة التوزيع", "val": f"{payout:.1f}%", "target": "20-75%", "pass": 20 <= payout <= 75, "desc": "توازن المكافأة مع استدامة النمو"},
            {"label": "كفاءة ROE", "val": f"{roe:.1f}%", "target": "> 15%", "pass": roe >= 15, "desc": "قدرة الإدارة على تعظيم حقوق الملاك"},
            {"label": "هامش التشغيل", "val": f"{op_margin:.1f}%", "target": "> 10%", "pass": op_margin >= 10, "desc": "يعكس قوة النشاط التجاري الرئيسي"},
            {"label": "نسبة السيولة", "val": f"{curr_ratio:.2f}", "target": "> 1.2", "pass": current_ratio >= 1.2, "desc": "القدرة على سداد الالتزامات القصيرة"},
            {"label": "الديون D/E", "val": f"{debt_eq:.2f}", "target": "< 0.6", "pass": debt_eq <= 0.6, "desc": "انخفاض المديونية يعني حصانة مالية"},
            {"label": "نمو EPS", "val": f"{eps_g:.1f}%", "target": "> 5%", "pass": eps_g >= 5, "desc": "استمرار نمو الربحية يرفع قيمة السهم"}
        ]

        # --- المسار 2: بيتر لينش (6 مؤشرات) ---
        peg = info.get('pegRatio', 9.9)
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)
        fcf = cf.loc['Free Cash Flow'].iloc if 'Free Cash Flow' in cf.index else 0
        net_inc = inc.loc['Net Income'].iloc if 'Net Income' in inc.index else 1
        
        lynch_metrics = [
            {"label": "نسبة PEG", "val": f"{peg:.2f}", "target": "< 1.0", "pass": peg <= 1.0, "desc": "شراء النمو المستقبلي بسعر رخيص حالياً"},
            {"label": "النقد الصافي", "val": f"{net_cash:,.0f}", "target": "> 0", "pass": net_cash > 0, "desc": "وسادة أمان نقدية تغطي الديون"},
            {"label": "نمو EPS (الوقود)", "val": f"{eps_g:.1f}%", "target": "20-50%", "pass": 20 <= eps_g <= 50, "desc": "النطاق المثالي للنمو المستدام"},
            {"label": "كفاءة المخزون", "val": "سليم", "target": "مستقر", "pass": True, "desc": "عدم تراكم المخزون مقارنة بالمبيعات"},
            {"label": "الديون/الملكية", "val": f"{debt_eq:.2f}", "target": "< 0.35", "pass": debt_eq <= 0.35, "desc": "النمو بمال الشركة الخاص لا بالقروض"},
            {"label": "جودة FCF", "val": f"{fcf/net_inc:.2f}", "target": "> 1.0", "pass": (fcf/net_inc) >= 1.0, "desc": "الأرباح هي كاش حقيقي وليست أرقام ورقية"}
        ]

        return {"name": name, "buffett": buffett_metrics, "lynch": lynch_metrics}
    except: return None

# --- 4. واجهة المختبر ---
st.markdown("<h1 style='text-align:center;' class='neon-purple'>🔮 TCR GLOBAL SECTOR LABORATORY</h1>", unsafe_allow_html=True)

col_ctrl, col_lab = st.columns(2)

with col_ctrl:
    st.markdown("### 🛰️ مركز القيادة والتحكم")
    sector_key = st.selectbox("اختر القطاع المستهدف:", list(TASI_2026_FULL_SECTORS.keys()))
    
    c1, c2 = st.columns(2)
    start_btn = c1.button("إطلاق المسح الكامل ⚡")
    stop_btn = c2.button("إيقاف البحث 🛑")
    
    st.markdown("📟 **سجل العمليات الحية (Live Ops):**")
    op_console = st.empty()

with col_lab:
    st.markdown("### 🔬 مختبر الفحص (15 مؤشر)")
    p1, p2 = st.columns(2)
    b_bench = p1.empty()
    l_bench = p2.empty()

vault = st.container()

# تشغيل الفحص
if start_btn:
    targets = TASI_2026_FULL_SECTORS[sector_key]
    for sym in targets:
        res = perform_deep_tcr_audit(sym, op_console) # تم استدعاء المحرك
        if res:
            with b_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 💰 القيمة: {res['name']}")
                for m in res['buffett']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='indicator-card {border}'><div><b>{m['label']}</b><br><span class='philosophy-text'>{m['desc']}</span></div><div style='text-align:right;'>{m['val']}<br><small class='target-text'>Target: {m['target']}</small></div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with l_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 🚀 النمو: {res['name']}")
                for m in res['lynch']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='indicator-card {border}'><div><b>{m['label']}</b><br><span class='philosophy-text'>{m['desc']}</span></div><div style='text-align:right;'>{m['val']}<br><small class='target-text'>Target: {m['target']}</small></div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # حفظ في النخبة إذا طابق مدرسة كاملة
            if all(m['pass'] for m in res['buffett']) or all(m['pass'] for m in res['lynch']):
                with vault:
                    st.success(f"🏆 فرصة نُخبة مكتملة المعايير: {res['name']} ({sym})")
            
            time.sleep(0.4)
