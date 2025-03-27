from dash import Dash, html, dash_table, dcc
import requests
import pandas as pd
import plotly.express as px

# Incorporate data
def get_nocodb_data():
    url = "http://localhost:8000/nocodb-data/"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Десериализуем JSON
        print("Полученные данные:", data)  # Отладочный вывод
        
        # Если data — это список, берем первый элемент (если он есть)
        if isinstance(data, list):
            if len(data) > 0 and isinstance(data[0], dict):  
                records = data  # Если список уже содержит объекты, используем его напрямую
            else:
                print("Ошибка: API вернул пустой список или некорректные данные")
                return pd.DataFrame()
        elif isinstance(data, dict):
            records = data.get('records', [])  # Если API возвращает словарь, ищем 'records'
        else:
            print("Ошибка: API вернул неожиданный формат данных")
            return pd.DataFrame()
        
        return pd.DataFrame(records)  # Преобразуем в DataFrame
    else:
        print("Ошибка при получении данных:", response.status_code)
        return pd.DataFrame()
# Initialize the app
app = Dash(__name__)

# Получаем данные
df = get_nocodb_data()

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        page_size=10
    ),
    dcc.Graph(figure=px.histogram(df, x='continent', y='pop', histfunc='avg'))
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)