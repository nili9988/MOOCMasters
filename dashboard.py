# Import Libraries
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px



#Data Access
def load_data_rolls():
    #Load Rolls Data
    dir_name = r'analytics data'
    rolls_file = dir_name + r'\student_profile_info_2021-05-24-1832.csv'
    rolls = pd.read_csv(rolls_file)
    return rolls

#Data Update and Write
def update_data_rolls(rolls):
    #Update Rolls Data
    dir_name = r'analytics data\Processed_Data'
    file_name = dir_name + r'\Cohort_File.csv'
    cohort_data = pd.read_csv(file_name)
    downloadWeek = date.today()
    rolls['Download_Week'] = downloadWeek
    cohort_data_new = pd.merge(rolls, cohort_data, how = 'outer')
    cohort_data_new.drop_duplicates(subset = ['email','enrollment_mode'], inplace=True, keep='last')
    cohort_data_new.to_csv(file_name)
    return cohort_data_new


rolls = load_data_rolls()
cohort_data = pd.DataFrame(update_data_rolls(rolls))

x_data = cohort_data.Download_Week.unique()
y_data = cohort_data.groupby(['Download_Week','enrollment_mode'])['enrollment_mode'].count()

#print(x_data,y_data)

# fig = px.bar(y_data,x = "Download_Week",y="count")
# fig.show()
# ax = cohort_data.groupby(['Download_Week','enrollment_mode'])['enrollment_mode'].count().plot(kind = 'bar')
# plt.show()
# plt.title("Enrollment Status")

#Creating dash platform
app = dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Welcome to MOOC Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dcc.Graph(
        id = 'Enrollment Over Time',
        figure={
            'data':[
                {'x':[x_data[0],x_data[1]],'y':[y_data[0],y_data[2]],'type':'bar','name':'Audit'},
                {'x':[x_data[0],x_data[1]],'y':[y_data[1],y_data[3]],'type':'bar','name':'Verified'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app.server.run(port=8000, host='127.0.0.1')








