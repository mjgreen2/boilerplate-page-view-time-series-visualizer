#####################################################################
#Solution to Page View Time Series Visualizer project
#Created in Visual Studio Code
#by Michael Green
#####################################################################

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
from datetime import datetime

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.DataFrame(pd.read_csv(
                    filepath_or_buffer = "fcc-forum-pageviews.csv"),   
                    columns = ['date', 'value']
                )

# Clean the data by filtering out days when the page views were in the top 2.5% of the dataset or bottom 2.5% of the dataset.
# (less than the 2.5th percentile and more than the 97.5th percentile)

df = df[(df['value'] >= df['value'].quantile(0.025)) 
                & (df['value'] <= df['value'].quantile(0.975))]

df_clean = df.copy()

df_clean.rename(columns={"value": "views"}, inplace=True)
df_clean['date'] = pd.to_datetime(df_clean['date'])
df_clean['year'] = 0
df_clean['Months'] = 0
df_clean.reset_index(inplace=True, drop = True)

for row in range(0, df_clean['date'].size):
    df_clean.loc[row, 'year'] = df_clean.loc[row, 'date'].year
    df_clean.loc[row, 'Months'] = df_clean.loc[row, 'date'].strftime('%B')

df_clean.set_index('date', inplace = True)

def draw_line_plot():
    # Create a `draw_line_plot` function that uses Matplotlib to draw a line chart similar to "examples/Figure_1.png". The title should be "Daily freeCodeCamp Forum Page Views 5/2016-12/2019". The label on the x axis should be "Date" and the label on the y axis should be "Page Views".
    fig, ax = plt.subplots(figsize = (33, 11))
    ax.title.set_text("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    sns.lineplot( 
            data = df_clean,
            x = 'date', 
            y = 'views',
            legend = False, 
            linestyle = 'solid',
            color = 'red'
            )

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    #Create a `draw_bar_plot` function that draws a bar chart similar to "examples/Figure_2.png". It should show average daily page views for each month grouped by year. The legend should show month labels and have a title of "Months". On the chart, the label on the x axis should be "Years" and the label on the y axis should be "Average Page Views".

    df_bar = df_clean[['year', 'Months', 'views']]

    df_bar = pd.melt(df_bar, id_vars = ['year', 'Months'], 
                    value_vars = ['views'])

    df_bar = df_bar.groupby(['year', 'Months'], as_index = False).mean()

    fig, ax = plt.subplots(figsize = (11, 9))
    sns.barplot(data = df_bar,
                x = 'year', 
                y = 'value', 
                hue = 'Months', 
                hue_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], 
                palette = "tab10",
            )

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(loc = 'upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    #df_box = df.copy()
    #df_box.reset_index(inplace=True)
    #df_box['year'] = [d.year for d in df_box.date]
    #df_box['month'] = [d.strftime('%b') for d in df_box.date]

    #Create a `draw_box_plot` function that uses Searborn to draw two adjacent box plots similar to "examples/Figure_3.png". These box plots should show how the values are distributed within a given year or month and how it compares over time. The title of the first chart should be "Year-wise Box Plot (Trend)" and the title of the second chart should be "Month-wise Box Plot (Seasonality)". Make sure the month labels on bottom start at "Jan" and the x and x axis are labeled correctly.

    df_box = df_clean.copy()
    short_month = {'January':'Jan', 'February':'Feb', 'March':'Mar', 'April':'Apr', 'May':'May', 'June':'Jun', 'July':'Jul', 'August':'Aug', 'September':'Sep', 'October':'Oct', 'November':'Nov', 'December':'Dec'}
    df_box['short_month'] = df_box['Months'].map(short_month)

    fig, ax = plt.subplots(ncols=2, figsize=(30,11))
    ax[0].title.set_text("Year-wise Box Plot (Trend)")
    ax[1].title.set_text("Month-wise Box Plot (Seasonality)")

    sns.boxplot(data = df_box,  
            x = 'year', 
            y = 'views', 
            palette = 'tab10',
            ax = ax[0]
            )
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")

    sns.boxplot(data = df_box,  
            x = 'short_month', 
            y = 'views', 
            order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            ax = ax[1]
            )
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
