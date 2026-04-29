import streamlit as st
import pandas as pd
import numpy as np

# Настройка страницы
st.set_page_config(page_title="GCC Economic Impact", layout="wide")

st.title("Моделирование макроэкономического эффекта мегапроектов ССПЗ")
st.markdown("Интерактивная модель для оценки влияния отраслевых инвестиций на диверсификацию ВВП и рынок труда. Разработано для дипломного исследования.")

# Боковая панель (Вводные данные)
st.sidebar.header("Параметры инвестиций")
focus = st.sidebar.selectbox("Отраслевой фокус мегапроектов", 
                             ["Технологии и ИИ", "Туризм и культура", "Зеленая энергетика", "Логистика и транспорт"])
investment = st.sidebar.slider("Ежегодные инвестиции (млрд $)", 5, 50, 20)
inst_quality = st.sidebar.radio("Качество институциональной среды", 
                                ["Высокое (Мультипликатор 2.5)", "Среднее (Мультипликатор 1.5)", "Низкое (Мультипликатор 1.0)"])

# Математическая логика модели
# Определяем мультипликатор
if "Высокое" in inst_quality:
    mult = 2.5
elif "Среднее" in inst_quality:
    mult = 1.5
else:
    mult = 1.0

# Определяем веса в зависимости от отрасли
if focus == "Технологии и ИИ":
    labor_boost, soft_power_boost, eco_boost = 0.8, 0.6, 0.4
elif focus == "Туризм и культура":
    labor_boost, soft_power_boost, eco_boost = 1.5, 1.5, 0.3
elif focus == "Зеленая энергетика":
    labor_boost, soft_power_boost, eco_boost = 0.5, 0.8, 2.0
else: # Логистика
    labor_boost, soft_power_boost, eco_boost = 1.0, 0.5, 0.2

# Расчет ВВП на 20 лет вперед (2025 - 2045)
years = np.arange(2025, 2046)
oil_gdp = [150] * 21  # Сырьевой ВВП считаем статичным для наглядности (150 млрд $)
non_oil_gdp = []
current_non_oil = 80.0 # Стартовый несырьевой ВВП

for i in range(21):
    # Прирост несырьевого ВВП = (инвестиции * мультипликатор * коэффициент) + базовый рост
    annual_growth = (investment * mult * 0.12) + 2.0
    current_non_oil += annual_growth
    non_oil_gdp.append(current_non_oil)

# Создаем датафрейм для графика
df = pd.DataFrame({
    "Год": years, 
    "Сырьевой ВВП (млрд $)": oil_gdp, 
    "Несырьевой ВВП (млрд $)": non_oil_gdp
}).set_index("Год")

# Вывод графика
st.subheader("Прогноз диверсификации экономики (Сырьевой vs Несырьевой ВВП)")
st.line_chart(df)

# Расчет итоговых метрик за 20 лет
total_inv_20y = investment * 20
final_labor_nat = min(25 + (total_inv_20y * labor_boost * mult * 0.015), 85) # Максимум 85% занятости
soft_power = min(40 + (total_inv_20y * soft_power_boost * mult * 0.04), 100)
eco_index = min(35 + (total_inv_20y * eco_boost * mult * 0.05), 100)

# Вывод карточек с результатами
st.subheader("Прогнозные макроэкономические индексы к 2045 году")
col1, col2, col3 = st.columns(3)
col1.metric("Национализация рынка труда", f"{final_labor_nat:.1f}%", "Стартовая: 25.0%")
col2.metric("Индекс «Мягкой силы»", f"{soft_power:.1f} / 100")
col3.metric("Индекс устойчивости (ESG)", f"{eco_index:.1f} / 100")

st.info("💡 **Как читать данные:** Изменяйте отраслевой фокус слева, чтобы увидеть, как туризм сильнее влияет на «Мягкую силу» и рабочие места, а зеленая энергетика резко повышает индекс ESG. Мультипликатор отражает эффективность государственных институтов.")
