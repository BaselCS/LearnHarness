# Anki Synthesis & Minimum Information Principle

When a concept has been thoroughly understood and verified via the check question:
1. Immediately invoke the tool `sync_anki_card`.
2. Formulate 1 to 2 atomic cards max adhering to the **Minimum Information Principle**:
   - Prefer Cloze deletion for mathematical equations or core rules (e.g. `In linear transformations, det(A) = 0 implies {{c1::volume collapses to 0}}`).
   - Prefer Basic for crisp conceptual definitions under 15 words.
3. Include LaTeX math notation `$...$` or `$$...$$` whenever presenting algebra or neural network weights.
4. Never quiz the user on trivial recall; synthesize only the generative foundations that prevent memory decay.
