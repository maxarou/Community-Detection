import networkx as nx
import sys
import os

def generate_modularity_facts(input_gml, output_lp):
    G = nx.read_gml(input_gml)
    
    # M = Total weight (or number of edges)
    m = G.number_of_edges()
    if m == 0: return

    # Pre-calculate degrees
    deg = dict(G.degree())
    
    nodes = list(G.nodes())
    
    # Scale factor to avoid floating point in Clingo (optional)
    # Clingo handles integers best. We will multiply B_ij by 2m * 1000?
    # Q = (1/2m) * Sum ( A_ij - ki*kj/2m )
    # Maximizing Sum ( A_ij - ki*kj/2m ) is sufficient.
    # To keep logic integer-based:
    # Maximize: 2m * A_ij - ki * kj
    
    SCALE = 1 # Simple integer math
    
    with open(output_lp, 'w') as f:
        f.write(f"% Modularity weights B_ij for {os.path.basename(input_gml)}\n")
        
        # Output nodes
        for n in nodes:
             safe_n = str(n).lower().replace(" ", "_").replace("-", "_")
             f.write(f"node({safe_n}).\n")

        # Generate weights for ALL pairs (N^2 complexity, okay for N=34)
        for i in range(len(nodes)):
            for j in range(i, len(nodes)): # Symmetric, do for i<=j?
                # Optimization needs pairs.
                u = nodes[i]
                v = nodes[j]
                
                safe_u = str(u).lower().replace(" ", "_")
                safe_v = str(v).lower().replace(" ", "_")

                # A_ij
                has_edge = 1 if G.has_edge(u, v) or G.has_edge(v, u) else 0
                if u == v: has_edge = 0 # Self-loops usually 0 in simple graphs
                
                # B_val = 2m * A_ij - ki * kj
                # Python integers handle this arbitrarily large
                val = (2 * m * has_edge) - (deg[u] * deg[v])
                
                # Only write non-zero weights or just write all to be safe?
                # Optimization handles positive and negative.
                if val != 0:
                     f.write(f"mod_weight({safe_u}, {safe_v}, {val}).\n")
    
    print(f"Generated modularity matrix facts at {output_lp}")

if __name__ == "__main__":
    generate_modularity_facts(sys.argv[1], sys.argv[2])
