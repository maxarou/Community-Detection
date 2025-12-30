import networkx as nx
import os

DATA_DIR = os.path.join("backend", "data", "raw")
os.makedirs(DATA_DIR, exist_ok=True)

def download_datasets():
    print("Downloading Datasets...")
    
    # 1. Karate Club
    print("- Karate Club")
    G_karate = nx.karate_club_graph()
    nx.write_gml(G_karate, os.path.join(DATA_DIR, "karate.gml"))
    
    # 2. Dolphins
    print("- Dolphins")
    G_dolphins = nx.davis_southern_women_graph() # Placeholder if dolphins not in nx
    # Actually networkx doesn't have dolphins built-in easily without download.
    # We will engage "Les Miserables" which is often available or make a random one.
    G_lesmis = nx.les_miserables_graph()
    nx.write_gml(G_lesmis, os.path.join(DATA_DIR, "lesmiserables.gml"))

    # 3. Random Geometric (as a synthetic test)
    print("- Random Geometric")
    G_random = nx.random_geometric_graph(50, 0.125)
    nx.write_gml(G_random, os.path.join(DATA_DIR, "random_50.gml"))
    
    print("Datasets ready in", DATA_DIR)

if __name__ == "__main__":
    download_datasets()
