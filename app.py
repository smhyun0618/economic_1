import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="기업 경영 시뮬레이션", page_icon="🏢", layout="wide")

# 게임 초기화
if "started" not in st.session_state:
    st.session_state.started = False

if "money" not in st.session_state:
    st.session_state.money = 100000000
    st.session_state.sales = 0
    st.session_state.expenses = 0
    st.session_state.workers = 5
    st.session_state.reputation = 50
    st.session_state.day = 1
    st.session_state.rd = 0
    st.session_state.marketing = 0
    st.session_state.production = 1
    st.session_state.stores = 1
    st.session_state.logs = []
    st.session_state.finished = False

# 초기화 함수
def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# 제목
st.title("🏢 나만의 기업 경영 시뮬레이션")
st.subheader("당신은 이제 CEO입니다! 30일 동안 회사를 성장시켜 보세요.")

# 회사 이름
if not st.session_state.started:
    company = st.text_input("회사 이름을 입력하세요", "미래기업")
    if st.button("🚀 회사 창업하기"):
        st.session_state.company = company
        st.session_state.started = True
        st.rerun()
    st.stop()

st.header(f"🏭 {st.session_state.company}")

# 게임 종료 여부
if st.session_state.finished:
    st.error("게임이 종료되었습니다!")
    st.stop()

# 경영 현황
st.markdown(f"### 📅 DAY {st.session_state.day} / 30")

c1, c2, c3 = st.columns(3)
c1.metric("💰 보유 자금", f"{st.session_state.money:,}원")
c2.metric("📈 누적 매출", f"{st.session_state.sales:,}원")
c3.metric("💸 누적 지출", f"{st.session_state.expenses:,}원")

c4, c5, c6 = st.columns(3)
c4.metric("👥 직원 수", f"{st.session_state.workers}명")
c5.metric("⭐ 기업 평판", f"{st.session_state.reputation}점")
c6.metric("🔬 기술 수준", f"{st.session_state.rd}단계")

st.divider()

# 경영 활동
st.header("📋 CEO 경영 활동")

a, b, c = st.columns(3)

with a:
    st.subheader("🏭 생산량 확대")
    st.write("비용: 500만 원")
    if st.button("생산 투자하기"):
        if st.session_state.money >= 5000000:
            st.session_state.money -= 5000000
            st.session_state.expenses += 5000000
            st.session_state.production += 1
            st.success("생산 시설을 확장했습니다!")
        else:
            st.warning("자금이 부족합니다.")

with b:
    st.subheader("📢 마케팅")
    st.write("비용: 300만 원")
    if st.button("광고 투자하기"):
        if st.session_state.money >= 3000000:
            st.session_state.money -= 3000000
            st.session_state.expenses += 3000000
            st.session_state.marketing += 1
            st.session_state.reputation = min(100, st.session_state.reputation + 5)
            st.success("마케팅 투자 성공!")
        else:
            st.warning("자금이 부족합니다.")

with c:
    st.subheader("👨‍💼 직원 채용")
    st.write("비용: 200만 원")
    if st.button("직원 채용하기"):
        if st.session_state.money >= 2000000:
            st.session_state.money -= 2000000
            st.session_state.expenses += 2000000
            st.session_state.workers += 1
            st.success("새로운 직원을 채용했습니다!")
        else:
            st.warning("자금이 부족합니다.")

d, e, f = st.columns(3)

with d:
    st.subheader("🔬 연구개발")
    st.write("비용: 700만 원")
    if st.button("R&D 투자하기"):
        if st.session_state.money >= 7000000:
            st.session_state.money -= 7000000
            st.session_state.expenses += 7000000
            st.session_state.rd += 1
            st.success("기술력이 향상되었습니다!")
        else:
            st.warning("자금이 부족합니다.")

with e:
    st.subheader("🏪 신규 매장")
    st.write("비용: 1,000만 원")
    if st.button("매장 개설하기"):
        if st.session_state.money >= 10000000:
            st.session_state.money -= 10000000
            st.session_state.expenses += 10000000
            st.session_state.stores += 1
            st.success("신규 매장을 개설했습니다!")
        else:
            st.warning("자금이 부족합니다.")

