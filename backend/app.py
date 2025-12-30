from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import uuid
import json
import networkx as nx

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_FACTS = os.path.join(BASE_DIR, "logic", "facts")
LOGIC_RULES = os.path.join(BASE_DIR, "logic", "rules")
ENGINE_PATH = os.path.join(BASE_DIR, "engines", "clingo_engine.py")
CONVERTER_PATH = os.path.join(BASE_DIR, "converters", "graph_converter.py")

os.makedirs(DATA_RAW, exist_ok=True)
os.makedirs(DATA_FACTS, exist_ok=True)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    files = [f for f in os.listdir(DATA_RAW) if f.endswith('.gml') or f.endswith('.csv')]
    datasets = []
    for f in files:
        datasets.append({"id": f, "name": f})
    return jsonify({"datasets": datasets})

@app.route('/api/graph/<graph_id>', methods=['GET'])
def get_graph(graph_id):
    path = os.path.join(DATA_RAW, graph_id)
    if not os.path.exists(path):
        return jsonify({"error": "Graph not found"}), 404
    
    try:
        if graph_id.endswith('.gml'):
            G = nx.read_gml(path)
        elif graph_id.endswith('.csv'):
            G = nx.read_edgelist(path, delimiter=',', data=False)
        else:
            return jsonify({"error": "Unsupported format"}), 400

        elements = []
        # Mapping from node key in G to the GML 'id' property
        node_id_map = {}
        
        for n in G.nodes():
            # In Karate, n is usually the ID already. 
            # In others, 'id' might be a separate attribute.
            nid = str(G.nodes[n].get('id', n))
            node_id_map[n] = nid
            elements.append({
                "data": {
                    "id": nid, 
                    "label": str(G.nodes[n].get('label', n))
                }
            })
            
        for u, v in G.edges():
            elements.append({
                "data": {
                    "source": node_id_map.get(u, str(u)), 
                    "target": node_id_map.get(v, str(v))
                }
            })
        
        return jsonify({"elements": elements})
    except Exception as e:
        return jsonify({"error": f"Failed to parse graph: {str(e)}"}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = file.filename
    path = os.path.join(DATA_RAW, filename)
    file.save(path)
    return jsonify({"message": "File uploaded", "id": filename})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    dataset_id = data.get('graph_id')
    algorithm = data.get('algorithm', 'label_propagation')
    
    if not dataset_id:
        return jsonify({"error": "Missing graph_id"}), 400

    raw_path = os.path.join(DATA_RAW, dataset_id)
    if not os.path.exists(raw_path):
        return jsonify({"error": "Dataset not found"}), 404

    # 1. Convert to Facts
    job_id = str(uuid.uuid4())
    facts_filename = f"{dataset_id}_{job_id}.lp"
    facts_path = os.path.join(DATA_FACTS, facts_filename)
    
    try:
        # Run converter script
        cmd = ["python", CONVERTER_PATH, raw_path, facts_path]
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Conversion failed", "details": str(e)}), 500

    # 2. Select Algorithm Rules
    rules = [os.path.join(LOGIC_RULES, "schema.lp")]
    if algorithm == "label_propagation":
        rules.append(os.path.join(LOGIC_RULES, "label_propagation.lp"))
    elif algorithm == "modularity_exact":
        # We need the modularity facts for this. 
        # Check if they exist, if not assume we need to generate them?
        # For now, let's try to use the _mod.lp file if it exists, roughly.
        # But wait, the standard converter doesn't make mod facts. 
        # We have 'modularity_converter.py'.
        
        # HACK: For specific standard datasets, we might have pre-generated it.
        # Ideally, we run the mod converter here too.
        mod_converter = os.path.join(BASE_DIR, "converters", "modularity_converter.py")
        facts_mod_filename = f"{dataset_id}_{job_id}_mod.lp"
        facts_mod_path = os.path.join(DATA_FACTS, facts_mod_filename)
        
        try:
           subprocess.run(["python", mod_converter, raw_path, facts_mod_path], check=True, capture_output=True)
           rules.append(os.path.join(LOGIC_RULES, "modularity.lp"))
           facts_path = facts_mod_path # Use the mod facts instead of standard facts 
        except subprocess.CalledProcessError as e:
           return jsonify({"error": "Modularity conversion failed", "details": str(e)}), 500
    elif algorithm == "clique_percolation":
        rules.append(os.path.join(LOGIC_RULES, "clique_percolation.lp"))
    elif algorithm == "louvain_baseline":
        try:
            G = nx.read_gml(raw_path, label='id') if dataset_id.endswith('.gml') else nx.read_edgelist(raw_path, delimiter=',')
            comms = nx.community.louvain_communities(G)
            final_comms = []
            for i, comm in enumerate(comms):
                for node in comm:
                    final_comms.append({"node": str(node), "community": str(i)})
            return jsonify({
                "job_id": job_id,
                "status": "completed",
                "results": final_comms,
                "algorithm": "louvain_baseline (NX)"
            })
        except Exception as e:
            return jsonify({"error": "Louvain failed", "details": str(e)}), 500
    else:
         rules.append(os.path.join(LOGIC_RULES, "label_propagation.lp"))

    # 3. Run Clingo Engine
    try:
        cmd_clingo = ["python", ENGINE_PATH, facts_path] + rules
        result = subprocess.run(cmd_clingo, capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({"error": "Clingo failed", "details": result.stderr}), 500
        
        try:
            communities = json.loads(result.stdout)
            if communities and len(communities) > 0:
                final_comms = communities[0]
            else:
                final_comms = []
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON from engine", "output": result.stdout}), 500

        return jsonify({
            "job_id": job_id, 
            "status": "completed", 
            "results": final_comms,
            "algorithm": algorithm
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/metrics', methods=['POST'])
def get_metrics():
    data = request.json
    dataset_id = data.get('graph_id')
    communities = data.get('communities') # List of {node, community}
    
    if not dataset_id or not communities:
        return jsonify({"error": "Missing data"}), 400

    path = os.path.join(DATA_RAW, dataset_id)
    try:
        if dataset_id.endswith('.gml'):
            G = nx.read_gml(path)
        elif dataset_id.endswith('.csv'):
            G = nx.read_edgelist(path, delimiter=',')
        else:
            return jsonify({"error": "Unsupported format"}), 400
    except Exception as e:
        return jsonify({"error": f"Load failed: {str(e)}"}), 500
    
    # Calculate Modularity Q
    # Ensure graph and communities use the same node IDs (strings for safety)
    try:
        # Create a mapping of string(node) to actual node object in G
        node_map = {str(n): n for n in G.nodes()}
        
        partition = []
        comm_dict = {}
        for item in communities:
            node_str = str(item['node'])
            if node_str in node_map:
                comm_dict.setdefault(item['community'], set()).add(node_map[node_str])
        
        partition = list(comm_dict.values())
        
        # Check if partition covers all nodes
        covered_nodes = set().union(*partition)
        all_nodes = set(G.nodes())
        if covered_nodes != all_nodes:
            # Add missing nodes to a "lost" community (or ignore? Better to 0 out or handle)
            missing = all_nodes - covered_nodes
            if missing:
                partition.append(missing)

        q = nx.community.modularity(G, partition)
    except Exception as e:
        print(f"Modularity failed: {e}")
        q = 0
        
    return jsonify({
        "modularity": round(q, 4),
        "num_communities": len(partition)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
