import streamlit as st
import random

st.set_page_config(
    page_title="CEO 경영 시뮬레이션",
    page_icon="🏢",
    layout="wide"
)

MAX_DAYS = 30

def init_game(company, product, category, price, cost, quality, production):
    st.session_state.game = {
        "company": company,
        "product": product,
        "category": category,
        "day": 1,
        "money": 100_000_000,
        "debt": 0,
        "price": price,
        "unit_cost": cost,
        "quality": quality,
        "marketing": 15,
        "brand": 10,
        "reputation": 30,
        "satisfaction": 50,
        "workers": 3,
        "capacity": 100,
        "production": production,
        "inventory": production,
        "stores": 1,
        "technology": 1,
        "market_share": 5.0,
        "competitor_price": int(price * 1.1),
        "competitor_strength": 30,
        "sales_total": 0,
        "expense_total": 0,
        "profit_total": 0,
        "total_sold": 0,
        "logs": [],
        "events": [],
        "last_sales": 0,
        "last_profit": 0,
        "last_units": 0,
        "last_event": "창업을 시작했습니다.",
        "finished": False
    }
    st.session_state.started = True


def log(message):
    g = st.session_state.game
    g["logs"].append(f"{g['day']}일차: {message}")
    g["logs"] = g["logs"][-50:]


def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


if "started" not in st.session_state:
    st.session_state.started = False


if not st.session_state.started:

    st.title("🏢 CEO 경영 시뮬레이션")
    st.subheader("나만의 기업을 만들어 대기업으로 성장시키세요!")

    company = st.text_input("회사 이름", "미래기업")
    product = st.text_input("판매할 상품", "스마트 텀블러")

    category = st.selectbox(
        "사업 분야",
        [
            "식품 및 음료",
            "패션 및 의류",
            "전자제품",
            "화장품",
            "게임 및 IT",
            "인공지능",
            "생활용품",
            "자동차",
            "기타"
        ]
    )

    st.header("상품 설정")

    price = st.number_input(
        "판매 가격 (원)",
        min_value=100,
        max_value=10000000,
        value=20000,
        step=1000
    )

    cost = st.number_input(
        "상품 생산 원가 (원)",
        min_value=100,
        max_value=10000000,
        value=8000,
        step=500
    )

    quality = st.slider("초기 제품 품질", 10, 100, 50)

    production = st.number_input(
        "초기 생산량",
        min_value=1,
        max_value=10000,
        value=50
    )

    st.info(
        "초기 자본금: 1억 원 | 마케팅: 15점 | "
        "평판: 30점 | 경영 기간: 30일"
    )

    if st.button("🚀 창업 시작하기", type="primary"):

        if not company.strip() or not product.strip():
            st.error("회사 이름과 상품명을 입력하세요.")

        elif cost >= price:
            st.error("판매 가격은 생산 원가보다 높아야 합니다.")

        else:
            init_game(
                company,
                product,
                category,
                price,
                cost,
                quality,
                production
            )
            st.rerun()

    st.stop()


g = st.session_state.game


if g["finished"]:

    st.title("🏆 최종 경영 평가")

    net_assets = g["money"] - g["debt"]

    if g["money"] <= 0:
        grade = "F - 기업 파산"
    elif net_assets >= 300_000_000 and g["reputation"] >= 80:
        grade = "S - 전설의 CEO"
    elif net_assets >= 200_000_000:
        grade = "A - 성공한 CEO"
    elif net_assets >= 100_000_000:
        grade = "B - 안정적인 CEO"
    elif net_assets > 0:
        grade = "C - 성장 가능성 있는 CEO"
    else:
        grade = "F - 경영 실패"

    st.header(grade)

    a, b, c = st.columns(3)

    a.metric("최종 현금", f"{g['money']:,}원")
    b.metric("순자산", f"{net_assets:,}원")
    c.metric("누적 매출", f"{g['sales_total']:,}원")

    a, b, c = st.columns(3)

    a.metric("총 판매량", f"{g['total_sold']:,}개")
    b.metric("기업 평판", f"{g['reputation']}/100")
    c.metric("시장 점유율", f"{g['market_share']:.1f}%")

    st.write(f"누적 지출: {g['expense_total']:,}원")
    st.write(f"누적 손익: {g['profit_total']:,}원")

    if g["money"] > 0:
        st.balloons()

    if st.button("새로운 기업 창업"):
        reset_game()

    st.stop()


