import sys
import json
import numpy as np
import os

# Updated path to data
DATA_DIR = "dbpa/exps/SFLLM/4.2-Table2"

# Define models as per the original run.py
model_ids = ["HuggingFaceTB/SmolLM-135M", "Gustavosta/MagicPrompt-Stable-Diffusion", "microsoft/Phi-3-mini-4k-instruct", "openai-community/gpt2", "mistralai/Mistral-7B-Instruct-v0.2", "meta-llama/Meta-Llama-3.1-8B-Instruct", "google/gemma-2-9b-it", "gpt-35-1106-vdsT-AE", "SWNorth-gpt-4-0613-20231016"]

def count_change(model_id):
    base_name = model_id.split("/")[-1]
    
    seeds = [9, 68, 145, 5998, 66215]
    data_list = []
    
    for seed in seeds:
        filename = os.path.join(DATA_DIR, f"{base_name}_prompt_robust_{seed}.json")
        with open(filename, 'r') as f:
            data_list.append(json.load(f))
    
    p_value = []
    effect_size = []
    for data in data_list:
        p_value.append(sum([1 for value in data.values() if value["p_value"] < 0.05]) / 8)
        effect_size.extend([value["effect_size"] for value in data.values()])
        
    return p_value, effect_size

print("\n=== Reproducing Table 2 Statistics (from existing experiment data) ===")
print(f"Reading data from: {DATA_DIR}")
all_change = dict()
missing_files = []

for model_id in model_ids:
    model = model_id.split("/")[-1]
    
    # Check if files exist
    seeds = [9, 68, 145, 5998, 66215]
    ready = True
    for seed in seeds:
        filename = os.path.join(DATA_DIR, f"{model}_prompt_robust_{seed}.json")
        if not os.path.exists(filename):
            missing_files.append(filename)
            ready = False
            break
    
    if ready:
        try:
            all_change[model] = count_change(model_id)
        except Exception as e:
            print(f"Error processing {model}: {e}")
            missing_files.append(f"{model} (error: {e})")

if missing_files:
    print("\nWarning: Some files are missing or errored:")
    for f in missing_files:
        print(f"  - {f}")

print("\nRESULTS:")
print("-" * 60)
print(f"{'Model':<40} | {'P-value Rej. Rate':<20} | {'Effect Size (JSD)':<20}")
print("-" * 60)

for model_id in model_ids:
    model = model_id.split("/")[-1]
    if model in all_change:
        p_value, effect_size = all_change[model]
        p_str = f"{np.mean(p_value):.4f} +- {np.std(p_value):.4f}"
        e_str = f"{np.mean(effect_size):.4f} +- {np.std(effect_size):.4f}"
        print(f"{model:<40} | {p_str:<20} | {e_str:<20}")
    else:
        print(f"{model:<40} | {'N/A':<20} | {'N/A':<20}")
print("-" * 60)
