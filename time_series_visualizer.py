import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import and clean data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')
# Remove top 2.5% and bottom 2.5% of page views
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

# Function to draw line plot
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(df.index, df['value'], color='red')
    ax.set_title("Daily Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    plt.xticks(rotation=45)
    fig.savefig('line_plot.png')
    return fig

# Function to draw bar plot
def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    df_group = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    # Ensure months are in correct order
    months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
    df_group = df_group[months_order]

    fig = df_group.plot(kind='bar', figsize=(15,7)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")
    plt.xticks(rotation=0)
    fig.savefig('bar_plot.png')
    return fig

# Function to draw box plots
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.month

    # Month-wise mapping for labels
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, axes = plt.subplots(1, 2, figsize=(20,7))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_xticklabels(month_labels)

    fig.savefig('box_plot.png')
    return fig

# If you want to test plots locally, you can call:
# draw_line_plot()
# draw_bar_plot()
# draw_box_plot()
