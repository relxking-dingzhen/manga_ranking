import pandas as pd
import streamlit as st
import plotly.express as px

merged_df = pd.read_csv('merged.csv')

st.title('漫画の人気ランキング')

like_limit = st.slider('likeの上限', 0, 16200, 200, 1)
comment_limit = st.slider('コメントの下限', 0, 1000, 50, 1)

filtered_df = merged_df[
    (merged_df['Like'] <= like_limit) &
    (merged_df['コメント'] >= comment_limit)
]

fig = px.scatter(
    filtered_df,
    x = 'Like',
    y = 'コメント',
    hover_data = ['タイトル', 'タイトルURL', 'コメント', 'Like', 'score'],
    title = '人気漫画の散布図'
)
st.plotly_chart(fig)


df_sorted = filtered_df.sort_values("score", ascending=False).head(10)

fig = px.bar(
    df_sorted,
    x="タイトル",
    y="score",
    orientation="v",
    title = '綜合人気（上位10件）'
)

fig.update_xaxes(
    categoryorder="total descending",
    title_text="",
    showticklabels=False
)
st.plotly_chart(fig)

selected_salon = st.selectbox('気になる漫画を選んで詳細を確認', filtered_df['タイトル'])

if selected_salon:
    url = filtered_df[filtered_df['タイトル'] == selected_salon]['タイトルURL'].values[0]
    st.markdown(f"[{selected_salon}のページへ移動]({url})", unsafe_allow_html=True)

sort_key = st.selectbox(
    "ランキング基準を選んでください",
    ("Like", "score", "コメント")
)

ascending = True if sort_key == "price" else False

st.subheader(f"{sort_key}によるサロンランキング（上位10件）")
ranking_df = filtered_df.sort_values(by=sort_key, ascending=ascending).head(10)

st.dataframe(ranking_df[["タイトル", "作品紹介", "タイトルURL", "score", "Like", "コメント", "作者"]])