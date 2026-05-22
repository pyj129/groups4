import streamlit as st
import pandas as pd
import random
from collections import defaultdict
from typing import List, Tuple, Dict

# 페이지 설정
st.set_page_config(page_title="소인수분해 탐구", layout="wide")

# ==================== 핵심 함수 모음 ====================

def prime_factorization(n: int) -> List[int]:
    """자연수를 소인수분해하여 소인수 리스트 반환"""
    if n < 2:
        return []
    
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def factors_to_dict(factors: List[int]) -> Dict[int, int]:
    """소인수 리스트를 {소인수: 지수} 딕셔너리로 변환"""
    result = defaultdict(int)
    for f in factors:
        result[f] += 1
    return dict(sorted(result.items()))


def format_prime_factorization(factors_dict: Dict[int, int]) -> str:
    """거듭제곱 형태로 포맷팅 (예: 2² × 3 × 5²)"""
    if not factors_dict:
        return "1"
    
    parts = []
    for prime, exponent in sorted(factors_dict.items()):
        if exponent == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{exponent}")
    return " × ".join(parts)


def get_all_divisors(factors_dict: Dict[int, int]) -> List[int]:
    """소인수분해 결과로부터 모든 약수를 생성"""
    if not factors_dict:
        return [1]
    
    primes = sorted(factors_dict.keys())
    divisors = [1]
    
    for prime in primes:
        exponent = factors_dict[prime]
        new_divisors = []
        for d in divisors:
            for e in range(1, exponent + 1):
                new_divisors.append(d * (prime ** e))
        divisors.extend(new_divisors)
    
    return sorted(set(divisors))


def create_divisor_table(factors_dict: Dict[int, int]) -> pd.DataFrame:
    """약수 표 생성 (가로축과 세로축에 소인수 배치)"""
    if not factors_dict:
        return pd.DataFrame({"약수": [1]})
    
    primes = sorted(factors_dict.keys())
    
    # 각 소인수별 가능한 지수 조합 생성
    rows = [1]
    for prime in primes:
        exponent = factors_dict[prime]
        new_rows = []
        for e in range(1, exponent + 1):
            for row in rows:
                new_rows.append(row * (prime ** e))
        rows.extend(new_rows)
    
    cols = [1]
    for i, prime in enumerate(primes[1:] if len(primes) > 1 else []):
        exponent = factors_dict[prime]
        new_cols = []
        for e in range(1, exponent + 1):
            for col in cols:
                new_cols.append(col * (prime ** e))
        cols.extend(new_cols)
    
    # 간단한 표 생성
    divisors = sorted(get_all_divisors(factors_dict))
    table_data = {"약수": divisors}
    return pd.DataFrame(table_data)


# ==================== UI 구성 ====================

st.title("🔢 소인수분해 탐구 학습실")
st.markdown("**중학교 1학년 수학 - 소인수분해 단원**")
st.divider()

# 입력 섹션
col1, col2 = st.columns([2, 1])
with col1:
    number = st.number_input(
        "탐구할 자연수를 입력하세요",
        min_value=2,
        max_value=10000,
        value=24,
        step=1
    )

with col2:
    st.info(f"📌 현재 선택: **{number}**")

if number < 2:
    st.error("2 이상의 자연수를 입력해주세요.")
    st.stop()

# 소인수분해 수행
factors = prime_factorization(number)
factors_dict = factors_to_dict(factors)

# ==================== 탭 구성 ====================
tab1, tab2, tab3 = st.tabs(["🔍 소인수분해 탐구", "📊 약수 구하기 표", "🎯 도전! 수학 퀴즈"])

# ==================== 탭 1: 소인수분해 시각화 ====================
with tab1:
    st.subheader(f"**{number}의 소인수분해**")
    
    # 방법 1: 나열법
    st.markdown("#### 📋 방법 1: 나열법")
    st.markdown("""
    자연수를 다른 자연수의 곱으로 계속 나누어 나가며 소수들만의 곱으로 표현합니다.
    """)
    
    # 나열법 시각화
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**단계별 과정:**")
        current = number
        step = 1
        for factor in factors:
            quotient = current // factor
            if quotient == 1:
                st.markdown(f"**Step {step}:** {current} = {factor} × 1")
            else:
                st.markdown(f"**Step {step}:** {current} = {factor} × {quotient}")
            current = quotient
            step += 1
    
    # 방법 2: 가지치기 (트리 구조)
    st.markdown("#### 🌳 방법 2: 소인수분해 가지치기")
    st.markdown("""
    자연수를 점진적으로 소인수로 분해하는 과정을 트리 구조로 나타냅니다.
    """)
    
    tree_text = f"""
    ```
                    {number}
                   /    \\
    """
    
    # 간단한 트리 구조 표현
    remaining = number
    level_factors = []
    for f in set(factors):
        if remaining % f == 0:
            tree_text += f"              {f}       {remaining // f}\n"
            remaining = remaining // f
            break
    
    tree_text += "    ```"
    st.markdown(tree_text)
    
    # 방법 3: L자형 나눗셈
    st.markdown("#### ➗ 방법 3: L자형 나눗셈")
    st.markdown("""
    가장 작은 소수부터 차례대로 아래로 나누어 내려갑니다.
    """)
    
    # L자형 나눗셈 표현
    division_text = "```\n"
    current = number
    sorted_factors = sorted(factors)
    
    division_text += f"  {' '*5} {current}\n"
    for i, f in enumerate(sorted_factors):
        current = current // f
        division_text += f"  {f} | {current if current > 1 else '1'}\n"
    
    division_text += "```"
    st.markdown(division_text)
    
    # 최종 결과
    st.divider()
    st.success(f"### ✅ 최종 결과")
    formatted = format_prime_factorization(factors_dict)
    st.latex(f"{number} = {formatted}")
    st.markdown(f"**또는:** {number} = {' × '.join(map(str, factors))}")

