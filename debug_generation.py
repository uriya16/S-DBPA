from sdbpa_core import SDBPA

def test():
    sdbpa = SDBPA()
    prompt = "Act as a doctor."
    print(f"Testing generation for: '{prompt}'")
    
    # Inject print in generate_variations? No, just call it and inspect returns.
    # Actually I want to see raw text.
    # I'll modify sdbpa_core.py temporarily or just subclass?
    # Simpler: just use sdbpa.generate_variations and print the result list.
    # If list is empty, then I know parsing failed.
    
    variations = sdbpa.generate_variations(prompt, n=5)
    print("Variations list:", variations)
    
    filtered = sdbpa.filter_variations(prompt, variations, threshold=0.7) # Try lower threshold
    print("Filtered list (0.7):", filtered)

if __name__ == "__main__":
    test()