st.title(f"🏢 {g['company']}")
st.caption(f"주력 상품: {g['product']} | 사업 분야: {g['category']}")

st.progress(min(g["day"] / MAX_DAYS, 1))
st.write(f"경영 {g['day']}일차 / 30일")

a, b, c, d = st.columns(4)

a.metric("💰 현금", f"{g['money']:,}원")
b.metric("📈 누적 매출", f"{g['sales_total']:,}원")
c.metric("💸 누적 지출", f"{g['expense_total']:,}원")
d.metric("🏦 부채", f"{g['debt']:,}원")

a, b, c, d = st.columns(4)

a.metric("📢 마케팅", f"{g['marketing']}/100")
b.metric("⭐ 제품 품질", f"{g['quality']}/100")
c.metric("😊 고객 만족도", f"{g['satisfaction']}/100")
d.metric("🏆 기업 평판", f"{g['reputation']}/100")

st.divider()
# 가격 전략

st.header("💵 1. 가격 전략")

st.write(f"경쟁사 가격: {g['competitor_price']:,}원")

new_price = st.number_input(
    "판매 가격 변경",
    min_value=100,
    max_value=10000000,
    value=int(g["price"]),
    step=500,
    key="price_input"
)

if st.button("가격 변경 적용"):
    g["price"] = new_price
    log(f"판매 가격을 {new_price:,}원으로 변경")
    st.rerun()

st.metric("개당 예상 마진", f"{g['price'] - g['unit_cost']:,}원")


# 마케팅

st.divider()
st.header("📢 2. 마케팅 전략")

marketing_methods = {
    "SNS 광고": (1000000, 0.80, 5, 12),
    "TV 광고": (8000000, 0.55, 8, 20),
    "인플루언서 협찬": (3000000, 0.65, 5, 20),
    "검색 광고": (1500000, 0.85, 4, 10),
    "할인 행사": (2000000, 0.75, 3, 12),
    "바이럴 마케팅": (500000, 0.40, 10, 30),
    "오프라인 이벤트": (2500000, 0.70, 4, 15),
    "유명인 모델 계약": (12000000, 0.50, 10, 25),
    "이메일 마케팅": (300000, 0.90, 2, 8),
    "스포츠 후원": (10000000, 0.60, 8, 22),
    "유튜브 광고": (4000000, 0.70, 6, 18),
    "옥외 광고": (5000000, 0.60, 5, 15)
}

st.write(f"현재 마케팅 효과: {g['marketing']}/100")
st.progress(g["marketing"] / 100)

cols = st.columns(3)

for i, (name, data) in enumerate(marketing_methods.items()):

    ad_cost, probability, low, high = data

    with cols[i % 3]:

        with st.container(border=True):

            st.subheader(name)
            st.write(f"비용: {ad_cost:,}원")
            st.write(f"성공 확률: {probability * 100:.0f}%")
            st.write(f"성공 시 상승: {low}~{high}점")

            if st.button("광고 실행", key=f"ad_{i}"):

                if g["money"] < ad_cost:
                    st.error("자금이 부족합니다.")

                else:
                    g["money"] -= ad_cost
                    g["expense_total"] += ad_cost

                    if random.random() < probability:

                        gain = random.randint(low, high)

                        g["marketing"] = min(
                            100,
                            g["marketing"] + gain
                        )

                        g["brand"] = min(100, g["brand"] + 3)
                        g["reputation"] = min(100, g["reputation"] + 2)

                        log(f"{name} 성공! 마케팅 +{gain}점")

                    else:

                        loss = random.randint(5, 15)

                        g["marketing"] = max(
                            0,
                            g["marketing"] - loss
                        )

                        g["reputation"] = max(
                            0,
                            g["reputation"] - 2
                        )

                        log(f"{name} 실패! 마케팅 -{loss}점")

                    st.rerun()


# 생산 관리

st.divider()
st.header("🏭 3. 생산 관리")

