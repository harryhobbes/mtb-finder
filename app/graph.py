import base64
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, 
                               FormatStrFormatter, 
                               AutoMinorLocator) 
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

def generate_history_graph(logs, lowest):
    # Generate the figure **without using pyplot**.
    fig = Figure(figsize=(9,4))
    ax = fig.subplots()

    # Set title and lowest value line
    print(lowest)
    ax.axhline(lowest, linestyle='--')
    ax.set_title('Product price history')

    # Set axis formatting and labels
    ax.set_ylabel('Price') 
    # Below can set the interval between prices
    #ax.yaxis.set_major_locator(MultipleLocator(100)) 
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}')) 

    ax.set_xlabel('Date') 
    # Text in the x-axis will be displayed in 'YYYY-mm' format.
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    #ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate(rotation=25)

    # Cleanup data for plotting
    dates = []
    values = []
    for log in logs:
        dates.append(log['created'])
        values.append(float(log['deal_text']))

    ax.plot_date(dates, values, linestyle='-')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"