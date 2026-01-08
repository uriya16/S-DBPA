import sys
print("Starting imports...")
try:
    import torch
    print(f"Torch imported: {torch.__version__}")
    if torch.cuda.is_available():
        print("CUDA available")
    else:
        print("CUDA NOT available")
    
    import transformers
    print(f"Transformers imported: {transformers.__version__}")
    
    from sentence_transformers import SentenceTransformer
    print("SentenceTransformers imported")
    
except Exception as e:
    print(f"FATAL ERROR: {e}")
print("Done.")
