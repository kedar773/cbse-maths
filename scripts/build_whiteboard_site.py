#!/usr/bin/env python3
"""
CBSE Mathematics Whiteboard Web Portal Compiler
Builds the complete interactive offline study website for CBSE Class 11 & 12 Mathematics
following the NCERT curriculum and segregating advanced/rationalized topics.
"""

import os
import re
import json
import glob
import markdown
import sys
from datetime import datetime, timezone

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"E:\maths_cbse"
OUT_DIR = r"E:\maths_cbse\maths_html_whiteboard"

CHAPTER_METADATA = {
    # Class 11
    "Class_11": [
        {
            "dir_pattern": "Sets_*",
            "slug": "01-sets",
            "title": "Sets",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["practical applications of sets", "cartesian product"],
            "key_concepts": ["Venn Diagrams", "$A \\cup B$, $A \\cap B$", "De Morgan's Laws", "Power Set $P(A) = 2^n$"]
        },
        {
            "dir_pattern": "Relations_and_Functions_20260905_1600",
            "slug": "02-relations-and-functions",
            "title": "Relations and Functions",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐",
            "yield": "Core Foundation",
            "advanced_keywords": ["binary"],
            "key_concepts": ["Cartesian Product $A \\times B$", "Domain & Range", "$f: X \\to Y$", "Function Types"]
        },
        {
            "dir_pattern": "Trigonometric_Functions_*",
            "slug": "03-trigonometric-functions",
            "title": "Trigonometric Functions",
            "domain": "Trigonometry",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["equations: principal and general"],
            "key_concepts": ["ASTC Quadrant Rule", "$\\cos(A \\pm B)$", "Double Angle $\\sin 2x$", "$\\tan(A+B)$"]
        },
        {
            "dir_pattern": "Complex_Numbers_*",
            "slug": "04-complex-numbers",
            "title": "Complex Numbers and Quadratic Equations",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["polar representation", "square root of complex"],
            "key_concepts": ["Euler Form $r e^{i\\theta}$", "Modulus $|z|$", "Conjugate $\\bar{z}$", "$i^2 = -1$"]
        },
        {
            "dir_pattern": "Linear_Inequalities_*",
            "slug": "05-linear-inequalities",
            "title": "Linear Inequalities",
            "domain": "Algebra",
            "priority": "⭐⭐⭐",
            "yield": "Core Foundation",
            "advanced_keywords": [],
            "key_concepts": ["Interval Notation $[a,b)$", "Sign Reversal on $\\times (-1)$", "Half-Plane Shading", "Strict vs Slack"]
        },
        {
            "dir_pattern": "Permutations_and_Combinations_*",
            "slug": "06-permutations-and-combinations",
            "title": "Permutations and Combinations",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["circular permutation", "derangements"],
            "key_concepts": ["$^n P_r = \\frac{n!}{(n-r)!}$", "$^n C_r = \\frac{n!}{r!(n-r)!}$", "$^n C_r = ^n C_{n-r}$", "Multiplication Rule"]
        },
        {
            "dir_pattern": "Binomial_Theorem_*",
            "slug": "07-binomial-theorem",
            "title": "Binomial Theorem",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["general and middle terms", "multinomial"],
            "key_concepts": ["General Term $T_{r+1}$", "$^n C_r a^{n-r} b^r$", "Pascal's Triangle", "Middle Terms"]
        },
        {
            "dir_pattern": "Sequences_and_Series_*",
            "slug": "08-sequences-and-series",
            "title": "Sequences and Series",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["special series", "sum to n terms of special"],
            "key_concepts": ["AP $a_n = a+(n-1)d$", "GP $a_n = ar^{n-1}$", "Sum $S_n$", "AM-GM Inequality"]
        },
        {
            "dir_pattern": "Straight_Lines_*",
            "slug": "09-straight-lines",
            "title": "Straight Lines",
            "domain": "Coordinate Geometry",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["normal form", "reduction to general form"],
            "key_concepts": ["Slope $m = \\tan\\theta$", "Point-Slope Form", "$y = mx+c$", "$m_1 m_2 = -1$"]
        },
        {
            "dir_pattern": "Conic_Sections_*",
            "slug": "10-conic-sections",
            "title": "Conic Sections",
            "domain": "Coordinate Geometry",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["degenerate conics"],
            "key_concepts": ["Parabola $y^2 = 4ax$", "Ellipse $\\frac{x^2}{a^2}+\\frac{y^2}{b^2}=1$", "Hyperbola", "Eccentricity $e$"]
        },
        {
            "dir_pattern": "Introduction_to_Three-Dimensio_*",
            "slug": "11-three-dimensional-geometry",
            "title": "Introduction to 3D Geometry",
            "domain": "Vectors & 3D",
            "priority": "⭐⭐⭐",
            "yield": "Core Foundation",
            "advanced_keywords": ["external division"],
            "key_concepts": ["Distance $\\sqrt{\\Delta x^2+\\Delta y^2+\\Delta z^2}$", "Section Formula", "Octants (8)", "Midpoint"]
        },
        {
            "dir_pattern": "Limits_and_Derivatives_*",
            "slug": "12-limits-and-derivatives",
            "title": "Limits and Derivatives",
            "domain": "Calculus",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["sandwich theorem proof", "l'hopital"],
            "key_concepts": ["$\\lim_{x\\to 0}\\frac{\\sin x}{x}=1$", "Product & Quotient Rule", "First Principle $f'(x)$", "Standard Derivatives"]
        },
        {
            "dir_pattern": "Statistics_*",
            "slug": "13-statistics",
            "title": "Statistics",
            "domain": "Statistics",
            "priority": "⭐⭐⭐⭐",
            "yield": "Core Foundation",
            "advanced_keywords": ["coefficient of variation"],
            "key_concepts": ["Mean Deviation", "Variance $\\sigma^2$", "Std Dev $\\sigma$", "Shortcut Formula"]
        },
        {
            "dir_pattern": "Probability_*",
            "slug": "14-probability",
            "title": "Probability",
            "domain": "Probability",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["axiomatic probability proofs"],
            "key_concepts": ["Sample Space $S$", "Mutually Exclusive", "Independent Events", "$P(A \\cup B)$"]
        }
    ],

    # Class 12
    "Class_12": [
        {
            "dir_pattern": "Relations_and_Functions_20260904_1209",
            "slug": "01-relations-and-functions",
            "title": "Relations and Functions",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["composition of functions", "binary operations"],
            "key_concepts": ["Equivalence Relation", "Injective (1-1)", "Surjective (Onto)", "Bijective Mapping"]
        },
        {
            "dir_pattern": "Inverse_Trigonometric_Function_*",
            "slug": "02-inverse-trigonometric-functions",
            "title": "Inverse Trigonometric Functions",
            "domain": "Trigonometry",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["graphs of inverse", "simplification of expressions"],
            "key_concepts": ["Principal Value Branch", "$\\sin^{-1}(\\sin x) = x$", "Domain & Range", "Complementary Identities"]
        },
        {
            "dir_pattern": "Matrices_*",
            "slug": "03-matrices",
            "title": "Matrices",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["elementary transformations", "row operations"],
            "key_concepts": ["Order $m \\times n$", "Matrix Mult $AB \\neq BA$", "$A = P + Q$ (Sym + Skew)", "$A^{-1} = \\frac{\\text{adj}(A)}{|A|}$"]
        },
        {
            "dir_pattern": "Determinants_*",
            "slug": "04-determinants",
            "title": "Determinants",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["properties of determinants", "triangular matrix"],
            "key_concepts": ["Expansion by Minors", "Area of Triangle", "Adjoint $\\text{adj}(A)$", "Matrix Method $AX=B$"]
        },
        {
            "dir_pattern": "Continuity_and_Differentiabili_*",
            "slug": "05-continuity-and-differentiability",
            "title": "Continuity and Differentiability",
            "domain": "Calculus",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["rolle's theorem", "mean value theorem", "lmvt"],
            "key_concepts": ["LHL = RHL = $f(c)$", "Chain Rule $\\frac{dy}{dx}$", "Logarithmic Diff", "Parametric Form"]
        },
        {
            "dir_pattern": "Application_of_Derivatives_*",
            "slug": "06-application-of-derivatives",
            "title": "Application of Derivatives",
            "domain": "Calculus",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["tangents and normals", "approximations and differentials"],
            "key_concepts": ["Rate of Change $\\frac{dy}{dx}$", "Monotonicity $f'(x) \\ge 0$", "Second Derivative Test", "Applied Optimization"]
        },
        {
            "dir_pattern": "Integrals_*",
            "slug": "07-integrals",
            "title": "Integrals",
            "domain": "Calculus",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["definite integral as the limit of a sum", "riemann sum"],
            "key_concepts": ["Substitution $\\int f(g)g'dx$", "By Parts (ILATE)", "$\\int e^x[f(x)+f'(x)]dx$", "King's Rule $\\int_0^a f(a-x)dx$"]
        },
        {
            "dir_pattern": "Application_of_Integrals_*",
            "slug": "08-application-of-integrals",
            "title": "Application of Integrals",
            "domain": "Calculus",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["area enclosed between two intersecting curves", "two parabolas"],
            "key_concepts": ["Area Under Curve $\\int y\\,dx$", "Symmetrical Curves", "Bounded Region", "Limit of Integration"]
        },
        {
            "dir_pattern": "Differential_Equations_*",
            "slug": "09-differential-equations",
            "title": "Differential Equations",
            "domain": "Calculus",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["formation of differential equations"],
            "key_concepts": ["Order & Degree", "Variable Separable", "Homogeneous ($y=vx$)", "Integrating Factor $e^{\\int P\\,dx}$"]
        },
        {
            "dir_pattern": "Vectors_*",
            "slug": "10-vectors",
            "title": "Vector Algebra",
            "domain": "Vectors & 3D",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["scalar triple product", "vector triple product", "coplanarity"],
            "key_concepts": ["Dot Product $\\vec{a}\\cdot\\vec{b}$", "Cross Product $\\vec{a}\\times\\vec{b}$", "Projection of Vector", "Unit Vector $\\hat{a}$"]
        },
        {
            "dir_pattern": "Three_Dimensional_Geometry_*",
            "slug": "11-three-dimensional-geometry",
            "title": "Three-Dimensional Geometry",
            "domain": "Vectors & 3D",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["equations of planes", "angle between planes", "coplanarity of lines"],
            "key_concepts": ["Direction Cosines $l^2+m^2+n^2=1$", "Line Equation $\\vec{r} = \\vec{a}+\\lambda\\vec{b}$", "Shortest Distance Skew Lines"]
        },
        {
            "dir_pattern": "Linear_Programming_*",
            "slug": "12-linear-programming",
            "title": "Linear Programming",
            "domain": "Algebra",
            "priority": "⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["transportation", "diet and cost minimization"],
            "key_concepts": ["Objective Function $Z$", "Feasible Region", "Corner Point Method", "Bounded vs Unbounded"]
        },
        {
            "dir_pattern": "Probability_20260904_1233",
            "slug": "13-probability",
            "title": "Probability",
            "domain": "Probability",
            "priority": "⭐⭐⭐⭐⭐",
            "yield": "High Yield 🔥",
            "advanced_keywords": ["bernoulli trials", "binomial distribution", "variance of random variable"],
            "key_concepts": ["Conditional $P(A|B)$", "Multiplication Rule", "Bayes' Theorem", "Total Probability Theorem"]
        }
    ]
}

