
# OMML XML strings for S-DBPA Report Equations

# xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"

# Equation 1: The Sampling Steps Block (Aligned)
# 1. P_raw = ...
# 2. P_sem = ...
# 3. forall p'_i ...
# 4. Statistic ...
SAMPLING_STEPS_OMML = """
<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:oMath>
    <m:eqArr>
      <m:e>
        <!-- Line 1 -->
        <m:r><m:t>1.</m:t></m:r><m:r><m:t>&#160;&#160;</m:t></m:r>
        <m:r><m:t>P</m:t></m:r><m:sSub><m:e><m:r><m:t>raw</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
        <m:r><m:t>=</m:t></m:r>
        <m:d><m:dPr><m:begChr m:val="{"/><m:endChr m:val="}"/></m:dPr><m:e>
          <m:sSup><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sup><m:r><m:t>'</m:t></m:r></m:sup></m:sSup><m:sSub><m:e><m:r><m:t>1</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
          <m:r><m:t>,...,</m:t></m:r>
          <m:sSup><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sup><m:r><m:t>'</m:t></m:r></m:sup></m:sSup><m:sSub><m:e><m:r><m:t>N</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
        </m:e></m:d>
        <m:r><m:t>~Generator(p)</m:t></m:r>
        <!-- Line 2 -->
        <m:r><m:t>&#10;2.</m:t></m:r><m:r><m:t>&#160;&#160;</m:t></m:r>
        <m:r><m:t>P</m:t></m:r><m:sSub><m:e><m:r><m:t>sem</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
        <m:r><m:t>=</m:t></m:r>
        <m:d><m:dPr><m:begChr m:val="{"/><m:endChr m:val="}"/></m:dPr><m:e>
          <m:r><m:t>x</m:t></m:r><m:r><m:t>∈</m:t></m:r><m:r><m:t>P</m:t></m:r><m:sSub><m:e><m:r><m:t>raw</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
          <m:r><m:t>|</m:t></m:r><m:r><m:t>cos(</m:t></m:r><m:r><m:t>ψ</m:t></m:r><m:r><m:t>(x),</m:t></m:r><m:r><m:t>ψ</m:t></m:r><m:r><m:t>(p))></m:t></m:r><m:r><m:t>τ</m:t></m:r>
        </m:e></m:d>
        <!-- Line 3 -->
        <m:r><m:t>&#10;3.</m:t></m:r><m:r><m:t>&#160;&#160;</m:t></m:r>
        <m:r><m:t>∀</m:t></m:r>
        <m:sSup><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sup><m:r><m:t>'</m:t></m:r></m:sup></m:sSup><m:sSub><m:e><m:r><m:t>i</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
        <m:r><m:t>∈</m:t></m:r><m:r><m:t>P</m:t></m:r><m:sSub><m:e><m:r><m:t>sem</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
        <m:r><m:t>,</m:t></m:r><m:r><m:t>&#160;</m:t></m:r>
        <m:sSup><m:e><m:r><m:t>r</m:t></m:r></m:e><m:sup><m:r><m:t>'</m:t></m:r></m:sup></m:sSup><m:sSub><m:e><m:r><m:t>i</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
        <m:r><m:t>~</m:t></m:r><m:r><m:t>f</m:t></m:r><m:sSub><m:e><m:r><m:t>θ</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub><m:r><m:t>(</m:t></m:r>
        <m:sSup><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sup><m:r><m:t>'</m:t></m:r></m:sup></m:sSup><m:sSub><m:e><m:r><m:t>i</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub><m:r><m:t>)</m:t></m:r>
        <!-- Line 4 -->
        <m:r><m:t>&#10;4.</m:t></m:r><m:r><m:t>&#160;&#160;</m:t></m:r>
        <m:r><m:t>Statistic:</m:t></m:r><m:r><m:t>T({</m:t></m:r>
        <m:sSup><m:e><m:r><m:t>r</m:t></m:r></m:e><m:sup><m:r><m:t>'</m:t></m:r></m:sup></m:sSup><m:sSub><m:e><m:r><m:t>i</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
        <m:r><m:t>},</m:t></m:r><m:r><m:t>R</m:t></m:r><m:sSub><m:e><m:r><m:t>ref</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub><m:r><m:t>)</m:t></m:r>
      </m:e>
    </m:eqArr>
  </m:oMath>
</m:oMathPara>
"""

