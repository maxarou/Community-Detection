import clingo
import json
import sys
import os

class ClingoEngine:
    def __init__(self, rules_paths):
        self.rules_paths = rules_paths

    def solve(self, facts_path=None, num_models=1):
        ctl = clingo.Control([f"{num_models}"])
        for path in self.rules_paths:
            if os.path.exists(path):
                ctl.load(path)
        if facts_path and os.path.exists(facts_path):
            ctl.load(facts_path)
            
        try:
            ctl.ground([("base", [])])
        except RuntimeError:
            return []
        
        models = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                atoms = model.symbols(shown=True)
                parsed_model = []
                for atom in atoms:
                    if atom.name == "community" and len(atom.arguments) == 2:
                        node = str(atom.arguments[0])
                        label = str(atom.arguments[1]) 
                        parsed_model.append({"node": node, "community": label})
                models.append(parsed_model)
        return models

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # print("Usage...", file=sys.stderr)
        sys.exit(1)

    facts = sys.argv[1]
    rules = sys.argv[2:]
    
    engine = ClingoEngine(rules)
    results = engine.solve(facts, num_models=1) 
    
    # Output purely JSON for the API to consume
    print(json.dumps(results))