production = st.number_input(
    "하루 생산 계획",
    min_value=0,
    max_value=g["capacity"],
    value=min(g["production"], g["capacity"]),
    key="production_input"
)

if st.button("생산 계획 변경"):
    g["production"] = production
    log(f"생산량을 {production}개로 변경")
    st.rerun()

st.write(f"생산 능력: {g['capacity']}개")
st.write(f"현재 재고: {g['inventory']}개")


# 연구개발

st.divider()
st.header("🔬 4. 연구개발")

st.write(f"현재 기술 단계: {g['technology']}")

if st.button("연구개발 투자 (500만 원)"):

    if g["money"] >= 5000000:

        g["money"] -= 5000000
        g["expense_total"] += 5000000
        g["technology"] += 1

        gain = random.randint(3, 8)
        g["quality"] = min(100, g["quality"] + gain)

        log(f"연구개발 성공! 품질 +{gain}점")
        st.success(f"제품 품질이 {gain}점 상승했습니다.")

        st.rerun()

    else:
        st.warning("자금이 부족합니다.")


# 직원 관리

st.divider()
st.header("👥 5. 인사 관리")

st.write(f"현재 직원: {g['workers']}명")
st.write(f"현재 생산 능력: {g['capacity']}개")

if st.button("직원 채용 (200만 원)"):

    if g["money"] >= 2000000:

        g["money"] -= 2000000
        g["expense_total"] += 2000000
        g["workers"] += 1
        g["capacity"] += 20

        log("직원 1명 채용 완료")
        st.rerun()

    else:
        st.warning("자금이 부족합니다.")


# 고객 관리

st.divider()
st.header("😊 6. 고객 관리")

st.metric("고객 만족도", f"{g['satisfaction']}/100")
st.progress(g["satisfaction"] / 100)

if st.button("고객 서비스 개선 (300만 원)"):

    if g["money"] >= 3000000:

        g["money"] -= 3000000
        g["expense_total"] += 3000000

        g["satisfaction"] = min(
            100,
            g["satisfaction"] + 12
        )

        g["reputation"] = min(
            100,
            g["reputation"] + 3
        )

        log("고객 서비스 개선 완료")
        st.rerun()

    else:
        st.warning("자금이 부족합니다.")


# 사업 확장

st.divider()
st.header("🏬 7. 사업 확장")

a, b = st.columns(2)

with a:

    st.subheader("신규 매장")
    st.write(f"현재 매장: {g['stores']}개")

    if st.button("매장 개설 (1,000만 원)"):

        if g["money"] >= 10000000:

            g["money"] -= 10000000
            g["expense_total"] += 10000000
            g["stores"] += 1

            log("신규 매장 개설 완료")
            st.rerun()

        else:
            st.warning("자금이 부족합니다.")


with b:

    st.subheader("은행 대출")
    st.write(f"현재 부채: {g['debt']:,}원")

    if st.button("1,000만 원 대출"):

        if g["debt"] + 10000000 <= 50000000:

            g["money"] += 10000000
            g["debt"] += 10000000

            log("1,000만 원 대출 실행")
            st.rerun()

        else:
            st.warning("대출 한도를 초과했습니다.")
# 하루 진행

st.divider()
st.header("📅 8. 하루 경영 진행")

st.info(
    "하루를 진행하면 판매량, 매출, 비용, "
    "경쟁사 변화와 무작위 사건이 발생합니다."
)

