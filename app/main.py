import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

df = pd.read_csv('data/world_population.csv')  # Asegúrate de que la ruta del archivo sea correcta

def millions_formatter(x, pos):
    return f'{x / 1e6}M'

def main():
    st.title("Dashboard de Población Mundial")

    # Opción para elegir el tipo de gráfico
    chart_type = st.radio("Elige el tipo de gráfico", ('Gráfico de Líneas', 'Gráfico de Áreas', 'Gráfico de Barras'))

    # Selección múltiple de países
    countries = df['Country/Territory'].unique()
    selected_countries = st.multiselect("Selecciona países", countries)

    # Seleccionar el año para el gráfico de barras
    year = '2022'  # Valor por defecto para el gráfico de barras
    if chart_type == 'Gráfico de Barras':
        year = st.selectbox("Selecciona el año", ['1970', '1980', '1990', '2000', '2010', '2015', '2020', '2022'])
        year_population_column = f'{year} Population'

    if selected_countries:
        # Filtrar DataFrame basado en países seleccionados
        filtered_df = df[df['Country/Territory'].isin(selected_countries)]

        # Preparar datos para los gráficos de líneas y áreas
        years = ['1970 Population', '1980 Population', '1990 Population', '2000 Population', 
                 '2010 Population', '2015 Population', '2020 Population', '2022 Population']
        melted_df = filtered_df.melt(id_vars=['Country/Territory'], value_vars=years,
        var_name='Year', value_name='Population')
        melted_df['Year'] = melted_df['Year'].str.split(' ').str[0] # Extraer solo el año
        if chart_type == 'Gráfico de Líneas':
            # Crear y mostrar el gráfico de líneas
            fig, ax = plt.subplots()
            sns.lineplot(x='Year', y='Population', hue='Country/Territory', data=melted_df, ax=ax)
            plt.xticks(rotation=45)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
            st.pyplot(fig)
        elif chart_type == 'Gráfico de Áreas':
            # Crear y mostrar el gráfico de áreas
            area_chart_df = melted_df.pivot(index='Year', columns='Country/Territory', values='Population')
            st.area_chart(area_chart_df)
        elif chart_type == 'Gráfico de Barras':
            # Filtrar DataFrame para el año seleccionado y mostrar el gráfico de barras
            year_df = df[df['Country/Territory'].isin(selected_countries)][['Country/Territory', year_population_column]]
            year_df = year_df.sort_values(by=year_population_column, ascending=False)
            fig, ax = plt.subplots()
            ax.bar(year_df['Country/Territory'], year_df[year_population_column])
            plt.xticks(rotation=45)
            plt.ylabel('Population')
            plt.title(f'Population in {year}')
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
            st.pyplot(fig)

if __name__ == "__main__":
    main()