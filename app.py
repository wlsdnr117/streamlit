import streamlit as st
import pandas as pd
import joblib

# 모델 로드
model = joblib.load("model.pkl")

# 예측에 필요한 전체 피처 목록
expected_cols = model.feature_names_in_

# 예측을 위한 카테고리와 사이즈 목록
category_list = [
    'Saree', 'Set', 'Western Dress', 'Top', 'Kurta', 'Blouse', 'Dupatta', 'Gown'
]

size_list = [
    'Free', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', '4XL', '5XL', '6XL'
]

# 카테고리 & 사이즈별 평균 가격 정보 로드 (사전 저장된 CSV 필요)
try:
    stats_df = pd.read_csv("price_stats.csv")  # columns: Category, Size, Min, Max, Mean
except:
    stats_df = pd.DataFrame()

# Streamlit 앱 UI 설정
st.title("🛍️ Amazon 의상 적정 단가 예측기")
st.write("카테고리와 사이즈를 선택하면 예측된 적정 단가와 해당 조합의 가격 통계를 확인할 수 있습니다.")

# 사용자 입력
category = st.selectbox("카테고리를 선택하세요:", category_list)
size = st.selectbox("사이즈를 선택하세요:", size_list)

# 예측을 위한 입력값 준비
input_dict = {
    f"Category_{category}": 1,
    f"Size_{size}": 1
}

# 누락된 피처는 0으로 채우고 순서 맞춤
for col in expected_cols:
    if col not in input_dict:
        input_dict[col] = 0

input_df = pd.DataFrame([input_dict])[expected_cols]

# 예측 실행
if st.button("적정 가격 예측하기"):
    prediction = model.predict(input_df)[0]
    st.subheader(f"✅ 예측된 적정 단가: ₹ {prediction:.2f}")

    # 통계 정보 표시
    if not stats_df.empty:
        stats_row = stats_df[(stats_df['Category'] == category) & (stats_df['Size'] == size)]
        if not stats_row.empty:
            min_price = stats_row['Min'].values[0]
            max_price = stats_row['Max'].values[0]
            mean_price = stats_row['Mean'].values[0]

            st.markdown(f"\n**📊 참고 가격 정보:**")
            st.markdown(f"- 최소 가격: ₹ {min_price:.2f}")
            st.markdown(f"- 최대 가격: ₹ {max_price:.2f}")
            st.markdown(f"- 평균 가격: ₹ {mean_price:.2f}")
        else:
            st.info("해당 조합에 대한 통계 데이터가 없습니다.")
    else:
        st.warning("가격 통계 데이터를 불러올 수 없습니다. 'price_stats.csv' 파일이 필요합니다.")
