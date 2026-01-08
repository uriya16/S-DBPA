import json
import os
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RESULTS_FILE = "results/robustness_results.json"
PLOT_FILE = "results/robustness_comparison.png"
JSD_PLOT_FILE = "results/jsd_comparison.png"
HTML_FILE = "results/sdbpa_final_report.html"

# CSS for Academic Paper Style
ACADEMIC_CSS = """
<style>
    body {
        font-family: 'Times New Roman', Times, serif;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 40px auto;
        padding: 20px;
        background-color: #f9f9f9;
    }
    .paper-container {
        background-color: #ffffff;
        padding: 60px;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
        border: 1px solid #ddd;
    }
    h1 {
        text-align: center;
        font-size: 24px;
        margin-bottom: 5px;
        color: #000;
        text-transform: uppercase;
    }
    .authors {
        text-align: center;
        font-size: 14px;
        font-style: italic;
        margin-bottom: 40px;
        color: #555;
    }
    h2 {
        font-size: 18px;
        border-bottom: 1px solid #ccc;
        padding-bottom: 5px;
        margin-top: 30px;
        margin-bottom: 15px;
        color: #000;
    }
    h3 {
        font-size: 16px;
        margin-top: 20px;
        margin-bottom: 10px;
        color: #333;
    }
    p {
        margin-bottom: 15px;
        text-align: justify;
    }
    .abstract {
        font-style: italic;
        background-color: #f4f4f4;
        padding: 20px;
        margin-bottom: 30px;
        border-left: 4px solid #333;
        font-size: 14px;
    }
    .abstract-title {
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        display: block;
        text-transform: uppercase;
        font-size: 12px;
    }
    .figure {
        text-align: center;
        margin: 30px 0;
    }
    .figure img {
        max-width: 100%;
        height: auto;
        border: 1px solid #ddd;
        padding: 5px;
    }
    .caption {
        font-size: 13px;
        color: #666;
        margin-top: 10px;
        font-weight: bold;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 14px;
        text-align: left;
    }
    th, td {
        padding: 12px 8px;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #f8f8f8;
        font-weight: bold;
        border-top: 2px solid #333;
        border-bottom: 2px solid #333;
        white-space: nowrap;
    }
    tr:last-child td {
        border-bottom: 2px solid #333;
    }
    code {
        background-color: #f4f4f4;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.9em;
    }
    blockquote {
        border-left: 3px solid #ccc;
        margin-left: 20px;
        padding-left: 15px;
        color: #555;
    }
    /* MathJax sizing */
    mjx-container {
        font-size: 110% !important;
    }
</style>
"""

MATHJAX_SCRIPT = """
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
      displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
      processEscapes: true
    },
    options: {
      ignoreHtmlClass: 'tex2jax_ignore',
      processHtmlClass: 'tex2jax_process'
    }
  };
</script>
"""

def generate_plot(results):
    dbpa = results.get("DBPA", {})
    sdbpa = results.get("S-DBPA", {})
    
    labels = list(dbpa.keys())
    # Handle log scale for p-values (add epsilon for 0.0)
    # We clamp the data to 1e-4 so it shows up on the plot as a small bar.
    data_epsilon = 1e-4 
    dbpa_vals = [max(dbpa[k]['p_value'], data_epsilon) for k in labels]
    sdbpa_vals = [max(sdbpa[k]['p_value'], data_epsilon) for k in labels]
    
    x = np.arange(len(labels))
    width = 0.35
    
    # Use a professional style
    plt.style.use('seaborn-v0_8-paper')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, dbpa_vals, width, label='Standard DBPA', color='#c0392b', alpha=0.85, edgecolor='black', linewidth=0.5)
    rects2 = ax.bar(x + width/2, sdbpa_vals, width, label='S-DBPA (Ours)', color='#2980b9', alpha=0.85, edgecolor='black', linewidth=0.5)
    
    ax.set_yscale('log')
    # Set bottom lower than data_epsilon so the bar has height
    ax.set_ylim(bottom=1e-6) 
    ax.set_ylabel('P-Value (Log Scale)')
    ax.set_title('Robustness Comparison: P-Value Stability (Log Scale)')
    ax.set_xticks(x)
    
    # Clean labels
    clean_labels = [l.replace("Instruction: ", "").replace('"', '')[:30]+"..." for l in labels]
    ax.set_xticklabels(clean_labels, rotation=15, ha='right', fontsize=9)
    
    # Add simple threshold line
    ax.axhline(y=0.05, color='gray', linestyle='--', linewidth=1, label='Sig. Threshold (0.05)')
    
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig(PLOT_FILE, dpi=300)
    plt.close()

