import streamlit as st
import pandas as pd
import joblib

# 모델 로드
model = joblib.load("model.pkl")

# 예측을 위한 카테고리와 사이즈 목록
category_list = [
    'Saree', 'Set', 'Western Dress', 'Top', 'Kurta', 'Blouse', 'Dupatta', 'Gown'
]

size_list = [
    'Free', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', '4XL', '5XL', '6XL'
]

# Streamlit 앱 UI 설정
st.title("🛍️ 적정 단가 예측기 (Category & Size 기반)")
st.write("카테고리와 사이즈를 선택하면 예측된 적정 단가를 보여줍니다.")

# 사용자 입력
category = st.selectbox("카테고리를 선택하세요:", category_list)
size = st.selectbox("사이즈를 선택하세요:", size_list)

# 예측을 위한 입력값 준비
input_dict = {
    f"Category_{category}": 1,
    f"Size_{size}": 1
}

# 모델 입력용 전체 더미 변수 구성
all_categories = [f"Category_{c}" for c in category_list if c != category]
all_sizes = [f"Size_{s}" for s in size_list if s != size]

for col in all_categories + all_sizes:
    input_dict[col] = 0

input_df = pd.DataFrame([input_dict])

# 예측 실행
if st.button("적정 가격 예측하기"):
    prediction = model.predict(input_df)[0]
    st.success(f"예측된 적정 단가: ₹ {prediction:.2f}")
