import streamlit as st
import yfinance as yf
import pandas as pd
import time

# 1. إعدادات الواجهة والاستقرار
st.set_page_config(page_title="TCR - Professional Analyzer", layout="wide")

# ميزة التخزين المؤقت: النتائج تبقى محفوظة لـ 24 ساعة لتوفير الجهد ومنع الحظر
@st.cache_data(ttl=86400)
def get_deep_analysis(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # سحب القوائم السنوية (لآخر 4 سنوات)
        financials = ticker.financials
        cashflow = ticker.cashflow
        
        if financials.empty or 'Operating Income' not in financials.index:
            return None

        # --- اختبار بيتر لينش وبافيت (الأرباح التشغيلية) ---
        # 1. نمو الربح التشغيلي (وليس صافي الربح) لضمان استبعاد الأرباح الاستثنائية
        op_inc = financials.loc['Operating Income']
        growth_rates = op_inc.pct_change(periods=-1).dropna()
        avg_op_growth = growth_rates.mean()

        # 2. جودة الأرباح (الربح التشغيلي vs صافي الربح)
        # يجب أن يكون أغلب الربح (أكثر من 85%) ناتجاً عن نشاط الشركة الأساسي
        net_inc = financials.loc['Net Income Common Stock Holders'].iloc[0]
        current_op_inc = op_inc.iloc[0]
        op_quality = current_op_inc / net_inc if net_inc > 0 else 0

        # 3. التدفق النقدي التشغيلي (هل الربح "كاش" حقيقي؟)
        ocf = cashflow.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cashflow.index else 0
        cash_ratio = ocf / current_op_inc if current_op_inc > 0 else 0

        # --- الفلترة الصارمة جداً ---
        if avg_op_growth >= 0.15 and op_quality > 0.85 and cash_ratio > 0.9:
            return {
                "الرمز": symbol,
                "الاسم": ticker.info.get('longName', 'N/A'),
                "نمو تشغيلي (3س)": f"{avg_op_growth*100:.1f}%",
                "جودة الأرباح (تشغيلية)": "✅ ممتازة" if op_quality > 0.9 else "⚠️ استثنائية",
                "تحويل الكاش": f"{cash_ratio*100:.0f}%",
                "P/E الحالي": round(ticker.info.get('trailingPE', 0), 2)
            }
        return None
    except:
        return None

# واجهة المستخدم
st.title("🛡️ نظام TCR: المحلل المالي العميق")
st.write("تحليل القوائم المالية التاريخية والتركيز على **الأرباح التشغيلية الحقيقية** فقط.")

if st.button("إطلاق الفحص التشغيلي الشامل 🔍"):
    found_stocks = []
    # نطاقات تاسي الأساسية
    ranges = [range(1000, 1331), range(2000, 2383), range(4000, 4349), range(7000, 7205)]
    all_codes = [f"{code}.SR" for r in ranges for code in r]
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, sym in enumerate(all_codes):
        status_text.text(f"جاري تحليل القوائم المالية لـ: {sym}")
        # استخدام الدالة المخزنة (Cache)
        res = get_deep_analysis(sym)
        if res:
            found_stocks.append(res)
        
        # تحديث شريط التقدم
        progress_bar.progress((i + 1) / len(all_codes))
        # فاصل زمني صغير لمنع الحظر (Rate Limiting)
        if i % 5 == 0: time.sleep(0.2)

    status_text.empty()
    if found_stocks:
        st.success(f"🎯 تم اكتشاف {len(found_stocks)} شركات بنمو تشغيلي حقيقي وصارم.")
        st.table(pd.DataFrame(found_stocks))
    else:
        st.warning("لم يتم العثور على شركات تطابق هذه المعايير الصارمة حالياً.")