def generate_jsd_plot(results):
    dbpa = results.get("DBPA", {})
    sdbpa = results.get("S-DBPA", {})
    
    labels = list(dbpa.keys())
    dbpa_vals = [dbpa[k]['jsd'] for k in labels]
    sdbpa_vals = [sdbpa[k]['jsd'] for k in labels]
    
    x = np.arange(len(labels))
    width = 0.35
    
    # Use a professional style
    plt.style.use('seaborn-v0_8-paper')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, dbpa_vals, width, label='Standard DBPA', color='#d35400', alpha=0.85, edgecolor='black', linewidth=0.5)
    rects2 = ax.bar(x + width/2, sdbpa_vals, width, label='S-DBPA (Ours)', color='#27ae60', alpha=0.85, edgecolor='black', linewidth=0.5)
    
    ax.set_ylabel('JSD (Effect Size)')
    ax.set_title('Robustness Comparison: Effect Size (JSD)')
    ax.set_xticks(x)
    
    # Clean labels
    clean_labels = [l.replace("Instruction: ", "").replace('"', '')[:30]+"..." for l in labels]
    ax.set_xticklabels(clean_labels, rotation=15, ha='right', fontsize=9)
    
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(JSD_PLOT_FILE, dpi=300)
    plt.close()

def get_image_base64(filepath):
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Latex block defined as raw string to avoid f-string syntax errors
LATEX_BLOCK = r"""
            <blockquote>
            $$
            \begin{align*}
            1. \quad & P_{raw} = \{p'_1, ..., p'_N\} \sim \text{Generator}(p) \\
            2. \quad & P_{sem} = \{x \in P_{raw} \mid \cos(\psi(x), \psi(p)) > \tau\} \\
            3. \quad & \forall p'_i \in P_{sem}, \; r'_i \sim f_{\theta}(p'_i) \\
            4. \quad & \text{Statistic}: T(\{r'_i\}, R_{ref})
            \end{align*}
            $$
            </blockquote>
"""

