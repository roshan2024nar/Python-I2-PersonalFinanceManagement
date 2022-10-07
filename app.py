import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Personal Finance Management', layout="wide",  page_icon=':bar_chart:')


@st.cache(allow_output_mutation=True)
def read_csv():
    data = pd.read_csv("static/datasets/personal_transactions.csv")
    data.rename(columns={'Transaction Type': 'Transaction_Type',
                'Account Name': 'Account_Name'}, inplace=True)
    return data


st.header("Personal Finance Management :bar_chart:")
data = read_csv()

l1, l2, l3, l4, l5 = st.columns(5)

with l1:
    tot_spend = data[data["Transaction_Type"] == "debit"]
    tot_spend = tot_spend.groupby(["Transaction_Type"])[
        "Amount"].sum().reset_index(name='Total')
    st.metric('Total Spend', value=round(tot_spend._get_value(0, 'Total'), 3))


with l2:
    tot_inc = data[data["Transaction_Type"] == "credit"]
    tot_inc = tot_inc.groupby(["Transaction_Type"])[
        "Amount"].sum().reset_index(name='Total')
    st.metric('Total Income', value=round(tot_inc._get_value(0, 'Total'), 3))

with l3:
    tot_avg = data[data["Transaction_Type"] == "debit"]
    tot_avg = tot_avg.groupby(["Transaction_Type"])[
        "Amount"].mean().reset_index(name='Total')
    st.metric('Average Spend', value=round(tot_avg._get_value(0, 'Total'), 3))

with l4:
    tot_avg_in = data[data["Transaction_Type"] == "credit"]
    tot_avg_in = tot_avg_in.groupby(["Transaction_Type"])[
        "Amount"].mean().reset_index(name='Total')
    st.metric('Average Income', value=round(
        tot_avg_in._get_value(0, 'Total'), 3))


with l5:
    st.metric('Total Savings', value=round(
        ((tot_inc._get_value(0, 'Total')-(tot_spend._get_value(0, 'Total')))), 3))


data['year'] = pd.to_datetime(data['Date']).dt.year
data['month'] = pd.to_datetime(data['Date']).dt.month_name()
data['month_year'] = pd.to_datetime(data['year'].astype(
    str) + '-' + data['month'].astype(str), yearfirst=True)


st.sidebar.header("Please select the filters Here :")
category = st.sidebar.multiselect(
    'Select The Category : ',
    options=data['Category'].unique(),
    default=data['Category'].unique())

month = st.sidebar.multiselect(
    'Select Months here : ',
    options=data['month'].unique(),
    default=data['month'].unique())

year = st.sidebar.multiselect(
    'Select Year here : ',
    options=data['year'].unique(),
    default=data['year'].unique())

data = data.query('Category == @category & month == @month & year == @year ')

tab1, tab2 = st.tabs(['Expenses', 'Income'])

with tab1:
    z1, z2, z3 = st.columns(3)
    with z2:
        st.markdown(
            f'<h1 style = "color: Red;font-size:35px;">{"Expense Analysis"}</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        exp_data = data.groupby(['Transaction_Type'])
        exp_data = exp_data.get_group('debit')
        fig = px.histogram(exp_data, x='Amount', y='Category',
                           barmode='group', width=800)
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        fig.update_layout(title_text="Total Expenses",
                          title_x=0.5, title_font_color='red')
        st.plotly_chart(fig, config={'displayModeBar': False})
        with st.expander("See Explanation"):
            st.write(
                'Above bar chart shows total spend on different category over a period of time.')

    with col2:
        # Account data
        debit_data = data.groupby(['Transaction_Type'])
        debit_data = debit_data.get_group('debit')
        fig2 = px.pie(debit_data, names='Account_Name', values='Amount')
        fig2.update_layout(title_text="Mode of Payment",
                           title_x=0.33, title_font_color='red')
        st.plotly_chart(fig2, config={'displayModeBar': False})
        with st.expander("See Explanation"):
            st.write(
                'Above pie chart shows different mode of payments used for expenses.')

    c1, c2, c3 = st.columns([1, 3, 1])

    with c2:
        budget = pd.read_csv('static/datasets/Budget.csv')
        debit_data = data[data["Transaction_Type"] == "debit"]
        debit_avg = debit_data.groupby(["Category"])[
            "Amount"].mean().reset_index(name='mean')
        fig7 = go.Figure()
        fig7.add_trace(
            go.Bar(name='Avg_Spend', x=debit_avg['Category'], y=debit_avg['mean']))
        fig7.add_trace(go.Scatter(
            name='Budget', x=budget['Category'], y=budget['Budget']))
        fig7.update_layout(width=850, height=600)
        fig7.update_xaxes(showgrid=False)
        fig7.update_yaxes(showgrid=False)
        fig7.update_layout(title_text="Spend vs Budget",
                           title_x=0.5, title_font_color='red')
        st.plotly_chart(fig7, config={'displayModeBar': False})
        with st.expander("See Explanation"):
            st.write('Above chart shows Average spend vs decided budget this help '
                     'to understand  if the person was under budget or over budget')


with tab2:
    z1, z2, z3 = st.columns(3)
    with z2:
        st.markdown(
            f'<h1 style = "color: #33ff33;font-size:35px;">{"Income Analysis"}</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([6, 4])

    with col2:

        credit_data = data.groupby(['Transaction_Type'])
        credit_data = credit_data.get_group('credit')
        fig3 = px.pie(credit_data, names='Account_Name',
                      values='Amount', width=600)
        fig3.update_layout(title_text="Mode of Payment",
                           title_x=0.3, title_font_color='green')
        st.plotly_chart(fig3, config={'displayModeBar': False})
        with st.expander("See Explanation"):
            st.write(
                'Above pie chart shows different mode of payments used for Income.')

    with col1:
        credit_data = data[data["Transaction_Type"] == "debit"]
        credit_avg = credit_data.groupby(["month_year"])[
            "Amount"].sum().reset_index(name='Total')
        fig8 = px.bar(data_frame=credit_avg, x='month_year', y='Total')
        fig8.update_xaxes(showgrid=False)
        fig8.update_yaxes(showgrid=False)
        fig8.update_layout(title_text="Total Income",
                           title_x=0.5, title_font_color='green')
        st.plotly_chart(fig8, config={'displayModeBar': False})
        with st.expander("See Explanation"):
            st.write(
                'Above bar chart shows total Income for different months over a period of time.')

    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
        mon_data = data.groupby(['month_year', 'Transaction_Type'])[
            'Amount'].sum().reset_index(name='Total')
        fig4 = px.bar(mon_data, x='month_year', y='Total',
                      color='Transaction_Type', barmode='group', width=900, height=600)

        fig4.update_xaxes(showgrid=False)
        fig4.update_yaxes(showgrid=False)
        fig4.update_layout(title_text="Income vs Expense",
                           title_x=0.5, title_font_color='green')
        st.plotly_chart(fig4, config={'displayModeBar': False})
        with st.expander("See Explanation"):
            st.write('Above chart shows expenses vs income for different months so that it is easy to compare how much '
                     'was earning and how much we spend.')
