#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from bidi.algorithm import get_display
from arabic_reshaper import reshape # Optional, usually needed for complex script
import pandas as pd

# Read data from CSV
df = pd.read_csv('timeline_data.csv')

# Get unique timelines from the data
unique_timelines = df['Timeline'].unique()

# Setup - larger figure for scrolling, enable interactive mode
fig = plt.figure(figsize=(20, 12))
ax = plt.gca()

# Enable interactive navigation (zoom and pan)
fig.canvas.toolbar_visible = True
fig.canvas.header_visible = True
fig.canvas.footer_visible = True

# 1. Helper function for Hebrew text
def make_hebrew(text):
    return get_display(text) # Reverses text for plotting

# 2. Dynamically create Y-axis positions based on unique timelines
y_positions = {}
y_labels = []
y_ticks = []


# Assign y-positions in reverse order (top to bottom)
for idx, timeline in enumerate(unique_timelines):
    y_position = len(unique_timelines) - idx
    y_positions[timeline] = y_position
    y_labels.append(make_hebrew(timeline))
    y_ticks.append(y_position)

plt.yticks(y_ticks, y_labels)

# Invert Y-axis so early timeline is at top
ax.invert_yaxis()

# Track label positions to avoid overlaps
label_positions = {timeline: [] for timeline in unique_timelines}

timeline_colors = {}

def get_timeline_color(timeline, alternate):
    if timeline not in timeline_colors:
        base_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        color = base_colors[len(timeline_colors) % len(base_colors)]
        if alternate:
            # Lighten the color for alternate entries
            color = mcolors.to_rgba(color, alpha=0.5)
        timeline_colors[timeline] = color
    return timeline_colors[timeline]

# 3. Helper to plot a reign/period
def plot_period(track_name, start_year, end_year, label, color):
    y = y_positions[track_name]
    # Plot the bar (linewidth controls thickness)
    ax.hlines(y, start_year, end_year, colors=color, linewidth=20)
    
    # Add a black square marker at the start of the timeline
    square_size = 0.15
    ax.add_patch(plt.Rectangle((start_year - square_size/2, y - square_size/2), 
                                square_size, square_size, 
                                facecolor='white', 
                                edgecolor='black', 
                                linewidth=1.5, 
                                zorder=3))
    
    # Add label in the middle of the bar with overlap detection
    mid_point = (start_year + end_year) / 2
    
    # Check for overlaps with existing labels on this timeline
    offset = 0.15
    for prev_start, prev_end, prev_offset in label_positions[track_name]:
        # If there's a horizontal overlap
        if not (end_year < prev_start or start_year > prev_end):
            # Alternate the offset (above or below the line)
            if prev_offset > 0:
                offset = -0.35  # Below the line
            else:
                offset = 0.35   # Above the line
    
    # Store this label's position for future overlap checks
    label_positions[track_name].append((start_year, end_year, offset))
    
    # Place the label
    va = 'bottom' if offset > 0 else 'top'
    ax.text(mid_point, y + offset, make_hebrew(label), ha='center', va=va, fontsize=9)

# Read and plot data from CSV
for i, row in df.iterrows():
    name = row['Name']
    start = row['From']
    end = row['To']
    timeline = row['Timeline']
    alternate = i % 2 == 0
    # Get color for this timeline
    color = get_timeline_color(timeline, alternate)
    
    # Plot the period
    plot_period(timeline, start, end, name, color)

# Formatting the Timeline
plt.grid(True, axis='x', linestyle='--', alpha=0.7)
plt.xlabel(make_hebrew("שנה"))

# Set X-axis limits dynamically based on data
x_min = df['From'].min() - 20
x_max = df['To'].max() + 20
plt.xlim(x_min, x_max)

plt.tight_layout()

# Show plot and keep window open
plt.show(block=True)