import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# Read the data
df = pd.read_csv('data/max-tokens-by-model.csv')

# Convert launch_date to datetime
df['launch_date'] = pd.to_datetime(df['launch_date'])

# Format y-axis with K notation
def format_func(value, _):
    if value >= 1000:
        return f'{int(value/1000)}K'
    return str(int(value))

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

# First subplot - Scatter plot
companies = df['company'].unique()
colors = {'OpenAI': '#00A67E', 'Anthropic': '#7B61FF', 'Google': '#4285F4', 
          'Cohere': '#FF6B6B', 'Deep Seek': '#FFA500'}
markers = {'OpenAI': 'o', 'Anthropic': 's', 'Google': '^', 
          'Cohere': 'D', 'Deep Seek': 'P'}

for company in companies:
    company_data = df[df['company'] == company]
    ax1.scatter(company_data['launch_date'], company_data['max_output_tokens'],
               label=company, color=colors[company], marker=markers[company], s=100)

# Second subplot - Line plot
for company in companies:
    company_data = df[df['company'] == company]
    sorted_data = company_data.sort_values('launch_date')
    ax2.plot(sorted_data['launch_date'], sorted_data['max_output_tokens'],
            label=company, color=colors[company], marker=markers[company], markersize=8)

# Add watermark to both plots
for ax in [ax1, ax2]:
    ax.text(0.02, 0.98, 'Analysis: Daniel Rosehill, Feb 8, 2025\nFrom: Public Data',
            transform=ax.transAxes, fontsize=8, alpha=0.5,
            verticalalignment='top')
    
    # Customize each plot
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax.set_ylim(0, 105000)
    ax.set_yticks([0, 25000, 50000, 75000, 100000])
    ax.set_ylabel('Maximum Output Tokens')

# Format x-axis dates
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.setp(ax2.get_xticklabels(), rotation=45)

# Add legends
ax1.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')

# Label models with 32K+ tokens on both plots
for _, row in df[df['max_output_tokens'] >= 32000].iterrows():
    ax1.annotate(row['model_name'],
                (row['launch_date'], row['max_output_tokens']),
                xytext=(10, 10), textcoords='offset points',
                fontsize=8, alpha=0.7)
    ax2.annotate(row['model_name'],
                (row['launch_date'], row['max_output_tokens']),
                xytext=(10, 10), textcoords='offset points',
                fontsize=8, alpha=0.7)

# Set titles for each subplot
ax1.set_title('LLM Maximum Output Tokens by Launch Date (Scatter)')
ax2.set_title('LLM Maximum Output Tokens by Launch Date (Connected)')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot
plt.savefig('plots/max_tokens_plot.png', dpi=300, bbox_inches='tight')
