import base64
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime

def test_graph():
    df = pd.read_csv('euro-daily-hist_1999_2022.csv')
    df = df.iloc[:, [0, 4, 28, -2]]
    df.columns = ['Date', 'CAD', 'NZD', 'USD']

    for col in ['CAD', 'NZD', 'USD']:
        df = df[df[col] != '-']
        df[col] = pd.to_numeric(df[col])
    
    df = df[df['Date'] >= '2022-12-01'].reset_index(drop=True)
    print(df.head(3))
    print(f'\nThe date range: {df.Date.min()}/{ df.Date.max()}')

def generate_test_graph():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

def generate_history_graph(logs):
    print(logs)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot(logs)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"