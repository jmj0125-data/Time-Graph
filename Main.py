import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")


# =========================================================
# 데이터 불러오기
# =========================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

df = pd.read_csv(DATA_URL)

# 날짜를 진짜 날짜 형식으로 변환
df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str),
    format="%Y%m%d"
)

# 숫자 열을 숫자형으로 변환
df["순위"] = pd.to_numeric(df["순위"], errors="coerce")
df["일관객"] = pd.to_numeric(df["일관객"], errors="coerce")
df["누적관객"] = pd.to_numeric(df["누적관객"], errors="coerce")
df["스크린수"] = pd.to_numeric(df["스크린수"], errors="coerce")
df["상영횟수"] = pd.to_numeric(df["상영횟수"], errors="coerce")


# =========================================================
# 그래프 1
# 영화별 날짜에 따른 일관객 변화
# =========================================================

st.header("그래프 1. 영화별 날짜에 따른 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")


fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
    }
)

fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    hovermode="x unified"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것:선택한 특정 영화의 관객의 변화를 알 수 있다.**")
st.empty()



# =========================================================
# 그래프 2
# 이 기간 일관객 합계 TOP 5 영화의 날짜별 일관객 변화
# =========================================================

st.divider()
st.header("그래프 2. 일관객 합계 TOP 5 영화의 날짜별 변화")

# 영화별 전체 기간 일관객 합계 계산
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

# TOP 5 영화만 선택
top5_df = df[df["영화명"].isin(top5_movies)].copy()

# 날짜와 영화명 순서대로 정렬
top5_df = top5_df.sort_values(["날짜", "영화명"])

# 여러 영화를 한 선 그래프로 표시
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계가 가장 큰 TOP 5 영화",
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

# 마우스를 올렸을 때 날짜와 관객 수 표시
fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}<br>"
        "날짜: %{x|%Y-%m-%d}<br>"
        "일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    hovermode="x unified",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것:영화와 날짜별 관객의 수 변화 추이를 알 수 있다.**")
st.empty()




# =========================================================
# 그래프 3
# 날짜별 10위권 일관객 합계
# =========================================================

st.divider()
st.header("그래프 3. 날짜별 10위권 일관객 합계")

# 날짜별 일관객 합계 계산
daily_audience = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 3일 찾기
top3_days = (
    daily_audience
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

# 영역 그래프
fig3 = px.area(
    daily_audience,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,"
    }
)

# 전체 날짜별 합계 툴팁
fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)

# 가장 큰 3일을 그래프 위에 표시
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=[
        date.strftime("%Y-%m-%d")
        for date in top3_days["날짜"]
    ],
    textposition="top center",
    marker=dict(
        size=10,
        color="red"
    ),
    name="합계 TOP 3",
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)",
    hovermode="x unified",
    showlegend=False
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것:날짜별 일일 관객의 합계를 볼 수 있다.**")
st.empty()




# ── 그래프 4. 기간 전체 관객 TOP 10 ─────────────────────────
st.header("4. 이 기간 관객이 가장 많았던 열 편")
total = (df.groupby("영화명", as_index=False)
           .agg(관객합계=("일관객", "sum"), 등장일수=("날짜", "count"))
           .nlargest(10, "관객합계"))
fig4 = px.bar(total.sort_values("관객합계"), x="관객합계", y="영화명",
              orientation="h", hover_data=["등장일수"])
st.plotly_chart(fig4, width="stretch")
st.caption("이 그래프로 알 수 있는 것: 특정 기간동안 관객이 가장 많았던 영화를 알 수 있다.")




# =========================================================
# 그래프 5
# 앞으로 추가할 그래프
# =========================================================

# ── 그래프 5. 월 × 요일 히트맵 ──────────────────────────────
st.header("5. 월과 요일로 접어 보기")
요일이름 = ["월", "화", "수", "목", "금", "토", "일"]
df["월"] = df["날짜"].dt.month
df["요일"] = df["날짜"].dt.weekday.map(lambda i: 요일이름[i])
pivot = (df.pivot_table(index="월", columns="요일", values="일관객", aggfunc="sum")
           .reindex(columns=요일이름))
fig5 = px.imshow(pivot, text_auto=".2s", aspect="auto",
                 labels=dict(x="요일", y="월", color="관객"))
st.plotly_chart(fig5, width="stretch")
st.caption("이 그래프로 알 수 있는 것: 월과 요일별로 관객이 가장 많았던 시기를 알 수 있다.")
