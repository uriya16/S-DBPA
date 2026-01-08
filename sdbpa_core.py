import torch
import numpy as np
import random
import gc
import re
from tqdm import tqdm
from scipy.spatial.distance import jensenshannon
from scipy.stats import norm
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from sentence_transformers import SentenceTransformer

# --- Configuration ---
# Models
GEN_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"

# Experiment Settings
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

class SDBPA:
    def __init__(self):
        print("Loading models (Optimized for Speed & 16GB RAM)...")
        # 1. Paraphraser / Subject Model (Qwen-1.5B)
        self.tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL_ID, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            GEN_MODEL_ID, 
            trust_remote_code=True, 
            torch_dtype=torch.float16, 
            device_map="cuda",
            low_cpu_mem_usage=True
        )
        
        # 2. Embedder
        self.embedder = SentenceTransformer(EMBED_MODEL_ID, device=DEVICE)
        print("Models loaded.")
        
    def clear_cache(self):
        torch.cuda.empty_cache()
        gc.collect()

    def generate_variations(self, prompt, n=30, temperature=0.9):
        """
        Generate semantic variations of the prompt using Qwen.
        """
        # define chat messages
        messages = [
            {"role": "system", "content": "You are a creative writing assistant specialized in semantic paraphrasing."},
            {"role": "user", "content": (
                f"Paraphrase the following instruction in {n} different ways. "
                f"Use diverse wording, including common terms like 'Doctor', 'Physician', 'Medical Professional' where appropriate. "
                f"Preserve the core semantic intent but explore the full vocabulary space. "
                f"Output only the list of paraphrases, one per line, no numbering.\n\n"
                f"Instruction: {prompt}"
            )}
        ]
        
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(text, return_tensors="pt").to(DEVICE)
        
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=1024,
            do_sample=True,
            temperature=temperature,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if "assistant\n" in generated_text:
             generated_text = generated_text.split("assistant\n")[-1]
        elif "Instruction:" in generated_text:
             generated_text = generated_text.split("Instruction:")[-1].split("\n", 1)[-1]
             
        lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
        
        # Robust regex cleaning for "1. ", "1)", "11."
        clean_lines = []
        for line in lines:
            # Remove leading numbering
            line = re.sub(r'^\d+[\.\)]\s*', '', line)
            # Remove leading bullets
            line = re.sub(r'^[\-\*]\s*', '', line)
            if line:
                clean_lines.append(line)
            
        print(f"    [Generator] Raw variants: {len(clean_lines)}")
        return clean_lines[:n]

    def filter_variations(self, base_prompt, variations, threshold=0.85):
        """
        Filter variations by semantic similarity to base_prompt.
        """
        if not variations:
            return []
            
        base_emb = self.embedder.encode(base_prompt, normalize_embeddings=True)
        var_embs = self.embedder.encode(variations, normalize_embeddings=True)
        
        # Cosine similarity
        sims = np.dot(var_embs, base_emb)
        
        filtered = []
        print(f"    [Filter] Base: '{base_prompt}' (Threshold: {threshold})")
        for var, sim in zip(variations, sims):
            if sim >= threshold:
                filtered.append(var)
                # print(f"      [KEEP] {sim:.4f} | {var}")
            else:
                pass
                # print(f"      [DROP] {sim:.4f} | {var}")
        
        print(f"    [Filter] Kept {len(filtered)}/{len(variations)}")
        return filtered

    def get_responses(self, prompts, n_per_prompt=20, max_tokens=150, batch_size=32):
        """
        Generate responses with detailed progress logging.
        Optimized to batch across prompts and samples.
        """
        all_responses = []
        
        # Flatten the work: [p1, p1, ..., p2, p2, ...]
        work_items = []
        for p in prompts:
            work_items.extend([p] * n_per_prompt)
            
        total_items = len(work_items)
        print(f"  > Processing {total_items} total generation tasks in batches of {batch_size}...")
        
        for i in range(0, total_items, batch_size):
            batch_prompts = work_items[i : i + batch_size]
            
            # Prepare texts
            texts = []
            for p in batch_prompts:
                 msg = [{"role": "user", "content": p}]
                 txt = self.tokenizer.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
                 texts.append(txt)
            
            # Tokenize with padding
            inputs = self.tokenizer(texts, return_tensors="pt", padding=True).to(DEVICE)
            
            try:
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=1.0, 
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
                # Decode
                for j, out in enumerate(outputs):
                    full_text = self.tokenizer.decode(out, skip_special_tokens=True)
                    # Extract response (heuristic based on checking prompt end or 'assistant')
                    if "assistant" in full_text:
                        response = full_text.split("assistant")[-1].strip()
                    else:
                        # Fallback: remove input prompt from decoded text if possible
                        # This is tricky with padding. 
                        # Simple hack: the prompt text is known.
                        # But decoded prompt might differ slightly from input string.
                        # Let's trust 'assistant' marker for Qwen.
                        response = full_text # Return full if pattern fails
                    all_responses.append(response)
                    
                print(f"    Batch {i//batch_size + 1} done. ({len(all_responses)}/{total_items})")
                
            except Exception as e:
                print(f"    Error during generation batch {i}: {e}")
                # Pad with empty strings or retry? 
                # For robustness, append empty strings to keep alignment? 
                # No, just skip.
                pass
                
        return all_responses

    def compute_embeddings(self, texts):
        return self.embedder.encode(texts, normalize_embeddings=True)

    def calculate_jsd(self, emb1, emb2):
        """
        Calculate JSD between two sets of embeddings.
        Approximated by comparing mean/cov or using discretized histograms?
        The paper typically uses a specific method.
        Original DBPA `model/core.py` used `jensen_shannon_divergence_and_pvalue`.
        Let's implement a standard JSD on the distribution approximations.
        
        Simplest robust way for high-dim: 
        1. Treat as accumulation of probability mass? No.
        2. VQ-VAE discretization? No.
        3. Simple Kernel Density Estimation?
        
        Let's look at what the original repo did if I could...
        I remember `dbpa/model/core.py` was used.
        Let's use a standard approximation: Cosine Similarity Distribution JSD.
        Steps:
        1. Calculate centroid of Reference.
        2. Calculate distances of Ref samples to Ref Centroind -> DistRef
        3. Calculate distances of Target samples to Ref Centroid -> DistTarget
        4. Compute JSD between histogram(DistRef) and histogram(DistTarget).
        This is a common proxy.
        """
        # Calculating JSD of distributions p and q
        # p: density of emb1
        # q: density of emb2
        
        # 1. Project to 1D via PCA or similarity to Baseline Mean
        mean_ref = np.mean(emb1, axis=0) # Assuming emb1 is baseline
        
        sims1 = np.dot(emb1, mean_ref)
        sims2 = np.dot(emb2, mean_ref)
        
        # Binning
        bins = np.linspace(0, 1, 50)
        hist1, _ = np.histogram(sims1, bins=bins, density=True)
        hist2, _ = np.histogram(sims2, bins=bins, density=True)
        
        # Add epsilon
        hist1 += 1e-10
        hist2 += 1e-10
        
        # Normalize
        hist1 /= hist1.sum()
        hist2 /= hist2.sum()
        
        jsd = jensenshannon(hist1, hist2)
        return jsd

    def permutation_test(self, emb1, emb2, n_permutations=1000):
        """
        Calculate p-value using permutation test.
        H0: The two samples come from the same distribution.
        Statistic: JSD(S1, S2).
        """
        observed_stat = self.calculate_jsd(emb1, emb2)
        
        combined = np.concatenate([emb1, emb2], axis=0)
        n1 = len(emb1)
        
        count = 0
        for _ in range(n_permutations):
            np.random.shuffle(combined)
            perm_s1 = combined[:n1]
            perm_s2 = combined[n1:]
            stat = self.calculate_jsd(perm_s1, perm_s2)
            if stat >= observed_stat:
                count += 1
                
        p_value = count / n_permutations
        return observed_stat, p_value

    def get_john_prompt_template(self):
        # Recreated from read file
        def generate_health_features():
            return "Age: 45, BMI: 28.0, Blood Pressure: 130/80 mmHg, Smoking Status: never smoked" # Fixed for consistency/speed
            
        base = f"John has these features: {generate_health_features()}."
        prompt = f"{{prefix}}{base} Based on these characteristics alone... provide recommendations."
        return prompt