if st.button("▶ 하루 진행하기", type="primary", use_container_width=True):

    produced = g["production"]
    production_cost = produced * g["unit_cost"]

    if g["money"] < production_cost:
        st.error("생산 비용이 부족합니다. 생산량을 줄이거나 대출을 받으세요.")
        st.stop()

    g["money"] -= production_cost
    g["expense_total"] += production_cost
    g["inventory"] += produced

    # 경쟁사 가격 변화

    if random.random() < 0.20:
        g["competitor_price"] = int(
            g["competitor_price"] * random.uniform(0.90, 1.10)
        )

    # 수요 계산

    price_ratio = g["price"] / max(1, g["competitor_price"])

    price_factor = max(
        0.2,
        min(1.7, 1.5 - price_ratio)
    )

    quality_factor = 0.5 + g["quality"] / 100
    marketing_factor = 0.5 + g["marketing"] / 100
    satisfaction_factor = 0.5 + g["satisfaction"] / 100
    brand_factor = 0.7 + g["brand"] / 200

    demand = int(
        40
        * price_factor
        * quality_factor
        * marketing_factor
        * satisfaction_factor
        * brand_factor
        * (1 + g["technology"] * 0.05)
        * (1 + g["stores"] * 0.2)
        * random.uniform(0.7, 1.3)
    )

    demand = int(
        demand * (1 - g["competitor_strength"] / 200)
    )

    sold = min(max(0, demand), g["inventory"])

    revenue = sold * g["price"]

    salary = g["workers"] * 200000
    rent = g["stores"] * 300000
    interest = int(g["debt"] * 0.001)

    daily_expenses = salary + rent + interest

    daily_profit = revenue - production_cost - daily_expenses

    g["money"] += revenue - daily_expenses
    g["sales_total"] += revenue
    g["expense_total"] += daily_expenses
    g["profit_total"] += daily_profit

    g["inventory"] -= sold
    g["total_sold"] += sold

    g["last_sales"] = revenue
    g["last_profit"] = daily_profit
    g["last_units"] = sold

    # 고객 만족도 변화

    if price_ratio > 1.3:
        g["satisfaction"] -= random.randint(2, 6)

    elif g["quality"] >= 75:
        g["satisfaction"] += random.randint(1, 4)

    else:
        g["satisfaction"] += random.randint(-2, 3)

    g["satisfaction"] = max(
        0,
        min(100, g["satisfaction"])
    )

    # 기업 평판 변화

    if g["satisfaction"] >= 80:
        g["reputation"] += random.randint(1, 3)

    elif g["satisfaction"] < 30:
        g["reputation"] -= random.randint(2, 5)

    g["reputation"] = max(
        0,
        min(100, g["reputation"])
    )

    # 시장 점유율 변화

    g["market_share"] = max(
        0,
        min(
            100,
            g["market_share"]
            + random.uniform(-1, 1)
            + (g["marketing"] - 20) / 100
        )
    )

    # 마케팅 효과 자연 감소

    g["marketing"] = max(
        0,
        g["marketing"] - random.randint(0, 3)
    )

    # 재고 보관 비용

    if g["inventory"] > 100:

        storage = (g["inventory"] - 100) * 100

        g["money"] -= storage
        g["expense_total"] += storage
        g["profit_total"] -= storage

    # 랜덤 사건

    event = random.randint(1, 18)

    if event == 1:

        bonus = 5000000

        g["money"] += bonus
        g["profit_total"] += bonus

        g["last_event"] = "🎉 제품 대박! 특별 수익 500만 원!"

    elif event == 2:

        loss = 3000000

        g["money"] -= loss
        g["expense_total"] += loss
        g["profit_total"] -= loss

        g["last_event"] = "📉 경기 침체! 300만 원 손실!"

    elif event == 3:

        g["reputation"] = min(
            100,
            g["reputation"] + 10
        )

        g["last_event"] = "🏆 우수 기업 선정! 평판 상승!"

    elif event == 4:

        loss = 2000000

        g["money"] -= loss
        g["expense_total"] += loss
        g["profit_total"] -= loss

        g["last_event"] = "⚠️ 설비 고장! 수리비 200만 원!"

    elif event == 5:

        g["quality"] = max(
            0,
            g["quality"] - 10
        )

        g["last_event"] = "😡 품질 문제 발생! 제품 품질 하락!"

    elif event == 6:

        loss = random.randint(5, 15)

        g["marketing"] = max(
            0,
            g["marketing"] - loss
        )

        g["last_event"] = f"📢 광고 피로도 증가! 마케팅 -{loss}점!"

    elif event == 7:

        g["quality"] = min(
            100,
            g["quality"] + 5
        )

        g["last_event"] = "💡 기술 혁신! 제품 품질 상승!"

    elif event == 8:

        g["competitor_strength"] = min(
            90,
            g["competitor_strength"] + 10
        )

        g["last_event"] = "⚔️ 강력한 경쟁사 등장!"

    elif event == 9:

        g["satisfaction"] = min(
            100,
            g["satisfaction"] + 10
        )

        g["last_event"] = "😊 고객들의 긍정적인 후기 증가!"

    elif event == 10:

        g["unit_cost"] = int(
            g["unit_cost"] * 1.10
        )

        g["last_event"] = "📦 원자재 가격 상승! 생산 원가 10% 증가!"

    elif event == 11:

        g["market_share"] = min(
            100,
            g["market_share"] + 5
        )

        g["last_event"] = "🚀 시장 점유율 확대!"

    elif event == 12:

        g["satisfaction"] = max(
            0,
            g["satisfaction"] - 15
        )

        g["last_event"] = "🔥 제품 불량 논란! 고객 만족도 급락!"

    elif event == 13:

        g["competitor_price"] = int(
            g["competitor_price"] * 0.85
        )

        g["last_event"] = "💥 경쟁사 가격 인하! 가격 경쟁 심화!"

    elif event == 14:

        bonus = 2000000

        g["money"] += bonus

        g["last_event"] = "🤝 투자자 유치 성공! 현금 200만 원 확보!"

    elif event == 15:

        g["workers"] = max(
            1,
            g["workers"] - 1
        )

        g["last_event"] = "👷 직원 퇴사! 인력이 감소했습니다."

    elif event == 16:

        g["satisfaction"] = max(
            0,
            g["satisfaction"] - 10
        )

        g["reputation"] = max(
            0,
            g["reputation"] - 8
        )

        g["last_event"] = "📰 부정적인 언론 보도! 평판 하락!"

    elif event == 17:

        g["brand"] = min(
            100,
            g["brand"] + 10
        )

        g["last_event"] = "✨ 브랜드 인지도 상승!"

    else:

        g["last_event"] = "☀️ 특별한 사건 없이 하루가 지나갔습니다."

    log(
        f"판매 {sold}개 / 매출 {revenue:,}원 / 손익 {daily_profit:,}원"
    )

    g["events"].append(g["last_event"])
    g["events"] = g["events"][-20:]

    g["day"] += 1

    # 파산 조건

    if g["money"] <= 0:

        g["finished"] = True
        log("💥 자금 고갈로 기업 파산!")

    elif g["satisfaction"] <= 0:

        g["finished"] = True
        log("💥 고객 만족도 붕괴!")

    elif g["day"] > MAX_DAYS:

        g["finished"] = True
        log("🎉 30일 경영 완료!")

    st.rerun()


