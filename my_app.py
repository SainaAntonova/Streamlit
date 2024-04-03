import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
import datetime as dt


st.markdown(
    """
    <div style="background-color:#f0f0f0;padding:10px;border-radius:10px;">
        <h1 style="color:#333;text-align:center;">🍽️ Чаевые в ресторане 🍽️</h1>
    </div>
    """,
    unsafe_allow_html=True
)

path = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
#path = '../learning/datasets/tips.csv'
tips = pd.read_csv(path)
tips['time_order'] = pd.to_datetime(np.random.uniform(pd.to_datetime('2023-01-01').timestamp(),
                                                pd.to_datetime('2023-01-31').timestamp(),
                                                size=len(tips)), unit='s').date
tips['time_order'] = pd.to_datetime(tips['time_order'])
tips['weekend'] = tips.day.isin(['Sat','Sun'])
tips['weekend'] = tips['weekend'].astype(int)
tips['tip_percentage']= np.round(100*(tips['tip']/tips['total_bill']), 1)

st.write("""### Данные""")
st.write(tips)

st.title("Визуализация данных")
# выпадающий список для выбора графика
option = st.sidebar.selectbox(
    '**Выберите график**:',  
    ('График динамики чаевых в зависимости от времени заказа',
     'Распределение значений размера счетов',
     'Зависимость размера чаевых от размера счета',
     'Взаимосвязь размера счета, чаевых и порции',
     'Взаимосвязь между днем недели и размером счета',
     'Сумма счетов по дням',
     'Чаевые за обед и ужин',
     'Тепловая карта корреляций числовых переменных',
     'Взаимосвязь размера счета и чаевых, с разделением по курящим/некурящим'))

# проверяем выбор пользователя и выводим нужный график
if option == 'График динамики чаевых в зависимости от времени заказа':
    tips_dynamics = tips.groupby('time_order')['tip'].mean().reset_index()
    fig = px.line(tips_dynamics, x='time_order', y='tip', markers=True, title='Динамика чаевых во времени')
    fig.update_layout(
        xaxis_title='Дата заказа',
        yaxis_title='Чаевые',
        xaxis=dict(tickangle=45),
    )
    st.plotly_chart(fig)
    
    tips_dynamics['time_order_timestamp'] = tips_dynamics['time_order'].astype(int) // 10**9
    min_date = dt.datetime.fromtimestamp(tips_dynamics['time_order_timestamp'].min())
    max_date = dt.datetime.fromtimestamp(tips_dynamics['time_order_timestamp'].max())
    date_range = st.slider("Выберите интервал дат:", min_value=min_date, max_value=max_date, value=(min_date, max_date))
    
    

elif option == 'Распределение значений размера счетов':
    st.write('Распределение значений размера счетов')
    fig = px.histogram(tips, x='total_bill', nbins=20, labels={'total_bill': 'Размер счета ($)', 'count': 'Частота'})
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    st.plotly_chart(fig)

elif option == 'Зависимость размера чаевых от размера счета':
    st.write('Зависимость размера чаевых от размера счета')
    st.scatter_chart(data=tips, x='tip', y='total_bill')

elif option == 'Взаимосвязь размера счета, чаевых и порции':
    st.write('Взаимосвязь размера счета, чаевых и порции')
    st.scatter_chart(data=tips, x='tip', y='total_bill', size='size')

elif option == 'Взаимосвязь между днем недели и размером счета':
    st.write('Взаимосвязь между днем недели и размером счета')
    st.scatter_chart(data=tips, x='day', y='tip', color='sex')
    st.write('В процентном соотношении. Общее ')
    a=pd.DataFrame(tips['day'].value_counts())
    a.reset_index(inplace=True)
    fig = px.pie(data_frame=a, values='count', names='day', hole=0.3)
    st.plotly_chart(fig)

    male_tips = tips[tips['sex'] == 'Male']
    male_counts = male_tips['day'].value_counts().reset_index()
    male_counts.columns = ['day', 'count']
    fig_male = px.pie(male_counts, values='count', names='day', title='Pie Chart. Мужчины', hole=0.3)
    st.plotly_chart(fig_male)

    female_tips = tips[tips['sex'] == 'Female']
    female_counts = female_tips['day'].value_counts().reset_index()
    female_counts.columns = ['day', 'count']
    fig_female = px.pie(female_counts, values='count', names='day', title='Pie Chart. Женщины', hole=0.3)
    st.plotly_chart(fig_female)
    


elif option == 'Сумма счетов по дням':
    st.write('Сумма счетов по дням')
    fig = px.box(tips, x='day', y='total_bill', color='time')
    st.plotly_chart(fig)

elif option == 'Чаевые за обед и ужин':
    option = st.sidebar.selectbox('**Выберите вид графика**:',
                                  ('Гистограммы чаевых за обед и ужин', 
                                  'Круговая диаграмма чаевых за обед и ужин'))
    if option == 'Гистограммы чаевых за обед и ужин':
        st.write("Гистограммы чаевых за обед и ужин")
        time_option = st.radio("Выберите время:", ('Обед', 'Ужин'))
        filtered_tips = tips[(tips['time'] == ('Lunch' if time_option == 'Обед' else 'Dinner'))]
        fig, ax = plt.subplots()
        sns.histplot(data=filtered_tips, x='tip', bins=10, color='skyblue', ax=ax)
        ax.set_title(f'Чаевые за {time_option.lower()}')
        ax.set_xlabel('Размер чаевых')
        ax.set_ylabel('Частота')
        st.pyplot(fig)
    elif option == 'Круговая диаграмма чаевых за обед и ужин':
        st.write("Круговая диаграмма чаевых за обед и ужин")
        fig=px.pie(tips, values='tip_percentage', names='time', hole=0.5)
        st.plotly_chart(fig)

elif option == 'Тепловая карта корреляций числовых переменных':
    st.write("Тепловая карта корреляций числовых переменных")
    numeric_columns = tips.select_dtypes(include='number')
    correlation_matrix = numeric_columns.corr().iloc[:, :9]
    correlation_df = correlation_matrix.stack().reset_index()
    correlation_df.columns = ['variable1', 'variable2', 'correlation']
    
    heatmap = alt.Chart(correlation_df).mark_rect().encode(
        x='variable1:O',
        y='variable2:O',
        color=alt.Color('correlation:Q', scale=alt.Scale(scheme='viridis'))
    ).properties(
         width=500,
        height=500
    ).configure_scale(
        bandPaddingInner=0.1
    )
    st.altair_chart(heatmap, use_container_width=True)

elif option == 'Взаимосвязь размера счета и чаевых, с разделением по курящим/некурящим':
    st.write("Взаимосвязь размера счета и чаевых, с разделением по курящим/некурящим")
    option = st.sidebar.selectbox('**Выберите scatter-график**:',
                                  ('Для женщин', 
                                  'Для мужчин'))
    if option == ('Для женщин'):
        data = tips[tips['sex'] == 'Female']
        st.scatter_chart(data=data, x='total_bill', y='tip', color='smoker')
    elif option == ('Для мужчин'):
        data = tips[tips['sex'] == 'Male']
        st.scatter_chart(data=data, x='total_bill', y='tip', color='smoker')

cat_gif_url = 'https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif'
if st.button('🥚🐰🥚НАЖМИ НА МЕНЯ🥚🐰🥚'): 
    st.image(cat_gif_url)