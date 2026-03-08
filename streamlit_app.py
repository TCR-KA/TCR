import streamlit as st
import yfinance as yf
import pandas as pd
import time

# إعدادات الصفحة
st.set_page_config(page_title="TCR - Tadawul Crawler & Ranker", layout="wide")

# العنوان والوصف
st.title("🚀 نظام TCR لفلترة السوق السعودي")
st.markdown("---")

# القائمة الجانبية للمعايير (يمكنك تعديلها يدوياً)
st.sidebar.header("⚙️ معايير الفحص (لينش/بافيت)")
target_peg = st.sidebar.number_input("الحد الأقصى لـ PEG", value=1.0)
target_pe = st.sidebar.number_input("الحد الأقصى لـ P/E", value=15.0)
min_growth = st.sidebar.slider("أدنى نمو للأرباح %", 0, 100, 20)

def analyze_stock(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if 'currentPrice' not in info: return None
        
        # استخراج البيانات المالية
        peg = info.get('pegRatio', 999)
        eps_g = info.get('earningsQuarterlyGrowth', 0) * 100
        debt_equity = info.get('debtToEquity', 999) / 100
        pe = info.get('trailingPE', 999)
        payout = info.get('payoutRatio', 0) * 100
        net_cash = info.get('totalCash', 0) - info.get('totalDebt', 0)

        # فحص النمو (Lynch) والعوائد (Buffett)
        is_growth = (peg <= target_peg and min_growth <= eps_g <= 50 and debt_equity < 0.35)
        is_value = (pe <= target_pe and 20 <= payout <= 60 and debt_equity <= 0.50)

        if is_growth or is_value:
            return {
                "الرمز": symbol,
                "الاسم": info.get('longName', 'N/A'),
                "السعر": info.get('currentPrice'),
                "النوع": "🚀 نمو" if is_growth else "💰 عوائد",
                "P/E": pe,
                "PEG": peg,
                "الديون": f"{debt_equity:.2f}",
                "النقد الصافي": f"{net_cash:,.0f} SAR"
            }
    except:
        return None

# زر البدء
if st.button("بدأ فحص السوق السعودي 🔍"):
    with st.spinner("جاري فحص جميع الشركات... قد يستغرق ذلك دقائق"):
        found = []
        # نطاقات السوق السعودي
        ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
        
        placeholder = st.empty()
        for r in ranges:
            for code in r:
                symbol = f"{code}.SR"
                placeholder.text(f"يتم فحص الآن: {symbol}")
                res = analyze_stock(symbol)
                if res:
                    found.append(res)
                time.sleep(0.1)

        if found:
            st.success(f"✅ تم العثور على {len(found)} فرص!")
            df = pd.DataFrame(found)
            st.table(df)
        else:
            st.warning("لم يتم العثور على فرص تطابق المعايير اليوم.")