# 최근 실적

st.divider()
st.header("📊 최근 경영 실적")

a, b, c = st.columns(3)

a.metric("당일 매출", f"{g['last_sales']:,}원")
b.metric("당일 손익", f"{g['last_profit']:,}원")
c.metric("당일 판매량", f"{g['last_units']:,}개")

st.info(g["last_event"])


# 시장 사건

st.subheader("📰 최근 시장 사건")

for event in reversed(g["events"][-5:]):
    st.write("📌 " + event)


# 경영 일지

st.subheader("📜 경영 일지")

for item in reversed(g["logs"][-15:]):
    st.write("📌 " + item)


# 사이드바

st.sidebar.title("🏢 CEO 정보")

st.sidebar.write(f"회사: {g['company']}")
st.sidebar.write(f"상품: {g['product']}")
st.sidebar.write(f"경영 일수: {min(g['day'], 30)}/30")
st.sidebar.write(f"현금: {g['money']:,}원")
st.sidebar.write(f"재고: {g['inventory']:,}개")
st.sidebar.write(f"부채: {g['debt']:,}원")

st.sidebar.divider()

st.sidebar.subheader("💡 경영 팁")

st.sidebar.write("1. 판매 가격을 신중하게 결정하세요.")
st.sidebar.write("2. 마케팅은 15점에서 시작합니다.")
st.sidebar.write("3. 광고 실패 시 마케팅이 하락합니다.")
st.sidebar.write("4. 과잉 생산은 재고 비용을 발생시킵니다.")
st.sidebar.write("5. 현금 흐름을 관리하세요.")

if st.sidebar.button("게임 초기화"):
    reset_game()