# ==================== 탭 2: 약수 구하기 ====================
with tab2:
    st.subheader(f"**{number}의 약수 구하기**")
    
    divisors = sorted(get_all_divisors(factors_dict))
    
    st.markdown("#### 📋 약수 표")
    st.markdown(f"""
    소인수분해 결과 {format_prime_factorization(factors_dict)} 에서
    약수는 각 소인수의 지수를 0 이상으로 조합하여 만들 수 있습니다.
    """)
    
    # 약수를 표로 표시
    col1, col2 = st.columns([2, 1])
    with col1:
        # 약수를 그리드로 표시
        divisor_df = pd.DataFrame({
            '약수': divisors,
            '검증': [f'{number} ÷ {d} = {number // d}' for d in divisors]
        })
        st.dataframe(divisor_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.info(f"""
        **약수의 개수**
        
        {format_prime_factorization(factors_dict)}
        
        약수의 개수 = ({' × '.join([f'({e}+1)' for e in factors_dict.values()])})
        
        = **{len(divisors)}개**
        """)
    
    # 생각해보기
    st.divider()
    st.markdown("#### 💭 생각해보기")
    st.markdown("""
    "수가 크다고 해서 항상 약수의 개수가 많을까?" 
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        # 예시 1: 24
        factors_24 = prime_factorization(24)
        factors_dict_24 = factors_to_dict(factors_24)
        divisors_24 = sorted(get_all_divisors(factors_dict_24))
        
        st.markdown(f"**24의 경우:**")
        st.markdown(f"- 소인수분해: {format_prime_factorization(factors_dict_24)}")
        st.markdown(f"- 약수의 개수: **{len(divisors_24)}개**")
        st.markdown(f"- 약수: {', '.join(map(str, divisors_24))}")
    
    with col2:
        # 예시 2: 25
        factors_25 = prime_factorization(25)
        factors_dict_25 = factors_to_dict(factors_25)
        divisors_25 = sorted(get_all_divisors(factors_dict_25))
        
        st.markdown(f"**25의 경우:**")
        st.markdown(f"- 소인수분해: {format_prime_factorization(factors_dict_25)}")
        st.markdown(f"- 약수의 개수: **{len(divisors_25)}개**")
        st.markdown(f"- 약수: {', '.join(map(str, divisors_25))}")
    
    st.warning("💡 **결론:** 25 > 24 이지만, 25의 약수는 3개, 24의 약수는 8개입니다. 따라서 수의 크기가 약수의 개수를 결정하지 않습니다!")

# ==================== 탭 3: 퀴즈 ====================
with tab3:
    st.subheader("🎯 도전! 수학 퀴즈")
    st.markdown("""
    다양한 문제 유형을 풀어 소인수분해를 완벽히 이해했는지 확인해보세요!
    """)
    
    # 퀴즈 타입 선택
    quiz_type = st.selectbox(
        "풀고 싶은 문제 유형을 선택하세요:",
        [
            "1️⃣ 소인수분해 하기",
            "2️⃣ 거듭제곱으로 올바르게 나타내기",
            "3️⃣ 약수의 개수 구하기"
        ]
    )
    
    st.divider()
    
    # 상태 초기화
    if 'quiz_answer' not in st.session_state:
        st.session_state.quiz_answer = None
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    
    if quiz_type == "1️⃣ 소인수분해 하기":
        # 문제 1: 소인수분해 하기
        random.seed(st.session_state.get('quiz_seed', 42))
        st.session_state.quiz_seed = random.randint(0, 1000)
        random.seed(st.session_state.quiz_seed)
        
        quiz_numbers = [12, 18, 20, 24, 30, 36, 40, 45, 50, 60]
        quiz_num = random.choice(quiz_numbers)
        quiz_factors = prime_factorization(quiz_num)
        quiz_answer_correct = ' × '.join(map(str, sorted(quiz_factors)))
        
        st.markdown(f"### 문제: **{quiz_num}을(를) 소인수분해하세요.**")
        st.markdown("*예: 12 = 2 × 2 × 3 (또는 2² × 3)*")
        
        user_answer = st.text_input("답을 입력하세요:")
        
        if st.button("정답 확인", key="quiz1_submit"):
            if user_answer.strip():
                # 정답 검증 (간단한 형식 체크)
                if '2' in user_answer and '3' in user_answer and quiz_num == 12:
                    st.success("✅ 정답입니다!")
                    st.balloons()
                elif '2' in user_answer and '5' in user_answer and quiz_num == 20:
                    st.success("✅ 정답입니다!")
                    st.balloons()
                else:
                    st.error(f"❌ 다시 풀어보세요.\n\n**정답:** {quiz_num} = {quiz_answer_correct}")
                    st.markdown("""
                    💡 **팁:** 가장 작은 소수부터 차례대로 나누어 보세요!
                    """)
            else:
                st.warning("답을 입력해주세요!")
    
    elif quiz_type == "2️⃣ 거듭제곱으로 올바르게 나타내기":
        # 문제 2: 거듭제곱 형태
        random.seed(st.session_state.get('quiz_seed2', 42))
        st.session_state.quiz_seed2 = random.randint(0, 1000)
        random.seed(st.session_state.quiz_seed2)
        
        quiz_numbers = [8, 12, 18, 24, 32, 36, 40, 48, 60, 72]
        quiz_num = random.choice(quiz_numbers)
        quiz_factors = prime_factorization(quiz_num)
        quiz_factors_dict = factors_to_dict(quiz_factors)
        quiz_answer_correct = format_prime_factorization(quiz_factors_dict)
        
        st.markdown(f"### 문제: **{quiz_num} = ?**")
        st.markdown("*거듭제곱을 사용하여 표현하세요. (예: 2² × 3)*")
        
        user_answer = st.text_input("답을 입력하세요:")
        
        if st.button("정답 확인", key="quiz2_submit"):
            if user_answer.strip():
                if '×' in user_answer or '^' in user_answer or '²' in user_answer or '³' in user_answer:
                    st.success("✅ 거듭제곱 형태로 잘 표현했습니다!")
                    st.info(f"**정답:** {quiz_num} = {quiz_answer_correct}")
                    st.balloons()
                else:
                    st.error(f"❌ 거듭제곱 형태로 표현해주세요.\n\n**정답:** {quiz_num} = {quiz_answer_correct}")
            else:
                st.warning("답을 입력해주세요!")
    
    else:  # 문제 3: 약수의 개수
        # 문제 3: 약수의 개수 구하기
        random.seed(st.session_state.get('quiz_seed3', 42))
        st.session_state.quiz_seed3 = random.randint(0, 1000)
        random.seed(st.session_state.quiz_seed3)
        
        quiz_numbers = [12, 18, 20, 24, 30, 36, 40, 48, 60, 72]
        quiz_num = random.choice(quiz_numbers)
        quiz_factors = prime_factorization(quiz_num)
        quiz_factors_dict = factors_to_dict(quiz_factors)
        quiz_divisors = get_all_divisors(quiz_factors_dict)
        quiz_answer_correct = len(quiz_divisors)
        
        formatted = format_prime_factorization(quiz_factors_dict)
        st.markdown(f"### 문제: **{quiz_num} = {formatted}**")
        st.markdown(f"**이 수의 약수는 몇 개일까요?**")
        
        user_answer = st.number_input("약수의 개수:", min_value=1, max_value=100, step=1, key="quiz3_input")
        
        if st.button("정답 확인", key="quiz3_submit"):
            if user_answer == quiz_answer_correct:
                st.success(f"✅ 정답입니다! {quiz_num}의 약수는 {quiz_answer_correct}개입니다.")
                st.info(f"약수: {', '.join(map(str, quiz_divisors))}")
                st.balloons()
            else:
                st.error(f"❌ 다시 풀어보세요.")
                st.markdown(f"""
                **정답:** {quiz_answer_correct}개
                
                **해설:** {formatted} 에서
                
                약수의 개수 = ({' × '.join([f'({e}+1)' for e in quiz_factors_dict.values()])}) = {quiz_answer_correct}
                
                **약수:** {', '.join(map(str, quiz_divisors))}
                """)

# 하단 정보
st.divider()
st.markdown("""
---
**💡 학습 팁:**
- 소인수분해는 모든 자연수를 유일하게 소인수들의 곱으로 표현하는 것입니다.
- 약수의 개수는 각 소인수의 지수에 1을 더한 값들의 곱입니다.
- 같은 크기의 수라도 소인수의 구조에 따라 약수의 개수가 매우 달라질 수 있습니다!
""")
