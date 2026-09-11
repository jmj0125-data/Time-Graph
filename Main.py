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

st.markdown("**이 그래프로 알 수 있는 것:**")
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

st.markdown("**이 그래프로 알 수 있는 것:**")
st.empty()



# =========================================================
# 그래프 3
# 앞으로 추가할 그래프
# =========================================================

st.divider()
st.header("그래프 3")

# 여기에 세 번째 그래프 코드를 작성하세요.

st.markdown("**이 그래프로 알 수 있는 것:**")
st.empty()


# =========================================================
# 그래프 4
# 앞으로 추가할 그래프
# =========================================================

st.divider()
st.header("그래프 4")

# 여기에 네 번째 그래프 코드를 작성하세요.

st.markdown("**이 그래프로 알 수 있는 것:**")
st.empty()


# =========================================================
# 그래프 5
# 앞으로 추가할 그래프
# =========================================================

st.divider()
st.header("그래프 5")

# 여기에 다섯 번째 그래프 코드를 작성하세요.

st.markdown("**이 그래프로 알 수 있는 것:**")
st.empty()


# =========================================================
# 그래프 6
# 앞으로 추가할 그래프
# =========================================================

st.divider()
st.header("그래프 6")

# 여기에 여섯 번째 그래프 코드를 작성하세요.

st.markdown("**이 그래프로 알 수 있는 것:**")
st.empty()
