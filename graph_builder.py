'''
Reads geo_data.csv, builds a networkx graph, and saves it as G.graphml 
for use with netvis.py.
'''
import pandas as pd
import networkx as nx
import numpy as np

def build_and_save_graph(csv_file='geo_data.csv', graph_file='G.graphml'):
    """
    Reads geocoded data, creates nodes with coordinates and types, 
    and adds edges to connect locations of the same 'type'.
    """
    # 1. Read data and filter for valid locations
    df = pd.read_csv(csv_file)
    
    # Ensure NA values are treated as NaN for coordinate columns
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    
    # Filter out locations where geocoding failed (those with NaN coordinates)
    valid_locations = df.dropna(subset=['latitude', 'longitude']).copy()
    
    G = nx.Graph()
    
    # 2. Add Nodes
    for _, row in valid_locations.iterrows():
        # Nodes are given coordinates and type attributes for the visualization
        G.add_node(row['location'], 
                   latitude=row['latitude'], 
                   longitude=row['longitude'], 
                   type=row['type'],
                   title=f"{row['location']} ({row['type']})",
                   size=15) 
    
    # 3. Add Edges (Connection Logic: connect locations that share the same type)
    location_types = valid_locations.groupby('type')['location'].apply(list)
    
    for loc_type, locations in location_types.items():
        if len(locations) > 1:
            # Connect all locations of the same type (e.g., all "museum" nodes)
            for i in range(len(locations)):
                for j in range(i + 1, len(locations)):
                    G.add_edge(locations[i], locations[j], type=loc_type, weight=2) 

    # Fallback: If no shared types exist, connect the first two nodes arbitrarily
    if G.number_of_nodes() > 1 and G.number_of_edges() == 0:
        nodes = list(G.nodes)
        G.add_edge(nodes[0], nodes[1], weight=1, type='arbitrary_connection')
        
    # 4. Save the graph for netvis.py
    nx.write_graphml(G, graph_file)
    print(f"Successfully saved graph to {graph_file}")

if __name__ == "__main__":
    build_and_save_graph()