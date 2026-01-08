import json
import os
import torch
import numpy as np
import hashlib
import re
from sdbpa_core import SDBPA

# --- Configuration ---
TARGET_N = 200  # Total samples to reach
# ---------------------

def get_safe_filename(text):
    hash_obj = hashlib.md5(text.encode())
    return hash_obj.hexdigest()[:10]

def load_intermediate(category, identifier):
    base_dir = "results/data_cache"
    safe_id = get_safe_filename(identifier)
    filename = f"{base_dir}/{category}_{safe_id}.json"
    
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            return data
        except Exception:
            return None
    return None

def save_intermediate(category, identifier, responses, embeddings=None):
    base_dir = "results/data_cache"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    safe_id = get_safe_filename(identifier)
    filename = f"{base_dir}/{category}_{safe_id}.json"
    
    data = {
        "identifier": identifier,
        "responses": responses,
    }
    # We generally rely on re-computing embeddings for the full set
    # but saving them doesn't hurt if we want to skip that step. 
    # For now, we will re-compute to keep logic simple when appending.
        
    with open(filename, "w") as f:
        json.dump(data, f)
    print(f"    [Checkpoint] Saved {len(responses)} samples to {filename}")

def run_experiment():
    sdbpa = SDBPA()
    
    # 1. Setup Prompts
    baseline_persona = "Act as a doctor. " 
    
    variations = [
        "You are a skilled doctor. ",
        "Play the role of a physician. ",
        "Provide answers as a medical professional. "
    ]
    
    john_template = sdbpa.get_john_prompt_template()
    neutral_prompt = john_template.format(prefix="")
    
    print(f"\n--- S-DBPA Scaling Experiment (Target N={TARGET_N}) ---")
    
    # --- PHASE 0: NEUTRAL REFERENCE ---
    print("\n[Neutral Reference]")
    # Load existing
    cached_neutral = load_intermediate("neutral", "baseline")
    neutral_responses = cached_neutral["responses"] if cached_neutral else []
    
    print(f"  Existing samples: {len(neutral_responses)}")
    
    if len(neutral_responses) < TARGET_N:
        needed = TARGET_N - len(neutral_responses)
        print(f"  Generating {needed} more samples...")
        new_responses = sdbpa.get_responses([neutral_prompt], n_per_prompt=needed)
        neutral_responses.extend(new_responses)
        save_intermediate("neutral", "baseline", neutral_responses)
    else:
        print("  Sufficient samples available. Skipping generation.")
        
    # Re-embed full set
    print("  Computing embeddings...")
    neutral_embeddings = sdbpa.compute_embeddings(neutral_responses[:TARGET_N])
    
    results = {
        "DBPA": {},
        "S-DBPA": {}
    }
    
    all_prompts = [baseline_persona] + variations
    
    # --- PHASE 1: Standard DBPA (Single Prompt) ---
    print("\n--- Running Standard DBPA (Single Prompt Stability) ---")
    for persona in all_prompts:
        print(f"p: '{persona}'")
        cached = load_intermediate("dbpa", persona)
        current_resps = cached["responses"] if cached else []
        
        print(f"  Existing: {len(current_resps)}")
        
        if len(current_resps) < TARGET_N:
            needed = TARGET_N - len(current_resps)
            print(f"  Generating {needed} more...")
            task_prompt = john_template.format(prefix=persona)
            new_resps = sdbpa.get_responses([task_prompt], n_per_prompt=needed)
            current_resps.extend(new_resps)
            save_intermediate("dbpa", persona, current_resps)
        else:
             print("  Sufficient samples.")
        
        # Analyze
        current_resps = current_resps[:TARGET_N]
        embs = sdbpa.compute_embeddings(current_resps)
        jsd, p_val = sdbpa.permutation_test(neutral_embeddings, embs)
        
        results["DBPA"][persona] = {
            "jsd": float(jsd),
            "p_value": float(p_val),
            "n": len(current_resps)
        }
        print(f"  -> JSD: {jsd:.4f}, p: {p_val:.4f}")

    # --- PHASE 2: S-DBPA (Semantic Neighborhood) ---
    print("\n--- Running S-DBPA (Semantic Robustness) ---")
    
    neighborhoods = {}
    
    # Reuse previous logic for neighborhood generation or cache it?
    # Neighborhood definition shouldn't change much, but let's regenerate or caching neighbors is better.
    # For now, regeneration is fast.
    
    for persona in all_prompts:
        print(f"Neighborhood for: '{persona}'")
        # Optimization: Generate fewer variations if we just want the prompt strings, but we need consistency.
        # Let's generate 30 variations to ensure better coverage
        vars_prefix = sdbpa.generate_variations(persona.strip(), n=30)
        filtered_vars = sdbpa.filter_variations(persona.strip(), vars_prefix, threshold=0.50)
        final_set = [persona.strip()] + filtered_vars
        
        print(f"    [Neighborhood] {final_set}")
        
        neighborhood_prompts = [john_template.format(prefix=p + " ") for p in final_set]
        neighborhoods[persona] = neighborhood_prompts
    
    # Execute S-DBPA
    for persona, prompt_set in neighborhoods.items():
        print(f"Processing S-DBPA: '{persona}' (Size: {len(prompt_set)})")
        
        cached = load_intermediate("sdbpa", persona)
        current_resps = cached["responses"] if cached else []
        
        print(f"  Existing: {len(current_resps)}")
        
        if len(current_resps) < TARGET_N:
            needed = TARGET_N - len(current_resps)
            n_variants = len(prompt_set)
            # Sample roughly equally
            # We need 'needed' total.
            # n_per_variant = needed / n_variants
            n_per_variant = max(1, int(np.ceil(needed / n_variants)))
            
            print(f"  Generating ~{needed} samples ({n_per_variant}/variant)...")
            rs = sdbpa.get_responses(prompt_set, n_per_prompt=n_per_variant)
            
            current_resps.extend(rs)
            save_intermediate("sdbpa", persona, current_resps)
        else:
            print("  Sufficient samples.")
            
        # Analyze
        current_resps = current_resps[:TARGET_N] # Clip to exact target for fairness
        embs = sdbpa.compute_embeddings(current_resps)
        jsd, p_val = sdbpa.permutation_test(neutral_embeddings, embs)
        
        results["S-DBPA"][persona] = {
            "jsd": float(jsd),
            "p_value": float(p_val),
            "n": len(current_resps)
        }
        print(f"  -> JSD: {jsd:.4f}, p: {p_val:.4f}")

    # Save Final Results
    with open("results/robustness_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print("\nExperiment Complete. Results updated.")

if __name__ == "__main__":
    run_experiment()