# Theorem 1 Inline Math
# S, p_a, p_b in S, P(r|p_a) = P(r|p_b), H_0
THEOREM_1_OMML = [
    # S (mathcal S)
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>S</m:t></m:r></m:oMath>""",
    # p_a, p_b in S
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sub><m:r><m:t>a</m:t></m:r></m:sub></m:sSub><m:r><m:t>,</m:t></m:r><m:sSub><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sub><m:r><m:t>b</m:t></m:r></m:sub></m:sSub><m:r><m:t>∈</m:t></m:r><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>S</m:t></m:r></m:oMath>""",
    # P(r|p_a) = P(r|p_b)
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>P(r|</m:t></m:r><m:sSub><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sub><m:r><m:t>a</m:t></m:r></m:sub></m:sSub><m:r><m:t>)=P(r|</m:t></m:r><m:sSub><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sub><m:r><m:t>b</m:t></m:r></m:sub></m:sSub><m:r><m:t>)</m:t></m:r></m:oMath>""",
    # H_0
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>H</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub></m:oMath>""",
    # R_ref
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>R</m:t></m:r></m:e><m:sub><m:r><m:t>ref</m:t></m:r></m:sub></m:sSub></m:oMath>"""
]

# Proof Math
PROOF_OMML = [
    # H_0
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>H</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub></m:oMath>""",
    # S
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>S</m:t></m:r></m:oMath>""",
    # x_task + x_persona
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>task</m:t></m:r></m:sub></m:sSub><m:r><m:t>+</m:t></m:r><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>persona</m:t></m:r></m:sub></m:sSub></m:oMath>""",
    # f_theta condition
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>f</m:t></m:r><m:sSub><m:e><m:r><m:t>θ</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub><m:r><m:t>(r|</m:t></m:r><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>task</m:t></m:r></m:sub></m:sSub><m:r><m:t>,</m:t></m:r><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>persona</m:t></m:r></m:sub></m:sSub><m:r><m:t>)=</m:t></m:r><m:r><m:t>f</m:t></m:r><m:sSub><m:e><m:r><m:t>θ</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub><m:r><m:t>(r|</m:t></m:r><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>task</m:t></m:r></m:sub></m:sSub><m:r><m:t>)</m:t></m:r></m:oMath>""",
    # R_ref, x_task
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>R</m:t></m:r></m:e><m:sub><m:r><m:t>ref</m:t></m:r></m:sub></m:sSub></m:oMath>""",
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>task</m:t></m:r></m:sub></m:sSub></m:oMath>""",
    # R_sem, R_ref, f_theta(|x_task)
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:sSub><m:e><m:r><m:t>R</m:t></m:r></m:e><m:sub><m:r><m:t>sem</m:t></m:r></m:sub></m:sSub></m:oMath>""",
    """<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>f</m:t></m:r><m:sSub><m:e><m:r><m:t>θ</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub><m:r><m:t>(⋅|</m:t></m:r><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>task</m:t></m:r></m:sub></m:sSub><m:r><m:t>)</m:t></m:r></m:oMath>"""
]

# Robustness Formula (Centered)
# omega_S = E_{p ~ S} [ E[D(r_p, r_ref)] ]
ROBUSTNESS_OMML = """
<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:oMath>
    <m:acc>
      <m:accPr><m:chr m:val="^"/></m:accPr>
      <m:e><m:r><m:t>ω</m:t></m:r></m:e>
    </m:acc>
    <m:sSub><m:e><m:r><m:t>S</m:t></m:r></m:e><m:sub><m:phantom/></m:sub></m:sSub>
    <m:r><m:t>=</m:t></m:r>
    <m:sSub>
      <m:e><m:r><m:t>E</m:t></m:r></m:e>
      <m:sub><m:r><m:t>p~S</m:t></m:r></m:sub>
    </m:sSub>
    <m:d><m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr><m:e>
      <m:r><m:t>E</m:t></m:r>
      <m:d><m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr><m:e>
        <m:r><m:t>D(</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>r</m:t></m:r></m:e><m:sub><m:r><m:t>p</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>,</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>r</m:t></m:r></m:e><m:sub><m:r><m:t>ref</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>)</m:t></m:r>
      </m:e></m:d>
    </m:e></m:d>
  </m:oMath>
</m:oMathPara>
"""
