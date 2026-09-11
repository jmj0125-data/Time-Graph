import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------------------
# 기본 설정
# -----------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)


# -----------------------------------------
# 제목
# -----------------------------------------
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "일별 박스오피스 데이터를 이용해 영화의 관객 변화를 살펴봅니다."
)


# -----------------------------------------
# 데이터 불러오기
# -----------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/"
    "greatsong/modudata/main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 열 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


df = load_data()


# =========================================
# 그래프 1
# =========================================
st.header("그래프 1. 영화별 날짜에 따른 일관객 변화")

# 영화 목록
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# 선택한 영화만 추출
movie_df = df[df["영화명"] == selected_movie].copy()

# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")


# -----------------------------------------
# 선 그래프
# -----------------------------------------
fig = px.line(
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
        "일관객": ":,"
    }
)

fig.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "일관객: %{y:,}명"
    "<extra></extra>"
)

fig.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
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
# 그래프 3
# =========================================
st.divider()

st.header("그래프 3. 날짜별 10위권 일관객 합계")

# 날짜별 10위권 일관객 합계 계산
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 날 3일 찾기
top3_days = daily_total.nlargest(3, "일관객").copy()

# 그래프에 표시할 날짜 라벨 만들기
top3_days["날짜_표시"] = top3_days["날짜"].dt.strftime("%Y-%m-%d")

# -----------------------------------------
# 영역 그래프
# -----------------------------------------
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)

# 마우스를 올렸을 때 날짜와 합계 표시
fig3.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "10위권 일관객 합계: %{y:,}명"
    "<extra></extra>"
)

# -----------------------------------------
# 합계가 가장 큰 3일 표시
# -----------------------------------------
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=top3_days["날짜_표시"],
    textposition="top center",
    marker=dict(size=10),
    name="일관객 합계 TOP 3",
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "10위권 일관객 합계: %{y:,}명"
    "<extra></extra>"
)

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)",
    hovermode="x unified"
)

st.plotly_chart(
    fig3,
    width="stretch"
)


# -----------------------------------------
# 그래프 설명 작성 공간
# -----------------------------------------
st.markdown("### 이 그래프로 알 수 있는 것")

st.info(
    "✏️ 여기에 이 그래프로 알 수 있는 내용을 직접 작성하세요."
)

