import streamlit as st
import yfinance as yf
import pandas as pd
import time
import plotly.graph_objects as go

# --- 1. إعدادات الواجهة السيبرانية الفاخرة ---
st.set_page_config(page_title="TCR Financial Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #ffffff; }
    .card { background: rgba(255, 255, 255, 0.03); border: 1px solid #bc13fe; border-radius: 15px; padding: 20px; box-shadow: 0 0 15px rgba(188, 19, 254, 0.2); }
    .neon-text { color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-weight: bold; }
    .stButton>button { background: linear-gradient(45deg, #bc13fe, #3d5afe); color: white; border-radius: 10px; height: 3.5em; width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك الرسوم التفاعلية ---
def create_gauge(title, value, min_val, max_val, target, suffix=""):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        number = {'suffix': suffix, 'font': {'size': 20}},
        title = {'text': title, 'font': {'size': 14, 'color': "#bc13fe"}},
        gauge = {
            'axis': {'range': [min_val, max_val], 'tickcolor': "#3d5afe"},
            'bar': {'color': "#bc13fe"},
            'steps': [{'range': [min_val, target], 'color': 'rgba(0, 255, 136, 0.1)'}],
            'threshold': {'line': {'color': "white", 'width': 2}, 'thickness': 0.75, 'value': target}
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#ffffff"}, height=220, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# --- 3. محرك التحليل المالي العميق (Manual Calculation) ---
def deep_financial_analysis(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # سحب القوائم المالية الخام (أهم خطوة للدقة)
        financials = ticker.quarterly_financials
        balance = ticker.quarterly_balance_sheet
        cashflow = ticker.quarterly_cash_flow
        info = ticker.info

        if financials.empty or balance.empty: return None

        # أ. حساب نمو الأرباح التشغيلية يدوياً (YoY)
        current_op_inc = financials.loc['Operating Income'].iloc[0]
        prev_year_op_inc = financials.loc['Operating Income'].iloc[4] if len(financials.columns) > 4 else financials.loc['Operating Income'].iloc[-1]
        op_growth = (current_op_inc - prev_year_op_inc) / abs(prev_year_op_inc) if prev_year_op_inc != 0 else 0

        # ب. حساب الديون الحقيقية (Net Debt / Equity)
        total_assets = balance.loc['Total Assets'].iloc[0]
        total_liab = balance.loc['Total Liabilities Net Minority Interest'].iloc[0]
        equity = total_assets - total_liab
        debt_ratio = total_liab / equity if equity > 0 else 9.9

        # ج. حساب جودة التدفق النقدي
        ocf = cashflow.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cashflow.index else 0
        net_inc = financials.loc['Net Income'].iloc[0]
        cash_quality = ocf / net_inc if net_inc > 0 else 0

        # د. مكررات السعر (P/E & PEG المحسوب يدوياً)
        current_price = info.get('currentPrice', 1)
        annual_eps = financials.loc['Net Income'].iloc[0:4].sum() / info.get('sharesOutstanding', 1)
        actual_pe = current_price / annual_eps if annual_eps > 0 else 99
        actual_peg = actual_pe / (op_growth * 100) if op_growth > 0 else 9.9

        metrics = {
            "PEG": actual_peg,
            "Growth": op_growth * 100,
            "PE": actual_pe,
            "Debt": debt_ratio,
            "Cash_Quality": cash_quality,
            "Payout": info.get('payoutRatio', 0) * 100,
            "Net_Cash": (info.get('totalCash', 0) - info.get('totalDebt', 0)) / 1e6
        }
        return {"name": info.get('longName', symbol), "symbol": symbol, "metrics": metrics}
    except: return None

# --- 4. بناء لوحة التحكم ---
st.markdown("<h1 style='text-align:center;' class='neon-text'>🛡️ TCR PROFESSIONAL LAB</h1>", unsafe_allow_html=True)

scanner_view = st.empty()
col_left, col_right = st.columns([2, 1])

with col_right:
    st.markdown("### 🏆 نُخبة السوق (المطابق)")
    elite_list = st.container()

if st.button("LAUNCH DEEP ANALYSIS (إطلاق التحليل العميق)"):
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{c}.SR" for r in ranges for c in r]

    for idx, sym in enumerate(all_codes):
        with scanner_view.container():
            st.markdown(f"#### 🔍 فحص ميزانية: <span class='neon-text'>{sym}</span>", unsafe_allow_html=True)
            
            res = deep_financial_analysis(sym)
            if res:
                m = res['metrics']
                st.markdown(f"**الشركة:** {res['name']}")
                
                # عرض العدادات ببطء لملاحظتها
                c1, c2, c3 = st.columns(3)
                c1.plotly_chart(create_gauge("PEG (المحسوب)", m['PEG'], 0, 3, 1), use_container_width=True, key=f"p_{idx}")
                c2.plotly_chart(create_gauge("النمو التشغيلي", m['Growth'], -20, 60, 20, "%"), use_container_width=True, key=f"g_{idx}")
                c3.plotly_chart(create_gauge("مكرر P/E الحقيقي", m['PE'], 0, 40, 15), use_container_width=True, key=f"e_{idx}")
                
                # فلاتر بيتر لينش وبافيت الصارمة
                is_elite = (m['PEG'] < 1.2 and m['Growth'] >= 15 and m['Debt'] < 0.4 and m['PE'] <= 18)
                
                if is_elite:
                    with elite_list:
                        st.success(f"✅ {res['name']} ({sym})")
                
                # فاصل زمني (0.8 ثانية) لتمكينك من قراءة النتائج بوضوح
                time.sleep(0.8)
            else:
                st.write("بيانات غير مكتملة.. تخطي")
