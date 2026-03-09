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
    .path-col { background: rgba(15, 15, 15, 0.9); border: 2px solid #bc13fe; border-radius: 15px; padding: 20px; min-height: 400px; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); margin-bottom:20px; }
    .indicator-card { background: #000; border: 1px solid #333; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-right: 5px solid #333; }
    .pass-border { border-right: 5px solid #00ff41 !important; }
    .fail-border { border-right: 5px solid #ff4b2b !important; }
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .opportunity-box { background: #0a0a0a; border: 2px dashed #00ff41; padding: 15px; border-radius: 15px; text-align: center; }
    .philosophy-text { font-size: 10px; color: #888; font-style: italic; display: block; margin-top: 5px; }
    .target-text { font-size: 11px; color: #3d5afe; font-weight: bold; }
    .op-log { background: #000; border: 1px solid #3d5afe; padding: 10px; border-radius: 10px; font-family: monospace; color: #00ff41; font-size: 11px; height: 100px; overflow-y: auto; }
    </style>
""", unsafe_allow_html=True)

# --- 2. قاعدة بيانات القطاعات الشاملة (TASI) ---
TASI_2026_SECTORS = {
    "الطاقة": ["2222.SR", "2223.SR", "2310.SR", "2030.SR"],
    "المواد الأساسية": ["2010.SR", "2020.SR", "2350.SR", "1211.SR", "2002.SR", "2380.SR", "1212.SR"],
    "السلع الرأسمالية": ["1301.SR", "1304.SR", "1320.SR", "2230.SR"],
    "النقل": ["4030.SR", "4040.SR", "4110.SR", "4260.SR"],
    "الرعاية الصحية": ["4009.SR", "4005.SR", "4001.SR", "4013.SR", "4011.SR"],
    "البنوك": ["1120.SR", "1150.SR", "1180.SR", "1010.SR", "1080.SR", "1020.SR", "1030.SR", "1060.SR"],
    "الاتصالات": ["7010.SR", "7020.SR", "7030.SR", "7040.SR"],
    "العقارات": ["4020.SR", "4150.SR", "4180.SR", "4190.SR", "4250.SR"],
    "التجزئة": ["4002.SR", "4004.SR", "4006.SR", "4008.SR"],
    "التقنية": ["7200.SR", "7201.SR", "7202.SR"],
    "تجزئة الأغذية": ["4160.SR", "4061.SR", "4290.SR"]
}

def safe_get(info, key, default=0):
    val = info.get(key)
    return val if val is not None else default

# --- 3. محرك التحليل المالي ---
def perform_deep_audit(symbol, op_log):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get('shortName', symbol)
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

        buffett = [
            {"label": "سجل التوزيع", "val": f"{div_years}Y", "target": "> 10Y", "pass": div_years >= 10, "desc": "الاستمرارية"},
            {"label": "مكرر P/E", "val": f"{pe:.1f}", "target": "< 18", "pass": pe <= 18, "desc": "السعر العادل"},
            {"label": "عائد التوزيع", "val": f"{div_yield:.1f}%", "target": "> 4%", "pass": div_yield >= 4, "desc": "الدخل النقدي"},
            {"label": "نسبة التوزيع", "val": f"{payout:.1f}%", "target": "20-75%", "pass": 20 <= payout <= 75, "desc": "الاستدامة"},
            {"label": "كفاءة ROE", "val": f"{roe:.1f}%", "target": "> 15%", "pass": roe >= 15, "desc": "قوة الإدارة"},
            {"label": "هامش التشغيل", "val": f"{op_margin:.1f}%", "target": "> 10%", "pass": op_margin >= 10, "desc": "قوة العمل"},
            {"label": "نسبة السيولة", "val": f"{curr_ratio:.2f}", "target": "> 1.2", "pass": curr_ratio >= 1.2, "desc": "الأمان"},
            {"label": "الديون D/E", "val": f"{debt_eq:.2f}", "target": "< 0.6", "pass": debt_eq <= 0.6, "desc": "التحرر المالي"},
            {"label": "نمو EPS", "val": f"{eps_g:.1f}%", "target": "> 5%", "pass": eps_g >= 5, "desc": "النمو الربحي"}
        ]

        lynch = [
            {"label": "نسبة PEG", "val": f"{peg:.2f}", "target": "< 1.0", "pass": peg <= 1.0, "desc": "نمو بسعر رخيص"},
            {"label": "النقد الصافي", "val": f"{net_cash:,.0f}", "target": "> 0", "pass": net_cash > 0, "desc": "السيولة الفائضة"},
            {"label": "نمو EPS", "val": f"{eps_g:.1f}%", "target": "20-50%", "pass": 20 <= eps_g <= 50, "desc": "النمو الصاروخي"},
            {"label": "الديون/الملكية", "val": f"{debt_eq:.2f}", "target": "< 0.35", "pass": debt_eq <= 0.35, "desc": "نمو بدون ديون"}
        ]
        
        return {"name": name, "symbol": symbol, "buffett": buffett, "lynch": lynch}
    except: return None

# --- 4. واجهة المستخدم ---
st.markdown("<h1 style='text-align:center;' class='neon-purple'>🔮 TCR GLOBAL SECTOR LAB v2.0</h1>", unsafe_allow_html=True)

col_ctrl, col_console = st.columns([1, 1])
with col_ctrl:
    sector_choice = st.selectbox("🎯 اختر القطاع المستهدف:", list(TASI_2026_SECTORS.keys()))
    scan_btn = st.button("إطلاق المسح السيبراني ⚡", use_container_width=True)

with col_console:
    log_area = st.empty()

# الحاويات الرئيسية
st.divider()
b_bench, l_bench = st.columns(2)
st.divider()
st.markdown("### 💎 رادار الفرص (Match 70%+)")
opp_value, opp_growth = st.columns(2)

if scan_btn:
    value_opportunities = []
    growth_opportunities = []

    for sym in TASI_2026_SECTORS[sector_choice]:
        log_area.markdown(f"<div class='op-log'>📡 جاري فحص: {sym}...</div>", unsafe_allow_html=True)
        res = perform_deep_audit(sym, log_area)
        
        if res:
            # عرض النتائج في المختبر
            with b_bench:
                st.markdown(f"<div class='path-col'><h4>💰 مدرسة القيمة: {res['name']}</h4>", unsafe_allow_html=True)
                for m in res['buffett']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='indicator-card {border}'><b>{m['label']}</b>: {m['val']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with l_bench:
                st.markdown(f"<div class='path-col'><h4>🚀 مدرسة النمو: {res['name']}</h4>", unsafe_allow_html=True)
                for m in res['lynch']:
                    border = "pass-border" if m['pass'] else "fail-border"
                    st.markdown(f"<div class='indicator-card {border}'><b>{m['label']}</b>: {m['val']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # فحص الفرص (نسبة النجاح)
            b_score = sum(1 for m in res['buffett'] if m['pass']) / len(res['buffett'])
            l_score = sum(1 for m in res['lynch'] if m['pass']) / len(res['lynch'])

            if b_score >= 0.7: value_opportunities.append(f"{res['name']} ({sym})")
            if l_score >= 0.7: growth_opportunities.append(f"{res['name']} ({sym})")
        
        time.sleep(0.1)

    # عرض الفرص في الخانات المنفصلة
    with opp_value:
        st.markdown("<div class='opportunity-box'>", unsafe_allow_html=True)
        st.success("🏢 فرص مدرسة القيمة")
        if value_opportunities:
            for op in value_opportunities: st.write(f"✅ {op}")
        else: st.write("لا توجد فرص مطابقة حالياً")
        st.markdown("</div>", unsafe_allow_html=True)

    with opp_growth:
        st.markdown("<div class='opportunity-box' style='border-color: #bc13fe;'>", unsafe_allow_html=True)
        st.info("🚀 فرص مدرسة النمو")
        if growth_opportunities:
            for op in growth_opportunities: st.write(f"🔥 {op}")
        else: st.write("لا توجد فرص مطابقة حالياً")
        st.markdown("</div>", unsafe_allow_html=True)

    log_area.success("✅ اكتمل المسح الشامل للقطاع!")
