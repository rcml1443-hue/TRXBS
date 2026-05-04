import streamlit as st
import pandas as pd

st.set_page_config(page_title="TRX Predictor", layout="centered")
st.title("📈 TRX Big/Small Analysis")

@st.cache_data
def load_data():
    try:
        # သင်တင်မယ့် CSV ဖိုင်အမည်နဲ့ တူရပါမယ်
        df = pd.read_csv('Feb+9+2026.xlsx - Sheet1.csv')
        return df['bs'].astype(str).tolist()
    except:
        return []

data_list = load_data()

if not data_list:
    st.error("Data file မတွေ့ပါ။ CSV ဖိုင်ကို အရင်တင်ပေးပါ။")
else:
    st.subheader("နောက်ဆုံးထွက် ၅ ခု ရိုက်ထည့်ပါ")
    cols = st.columns(5)
    inputs = [cols[i].selectbox(f"#{i+1}", ["B", "S"], key=f"in_{i}") for i in range(5)]

    if st.button("Predict Next Result", use_container_width=True):
        matches_b, matches_s = 0, 0
        for i in range(len(data_list) - 5):
            if data_list[i : i+5] == inputs:
                next_val = data_list[i+5]
                if next_val == 'B': matches_b += 1
                elif next_val == 'S': matches_s += 1
        
        total = matches_b + matches_s
        if total > 0:
            b_per, s_per = (matches_b/total)*100, (matches_s/total)*100
            st.success(f"တွေ့ရှိမှုအရေအတွက်: {total} ကြိမ်")
            c1, c2 = st.columns(2)
            c1.metric("Big (B)", f"{round(b_per, 1)}%")
            c2.metric("Small (S)", f"{round(s_per, 1)}%")
            st.progress(int(b_per))
        else:
            st.warning("ဒီ Pattern မျိုး ယခင် Data ထဲမှာ မရှိသေးပါ။")
