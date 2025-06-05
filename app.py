import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import emoji
from collections import Counter

# Use Seaborn whitegrid with dark background tweaks
sns.set_theme(style="whitegrid")

st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon="💬", layout="wide")

# Inject Google Fonts & custom CSS for modern dark theme and UI
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">

<style>
    /* Global font and background */
    body, .stApp {
        background-color: #121212 !important;
        color: #e0e0e0 !important;
        font-family: 'Montserrat', sans-serif;
    }

    /* Headings */
    h1, h2, h3 {
        color: #00bcd4 !important;
        font-weight: 700 !important;
        user-select: none;
        margin-bottom: 0.3rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1f1f1f !important;
        color: #b2dfdb !important;
        font-weight: 600;
        padding: 1.2rem;
    }

    /* Sidebar Title */
    .css-1d391kg h1, .css-1d391kg h2 {
        color: #00bcd4 !important;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #00bcd4 0%, #0097a7 100%);
        border: none;
        border-radius: 12px;
        padding: 10px 30px;
        color: #121212;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 10px rgba(0, 188, 212, 0.5);
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #0097a7 0%, #00bcd4 100%);
        color: white;
        cursor: pointer;
        box-shadow: 0 6px 15px rgba(0, 188, 212, 0.8);
        transform: scale(1.05);
    }

    /* Metrics cards */
    .metric-card {
        background-color: #212121;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.6);
        text-align: center;
        margin: 0.5rem;
        transition: background-color 0.3s ease;
    }
    .metric-card:hover {
        background-color: #00bcd4;
        color: #121212 !important;
        cursor: default;
        box-shadow: 0 8px 20px rgba(0,188,212,0.8);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        user-select: text;
    }
    .metric-label {
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.1px;
    }

    /* Section containers */
    .section-container {
        background-color: #212121;
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 6px 18px rgba(0,0,0,0.7);
    }

    /* Dataframe styling with hover */
    .dataframe tbody tr:hover {
        background-color: #004d40 !important;
        color: #a7ffeb !important;
    }

    /* Plot figure styling */
    .stPlotlyChart, .stPyplot {
        border-radius: 20px;
        box-shadow: 0 6px 15px rgba(0,188,212,0.3);
        padding: 1rem;
        background: #121212;
        margin-bottom: 2rem;
    }

    /* Scrollbar for dataframe */
    div[data-testid="stDataFrameContainer"] > div > div > div {
        scrollbar-width: thin;
        scrollbar-color: #00bcd4 #121212;
    }
    div[data-testid="stDataFrameContainer"] > div > div > div::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    div[data-testid="stDataFrameContainer"] > div > div > div::-webkit-scrollbar-track {
        background: #121212;
    }
    div[data-testid="stDataFrameContainer"] > div > div > div::-webkit-scrollbar-thumb {
        background-color: #00bcd4;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar title and upload
st.sidebar.title("💬 WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat (txt)", type=['txt'])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Analyze"):
        # Stats
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)

        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.title("📊 Top Statistics")

        cols = st.columns(4)
        metrics = [
            ("Messages", num_messages, "📩"),
            ("Words", num_words, "✍️"),
            ("Media Shared", num_media, "🖼️"),
            ("Links Shared", num_links, "🔗"),
        ]

        for idx, (label, value, icon) in enumerate(metrics):
            with cols[idx]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{value:,}</div>
                    <div class="metric-label">{icon} {label}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


        # Monthly Timeline
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.subheader("🗓 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 4), dpi=110)
        ax.plot(timeline['time'], timeline['message'], marker='o', color='#00bcd4', linewidth=2)
        ax.set_xlabel('Month-Year', fontsize=12, color='#e0e0e0')
        ax.set_ylabel('Messages', fontsize=12, color='#e0e0e0')
        ax.tick_params(colors='#b2dfdb')
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)


        # Daily Timeline
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.subheader("📅 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 4), dpi=110)
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], marker='.', color='#009688', linewidth=2)
        ax.set_xlabel('Date', fontsize=12, color='#e0e0e0')
        ax.set_ylabel('Messages', fontsize=12, color='#e0e0e0')
        ax.tick_params(colors='#b2dfdb')
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)


        # Activity Maps
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.subheader("🕒 Activity Map")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Most Busy Day**")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 3), dpi=110)
            ax.bar(busy_day.index, busy_day.values, color='#4db6ac', edgecolor='#004d40')
            ax.set_ylabel('Messages', color='#e0e0e0')
            ax.tick_params(colors='#b2dfdb')
            st.pyplot(fig)

        with col2:
            st.markdown("**Most Busy Month**")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 3), dpi=110)
            ax.bar(busy_month.index, busy_month.values, color='#80cbc4', edgecolor='#004d40')
            ax.set_ylabel('Messages', color='#e0e0e0')
            ax.tick_params(colors='#b2dfdb')
            st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)


        # Weekly Heatmap
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.subheader("📊 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 4), dpi=110)
        sns.heatmap(user_heatmap, cmap="coolwarm", ax=ax, cbar_kws={"shrink": .75}, linewidths=.5, linecolor='#263238')
        ax.tick_params(colors='#b2dfdb')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)


        # Busiest Users
        if selected_user == "Overall":
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.subheader("🔥 Most Busy Users")
            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns([3, 1])
            with col1:
                fig, ax = plt.subplots(figsize=(8, 4), dpi=110)
                ax.bar(x.index, x.values, color='#26a69a', edgecolor='#004d40')
                ax.set_ylabel('Messages', color='#e0e0e0')
                ax.tick_params(axis='x', rotation=45, colors='#b2dfdb')
                ax.tick_params(axis='y', colors='#b2dfdb')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df.style.background_gradient(cmap='coolwarm'))
            st.markdown('</div>', unsafe_allow_html=True)

        # Wordcloud
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.subheader("☁️ Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 4), dpi=110)
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)


        # Most Common Words
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.subheader("📈 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 4), dpi=110)
        ax.barh(most_common_df[0], most_common_df[1], color='#26a69a')
        ax.invert_yaxis()
        ax.tick_params(colors='#b2dfdb')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)


        # Emoji Analysis
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.subheader("😀 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        if not emoji_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df.style.format({1: "{:.2f}"}).background_gradient(cmap="PuRd"))
            with col2:
                fig, ax = plt.subplots(figsize=(5, 5), dpi=110)
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%", colors=sns.color_palette("PuRd"))
                st.pyplot(fig)
        else:
            st.info("No emojis found for this selection.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center; padding: 4rem;">
        <h2 style="color:#00bcd4; font-weight: 700; user-select:none; font-family: 'Montserrat', sans-serif;">
            Upload your WhatsApp chat file to get started.
        </h2>
        <p style="color:#b2dfdb; font-size: 1.3rem;">
            Export WhatsApp chat as a .txt file and upload here.
        </p>
    </div>
    """, unsafe_allow_html=True)
