from sdbpa_core import SDBPA

def debug_neighborhoods():
    sdbpa = SDBPA()
    
    prompts = [
        "Act as a doctor. ",
        "You are a skilled doctor. ",
        "Play the role of a physician. ",
        "Provide answers as a medical professional. "
    ]
    
    neighborhoods = {}
    
    print("\n--- Generating Neighborhoods (N=30, Temp=0.9) ---")
    
    for p in prompts:
        print(f"\nPrompt: '{p}'")
        # Generating
        vars = sdbpa.generate_variations(p.strip(), n=30, temperature=0.9)
        # Filtering
        filtered = sdbpa.filter_variations(p.strip(), vars, threshold=0.50)
        
        final_set = set([p.strip()] + filtered)
        neighborhoods[p] = final_set
        
        print(f"  Generated: {len(vars)}")
        print(f"  Kept: {len(filtered)}")
        print(f"  Final Size: {len(final_set)}")
        print(f"  Samples: {list(final_set)[:5]}...")

    print("\n--- Overlap Analysis ---")
    base_set = neighborhoods[prompts[0]]
    
    for p in prompts[1:]:
        comp_set = neighborhoods[p]
        intersection = base_set.intersection(comp_set)
        jaccard = len(intersection) / len(base_set.union(comp_set))
        print(f"\n'{prompts[0]}' vs '{p}'")
        print(f"  Intersection: {len(intersection)}")
        print(f"  Jaccard Index: {jaccard:.4f}")
        if len(intersection) > 0:
            print(f"  Common items: {list(intersection)[:3]}...")
        else:
            print("  [WARNING] Disjoint neighborhoods!")

if __name__ == "__main__":
    debug_neighborhoods()
