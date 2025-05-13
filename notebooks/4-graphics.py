# this script creates graphics to show differences in groups being selected as the top group
# input: ../data/output/performance_ranking.csv
# columns: demo,top,top_og,selection_rate,disparate_impact_ratio,job,model,rank
# we plot the selection_rate by demo
# demo (demographics) are White, Black, Asian, Hispanic and Man and Woman. We used abbreviations. Read the dataset to understand. total 8 demos.

# the graphic is a horizontal bar chart. y-axis are the demos. x-axis is the selection_rate.
# draw the bars from 12.5%, so they go left or right based on that
# add annotation on the top left saying "worse treatment" and top right saying "better treatment"

# allow customizability to change input file, which could have 2 demos instead and have different abbreviation mappings

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the current working directory to the script directory
script_dir: str = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# toggle group
# suffix = "" # default analysis, using race and gender
suffix = "caste/" # caste

def create_selection_rate_plot(input_file=f'../data/output/{suffix}performance_ranking.csv', 
                             demo_mapping=None,
                             reference_rate=None):
    """
    Create separate horizontal bar charts showing selection rates by demographic groups for each job.
    
    Args:
        input_file (str): Path to the CSV file containing the data
        demo_mapping (dict): Optional mapping for demographic abbreviations
        reference_rate (float): Reference rate to center the bars around. If None, will be set based on analysis type.
    """
    # Read the data
    df = pd.read_csv(input_file)
    
    # Set reference rate and limits based on analysis type
    if "caste" in input_file:
        reference_rate = 0.50  # 50% for caste analysis
        xlim_min, xlim_max = 0.35, 0.65  # 35% to 65% for caste
        xticks = [0.35, 0.40, 0.50, 0.60, 0.65]  # Custom ticks for caste
    else:
        reference_rate = 0.125  # 12.5% for race/gender analysis
        xlim_min, xlim_max = 0.06, 0.20  # 6% to 20% for race/gender
        xticks = [0.08, 0.10, 0.125, 0.15, 0.17]  # Custom ticks for race/gender
    
    # Default demographic mapping if none provided
    if demo_mapping is None:
        if "caste" in input_file:
            demo_mapping = {
                'Dalit_W': 'Dalit',
                'Brahmin_W': 'Brahmin'
            }
        else:
            demo_mapping = {
                'B_W': 'Black Woman',
                'B_M': 'Black Man',
                'W_W': 'White Woman',
                'W_M': 'White Man',
                'A_W': 'Asian Woman',
                'A_M': 'Asian Man',
                'H_W': 'Hispanic Woman',
                'H_M': 'Hispanic Man'
            }
    
    # Get unique jobs
    jobs = df['job'].unique()
    
    # Create a plot for each job
    for job in jobs:
        # Create new figure for each job
        plt.figure(figsize=(10, 6))
        
        # Filter data for this job
        job_data = df[df['job'] == job]
        
        # Calculate average selection rate for each demographic
        avg_rates = job_data.groupby('demo')['selection_rate'].mean()
        
        # Sort the rates in descending order
        avg_rates = avg_rates.sort_values(ascending=True)
        
        # Set style
        sns.set_style("whitegrid")
        
        # Create horizontal bars
        bars = plt.barh(range(len(avg_rates)), 
                       [rate - reference_rate for rate in avg_rates],
                       left=reference_rate)
        
        # Add labels and title
        plt.yticks(range(len(avg_rates)), [demo_mapping.get(demo, demo) for demo in avg_rates.index])
        plt.xlabel('Selection Rate (%)')
        plt.title(f'Selection Rate by Demographic Group - {job.title()}')
        
        # Set x-axis limits and format as percentages
        plt.xlim(xlim_min, xlim_max)
        plt.xticks(xticks)
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*100:.1f}%'))
        
        # Add reference line
        plt.axvline(x=reference_rate, color='black', linestyle='--', alpha=0.5)
        
        # Add annotations at the corners of the plot
        plt.text(xlim_min, len(avg_rates) - 0.5, 'Worse Treatment', ha='left', va='center')
        plt.text(xlim_max, len(avg_rates) - 0.5, 'Better Treatment', ha='right', va='center')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(f'../data/output/{suffix}selection_rate_by_demo_{job.lower().replace(" ", "_")}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    create_selection_rate_plot()