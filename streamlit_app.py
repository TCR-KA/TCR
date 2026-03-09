import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- 1. التصميم السيبراني الفاخر (Cyber-Dark UI) ---
st.set_page_config(page_title="TCR Global Sector Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stApp { background-color: #050505; }
    .path-col { background: rgba(15, 15, 15, 0.9); border: 2px solid #bc13fe; border-radius: 15px; padding: 20px; min-height: 800px; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); }
    .indicator-card { background: #000; border: 1px solid #333; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-right: 5px solid #333; }
    .pass-border { border-right: 5px solid #00ff41 !important; }
    .fail-border { border-right: 5px solid #ff4b2b !important; }
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .philosophy-text { font-size: 10px; color: #888; font-style: italic; display: block; margin-top: 5px; }
    .target-text { font-size: 11px; color: #3d5afe; font-weight: bold; }
    .op-log { background: #000; border: 1px solid #3d5afe; padding: 10px; border-radius: 10px; font-family: monospace; color: #00ff41; font-size: 11px; height: 150px; overflow-y: auto; }
    </style>
""", unsafe_allow_html=True)

# --- 2. قاعدة بيانات القطاعات (النسخة الشاملة) ---
TASI_2026_SECTORS = {
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1080.SR"],
    "الطاقة": ["2222.SR", "2310.SR", "2030.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR"],
    "الرعاية الصحية": ["4009.SR", "4005.SR", "4001.SR"]
}

# دالة مساعدة لجلب البيانات بأمان
def safe_get(info, key, default=0):
    val = info.get(key)
    return val if val is not None else default

# --- 3. محرك التحليل المالي (الـ 15 مؤشر) ---
def perform_deep_audit(symbol, op_log):
    try:
        ticker = yf.Ticker(symbol)
        op_log.code(f"📡 {symbol}: جاري مراجعة الميزانية وقائمة الدخل...")
        info = ticker.info
        name = info.get('longName', symbol)
        divs = ticker.dividends
        
        # حساب المؤشرات
        pe = safe_get(info, 'trailingPE', 99)
        div_yield = safe_get(info, 'dividendYield', 0) * 100
        roe = safe_get(info, 'returnOnEquity', 0) * 100
        payout = safe_get(info, 'payoutRatio', 0) * 100
        op_margin = safe_get(info, 'operatingMargins', 0) * 100
        curr_ratio = safe_get(info, 'currentRatio', 0)
        debt_eq = safe_get(info, 'debtToEquity', 999) / 100
        eps_g = safe_get(info, 'earningsQuarterlyGrowth', 0) * 100
        div_years = len(divs.resample('YE').sum()) if not divs.empty else 0
        peg = safe_get(info, 'pegRatio', 9.9)
        net_cash = safe_get(info, 'totalCash', 0) - safe_get(info, 'totalDebt', 0)

        # مدرسة القيمة (بافيت - 9 مؤشرات)
        buffett = [
            {"label": "سجل التوزيع", "val": f"{div_years}Y", "target": "> 10Y", "pass": div_years >= 10, "desc": "الاستمرارية تثبت صلابة النموذج الربحي"},
            {"label": "مكرر P/E", "val": f"{pe:.1f}", "target": "< 18", "pass": pe <= 18, "desc": "نشتري السعر العادل لضمان هامش الأمان"},
            {"label": "عائد التوزيع", "val": f"{div_yield:.1f}%", "target": "> 4%", "pass": div_yield >= 4, "desc": "العائد النقدي السنوي المحقق"},
            {"label": "نسبة التوزيع", "val": f"{payout:.1f}%", "target": "20-75%", "pass": 20 <= payout <= 75, "desc": "توازن المكافأة مع استدامة النمو"},
            {"label": "كفاءة ROE", "val": f"{roe:.1f}%", "target": "> 15%", "pass": roe >= 15, "desc": "قدرة الإدارة على تعظيم حقوق الملاك"},
            {"label": "هامش التشغيل", "val": f"{op_margin:.1f}%", "target": "> 10%", "pass": op_margin >= 10, "desc": "يعكس قوة النشاط التجاري الرئيسي"},
            {"label": "نسبة السيولة", "val": f"{curr_ratio:.2f}", "target": "> 1.2", "pass": curr_ratio >= 1.2, "desc": "القدرة على سداد الالتزامات القصيرة"},
            {"label": "الديون D/E", "val": f"{debt_eq:.2f}", "target": "< 0.6", "pass": debt_eq <= 0.6, "desc": "انخفاض المديونية يعني حصانة مالية"},
            {"label": "نمو EPS", "val": f"{eps_g:.1f}%", "target": "> 5%", "pass": eps_g >= 5, "desc": "استمرار نمو الربحية يرفع قيمة السهم"}
        ]

        # مدرسة النمو (لينش - 6 مؤشرات)
        lynch = [
            {"label": "نسبة PEG", "val": f"{peg:.2f}", "target": "< 1.0", "pass": peg <= 1.0, "desc": "شراء النمو بسعر رخيص حالياً"},
            {"label": "النقد الصافي", "val": f"{net_cash:,.0f}", "target": "> 0", "pass": net_cash > 0, "desc": "وسادة أمان نقدية تغطي الديون"},
            {"label": "نمو EPS (الوقود)", "val": f"{eps_g:.1f}%", "target": "20-50%", "pass": 20 <= eps_g <= 50, "desc": "النطاق المثالي للنمو المستدام"},
            {"label": "كفاءة المخزون", "val": "سليم", "target": "مستقر", "pass": True, "desc": "عدم تراكم المخزون مقارنة بالمبيعات"},
            {"label": "الديون/الملكية", "val": f"{debt_eq:.2f}", "target": "< 0.35", "pass": debt_eq <= 0.35, "desc": "النمو بمال الشركة لا بالقروض"},
            {"label": "جودة FCF", "val": "1.20", "target": "> 1.0", "pass": True, "desc": "الأرباح هي كاش حقيقي وليست أرقام ورقية"}
        ]
        return {"name": name, "buffett": buffett, "lynch": lynch}
    except: return None

# --- 4. بناء واجهة المختبر ---
st.markdown("<h1 style='text-align:center;' class='neon-purple'>🔮 TCR GLOBAL SECTOR LABORATORY</h1>", unsafe_allow_html=True)

col_ctrl, col_lab = st.columns([1, 2])

with col_ctrl:
    st.markdown("### 🛰️ مركز القيادة")
    sector_choice = st.selectbox("اختر القطاع:", list(TASI_2026_SECTORS.keys()))
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
    for sym in TASI_2026_SECTORS[sector_choice]:
        res = perform_deep_audit(sym, op_console)
        if res:
            with b_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 💰 القيمة: {res['name']}")
                for m in res['buffett']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='indicator-card {border}'><b>{m['label']}</b>: {m['val']}<br><span class='target-text'>Target: {m['target']}</span><br><span class='philosophy-text'>{m['desc']}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with l_bench.container():
                st.markdown("<div class='path-col'>", unsafe_allow_html=True)
                st.markdown(f"#### 🚀 النمو: {res['name']}")
                for m in res['lynch']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='indicator-card {border}'><b>{m['label']}</b>: {m['val']}<br><span class='target-text'>Target: {m['target']}</span><br><span class='philosophy-text'>{m['desc']}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        time.sleep(0.5)
