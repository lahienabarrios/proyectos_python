import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator
from datetime import timedelta

# Paso 1: Cargar los datos
df = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv', 
    usecols=['date', 'location', 'total_vaccinations_per_hundred'], 
    parse_dates=['date'])

countries = ['United States', 'Germany', 'United Kingdom', 'Israel', 'Argentina','Brazil']
df = df[df['location'].isin(countries)]

# Paso 2: Resumen de datos
pivot = pd.pivot_table(
    data=df,                                    # Seleccionar el dataframe
    index='date',                               # "rows" (filas) del dataframe
    columns='location',                         # Valores a mostrar como columnas
    values='total_vaccinations_per_hundred',    # Qué valores agregar
    aggfunc='mean',                             # Cómo agregar datos
    )

pivot = pivot.fillna(method='ffill')

# Paso 3: Configurar las "key" para la visualización
main_country = 'United States'
colors = {country:('grey' if country!= main_country else '#129583') for country in countries}
alphas = {country:(0.75 if country!= main_country else 1.0) for country in countries}

# Paso 4: Mostrar todos los paises
fig, ax = plt.subplots(figsize=(12,8))
fig.patch.set_facecolor('#F5F5F5')    # Cambiar el color de fondo a gris claro
ax.patch.set_facecolor('#F5F5F5')     # Change background color to a light grey

for country in countries:
    ax.plot(
        pivot.index,              # Valores x a usar
        pivot[country],           # Valores y a usar
        color=colors[country],    # Cómo colorear línea
        alpha=alphas[country]     # Qué transparencia usar para línea
    )
    ax.text(
        x = pivot.index[-1] + timedelta(days=2),    # Dónde colocar el texto en relación con el eje x
        y = pivot[country].max(),                   # Que tan alto colocar el texto
        color = colors[country],                    # Que color darle a tu texto
        s = country,                                # Qué escribir
        alpha=alphas[country]                       # Que transparencia usar
    )

# Paso 5: Configurar ejes
## A) Dar formato a lo que se muestra en los ejes y cómo se muestra
date_form = DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=1))
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45)
plt.ylim(0,100)

## B) Personalizar ejes y agregar una cuadrícula
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#3f3f3f')
ax.spines['left'].set_color('#3f3f3f')
ax.tick_params(colors='#3f3f3f')
ax.grid(alpha=0.1)

## C) Agregar un título y etiquetas de eje
plt.ylabel('Total Vacunas cada 100 Personas', fontsize=12, alpha=0.9)
plt.xlabel('Datos', fontsize=12, alpha=0.9)
plt.title('COVID-19 Vacunas a lo largo del tiempo', fontsize=18, weight='bold', alpha=0.9)

# D) Disfruta Del Gráfico!
plt.show() 
