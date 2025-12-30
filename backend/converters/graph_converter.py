import networkx as nx
import os
import sys

def convert_graph_to_clingo(input_path, output_path):
    """
    Converts a graph file (GML, CSV, etc.) into Clingo facts.
    """
    print(f"Converting {input_path} to {output_path}...")
    
    # Load Graph
    if input_path.endswith('.gml'):
        G = nx.read_gml(input_path)
    elif input_path.endswith('.csv'):
        # Assumes Source,Target CSV
        G = nx.read_edgelist(input_path, delimiter=',', data=False, create_using=nx.DiGraph)
    else:
        raise ValueError("Unsupported format. Use .gml or .csv")

    with open(output_path, 'w') as f:
        f.write(f"% Generated from {os.path.basename(input_path)}\n")
        
        # Write Nodes
        for n in G.nodes():
            # Ensure node IDs are safe for Clingo (lowercase, no spaces if symbolic)
            # For simplicity, we assume integer identifiers or simple strings.
            # If ids are numeric, keep them. If strings, ensure lowercase.
            safe_id = str(n).lower().replace(" ", "_").replace("-", "_")
            f.write(f"node({safe_id}).\n")
            
        # Write Edges
        # Treat as undirected for community detection usually, 
        # but we produce symmetric edge facts for pure Datalog rules 
        # if the algorithm expects neighbor lookups in both directions.
        for u, v in G.edges():
            safe_u = str(u).lower().replace(" ", "_").replace("-", "_")
            safe_v = str(v).lower().replace(" ", "_").replace("-", "_")
            
            f.write(f"edge({safe_u}, {safe_v}).\n")
            f.write(f"edge({safe_v}, {safe_u}).\n") # Symmetric

    print(f"Done. Wrote {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python graph_converter.py <input_file> <output_lp_file>")
        sys.exit(1)
        
    convert_graph_to_clingo(sys.argv[1], sys.argv[2])
