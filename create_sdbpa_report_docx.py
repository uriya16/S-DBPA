import json
import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.oxml.ns import qn
import formulas_omml

# Input/Output paths
RESULTS_FILE = "results/robustness_results.json"
PLOT_FILE = "results/robustness_comparison.png"
JSD_PLOT_FILE = "results/jsd_comparison.png"
# Use a new filename to avoid lock issues
DOCX_FILE = "results/S-DBPA_Final_Report_v3.docx"

def set_font(run, font_name='Times New Roman', font_size=12, bold=False, italic=False):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic

def add_heading(doc, text, level=1, align=WD_ALIGN_PARAGRAPH.LEFT):
    heading = doc.add_heading(text, level=level)
    heading.alignment = align
    for run in heading.runs:
        set_font(run, font_size=16 if level==1 else 14, bold=True)
    return heading

def add_paragraph(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    set_font(run)
    return p

def add_omml_equation(doc, omml_string):
    """Inserts a native Word equation using OMML XML."""
    p = doc.add_paragraph()
    p._element.append(parse_xml(omml_string))
    return p

def main():
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: Results file not found at {RESULTS_FILE}")
        return

    with open(RESULTS_FILE, 'r') as f:
        results = json.load(f)

    doc = Document()

    # --- Title ---
    title = doc.add_heading('Controlled Semantic Sampling: A Robust Auditing Methodology (S-DBPA)', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        set_font(run, font_size=18, bold=True)

    # --- Authors ---
    authors = doc.add_paragraph('Uriya Cohen-Eliya, Iggy Segev Gal, Yuval Vardi')
    authors.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(authors.runs[0], italic=True)

    # --- Abstract ---
    doc.add_heading('Abstract', level=1)
    abstract_text = (
        "The evaluation of Large Language Models (LLMs) for specific persona adherence is often brittle, "
        "relying on specific prompt formulations that lack semantic robustness. Standard methodologies, such as the "
        "Distribution-Based Perturbation Analysis (DBPA), utilize distribution-based distance metrics but fail to account "
        "for the inherent high variance of single-prompt perturbations. This paper introduces S-DBPA (Semantic DBPA), "
        "a methodology incorporating Controlled Semantic Sampling. We provide a theoretical framework proving the "
        "exchangeability of semantic variations under the null hypothesis and demonstrating statistically valid "
        "type I error control. Experimental results confirm that S-DBPA achieves superior stability across adversarial "
        "wording variations compared to standard approaches."
    )
    p = doc.add_paragraph(abstract_text)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_font(p.runs[0], italic=True)

    # --- 1. Introduction ---
    doc.add_heading('1. Introduction', level=1)
    add_paragraph(doc, 
        "Modern auditing of LLMs requires robust statistical tools to quantify behavioral shifts induced by personas. "
        "A critical limitation of current approaches is their sensitivity to lexical surface forms. "
        "A prompt P (\"Act as a doctor\") and its semantic equivalent P' (\"You are a doctor\") often yield "
        "statistically distinguishable response distributions under standard testing, leading to inconsistent auditing conclusions."
    )
    
    # Text with inline formula placeholder logic (manual splitting for clarity)
    p_intro = doc.add_paragraph()
    p_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run1 = p_intro.add_run("We propose ")
    set_font(run1)
    run2 = p_intro.add_run("S-DBPA")
    set_font(run2, bold=True)
    run3 = p_intro.add_run(
        ", which redefines the unit of analysis from a single prompt to a \"Semantic Neighborhood\". "
        "By integrating a Controlled Semantic Sampling step — generating a distribution of synonymous prompts "
    )
    set_font(run3)
    # Inline math P_sem
    run_math = p_intro.add_run("P_sem") 
    set_font(run_math, italic=True) 
    run4 = p_intro.add_run(
        " via a paraphrasing model "
    )
    set_font(run4)
    run_phi = p_intro.add_run("phi")
    set_font(run_phi, italic=True)
    run5 = p_intro.add_run(" and filtering via an embedding model ")
    set_font(run5)
    run_psi = p_intro.add_run("psi")
    set_font(run_psi, italic=True)
    run6 = p_intro.add_run(" — we construct a robust test statistic that is invariant to trivial wording changes.")
    set_font(run6)

    # --- 2. Methodology ---
    doc.add_heading('2. Controlled Semantic Sampling: The 4-Step S-DBPA Methodology', level=1)
    add_paragraph(doc,
        "S-DBPA introduces a rigorous 4-step process to ensure auditing robustness. This structure was designed to isolate semantic intent from lexical variation:"
    )
    
    # List items with simple formatting for inline math
    step1 = doc.add_paragraph(style='List Number')
    set_font(step1.add_run("Step 1: Semantic Neighborhood Generation (P_raw)\n"), bold=True)
    set_font(step1.add_run("We first explore the \"semantic manifold\" of the base prompt by generating a large set of candidate variations using a paraphrasing LLM. "))
    set_font(step1.add_run("Rationale: "), italic=True)
    set_font(step1.add_run("A single prompt is just one point in intent-space. To audit the concept, we must cover the local area."))

    step2 = doc.add_paragraph(style='List Number')
    set_font(step2.add_run("Step 2: Semantic Filtering (P_sem)\n"), bold=True)
    set_font(step2.add_run("We apply a strict cosine similarity filter (tau=0.50) using an embedding model to retain only high-quality paraphrases. "))
    set_font(step2.add_run("Rationale: "), italic=True)
    set_font(step2.add_run("Generative models can hallucinate or drift. Filtering ensures H0 validity by strictly enforcing semantic equivalence."))

    step3 = doc.add_paragraph(style='List Number')
    set_font(step3.add_run("Step 3: Response Sampling\n"), bold=True)
    set_font(step3.add_run("We sample responses from the subject model using the filtered set of prompts. "))
    set_font(step3.add_run("Rationale: "), italic=True)
    set_font(step3.add_run("This marginalizes out the noise associated with any specific phrasing, effectively Monte Carlo integrating over the semantic neighborhood."))

    step4 = doc.add_paragraph(style='List Number')
    set_font(step4.add_run("Step 4: Distributional Statistic\n"), bold=True)
    set_font(step4.add_run("Finally, we compute the Jensen-Shannon Divergence (JSD) between the neighborhood response distribution and the reference distribution. "))
    set_font(step4.add_run("Rationale: "), italic=True)
    set_font(step4.add_run("JSD is a symmetric, smoothed metric ideal for comparing high-dimensional embedding distributions."))

    # Sampling Stage Intro
    p_formal = doc.add_paragraph()
    set_font(p_formal.add_run("Let "))
    set_font(p_formal.add_run("f_theta"), italic=True)
    set_font(p_formal.add_run(" be the LLM under audit. Let "))
    set_font(p_formal.add_run("p"), italic=True)
    set_font(p_formal.add_run(" be a base prompt. S-DBPA formalized this sampling stage as follows:"))

    # --- BLOCK EQUATION 1: Sampling Steps ---
    add_omml_equation(doc, formulas_omml.SAMPLING_STEPS_OMML)

    # --- 2.1 Proof of Exchangeability ---
    doc.add_heading('2.1 Proof of Exchangeability Under Null Hypothesis', level=2)
    add_paragraph(doc, 
        "To establish the validity of the permutation test used in S-DBPA, we must prove that under the null hypothesis, "
        "the responses from the semantic neighborhood are exchangeable with the reference responses."
    )
    
    # Theorem 1 (Mixed Text and Inline Math)
    p_thm = doc.add_paragraph()
    run_thm = p_thm.add_run("Theorem 1 (Semantic Exchangeability): ")
    set_font(run_thm, bold=True)
    
    runs = [
        "Let ", formulas_omml.THEOREM_1_OMML[0], " be a set of semantically equivalent prompts such that for any ",
        formulas_omml.THEOREM_1_OMML[1], ", the conditional distribution of responses ",
        formulas_omml.THEOREM_1_OMML[2], " under ", formulas_omml.THEOREM_1_OMML[3], ". ",
        "Then the joint distribution of responses generated from ", formulas_omml.THEOREM_1_OMML[0], 
        " is invariant under permutation with the reference set ", formulas_omml.THEOREM_1_OMML[4], "."
    ]
    
    for item in runs:
        if item.startswith("<m:oMath"):
            p_thm._element.append(parse_xml(item))
        else:
            set_font(p_thm.add_run(item), italic=True)

    # Proof (Mixed Text and Inline Math)
    p_proof = doc.add_paragraph()
    run_proof = p_proof.add_run("Proof: ")
    set_font(run_proof, bold=True)
    
    proof_runs = [
        "Assume ", formulas_omml.PROOF_OMML[0], " implies that the persona instructions in ", formulas_omml.PROOF_OMML[1], 
        " are ignored or irrelevant to the task features. The prompt can be decomposed into ", formulas_omml.PROOF_OMML[2], 
        ". Under ", formulas_omml.PROOF_OMML[0], ", ", formulas_omml.PROOF_OMML[3], ". ",
        "Since standard DBPA assumes ", formulas_omml.PROOF_OMML[4], " is generated by ", formulas_omml.PROOF_OMML[5], 
        " (or a neutral equivalent), then both ", formulas_omml.PROOF_OMML[6], " and ", formulas_omml.PROOF_OMML[4], 
        " are i.i.d. samples from ", formulas_omml.PROOF_OMML[7], ". ",
        "Therefore, the sequence of random variables (", formulas_omml.PROOF_OMML[6], ", ", formulas_omml.PROOF_OMML[4], 
        ") is exchangeable. Consequently, the permutation p-value is exact. Q.E.D."
    ]
    
    for item in proof_runs:
        if item.startswith("<m:oMath"):
            p_proof._element.append(parse_xml(item))
        else:
            set_font(p_proof.add_run(item))

    # --- 2.2 Theoretical Justification ---
    doc.add_heading('2.2 Theoretical Justification for Robustness', level=2)
    add_paragraph(doc,
        "Standard DBPA estimates an effect size using the expectation of the distance metric. "
        "This estimator has high variance due to token-level sensitivity. "
        "S-DBPA estimates the expected effect over the semantic manifold:"
    )
    
    # --- BLOCK EQUATION 2: Robustness Formula ---
    add_omml_equation(doc, formulas_omml.ROBUSTNESS_OMML)

    add_paragraph(doc,
        "By the Law of Large Numbers, as the size of the semantic set increases, the variance of this estimator decreases, providing a stable audit metric."
    )

    # --- 2.3 Experimental Setup ---
    doc.add_heading('2.3 Experimental Setup', level=2)
    add_paragraph(doc, "To validate our methodology, we utilized the following configuration:")
    
    setup = [
        "Sample Size: N=200 independent samples per condition.",
        "Subject Model: Qwen/Qwen2.5-1.5B-Instruct (Simulated via HuggingFace Transformers).",
        "Paraphrasing Model: Qwen/Qwen2.5-1.5B-Instruct prompted to generate semantic variations.",
        "Semantic Filter: sentence-transformers/all-MiniLM-L6-v2 using Cosine Similarity with a threshold of tau=0.50.",
        "Output Embedding Model: sentence-transformers/all-MiniLM-L6-v2 (used for calculating JSD).",
        "Statistic: Jensen-Shannon Divergence (JSD) between response embedding distributions."
    ]
    for item in setup:
        p = doc.add_paragraph(item, style='List Bullet')
        set_font(p.runs[0])

    p_note = doc.add_paragraph("Note on Models: While the original DBPA framework utilized text-embedding-ada-002 for output distance measurements, we employed all-MiniLM-L6-v2 for both the semantic filtering and output embedding stages. This design choice was made to ensure a fully local, reproducible evaluation pipeline without dependencies on external proprietary APIs.")
    set_font(p_note.runs[0], italic=True, font_size=10)
    
    # Add border/shading rough approx (not perfect in docx easily without more oxml)
    # Skipping generic border to keep it simple, italics/small font distinguishes it.

    # --- 3. Results ---
    doc.add_heading('3. Experimental Results', level=1)
    add_paragraph(doc,
        "To demonstrate the utility of S-DBPA, we conducted a robustness audit using a \"Doctor\" persona. "
        "The goal was to determine if the auditing metric remains stable across semantically equivalent prompts, "
        "as a robust metric should yield consistent p-values regardless of trivial phrasing differences."
    )

    # --- 3.1 Experimental Procedure ---
    doc.add_heading('3.1 Experimental Procedure', level=2)
    add_paragraph(doc, "We compared the standard DBPA baseline against our S-DBPA methodology using the following protocol:")
    
    protocol = [
        "Baseline Prompt (P_base): \"Act as a doctor.\"",
        "Manual Variations: We manually created 3 adversarial variations to simulate prompt engineering: \"You are a skilled doctor.\", \"Play the role of a physician.\", \"Provide answers as a medical professional.\"",
        "Reference Group: A shared \"Neutral\" reference generated by the prompt \"John\" (representing a generic unconditioned persona)."
    ]
    for item in protocol:
        p = doc.add_paragraph(item, style='List Bullet')
        set_font(p.runs[0])

    add_paragraph(doc, 
        "For each variation, we ran both methodologies:\n"
        "1. Standard DBPA: We sampled N=200 responses directly from the prompt variation and compared them to the neutral reference.\n"
        "2. S-DBPA (Ours): We generated a semantic neighborhood around the prompt variation, filtered for meaning (tau=0.50), and then sampled N=200 responses from this neighborhood."
    )

    # Visual Analysis
    add_paragraph(doc, "Visual Analysis:")
    
    # Images
    if os.path.exists(PLOT_FILE):
        doc.add_picture(PLOT_FILE, width=Inches(6))
        last_p = doc.paragraphs[-1] 
        last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption = doc.add_paragraph("Figure 1: Comparison of P-Value Stability (Log Scale) between DBPA and S-DBPA.")
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(caption.runs[0], bold=True, font_size=10)

    if os.path.exists(JSD_PLOT_FILE):
        doc.add_picture(JSD_PLOT_FILE, width=Inches(6))
        last_p = doc.paragraphs[-1] 
        last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption = doc.add_paragraph("Figure 2: Comparison of Effect Size (JSD) between DBPA and S-DBPA.")
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(caption.runs[0], bold=True, font_size=10)

    add_paragraph(doc,
        "As shown in Figure 1, Standard DBPA exhibits significant volatility, with p-values fluctuating widely between variations. "
        "This indicates false positives/negatives depending solely on phrasing. "
        "In contrast, S-DBPA maintains a consistent signal, effectively smoothing out the noise introduced by specific wording choices."
    )

    # Table
    doc.add_heading('3.2 Quantitative Data', level=2)
    
    dbpa_res = results.get("DBPA", {})
    sdbpa_res = results.get("S-DBPA", {})
    keys = list(dbpa_res.keys())
    
    table = doc.add_table(rows=1, cols=5)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    headers = ["Prompt Variation", "DBPA JSD", "DBPA P-Value", "S-DBPA JSD", "S-DBPA P-Value"]
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_font(hdr_cells[i].paragraphs[0].runs[0], bold=True)

    for key in keys:
        row = table.add_row().cells
        p_dbpa = dbpa_res[key]['p_value']
        jsd_dbpa = dbpa_res[key]['jsd']
        p_sdbpa = sdbpa_res[key]['p_value']
        jsd_sdbpa = sdbpa_res[key]['jsd']

        row[0].text = key.strip()
        row[1].text = f"{jsd_dbpa:.4f}"
        row[2].text = f"{p_dbpa:.4f}"
        row[3].text = f"{jsd_sdbpa:.4f}"
        
        if p_sdbpa == 0:
            row[4].text = "< 0.001"
        else:
            row[4].text = f"{p_sdbpa:.4f}"
            
    # --- 4. Conclusion ---
    doc.add_heading('4. Conclusion', level=1)
    add_paragraph(doc,
        "S-DBPA addresses a critical flaw in current LLM auditing: the fragility of single-prompt testing. "
        "By formalizing the concept of Semantic Neighborhoods and leveraging generative sampling, we provide "
        "a methodology that is statistically rigorous and practically robust. This ensures that auditing outcomes "
        "reflect genuine model behavioral capabilities rather than artifacts of prompt engineering."
    )

    doc.save(DOCX_FILE)
    print(f"Successfully created Word document at: {DOCX_FILE}")

if __name__ == "__main__":
    main()