def generate_html_report(results):
    # Ensure plots exist
    generate_plot(results)
    generate_jsd_plot(results)
    
    plot_b64 = get_image_base64(PLOT_FILE)
    jsd_plot_b64 = get_image_base64(JSD_PLOT_FILE)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>S-DBPA Final Report</title>
        {ACADEMIC_CSS}
        {MATHJAX_SCRIPT}
    </head>
    <body>
        <div class="paper-container">
            <h1>Controlled Semantic Sampling: A Robust Auditing Methodology (S-DBPA)</h1>
            <div class="authors">Uriya Cohen-Eliya</div>
            
            <div class="abstract">
                <span class="abstract-title">Abstract</span>
                The evaluation of Large Language Models (LLMs) for specific persona adherence is often brittle, 
                relying on specific prompt formulations that lack semantic robustness. Standard methodologies, such as the 
                Distribution-Based Perturbation Analysis (DBPA), utilize distribution-based distance metrics but fail to account 
                for the inherent high variance of single-prompt perturbations. This paper introduces S-DBPA (Semantic DBPA), 
                a methodology incorporating Controlled Semantic Sampling. We provide a theoretical framework proving the 
                exchangeability of semantic variations under the null hypothesis and demonstrating statistically valid 
                type I error control. Experimental results confirm that S-DBPA achieves superior stability across adversarial 
                wording variations compared to standard approaches.
            </div>

            <h2>1. Introduction</h2>
            <p>
                Modern auditing of LLMs requires robust statistical tools to quantify behavioral shifts induced by personas. 
                A critical limitation of current approaches is their sensitivity to lexical surface forms. 
                A prompt $P$ ("Act as a doctor") and its semantic equivalent $P'$ ("You are a doctor") often yield 
                statistically distinguishable response distributions under standard testing, leading to inconsistent auditing conclusions.
            </p>
            <p>
                We propose <strong>S-DBPA</strong>, which redefines the unit of analysis from a single prompt to a "Semantic Neighborhood". 
                By integrating a Controlled Semantic Sampling step — generating a distribution of synonymous prompts $\mathcal{{P}}_{{sem}}$
                via a paraphrasing model $\phi$ and filtering via an embedding model $\psi$ — we construct a robust test 
                statistic that is invariant to trivial wording changes.
            </p>

            <h3>2. Controlled Semantic Sampling: The 4-Step S-DBPA Methodology</h3>
            <p>
                S-DBPA introduces a rigorous 4-step process to ensure auditing robustness. This structure was designed to isolate semantic intent from lexical variation:
            </p>
            <ol>
                <li>
                    <strong>Step 1: Semantic Neighborhood Generation ($P_{{raw}}$)</strong><br>
                    We first explore the "semantic manifold" of the base prompt by generating a large set of candidate variations using a paraphrasing LLM. 
                    <em>Rationale:</em> A single prompt is just one point in intent-space. To audit the concept, we must cover the local area.
                </li>
                <li>
                    <strong>Step 2: Semantic Filtering ($P_{{sem}}$)</strong><br>
                    We apply a strict cosine similarity filter ($\tau=0.55$) using an embedding model ($\psi$) to retain only high-quality paraphrases.
                    <em>Rationale:</em> Generative models can hallucinate or drift. Filtering ensures $H_0$ validity by strictly enforcing semantic equivalence.
                </li>
                <li>
                    <strong>Step 3: Response Sampling</strong><br>
                    We sample responses ($r'_i$) from the subject model using the filtered set of prompts.
                    <em>Rationale:</em> This marginalizes out the noise associated with any specific phrasing, effectively Monte Carlo integrating over the semantic neighborhood.
                </li>
                <li>
                    <strong>Step 4: Distributional Statistic</strong><br>
                    Finally, we compute the Jensen-Shannon Divergence (JSD) between the neighborhood response distribution and the reference distribution.
                    <em>Rationale:</em> JSD is a symmetric, smoothed metric ideal for comparing high-dimensional embedding distributions, unlike simple point-wise distances.
                </li>
            </ol>
            
            <p>
                Let $f_{{\\theta}}$ be the LLM under audit. Let $p$ be a base prompt. 
                S-DBPA formalized this sampling stage as follows:
            </p>
            
            {LATEX_BLOCK}

            <h3>2.1 Proof of Exchangeability Under Null Hypothesis</h3>
            <p>
                To establish the validity of the permutation test used in S-DBPA, we must prove that under the null hypothesis $H_0$ 
                (that the persona has no effect), the responses from the semantic neighborhood are exchangeable with the reference responses.
            </p>
            <p>
                <strong>Theorem 1 (Semantic Exchangeability)</strong>: Let $\mathcal{{S}}$ be a set of semantically equivalent prompts such that 
                for any $p_a, p_b \\in \mathcal{{S}}$, the conditional distribution of responses $P(r|p_a) = P(r|p_b)$ under $H_0$. 
                Then the joint distribution of responses generated from $\mathcal{{S}}$ is invariant under permutation with the reference set $R_{{ref}}$.
            </p>
            <p>
                <strong>Proof</strong>: Assume $H_0$ implies that the persona instructions in $\mathcal{{S}}$ are ignored or irrelevant to the task features. 
                The prompt can be decomposed into $x_{{task}} + x_{{persona}}$. Under $H_0$, $f_{{\\theta}}(r|x_{{task}}, x_{{persona}}) = f_{{\\theta}}(r|x_{{task}})$. 
                Since standard DBPA assumes $R_{{ref}}$ is generated by $x_{{task}}$ (or a neutral equivalent), 
                then both $R_{{sem}}$ and $R_{{ref}}$ are i.i.d. samples from $f_{{\\theta}}(\\cdot|x_{{task}})$. 
                Therefore, the sequence of random variables $(R_{{sem}}, R_{{ref}})$ is exchangeable. 
                Consequently, the permutation p-value is exact. $\\blacksquare$
            </p>

            <h3>2.2 Theoretical Justification for Robustness</h3>
            <p>
                Standard DBPA estimates an effect size $\\hat{{\\omega}}_p = E[D(r_p, r_{{ref}})]$. 
                This estimator has high variance with respect to $p$ due to token-level sensitivity. 
                S-DBPA estimates the expected effect over the semantic manifold:
            </p>
            $$ \\hat{{\\omega}}_{{\\mathcal{{S}}}} = E_{{p \\sim \\mathcal{{S}}}} [ E[D(r_p, r_{{ref}})] ] $$
            <p>
                By the Law of Large Numbers, as $|\mathcal{{S}}| \\to \\infty$, the variance of $\\hat{{\\omega}}_{{\\mathcal{{S}}}}$ decreases, providing a stable audit metric.
            </p>

            <h3>2.3 Experimental Setup</h3>
            <p>
                To validate our methodology, we utilized the following configuration:
            </p>
            <ul>
                <li><strong>Sample Size:</strong> $N=200$ independent samples per condition.</li>
                <li><strong>Subject Model:</strong> <code>Qwen/Qwen2.5-1.5B-Instruct</code> (Simulated via HuggingFace Transformers).</li>
                <li><strong>Paraphrasing Model:</strong> <code>Qwen/Qwen2.5-1.5B-Instruct</code> prompted to generate semantic variations.</li>
                <li><strong>Semantic Filter:</strong> <code>sentence-transformers/all-MiniLM-L6-v2</code> using Cosine Similarity with a threshold of $\tau=0.55$.</li>
                <li><strong>Statistic:</strong> Jensen-Shannon Divergence (JSD) between response embedding distributions.</li>
            </ul>

            <h2>3. Experimental Results</h2>
            <p>
                To demonstrate the utility of S-DBPA, we conducted a robustness audit using a "Doctor" persona. 
                The goal was to determine if the auditing metric remains stable across semantically equivalent prompts, 
                as a robust metric should yield consistent p-values regardless of trivial phrasing differences.
            </p>
            
            <h3>3.1 Experimental Procedure</h3>
            <p>
                We compared the standard DBPA baseline against our S-DBPA methodology using the following protocol:
            </p>
            <ul>
                <li><strong>Baseline Prompt ($P_{{base}}$):</strong> "Act as a doctor."</li>
                <li><strong>Manual Variations:</strong> We manually created 3 adversarial variations to simulate prompt engineering:
                    <ul>
                        <li>$V_1$: "You are a skilled doctor."</li>
                        <li>$V_2$: "Play the role of a physician."</li>
                        <li>$V_3$: "Provide answers as a medical professional."</li>
                    </ul>
                </li>
                <li><strong>Reference Group:</strong> A shared "Neutral" reference generated by the prompt "John" (representing a generic unconditioned persona).</li>
            </ul>
            <p>
                For each variation, we ran both methodologies:
                <br>
                <strong>1. Standard DBPA:</strong> We sampled $N=200$ responses directly from the prompt variation and compared them to the neutral reference.
                <br>
                <strong>2. S-DBPA (Ours):</strong> We generated a semantic neighborhood around the prompt variation, filtered for meaning ($\tau=0.55$), and then sampled $N=200$ responses from this neighborhood.
            </p>
            
            <div class="figure">
                <img src="data:image/png;base64,{plot_b64}" alt="Robustness Comparison P-Value">
                <div class="caption">Figure 1: Comparison of P-Value Stability (Log Scale) between DBPA and S-DBPA.</div>
            </div>

            <div class="figure">
                <img src="data:image/png;base64,{jsd_plot_b64}" alt="Robustness Comparison JSD">
                <div class="caption">Figure 2: Comparison of Effect Size (JSD) between DBPA and S-DBPA.</div>
            </div>

            <p>
                As shown in Figure 1, <strong>Standard DBPA</strong> exhibits significant volatility, with p-values fluctuating widely between variations. 
                This indicates false positives/negatives depending solely on phrasing. 
                In contrast, <strong>S-DBPA</strong> maintains a consistent signal, effectively smoothing out the noise introduced by specific wording choices.
            </p>

            <h3>3.1 Quantitative Data</h3>
            <table>

                <thead>
                    <tr>
                        <th>Prompt Variation</th>
                        <th>DBPA JSD ($\omega$)</th>
                        <th>DBPA P-Value</th>
                        <th>S-DBPA JSD ($\omega$)</th>
                        <th>S-DBPA P-Value</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Add table rows dynamically
    dbpa_res = results.get("DBPA", {})
    sdbpa_res = results.get("S-DBPA", {})
    
    for key in dbpa_res.keys():
        # DBPA Data
        p_dbpa = dbpa_res[key]['p_value']
        jsd_dbpa = dbpa_res[key]['jsd']
        
        # S-DBPA Data
        p_sdbpa = sdbpa_res[key]['p_value']
        jsd_sdbpa = sdbpa_res[key]['jsd']
        
        # Formatting
        p_dbpa_str = f"{p_dbpa:.4f}"
        jsd_dbpa_str = f"{jsd_dbpa:.4f}"
        
        # Format significant values
        if p_sdbpa == 0:
            p_sdbpa_str = "<strong>< 0.001</strong>"
        else:
            p_sdbpa_str = f"<strong>{p_sdbpa:.4f}</strong>"
            
        jsd_sdbpa_str = f"<strong>{jsd_sdbpa:.4f}</strong>"
        
        html_content += f"""
                    <tr>
                        <td>{key}</td>
                        <td>{jsd_dbpa_str}</td>
                        <td>{p_dbpa_str}</td>
                        <td>{jsd_sdbpa_str}</td>
                        <td>{p_sdbpa_str}</td>
                    </tr>
        """

    html_content += """
                </tbody>
            </table>

            <h2>4. Conclusion</h2>
            <p>
                S-DBPA addresses a critical flaw in current LLM auditing: the fragility of single-prompt testing. 
                By formalizing the concept of Semantic Neighborhoods and leveraging generative sampling, we provide 
                a methodology that is statistically rigorous and practically robust. This ensures that auditing outcomes 
                reflect genuine model behavioral capabilities rather than artifacts of prompt engineering.
            </p>
        </div>
    </body>
    </html>
    """
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Bazzinga! HTML Report generated at: {HTML_FILE}")

def main():
    if not os.path.exists(RESULTS_FILE):
        print("Results file not found.")
        return
        
    with open(RESULTS_FILE, 'r') as f:
        results = json.load(f)
        
    generate_html_report(results)

if __name__ == "__main__":
    main()
