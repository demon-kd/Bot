import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Since the mermaid service is having connectivity issues, let's create this as a Plotly network diagram
# Create the Discord Bot Architecture diagram using Plotly

# Define node positions for a hierarchical layout
node_positions = {
    'Discord API': (0, 4),
    'discord.py Library': (0, 3.2),
    'Bot Core': (0, 2.4),
    'Music System': (-2, 1.6),
    'Command Handler': (0, 1.6),
    'Moderation System': (2, 1.6),
    'yt-dlp': (-3, 0.8),
    'FFmpeg': (-2, 0.8),
    'YouTube': (-1, 0.8),
    'Slash Commands': (-0.5, 0.8),
    'Button Events': (0.5, 0.8),
    'Profanity Filter': (1.5, 0.8),
    'Infractions DB': (2.5, 0.8),
    'Multi-Server Queue Manager': (0, 0),
    'Guild 1': (-1, -0.8),
    'Guild 2': (0, -0.8),
    'Guild N': (1, -0.8)
}

# Define edges (connections)
edges = [
    ('Discord API', 'discord.py Library'),
    ('discord.py Library', 'Bot Core'),
    ('Bot Core', 'Music System'),
    ('Bot Core', 'Command Handler'),
    ('Bot Core', 'Moderation System'),
    ('Music System', 'yt-dlp'),
    ('Music System', 'FFmpeg'),
    ('Music System', 'YouTube'),
    ('Command Handler', 'Slash Commands'),
    ('Command Handler', 'Button Events'),
    ('Moderation System', 'Profanity Filter'),
    ('Moderation System', 'Infractions DB'),
    ('Bot Core', 'Multi-Server Queue Manager'),
    ('Multi-Server Queue Manager', 'Guild 1'),
    ('Multi-Server Queue Manager', 'Guild 2'),
    ('Multi-Server Queue Manager', 'Guild N')
]

# Create edge traces
edge_x = []
edge_y = []
for edge in edges:
    x0, y0 = node_positions[edge[0]]
    x1, y1 = node_positions[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

# Create node traces
node_x = [pos[0] for pos in node_positions.values()]
node_y = [pos[1] for pos in node_positions.values()]
node_text = list(node_positions.keys())

# Define node colors based on system type
node_colors = []
for node in node_text:
    if node in ['Discord API', 'discord.py Library', 'Bot Core']:
        node_colors.append('#1FB8CD')  # Strong cyan for core components
    elif node in ['Music System', 'Command Handler', 'Moderation System']:
        node_colors.append('#DB4545')  # Bright red for main systems
    elif node in ['Multi-Server Queue Manager']:
        node_colors.append('#2E8B57')  # Sea green for queue manager
    else:
        node_colors.append('#5D878F')  # Cyan for sub-components

# Create the figure
fig = go.Figure()

# Add edges
fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=2, color='#333333'),
    hoverinfo='none',
    mode='lines',
    showlegend=False
))

# Add nodes
fig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    hoverinfo='text',
    text=node_text,
    textposition="middle center",
    textfont=dict(size=10, color='white'),
    marker=dict(
        size=30,
        color=node_colors,
        line=dict(width=2, color='#333333')
    ),
    showlegend=False
))

# Update layout
fig.update_layout(
    title='Discord Bot Architecture',
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='white',
    annotations=[
        dict(
            text="Data flows from Discord API down through the Bot Core to various systems",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.5, y=-0.1, xanchor='center', yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Save the chart
fig.write_image('discord_bot_architecture.png')
fig.write_image('discord_bot_architecture.svg', format='svg')

print("Chart saved successfully as PNG and SVG")