with f:
    st.subheader("📊 기업 정보")
    st.write(f"생산 수준: {st.session_state.production}")
    st.write(f"마케팅 수준: {st.session_state.marketing}")
    st.write(f"매장 수: {st.session_state.stores}")

st.divider()

# 하루 진행
st.header("📅 하루 경영하기")

if st.button("▶ 하루 진행하기", type="primary", use_container_width=True):

    # 매출 계산
    base_sales = (
        2000000
        * st.session_state.production
        * st.session_state.stores
        * (1 + st.session_state.rd * 0.15)
        * (1 + st.session_state.marketing * 0.10)
        * (1 + st.session_state.workers * 0.03)
    )

    sales = int(base_sales * random.uniform(0.7, 1.3))

    # 지출 계산
    salary = st.session_state.workers * 200000
    operating = st.session_state.stores * 300000
    expenses = salary + operating

    # 매출 및 지출 반영
    st.session_state.money += sales - expenses
    st.session_state.sales += sales
    st.session_state.expenses += expenses

    st.session_state.logs.append(
        f"DAY {st.session_state.day}: 매출 {sales:,}원 / 지출 {expenses:,}원"
    )

    st.success(f"오늘 매출: {sales:,}원")
    st.info(f"오늘 지출: {expenses:,}원")

    # 돌발 이벤트
    event = random.randint(1, 5)

    if event == 1:
        bonus = 3000000
        st.session_state.money += bonus
        st.success("🎉 제품 대박! 추가 수익 300만 원!")

    elif event == 2:
        loss = 2000000
        st.session_state.money -= loss
        st.error("📉 경기 침체! 200만 원 손실!")

    elif event == 3:
        st.session_state.reputation = min(
            100, st.session_state.reputation + 10
        )
        st.success("🏆 우수 기업 선정! 평판 상승!")

    elif event == 4:
        loss = 1000000
        st.session_state.money -= loss
        st.warning("⚠️ 예상치 못한 비용 100만 원 발생!")

    elif event == 5:
        st.session_state.rd += 1
        st.success("💡 혁신 기술 발견! 기술 수준 상승!")

    st.session_state.day += 1

    # 게임 종료 판정
    if st.session_state.money <= 0:
        st.session_state.finished = True
        st.error("💥 파산했습니다!")

    elif st.session_state.day > 30:
        st.session_state.finished = True
        st.balloons()
        st.success("🎉 30일 경영 완료!")

    st.rerun()

# 경영 기록
st.divider()
st.header("📜 경영 일지")

for log in reversed(st.session_state.logs[-10:]):
    st.write("📌 " + log)

# 최종 결과
if st.session_state.finished:
    st.divider()
    st.header("🏆 최종 경영 평가")

    money = st.session_state.money
    reputation = st.session_state.reputation

    if money >= 200000000 and reputation >= 80:
        grade = "S - 최고의 경영자"
    elif money >= 150000000:
        grade = "A - 우수 경영자"
    elif money >= 100000000:
        grade = "B - 양호한 경영자"
    elif money > 0:
        grade = "C - 노력하는 경영자"
    else:
        grade = "F - 경영 실패"

    st.subheader(f"최종 등급: {grade}")
    st.write(f"최종 보유 자금: {money:,}원")
    st.write(f"누적 매출: {st.session_state.sales:,}원")
    st.write(f"기업 평판: {reputation}점")

    if money > 0:
        st.balloons()

    if st.button("🔄 새 게임 시작"):
        reset_game()

# 게임 초기화
if st.sidebar.button("게임 처음부터 다시 하기"):
    reset_game()

st.sidebar.title("📖 게임 안내")
st.sidebar.write("1. 경영 활동을 선택하세요.")
st.sidebar.write("2. 하루 진행 버튼을 누르세요.")
st.sidebar.write("3. 매출과 지출을 확인하세요.")
st.sidebar.write("4. 30일 동안 회사를 성장시키세요!")
