import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.title("⚡ Generator Power Breach Monitor")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Threshold input
threshold = st.number_input("Set Threshold", value=1660000.0)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Preprocess
    df["time_sent"] = pd.to_datetime(df["time_sent"])
    df = df.sort_values("time_sent")
    df["sys_w_abs"] = df["sys_w"].abs()

    col = df["sys_w_abs"]

    # Stats
    st.subheader("📊 Statistics")
    st.write({
        "Mean": col.mean(),
        "Median": col.median(),
        "Min": col.min(),
        "Max": col.max(),
        "Std Dev": col.std()
    })

    # Breach detection
    df["breach"] = df["sys_w_abs"] > threshold
    outliers = df[df["breach"]]

    st.write("⚠️ Number of Breaches:", len(outliers))

    # Plot
    fig, ax = plt.subplots(figsize=(12,6))

    ax.plot(df["time_sent"], df["sys_w_abs"], label="|sys_w|")

    ax.axhline(threshold, linestyle="--", linewidth=2, label="Threshold")

    ax.fill_between(df["time_sent"],
                    threshold,
                    df["sys_w_abs"],
                    where=df["sys_w_abs"] > threshold,
                    alpha=0.3)

    ax.scatter(outliers["time_sent"],
               outliers["sys_w_abs"],
               s=30,
               label="Breaches")

    ax.set_title("Power vs Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("|sys_w|")

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    ax.legend()
    ax.grid()

    st.pyplot(fig)
st.dataframe(outliers[["time_sent", "sys_w_abs"]])
st.download_button("Download Breaches CSV",
                   outliers.to_csv(index=False),
                   "breaches.csv")
df["rolling"] = df["sys_w_abs"].rolling(50).mean()
ax.plot(df["time_sent"], df["rolling"], linewidth=2, label="Trend")