def clean_frontmatter(content):
    """Strips YAML frontmatter and author branding banners."""
    content = re.sub(r'^---\n[\s\S]*?\n---\n', '', content)
    content = re.sub(r'>?\s*###?\s*\*\*⚡\s*Powered by.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\*\*⚡\s*Powered by.*?\*\*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'>?\s*###?\s*⚡\s*Powered by.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'⚡\s*Powered by.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'#\s*MASTER TEACHING NOTE:.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\*\*Author:\*\*.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\*\*Class (?:11|12) Mathematics \(CBSE / NCERT Alignment\)\*\*.*?\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\*\*Subtopic Module \d+:?\*\*.*?\n', '', content, flags=re.IGNORECASE)
    return content.strip()

def safe_markdown(text):
    """Renders markdown to HTML while safeguarding all LaTeX delimiters."""
    # Strip any dead local file or artifact links
    text = re.sub(r'\[([^\]]+)\]\((?:file:///|\S*?\.md\b)[^\)]*\)', r'\1', text)
    text = re.sub(r'📄\s*\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'The complete document has been saved.*?\n?', '', text, flags=re.IGNORECASE)

    math_blocks = []
    
    def save_disp(m):
        idx = len(math_blocks)
        math_blocks.append(m.group(0))
        return f"@@MDISP{idx}@@"

    def save_inl(m):
        idx = len(math_blocks)
        math_blocks.append(m.group(0))
        return f"@@MINL{idx}@@"

    # Protect display math ($$...$$ or \[...\])
    t = re.sub(r"\$\$[\s\S]*?\$\$", save_disp, text)
    t = re.sub(r"\\\[[\s\S]*?\\\]", save_disp, t)
    # Protect inline math ($...$ or \(...\))
    t = re.sub(r"(?<!\\)\$([^\$\n]+?)\$", save_inl, t)
    t = re.sub(r"\\\([\s\S]*?\\\)", save_inl, t)

    # Style Step-Marking brackets e.g. [½ Mark], [1 Mark], [Formula: ½ Mark]
    # Executed on protected text `t` so math blocks are NEVER corrupted with HTML spans!
    t = re.sub(
        r'\[(.*?(?:Mark|Marks).*?)\]',
        r'<span class="step-mark-tag">[\1]</span>',
        t
    )

    # Style Priority stars
    t = re.sub(
        r'(⭐{2,5})',
        r'<span class="star-icon">\1</span>',
        t
    )

    html = markdown.markdown(t, extensions=['tables', 'fenced_code'])

    # Restore math
    for idx, m in enumerate(math_blocks):
        # Sanitize any accidental spans inside math
        clean_m = re.sub(r'<span class="step-mark-tag">\[(.*?)\]</span>', r'[\1]', m)
        html = html.replace(f"@@MDISP{idx}@@", clean_m)
        html = html.replace(f"@@MINL{idx}@@", clean_m)

    # Clean residual branding
    html = re.sub(r'<p><strong>\s*⚡\s*Powered by.*?</strong></p>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<p>⚡\s*Powered by.*?</p>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'⚡\s*Powered by.*?😎', '', html, flags=re.IGNORECASE)

    return html

def parse_module(file_path):
    """Parses a markdown subtopic module file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    title_match = re.search(r'title:\s*["\'](.*?)["\']', raw)
    title = title_match.group(1) if title_match else os.path.basename(file_path)
    
    body = clean_frontmatter(raw)
    return {
        "title": title,
        "raw": body,
        "file": os.path.basename(file_path)
    }

def extract_sections(parsed_modules, advanced_keywords):
    """Splits chapter content into the 5 Whiteboard tabs."""
    concepts_html = []
    examples_html = []
    pyq_html = []
    traps_html = []
    advanced_html = []

    search_items = []

    for mod in parsed_modules:
        fname = mod['file'].lower()
        title = mod['title']
        raw = mod['raw']

        # Is this an Advanced/Rationalized topic?
        is_adv = any(k.lower() in title.lower() or k.lower() in fname for k in advanced_keywords)

        if "speed_hacks" in fname or "examiner_traps" in fname:
            # Traps & Speed Hacks Tab
            html = safe_markdown(raw)
            traps_html.append(f"""
              <div class="whiteboard-card trap-module-wrap">
                <div class="sticky-note red" style="margin-bottom: 1.5rem;">
                  <div class="sticky-title">⚠️ Examiner Traps &amp; Speed Hacks</div>
                  Master these critical board traps to prevent negative marks and avoidable slips.
                </div>
                {html}
              </div>
            """)
        elif "pyq" in fname or "exemplar" in fname or "application_bank" in fname:
            # PYQ & Question Bank Tab
            # Strip any dead artifact links in raw
            raw = re.sub(r'\[([^\]]+)\]\((?:file:///|\S*?\.md\b)[^\)]*\)', r'\1', raw)
            raw = re.sub(r'📄\s*\[.*?\]\(.*?\)', '', raw)
            raw = re.sub(r'The complete document has been saved.*?\n?', '', raw, flags=re.IGNORECASE)

            # Parse questions (both ### Question and #### Question)
            q_splits = re.split(r'(?=(?:###|####)\s+Question\s+)', raw)
            intro = q_splits[0]
            if intro.strip():
                pyq_html.append(f"<div class='pyq-intro' style='margin-bottom: 1rem;'>{safe_markdown(intro)}</div>")

            for q_text in q_splits[1:]:
                q_lines = q_text.strip().split('\n')
                head_line = q_lines[0]
                q_body = '\n'.join(q_lines[1:])

                # Extract year / marks tags
                year_match = re.search(r'CBSE\s*(20\d\d)', head_line)
                if year_match:
                    year = year_match.group(1)
                    badge_label = f"CBSE {year}"
                elif "case" in head_line.lower():
                    year = "Case Study"
                    badge_label = "CBSE Case Study"
                elif "exemplar" in head_line.lower():
                    year = "Exemplar"
                    badge_label = "NCERT Exemplar"
                elif "hots" in head_line.lower():
                    year = "HOTS"
                    badge_label = "CBSE HOTS"
                else:
                    year = "Board Core"
                    badge_label = "CBSE Question"

                marks_match = re.search(r'(\d+)\s*Marks?', head_line, re.IGNORECASE)
                marks = marks_match.group(1) if marks_match else "1"

                prob_match = re.search(r'⭐{3,5}', head_line)
                prob_stars = prob_match.group(0) if prob_match else "⭐⭐⭐⭐"

                prob_percent = "92%" if len(prob_stars) == 5 else ("80%" if len(prob_stars) == 4 else "65%")

                # Separate question from solution (split at FIRST occurrence of solution header)
                sol_match = re.search(r'(?:#{3,4}\s+)?(?:\*\*)?(?:Step-by-Step\s+)?(?:Model\s+Solution|CBSE\s+Marking\s+Scheme|Solution)(?:\*\*)?:?', q_body, re.IGNORECASE)
                if sol_match:
                    actual_q = q_body[:sol_match.start()]
                    actual_sol = q_body[sol_match.start():]
                else:
                    actual_q = q_body
                    actual_sol = ""

                q_card_id = f"q_{len(search_items)}"
                clean_title = re.sub(r'^#{3,4}\s*', '', head_line).strip()
                rendered_q = safe_markdown(actual_q)
                rendered_sol = safe_markdown(actual_sol)

                pyq_html.append(f"""
                  <div class="question-card" id="{q_card_id}" data-year="{year}" data-marks="{marks}">
                    <div class="question-header">
                      <div class="question-tags">
                        <span class="badge-pyq-stamp animate-stamp">{badge_label}</span>
                        <span class="badge-priority">{prob_stars} Priority</span>
                        <span class="badge-yield-high">{marks} Mark{'s' if marks != '1' else ''}</span>
                        <div class="prob-indicator-wrap">
                          <span>Exam Prob:</span>
                          <div class="prob-track"><div class="prob-fill high" data-prob="{prob_percent}"></div></div>
                        </div>
                      </div>
                    </div>
                    <div class="question-title" style="margin-bottom: 0.5rem;">{safe_markdown(clean_title)}</div>
                    <div class="question-text">{rendered_q}</div>
                    {f'''
                    <details class="solution-accordion">
                      <summary class="solution-toggle">
                        <span>📝 View CBSE Model Solution &amp; Step-Marking Scheme</span>
                        <span>▼</span>
                      </summary>
                      <div class="solution-body">
                        {rendered_sol}
                        <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px dashed #cbd5e1;">
                          <label class="step-check-label">
                            <input type="checkbox" class="step-checkbox"> I Understand This Solution Step
                          </label>
                        </div>
                      </div>
                    </details>
                    ''' if actual_sol else ''}
                  </div>
                """)

                search_items.append({
                    "type": "pyq",
                    "title": clean_title,
                    "snippet": actual_q[:140].replace('\n', ' '),
                    "targetId": q_card_id,
                    "badge": f"{badge_label} • {marks}M"
                })

        elif is_adv:
            # Advanced Studies Tab
            html = safe_markdown(raw)
            advanced_html.append(f"""
              <div class="whiteboard-card adv-module-card" style="margin-bottom: 2rem;">
                <div class="sticky-note purple" style="margin-bottom: 1.25rem;">
                  <div class="sticky-title">🚀 Advanced Extension: {title}</div>
                  <strong>CBSE Syllabus Advisory:</strong> This module covers competitive concepts, proofs, and higher lemmas (JEE Main/Advanced). Focus on this after completing the NCERT core.
                </div>
                {html}
              </div>
            """)
        else:
            # Core NCERT Concepts & Solved Examples
            # Separate examples from theory
            ex_splits = re.split(r'(?=###\s+Example\s+\d+)', raw)
            theory_part = ex_splits[0]
            examples_part = ex_splits[1:]

            if theory_part.strip():
                t_html = safe_markdown(theory_part)
                note_colors = ['yellow', 'blue', 'green', 'pink', 'purple']
                n_color = note_colors[len(concepts_html) % len(note_colors)]
                
                sticky_info = f"""
                  <div class="sticky-note {n_color}" style="margin: 1.5rem 0 2rem;">
                    <div class="sticky-title">📌 {title} — Essential Whiteboard Takeaways</div>
                    <p><span class="sticky-text-navy">📘 Core NCERT Concept:</span> Master the foundational definitions and structural conditions before solving numerical problems.</p>
                    <p><span class="sticky-text-red">⚠️ Examiner Trap Alert:</span> <span class="sticky-highlight">Do not skip identity statements or substitution lines.</span> CBSE evaluators penalize missing algebraic connections.</p>
                    <p><span class="sticky-text-green">💡 Official Step-Marking Rule:</span> Allocate full attention to writing units, signs, and explicit equations to secure all step marks (½M / 1M).</p>
                    <p><span class="sticky-text-purple">🎯 Student Practice Tip:</span> Practice reproducing the key steps on your Whiteboard Scribble Pad before consulting the model solution.</p>
                  </div>
                """
                concepts_html.append(f"""
                  <div class="whiteboard-section concept-block" style="margin-bottom: 2rem;">
                    {sticky_info}
                    {t_html}
                  </div>
                """)

            for ex_text in examples_part:
                ex_lines = ex_text.strip().split('\n')
                ex_title = ex_lines[0].replace('###', '').strip()
                ex_body = '\n'.join(ex_lines[1:])

                ex_id = f"ex_{len(search_items)}"
                rendered_ex = safe_markdown(ex_body)

                examples_html.append(f"""
                  <div class="question-card example-card" id="{ex_id}" style="border-left: 5px solid var(--marker-blue);">
                    <div class="question-header">
                      <div class="question-title" style="color: var(--marker-blue);">
                        💡 {ex_title}
                      </div>
                      <div class="question-tags">
                        <span class="badge-yield-high">Solved Example</span>
                        <span class="badge-priority">⭐⭐⭐⭐⭐ Must-Know</span>
                      </div>
                    </div>
                    <div class="question-text">
                      {rendered_ex}
                    </div>
                    <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px dashed #cbd5e1;">
                      <label class="step-check-label">
                        <input type="checkbox" class="step-checkbox"> I Mastered This Worked Example
                      </label>
                    </div>
                  </div>
                """)

                search_items.append({
                    "type": "concept",
                    "title": ex_title,
                    "snippet": ex_body[:130].replace('\n', ' '),
                    "targetId": ex_id,
                    "badge": "Solved Example"
                })

    return {
        "concepts": '\n'.join(concepts_html),
        "examples": '\n'.join(examples_html),
        "pyqs": '\n'.join(pyq_html),
        "traps": '\n'.join(traps_html),
        "advanced": '\n'.join(advanced_html),
        "search_items": search_items
    }

def get_contact_modal_html():
    """Generates the reusable contact and feedback modal for Kedar's Academy."""
    return """
  <!-- Contact Information & Feedback Modal -->
  <div id="contactModal" class="contact-modal-overlay" aria-hidden="true" role="dialog" aria-labelledby="contactModalTitle">
    <div class="contact-modal-container">
      <div class="contact-modal-header">
        <div class="contact-header-text">
          <h3 id="contactModalTitle">Instructor Contact &amp; Centers</h3>
          <p>Get in touch with Kedar Krishna for classes, doubt clearing, or engine feedback</p>
        </div>
        <button id="closeContactModal" class="contact-close-btn" aria-label="Close modal">&times;</button>
      </div>

      <div class="contact-modal-body">
        <!-- Instructor Details Card -->
        <div class="instructor-card">
          <div class="contact-avatar">
            <span>KA</span>
          </div>
          <div class="contact-details">
            <div class="instructor-name">Kedar Krishna</div>
            <div class="instructor-role">Chemistry Educator &bull; CBSE &amp; JEE Specialist</div>
            <a href="mailto:chemistrykedar@gmail.com" class="contact-email-link" title="Click to send an email">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              chemistrykedar@gmail.com
            </a>
          </div>
        </div>

        <!-- Teaching Centers -->
        <div class="centers-section">
          <div class="modal-section-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
            Teaching Centers (Bhubaneswar)
          </div>
          <div class="centers-grid">
            <div class="center-card">
              <div class="center-header">
                <span class="center-tag">Center 1</span>
                <span class="center-title">Arundhati Vihar</span>
              </div>
              <div class="center-address">
                Jagasera, near Paikarapur, Bhubaneswar, Khordha &ndash; <strong class="center-pin">752054</strong>
              </div>
            </div>
            <div class="center-card">
              <div class="center-header">
                <span class="center-tag">Center 2</span>
                <span class="center-title">Jagannath Vihar</span>
              </div>
              <div class="center-address">
                Lane-1, near Fire station, Bhubaneswar &ndash; <strong class="center-pin">751003</strong>
              </div>
            </div>
          </div>
        </div>

        <!-- Feedback / Ask Doubt Form -->
        <div class="feedback-section">
          <div class="modal-section-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            Ask a Doubt / Direct Message
          </div>
          <form id="feedbackForm" class="feedback-form">
            <div class="form-row">
              <div class="form-group">
                <label for="fbName">Your Name</label>
                <input type="text" id="fbName" class="form-input" placeholder="e.g. Student Name" required>
              </div>
              <div class="form-group">
                <label for="fbClass">Target / Standard</label>
                <select id="fbClass" class="form-input">
                  <option value="Class 12">Class 12 CBSE Board</option>
                  <option value="Class 11">Class 11 CBSE Foundation</option>
                  <option value="JEE Main / Adv">JEE Main / Advanced Aspirant</option>
                  <option value="Parent / Inquiry">Parent / General Inquiry</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="fbSubject">Topic / Question Reference</label>
              <input type="text" id="fbSubject" class="form-input" placeholder="e.g. Doubt in Calculus / Matrix Inverses" required>
            </div>

            <div class="form-group">
              <label for="fbMessage">Your Doubt / Message</label>
              <textarea id="fbMessage" class="form-input form-textarea" rows="3" placeholder="Describe your doubt, query, or feedback here..." required></textarea>
            </div>

            <button type="submit" class="feedback-submit-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
              Send Message to Kedar Krishna
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
"""

def get_google_verification_meta():
    """Reads Google verification code if provided in google_verification.txt or env var."""
    ver_file = os.path.join(OUT_DIR, "google_verification.txt")
    code = os.environ.get("GOOGLE_SITE_VERIFICATION_MATHS", os.environ.get("GOOGLE_SITE_VERIFICATION", ""))
    if not code and os.path.exists(ver_file):
        try:
            with open(ver_file, "r", encoding="utf-8") as f:
                code = f.read().strip()
        except Exception:
            code = ""
    if code:
        return f'<meta name="google-site-verification" content="{code}">'
    return '<!-- Google Search Console Verification Meta Tag: add code to google_verification.txt or place here -->'

def generate_sitemap(manifest_curriculum):
    """Generates a standard sitemap.xml for Google Search Console and crawlers."""
    base_url = "https://kedar773.github.io/cbse-maths/"
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        f'    <loc>{base_url}</loc>',
        f'    <lastmod>{now_str}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>'
    ]

    for cls_key in ["class_11", "class_12"]:
        folder = "class-11" if cls_key == "class_11" else "class-12"
        for ch in manifest_curriculum.get(cls_key, []):
            slug = ch['slug']
            ch_url = f"{base_url}{folder}/{slug}/index.html"
            xml_lines.extend([
                '  <url>',
                f'    <loc>{ch_url}</loc>',
                f'    <lastmod>{now_str}</lastmod>',
                '    <changefreq>weekly</changefreq>',
                '    <priority>0.8</priority>',
                '  </url>'
            ])

    xml_lines.append('</urlset>')
    sitemap_path = os.path.join(OUT_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines) + "\n")
    print(f"[OK] Generated Sitemap: {sitemap_path} ({len(xml_lines)-3} URLs)")

def generate_robots_txt():
    """Generates robots.txt for search engine crawlers and Googlebot."""
    content = """User-agent: *
Allow: /

Sitemap: https://kedar773.github.io/cbse-maths/sitemap.xml
"""
    robots_path = os.path.join(OUT_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Generated robots.txt: {robots_path}")

def generate_chapter_page(cls_name, ch_meta, chapter_dir, global_search_list):
    """Generates the full standalone whiteboard chapter HTML file."""
    cls_num = "11" if "11" in cls_name else "12"
    slug = ch_meta['slug']
    title = ch_meta['title']
    domain = ch_meta['domain']
    out_dir = os.path.join(OUT_DIR, f"class-{cls_num}", slug)
    os.makedirs(out_dir, exist_ok=True)

    # Collect markdown files
    md_files = sorted(glob.glob(os.path.join(chapter_dir, "*.md")))
    parsed = [parse_module(f) for f in md_files if "FULL_COMPILED" not in f]

    sections = extract_sections(parsed, ch_meta.get('advanced_keywords', []))

    # Add items to global search list
    for item in sections['search_items']:
        item['class'] = cls_num
        item['chapter'] = title
        item['url'] = f"class-{cls_num}/{slug}/index.html#{item['targetId']}"
        global_search_list.append(item)

    # Add chapter entry itself
    global_search_list.append({
        "type": "chapter",
        "class": cls_num,
        "chapter": title,
        "title": f"Chapter: {title}",
        "snippet": f"Complete NCERT Class {cls_num} {domain} module with Solved Examples, CBSE PYQs and Marking Schemes.",
        "url": f"class-{cls_num}/{slug}/index.html",
        "badge": ch_meta['priority']
    })

    has_advanced = bool(sections['advanced'].strip())

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Class {cls_num} {title} // CBSE Mathematics Whiteboard</title>
  <meta name="description" content="CBSE Class {cls_num} Mathematics chapter notes, solved examples with official CBSE marking breakdown, 2020-2025 board PYQs for {title}.">
  <meta name="keywords" content="{title}, CBSE Class {cls_num} Mathematics, NCERT Class {cls_num} Math, CBSE Board Exam PYQs, Marking Scheme, JEE Main Mathematics">
  <meta name="author" content="Kedar Krishna">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://kedar773.github.io/cbse-maths/class-{cls_num}/{slug}/index.html">

  <!-- OpenGraph / Social Sharing -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://kedar773.github.io/cbse-maths/class-{cls_num}/{slug}/index.html">
  <meta property="og:title" content="Class {cls_num} {title} // CBSE Mathematics Whiteboard">
  <meta property="og:description" content="CBSE Class {cls_num} Mathematics chapter notes, solved examples with official CBSE marking breakdown, 2020-2025 board PYQs for {title}.">
  <meta property="og:site_name" content="Kedar's Academy Mathematics Engine">
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Kalam:wght@400;700&family=Patrick+Hand&display=swap" rel="stylesheet">
  
  <!-- Stylesheets -->
  <link rel="stylesheet" href="../../assets/css/whiteboard.css">
  <link rel="stylesheet" href="../../assets/css/whiteboard-animations.css">
  <link rel="stylesheet" href="../../assets/css/chapter.css">
  <link rel="stylesheet" href="../../assets/vendor/katex/katex.min.css">
  
  <!-- KaTeX Engine -->
  <script src="../../assets/vendor/katex/katex.min.js"></script>
  <script src="../../assets/vendor/katex/contrib/auto-render.min.js"></script>
</head>
<body data-chapter-slug="class-{cls_num}-{slug}">

  <!-- Whiteboard Top Reading Progress Bar -->
  <div class="reading-progress-bar"></div>

  <!-- Sticky Whiteboard Header -->
  <header class="chapter-header">
    <div class="chapter-nav-wrap">
      <div class="chapter-nav-left">
        <a href="../../index.html" class="back-link" title="Return to Portal Hub">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
          Portal
        </a>
        <div class="chapter-meta">
          <div class="chapter-breadcrumb">
            <span>Class {cls_num}</span>
            <span>&bull;</span>
            <span class="badge-branch">{domain}</span>
            <span>&bull;</span>
            <span class="badge-priority">{ch_meta['priority']}</span>
          </div>
          <h1>{title}</h1>
        </div>
      </div>

      <div class="chapter-nav-right">
        <button class="board-tool-btn contact-modal-trigger" title="Contact Kedar Krishna / Ask Doubt">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
          Contact
        </button>
        <button class="board-tool-btn open-search-trigger" title="Quick Search (Ctrl+K)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          Search <kbd style="font-size: 0.7rem; background: #e2e8f0; padding: 0.1rem 0.3rem; border-radius: 4px;">Ctrl+K</kbd>
        </button>
        <button id="gridToggleBtn" class="board-tool-btn" title="Switch Whiteboard Grid Pattern">
          ⁝⁝ Grid: Dots
        </button>
        <button id="markCompletedBtn" class="board-tool-btn" title="Track Mastery">
          ○ Mark Complete
        </button>
      </div>
    </div>

    <!-- 5-Tab Navigation Bar -->
    <div class="chapter-tabs-bar">
      <div class="chapter-tabs">
        <button class="tab-item active" data-target="panel-concepts">
          📋 NCERT Core Notes
        </button>
        <button class="tab-item" data-target="panel-examples">
          💡 Solved Examples &amp; Step Marking
        </button>
        <button class="tab-item" data-target="panel-pyqs">
          🎯 Board Exam PYQ Vault (2020–2025)
        </button>
        <button class="tab-item" data-target="panel-traps">
          ⚠️ Examiner Traps &amp; Hacks
        </button>
        {f'''
        <button class="tab-item tab-advanced" data-target="panel-advanced">
          🚀 Advanced Studies (JEE Scope)
        </button>
        ''' if has_advanced else ''}
      </div>
    </div>
  </header>

  <!-- Floating Mobile Header Toggle Pill (Appears when Header moves up) -->
  <button id="headerTogglePill" class="header-toggle-pill" aria-label="Show Navigation &amp; Tabs">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
    <span>Menu &amp; Tabs</span>
  </button>

  <!-- Main Content Container -->
  <main class="board-container">
    <div class="whiteboard-frame">
      <div style="padding: 1.5rem 1.75rem;">

        <!-- Panels Container -->
        <div class="panels-container">
          
          <!-- TAB 1: NCERT Core Notes -->
          <div id="panel-concepts" class="view-panel active">
            <div class="sticky-note" style="margin-bottom: 2rem;">
              <div class="sticky-title">📘 NCERT Classroom Notes: {title}</div>
              Strictly aligned with current CBSE syllabus guidelines. Focus on fundamental definitions, intuitive proofs, and key identities.
            </div>
            {sections['concepts']}
          </div>

          <!-- TAB 2: Solved Examples with Step Marking -->
          <div id="panel-examples" class="view-panel">
            <div class="sticky-note green" style="margin-bottom: 2rem;">
              <div class="sticky-title">💡 High-Yield Worked Examples</div>
              Each solution explicitly breaks down where CBSE examiners award step marks (½ mark for formula, 1 mark for substitutions).
            </div>
            {sections['examples'] if sections['examples'].strip() else '<p style="text-align: center; padding: 2rem;">Core worked examples are integrated into Tab 1 and Tab 3.</p>'}
          </div>

          <!-- TAB 3: Board Exam PYQ Vault -->
          <div id="panel-pyqs" class="view-panel">
            <div class="sticky-note blue" style="margin-bottom: 1.5rem;">
              <div class="sticky-title">🎯 CBSE Board Exam Questions Vault (2020–2025)</div>
              Real examination questions categorized by official CBSE marks weightage. Practice writing out each step before checking model answers.
            </div>

            <!-- PYQ Filter Chips -->
            <div class="pyq-filter-bar">
              <div class="filter-group">
                <span class="filter-label">Filter Marks:</span>
                <button class="filter-chip active" data-filter="all">All</button>
                <button class="filter-chip" data-filter="1m">1 Mark (MCQ/AR)</button>
                <button class="filter-chip" data-filter="2m">2 Marks (VSA)</button>
                <button class="filter-chip" data-filter="3m">3 Marks (SA)</button>
                <button class="filter-chip" data-filter="4m">4 Marks (Case Study)</button>
                <button class="filter-chip" data-filter="5m">5 Marks (LA)</button>
              </div>
              <div class="filter-group">
                <span class="filter-label">Exam Year:</span>
                <button class="filter-chip" data-filter="2024">2024</button>
                <button class="filter-chip" data-filter="2023">2023</button>
                <button class="filter-chip" data-filter="2022">2022</button>
              </div>
            </div>

            {sections['pyqs']}
          </div>

          <!-- TAB 4: Examiner Traps & Speed Hacks -->
          <div id="panel-traps" class="view-panel">
            {sections['traps']}
          </div>

          <!-- TAB 5: Advanced Studies (Segregated Beyond NCERT Core) -->
          {f'''
          <div id="panel-advanced" class="view-panel">
            <div class="advanced-scope-banner">
              <div class="advanced-scope-icon">🚀</div>
              <div class="advanced-scope-text">
                <h3>Advanced Studies &amp; Competitive Extension (JEE Main &amp; Advanced)</h3>
                <p><strong>Note for CBSE Board Candidates:</strong> The topics below are rationalized from the core board exam paper or extend beyond the NCERT textbook. Preserved strictly for students preparing for JEE, Olympiads, and university entrance.</p>
              </div>
            </div>
            {sections['advanced']}
          </div>
          ''' if has_advanced else ''}

        </div>
      </div>
    </div>
  </main>

  <!-- Chapter Footer -->
  <footer class="portal-footer">
    <div class="footer-content">
      <div class="footer-brand">
        <h3>CBSE Class {cls_num} Mathematics &bull; {title}</h3>
        <p>Curated strictly per NCERT syllabus guidelines and official CBSE marking schemes</p>
      </div>

      <div class="powered-by-wrap">
        <div class="powered-by-text">
          <span>⚡</span> Powered By Kedar's Academy
        </div>
      </div>

      <button class="footer-contact-trigger contact-modal-trigger">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
        <span>Connect with Kedar Krishna / Offline Teaching Centers</span>
      </button>

      <p class="copyright-sub">&copy; 2026 Kedar's Academy. All rights reserved. Dedicated to conceptual excellence in CBSE &amp; JEE Mathematics.</p>
    </div>
  </footer>

  {get_contact_modal_html()}

  <!-- Interactive Whiteboard Scratchpad Drawer -->
  <div id="scratchpadModal">
    <div class="scratchpad-header">
      <div class="scratchpad-title">
        <span>✏️</span> Student Whiteboard Scribble Pad
      </div>
      <button id="scratchpadCloseBtn" class="scratchpad-btn" title="Close Scratchpad">&times;</button>
    </div>
    <div class="scratchpad-toolbar">
      <button id="toolPen" class="scratchpad-btn active">Pen</button>
      <button id="toolHighlighter" class="scratchpad-btn">Highlighter</button>
      <button id="toolEraser" class="scratchpad-btn">Eraser</button>
      <span style="font-size: 0.8rem; color: #64748b; margin-left: 0.4rem;">Color:</span>
      <div class="color-dot active" data-color="#1e293b" style="background: #1e293b;" title="Charcoal"></div>
      <div class="color-dot" data-color="#1d4ed8" style="background: #1d4ed8;" title="Royal Blue"></div>
      <div class="color-dot" data-color="#dc2626" style="background: #dc2626;" title="Red Marker"></div>
      <div class="color-dot" data-color="#15803d" style="background: #15803d;" title="Green"></div>
      <div class="color-dot" data-color="#7e22ce" style="background: #7e22ce;" title="Purple"></div>
      <input type="range" id="scratchpadSize" min="1" max="15" value="3" style="width: 60px; margin-left: auto;" title="Stroke Size">
      <button id="scratchpadUndoBtn" class="scratchpad-btn">Undo</button>
      <button id="scratchpadClearBtn" class="scratchpad-btn" style="color: #dc2626;">Clear</button>
    </div>
    <div class="scratchpad-canvas-wrap">
      <canvas id="scratchpadCanvas"></canvas>
    </div>
  </div>

  <!-- Floating Scratchpad Trigger Button -->
  <button id="scratchpadToggleBtn" class="btn-scratchpad-toggle" title="Open Whiteboard Scratchpad to Solve Problems">
    <span>✏️</span> Whiteboard Pad
  </button>

  <!-- Core JavaScript Modules -->
  <script src="../../assets/js/whiteboard-animations.js"></script>
  <script src="../../assets/js/whiteboard-scratchpad.js"></script>
  <script src="../../assets/js/search-engine.js"></script>
  <script src="../../assets/js/contact-modal.js"></script>
  <script src="../../assets/js/chapter-engine.js"></script>
</body>
</html>
"""
    out_file = os.path.join(out_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"  [OK] Generated {cls_name} :: {slug}/index.html ({len(html_content)} bytes)")

def generate_portal_hub(global_search_list):
    """Compiles the Master Whiteboard Hub (index.html)."""
    # Group chapters by Class
    cards_11 = []
    cards_12 = []

    sticker_colors = ["", "purple", "green", "amber"]

    for item in CHAPTER_METADATA["Class_11"]:
        concepts_stickers = "".join([
            f'<span class="concept-sticker {sticker_colors[idx % len(sticker_colors)]}">{c}</span>'
            for idx, c in enumerate(item.get("key_concepts", []))
        ])
        cards_11.append(f"""
          <div class="chapter-card" data-domain="{item['domain'].lower()}" data-slug="class-11-{item['slug']}">
            <div class="card-top">
              <span class="card-domain-badge">{item['domain']}</span>
              <span class="completion-indicator">○ Incomplete</span>
            </div>
            <h3 class="card-title">
              <a href="class-11/{item['slug']}/index.html">{item['title']}</a>
            </h3>
            <div class="card-meta-row">
              <span class="badge-priority">{item['priority']} Priority</span>
              <span class="badge-yield-high">{item['yield']}</span>
            </div>
            <div class="card-concepts-wrap" style="margin: 0.85rem 0 1.25rem;">
              <span style="font-size: 0.82rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 0.45rem;">
                📌 Core Concepts &amp; Formulas:
              </span>
              <div style="display: flex; flex-wrap: wrap; gap: 0.35rem;">
                {concepts_stickers}
              </div>
            </div>
            <div class="card-bottom">
              <a href="class-11/{item['slug']}/index.html" class="btn-enter-board">
                Open Whiteboard &rarr;
              </a>
            </div>
          </div>
        """)

    for item in CHAPTER_METADATA["Class_12"]:
        concepts_stickers = "".join([
            f'<span class="concept-sticker {sticker_colors[idx % len(sticker_colors)]}">{c}</span>'
            for idx, c in enumerate(item.get("key_concepts", []))
        ])
        cards_12.append(f"""
          <div class="chapter-card" data-domain="{item['domain'].lower()}" data-slug="class-12-{item['slug']}">
            <div class="card-top">
              <span class="card-domain-badge">{item['domain']}</span>
              <span class="completion-indicator">○ Incomplete</span>
            </div>
            <h3 class="card-title">
              <a href="class-12/{item['slug']}/index.html">{item['title']}</a>
            </h3>
            <div class="card-meta-row">
              <span class="badge-priority">{item['priority']} Priority</span>
              <span class="badge-yield-high">{item['yield']}</span>
            </div>
            <div class="card-concepts-wrap" style="margin: 0.85rem 0 1.25rem;">
              <span style="font-size: 0.82rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 0.45rem;">
                📌 Core Concepts &amp; Formulas:
              </span>
              <div style="display: flex; flex-wrap: wrap; gap: 0.35rem;">
                {concepts_stickers}
              </div>
            </div>
            <div class="card-bottom">
              <a href="class-12/{item['slug']}/index.html" class="btn-enter-board">
                Open Whiteboard &rarr;
              </a>
            </div>
          </div>
        """)

    portal_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CBSE Mathematics Whiteboard Engine // Class 11 &amp; 12 NCERT</title>
  <meta name="description" content="Immersive Whiteboard study engine strictly aligned with CBSE Class 11 &amp; 12 Mathematics NCERT syllabus. Step-by-step marking schemes, PYQs (2020-2025), formulas and exam traps.">
  <meta name="keywords" content="CBSE Mathematics, Class 11 Maths, Class 12 Maths, NCERT Maths, CBSE Board Exam, PYQs 2020-2025, Marking Schemes, Formulas, JEE Main Maths">
  <meta name="author" content="Kedar Krishna">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://kedar773.github.io/cbse-maths/">

  {get_google_verification_meta()}

  <!-- OpenGraph / Social Sharing -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://kedar773.github.io/cbse-maths/">
  <meta property="og:title" content="CBSE Mathematics Whiteboard Engine // Class 11 &amp; 12 NCERT">
  <meta property="og:description" content="Immersive Whiteboard study engine strictly aligned with CBSE Class 11 &amp; 12 Mathematics NCERT syllabus. Step-by-step marking schemes, PYQs (2020-2025), formulas and exam traps.">
  <meta property="og:site_name" content="Kedar's Academy Mathematics Engine">

  <!-- Schema.org Educational JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    "name": "Kedar's Academy Mathematics Engine",
    "url": "https://kedar773.github.io/cbse-maths/",
    "description": "Comprehensive CBSE Class 11 and Class 12 Mathematics digital whiteboard with NCERT pure-line notes, solved examples, step-wise marking schemes, and PYQs.",
    "founder": {{
      "@type": "Person",
      "name": "Kedar Krishna"
    }}
  }}
  </script>

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Kalam:wght@400;700&family=Patrick+Hand&display=swap" rel="stylesheet">

  <!-- Stylesheets -->
  <link rel="stylesheet" href="assets/css/whiteboard.css">
  <link rel="stylesheet" href="assets/css/whiteboard-animations.css">
  <link rel="stylesheet" href="assets/vendor/katex/katex.min.css">

  <style>
    /* Portal Specific Styling */
    .portal-hero {{
      text-align: center;
      padding: 3.5rem 1.5rem 2rem;
      position: relative;
    }}
    .portal-tag-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: #fef9c3;
      border: 1px solid #fde047;
      color: #854d0e;
      font-family: var(--font-title);
      font-size: 0.95rem;
      font-weight: 700;
      padding: 0.35rem 1rem;
      border-radius: 20px;
      margin-bottom: 1.25rem;
      box-shadow: 0 2px 8px rgba(253, 224, 71, 0.25);
    }}
    .portal-title {{
      font-size: clamp(2.4rem, 4.5vw, 3.6rem);
      color: var(--marker-black);
      margin-bottom: 0.75rem;
    }}
    .portal-subtitle {{
      max-width: 780px;
      margin: 0 auto 2rem;
      font-size: 1.15rem;
      color: var(--marker-slate);
      line-height: 1.6;
    }}
    .portal-search-bar {{
      max-width: 620px;
      margin: 0 auto 2.5rem;
      position: relative;
    }}
    .portal-search-input {{
      width: 100%;
      padding: 1rem 1.25rem 1rem 3rem;
      border: 2px solid #cbd5e1;
      border-radius: 30px;
      font-size: 1.05rem;
      font-family: var(--font-body);
      background: #ffffff;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
      outline: none;
      transition: all 0.2s ease;
    }}
    .portal-search-input:focus {{
      border-color: var(--marker-blue);
      box-shadow: 0 6px 25px rgba(29, 78, 216, 0.15);
    }}
    .search-icon-pos {{
      position: absolute;
      top: 50%;
      left: 1.2rem;
      transform: translateY(-50%);
      color: #94a3b8;
    }}

    /* Stats HUD */
    .portal-stats-hud {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 1.5rem;
      flex-wrap: wrap;
      margin-bottom: 3rem;
    }}
    .stat-pill {{
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      padding: 0.75rem 1.4rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
      min-width: 130px;
    }}
    .stat-number {{
      font-family: var(--font-title);
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--marker-blue);
      line-height: 1;
    }}
    .stat-label {{
      font-size: 0.8rem;
      font-weight: 600;
      color: #64748b;
      margin-top: 0.25rem;
      text-transform: uppercase;
    }}

    /* Class Switcher & Domain Filter Toolbar */
    .portal-controls-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 2rem;
      padding-bottom: 1rem;
      border-bottom: 2px solid #e2e8f0;
    }}
    .portal-class-tabs {{
      display: flex;
      gap: 0.5rem;
      background: #e2e8f0;
      padding: 0.3rem;
      border-radius: 12px;
    }}
    .portal-class-tab {{
      padding: 0.6rem 1.4rem;
      font-family: var(--font-title);
      font-size: 1.1rem;
      font-weight: 700;
      border: none;
      background: transparent;
      color: #475569;
      border-radius: 9px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .portal-class-tab.active {{
      background: #ffffff;
      color: var(--marker-blue);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }}
    .domain-chips-wrap {{
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
    }}
    .domain-filter-chip {{
      padding: 0.35rem 0.8rem;
      border-radius: 16px;
      border: 1px solid #cbd5e1;
      background: #ffffff;
      font-size: 0.85rem;
      font-weight: 600;
      color: #475569;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .domain-filter-chip:hover {{
      background: #f1f5f9;
    }}
    .domain-filter-chip.active {{
      background: var(--marker-blue);
      color: #ffffff;
      border-color: var(--marker-blue);
    }}

    /* Chapter Cards Grid */
    .chapters-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.5rem;
    }}
    .chapter-card {{
      background: #ffffff;
      border: 2px solid #e2e8f0;
      border-radius: 14px;
      padding: 1.4rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
      transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
      position: relative;
    }}
    .chapter-card:hover {{
      transform: translateY(-4px);
      border-color: var(--marker-blue);
      box-shadow: 0 10px 28px rgba(29, 78, 216, 0.1);
    }}
    .card-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.75rem;
    }}
    .card-domain-badge {{
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--marker-blue);
      background: var(--marker-blue-bg);
      border: 1px solid #bfdbfe;
      padding: 0.15rem 0.55rem;
      border-radius: 10px;
    }}
    .completion-indicator {{
      font-size: 0.75rem;
      font-weight: 700;
      color: #64748b;
      background: #f1f5f9;
      padding: 0.15rem 0.55rem;
      border-radius: 10px;
    }}
    .card-title {{
      font-size: 1.35rem;
      margin-bottom: 0.75rem;
      color: #0f172a;
    }}
    .card-title a {{
      color: inherit;
    }}
    .card-meta-row {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
      flex-wrap: wrap;
      margin-bottom: 1.25rem;
    }}
    .btn-enter-board {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      padding: 0.65rem 1rem;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-family: var(--font-title);
      font-size: 1rem;
      font-weight: 700;
      color: var(--marker-blue);
      transition: all 0.2s ease;
    }}
    .btn-enter-board:hover {{
      background: var(--marker-blue);
      color: #ffffff;
      border-color: var(--marker-blue);
      text-decoration: none;
    }}
  </style>
</head>
<body>

  <!-- Whiteboard Top Reading Progress Bar -->
  <div class="reading-progress-bar"></div>

  <!-- Hero Section -->
  <section class="portal-hero">
    <!-- Top Corner Contact Trigger -->
    <button id="contactModalToggle" class="portal-corner-contact contact-modal-trigger" title="Contact Kedar Krishna &amp; Teaching Centers">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
      <span>Contact</span>
    </button>

    <!-- Stacked Line Formation Brand Message -->
    <div class="portal-brand-stacked">
      <div class="stacked-brand-line1">Kedar's Academy</div>
      <div class="stacked-brand-line2">Mathematics Engine</div>
    </div>

    <div class="portal-tag-badge">
      <span>&#9733; CBSE CLASS 11 &amp; 12 // NCERT STRICT STANDARDS</span>
    </div>

    <h1 class="portal-title">
      Classroom Whiteboard <br>
      <span style="color: var(--marker-blue);">Mathematics Engine</span>
    </h1>

    <p class="portal-subtitle">
      Comprehensive interactive mathematics lecture whiteboard engineered for CBSE students. Strictly NCERT aligned explanations, step-by-step CBSE marking schemes, 5-year PYQ vault (2020–2025), and isolated advanced studies for competitive examinations.
    </p>

    <!-- Global Search Bar -->
    <div class="portal-search-bar">
      <svg class="search-icon-pos" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input type="text" id="heroSearchInput" class="portal-search-input" placeholder="Search concepts, formulas, or CBSE questions... (Press Ctrl+K)">
    </div>

    <!-- Stats HUD -->
    <div class="portal-stats-hud">
      <div class="stat-pill">
        <span class="stat-number">27</span>
        <span class="stat-label">Total Chapters</span>
      </div>
      <div class="stat-pill">
        <span class="stat-number">14</span>
        <span class="stat-label">Class 11 Chapters</span>
      </div>
      <div class="stat-pill">
        <span class="stat-number">13</span>
        <span class="stat-label">Class 12 Chapters</span>
      </div>
      <div class="stat-pill">
        <span class="stat-number" style="color: var(--marker-green);">100%</span>
        <span class="stat-label">NCERT Aligned</span>
      </div>
      <div class="stat-pill">
        <span class="stat-number" id="statMasteredCount" style="color: var(--marker-amber);">0</span>
        <span class="stat-label">Mastered</span>
      </div>
    </div>
  </section>

  <!-- Main Directory Container -->
  <main class="board-container">
    <div class="whiteboard-frame">
      <div style="padding: 1.5rem 1.75rem;">

        <!-- Control Toolbar: Class 11 vs 12 Switcher & Domain Filter -->
        <div class="portal-controls-bar">
          <div class="portal-class-tabs">
            <button class="portal-class-tab active" data-class="12">Class 12 (Board Core)</button>
            <button class="portal-class-tab" data-class="11">Class 11 (Foundation)</button>
          </div>

          <div class="domain-chips-wrap">
            <button class="domain-filter-chip active" data-domain="all">All Domains</button>
            <button class="domain-filter-chip" data-domain="calculus">Calculus</button>
            <button class="domain-filter-chip" data-domain="algebra">Algebra</button>
            <button class="domain-filter-chip" data-domain="vectors & 3d">Vectors &amp; 3D</button>
            <button class="domain-filter-chip" data-domain="probability">Probability</button>
            <button class="domain-filter-chip" data-domain="trigonometry">Trigonometry</button>
            <button class="domain-filter-chip" data-domain="coordinate geometry">Coordinate Geometry</button>
          </div>
        </div>

        <!-- Class 12 Directory Section -->
        <section class="class-directory-section" data-class="12">
          <div class="sticky-note blue" style="margin-bottom: 1.75rem;">
            <div class="sticky-title">🎯 CBSE Class 12 Mathematics (Complete 13 Chapters)</div>
            Featuring full step-marking solutions, 2020-2025 PYQ vault, speed verification hacks, and segregated advanced studies for JEE.
          </div>

          <div class="chapters-grid">
            {''.join(cards_12)}
          </div>
        </section>

        <!-- Class 11 Directory Section -->
        <section class="class-directory-section" data-class="11" style="display: none;">
          <div class="sticky-note yellow" style="margin-bottom: 1.75rem;">
            <div class="sticky-title">📘 CBSE Class 11 Mathematics (Complete 14 Chapters)</div>
            Strengthening core mathematical foundations, competency questions, and exemplar problems.
          </div>

          <div class="chapters-grid">
            {''.join(cards_11)}
          </div>
        </section>

      </div>
    </div>
  </main>

  <!-- Portal Footer -->
  <footer class="portal-footer">
    <div class="footer-content">
      <div class="footer-brand">
        <h3>Kedar's Academy Mathematics Engine</h3>
        <p>Interactive Whiteboard Architecture for CBSE Class 11 &amp; 12 Mathematics</p>
      </div>

      <div class="powered-by-wrap">
        <div class="powered-by-text">
          <span>⚡</span> Powered By Kedar's Academy
        </div>
      </div>

      <button class="footer-contact-trigger contact-modal-trigger" id="footerContactBtn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
        <span>Connect with Kedar Krishna / Teaching Centers (Bhubaneswar)</span>
      </button>

      <p class="copyright-sub">&copy; 2026 Kedar's Academy. All rights reserved. Strict NCERT Syllabus &amp; CBSE Exam Patterns.</p>
    </div>
  </footer>

  {get_contact_modal_html()}

  <!-- Interactive Whiteboard Scratchpad Drawer -->
  <div id="scratchpadModal">
    <div class="scratchpad-header">
      <div class="scratchpad-title">
        <span>✏️</span> Whiteboard Scratchpad
      </div>
      <button id="scratchpadCloseBtn" class="scratchpad-btn" title="Close">&times;</button>
    </div>
    <div class="scratchpad-toolbar">
      <button id="toolPen" class="scratchpad-btn active">Pen</button>
      <button id="toolHighlighter" class="scratchpad-btn">Highlighter</button>
      <button id="toolEraser" class="scratchpad-btn">Eraser</button>
      <div class="color-dot active" data-color="#1e293b" style="background: #1e293b;"></div>
      <div class="color-dot" data-color="#1d4ed8" style="background: #1d4ed8;"></div>
      <div class="color-dot" data-color="#dc2626" style="background: #dc2626;"></div>
      <div class="color-dot" data-color="#15803d" style="background: #15803d;"></div>
      <input type="range" id="scratchpadSize" min="1" max="15" value="3" style="width: 60px; margin-left: auto;">
      <button id="scratchpadUndoBtn" class="scratchpad-btn">Undo</button>
      <button id="scratchpadClearBtn" class="scratchpad-btn" style="color: #dc2626;">Clear</button>
    </div>
    <div class="scratchpad-canvas-wrap">
      <canvas id="scratchpadCanvas"></canvas>
    </div>
  </div>

  <button id="scratchpadToggleBtn" class="btn-scratchpad-toggle">
    <span>✏️</span> Whiteboard Pad
  </button>

  <!-- KaTeX Math Engine for Concept Stickers -->
  <script src="assets/vendor/katex/katex.min.js"></script>
  <script src="assets/vendor/katex/contrib/auto-render.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", function() {{
      if (typeof renderMathInElement === "function") {{
        renderMathInElement(document.body, {{
          delimiters: [
            {{ left: "$$", right: "$$", display: true }},
            {{ left: "$", right: "$", display: false }},
            {{ left: "\\(", right: "\\)", display: false }},
            {{ left: "\\[", right: "\\]", display: true }}
          ],
          throwOnError: false
        }});
      }}
    }});
  </script>

  <!-- Scripts -->
  <script src="assets/js/whiteboard-animations.js"></script>
  <script src="assets/js/whiteboard-scratchpad.js"></script>
  <script src="assets/js/search-engine.js"></script>
  <script src="assets/js/contact-modal.js"></script>
  <script src="assets/js/portal-engine.js"></script>
</body>
</html>
"""
    hub_file = os.path.join(OUT_DIR, "index.html")
    with open(hub_file, "w", encoding="utf-8") as f:
        f.write(portal_html)
    print(f"  [OK] Generated Master Hub :: index.html ({len(portal_html)} bytes)")

def main():
    print("=================================================================")
    print("Starting CBSE Mathematics Whiteboard Site Compilation Pipeline...")
    print("=================================================================")

    global_search_list = []
    manifest_curriculum = {"class_11": [], "class_12": []}

    for cls_name in ["Class_11", "Class_12"]:
        print(f"\n--- Compiling {cls_name} Chapters ---")
        meta_list = CHAPTER_METADATA[cls_name]
        key = "class_11" if "11" in cls_name else "class_12"

        for meta in meta_list:
            pat = meta["dir_pattern"]
            matches = glob.glob(os.path.join(ROOT_DIR, cls_name, pat))
            if not matches:
                print(f"  [WARN] No directory match found for pattern: {pat}")
                continue
            ch_dir = matches[0]
            generate_chapter_page(cls_name, meta, ch_dir, global_search_list)

            manifest_curriculum[key].append({
                "slug": meta["slug"],
                "title": meta["title"],
                "domain": meta["domain"],
                "priority": meta["priority"],
                "yield": meta["yield"]
            })

    # Save Search Index
    search_path = os.path.join(OUT_DIR, "assets", "data", "search_index.json")
    with open(search_path, "w", encoding="utf-8") as f:
        json.dump(global_search_list, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Generated Search Index: {search_path} ({len(global_search_list)} searchable items)")

    # Save Curriculum Manifest
    manifest_path = os.path.join(OUT_DIR, "assets", "data", "curriculum_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_curriculum, f, indent=2, ensure_ascii=False)
    print(f"[OK] Generated Mobile Curriculum Manifest: {manifest_path}")

    # Generate Master Portal Hub
    print("\n--- Compiling Master Portal Hub ---")
    generate_portal_hub(global_search_list)

    # Generate Sitemap and Robots.txt for Search Console
    print("\n--- Generating Sitemap & Robots.txt ---")
    generate_sitemap(manifest_curriculum)
    generate_robots_txt()

    print("\n=================================================================")
    print("CBSE Mathematics Whiteboard Site Generated Successfully!")
    print(f"Location: {OUT_DIR}")
    print("=================================================================")

if __name__ == "__main__":
    main()
