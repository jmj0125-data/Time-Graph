# =========================================
# 그래프 2
# =========================================
st.divider()

st.header("그래프 2. 일관객 합계가 가장 큰 영화 5편")

# 영화별 일관객 합계 계산
movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

# 일관객 합계 상위 5편
top5_movies = movie_total.head(5).index.tolist()

# 상위 5편의 데이터만 추출
top5_df = df[df["영화명"].isin(top5_movies)].copy()

# 날짜순으로 정렬
top5_df = top5_df.sort_values(["날짜", "영화명"])


# -----------------------------------------
# 선 그래프
# -----------------------------------------
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "영화명": True,
        "일관객": ":,"
    }
)

fig2.update_traces(
    hovertemplate=
    "영화: %{fullData.name}<br>"
    "날짜: %{x|%Y-%m-%d}<br>"
    "일관객: %{y:,}명"
    "<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    hovermode="x unified",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    width="stretch"
)


# -----------------------------------------
# 그래프 설명 작성 공간
# -----------------------------------------
st.markdown("### 이 그래프로 알 수 있는 것")

st.info(
    "✏️ 여기에 이 그래프로 알 수 있는 내용을 직접 작성하세요."
)


# =========================================
# 그래프 3을 추가할 때 사용할 구역
# =========================================
st.divider()

st.header("그래프 3")
st.write("다음 그래프를 이곳에 추가하세요.")

st.markdown("### 이 그래프로 알 수 있는 것")

st.info(
    "✏️ 여기에 이 그래프로 알 수 있는 내용을 직접 작성하세요."
)
