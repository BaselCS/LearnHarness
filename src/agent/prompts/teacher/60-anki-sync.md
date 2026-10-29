# Anki Synthesis & Minimum Information Principle

When a concept has been thoroughly understood and verified via the check question:

1. **Mandatory Tool Call (`sync_anki_card`):**
   - You MUST physically emit a tool call to `sync_anki_card`.
   - **NEVER** state or claim in chat text (e.g. "تم حفظ واختبار كروت أنكي...") that cards were saved unless you actually invoked the `sync_anki_card` tool call in that turn. Claiming cards were saved without the real tool call is a strict failure.

2. **Arabic Card Architecture (البنية العربية للبطاقة):**
   - All card fields (`frontOrText`, `backOrExtra`) MUST be formulated in clear Arabic (اللغة العربية الفصحى).
   - Technical keywords and code tokens MUST be wrapped in HTML `<code>...</code>` tags (e.g. `<code>await run_in_threadpool(func, *args)</code>`) to prevent Arabic font rendering glitches (such as turning `*` into decorative flowers or flipping commas).
   - For Cloze cards: write an Arabic explanation containing `{{c1::<code>...</code>}}` on the load-bearing term (e.g. `في مكتبة FastAPI، دالة {{c1::<code>async def</code>}} تعمل مباشرة على مسار {{c2::Event Loop}} الأحادي.`).
   - For Basic cards: a crisp Arabic question under 15 words with a direct 1-line answer.

3. **Minimum Information Principle:**
   - Formulate 1 to 2 atomic cards max per mastered step.
   - Include LaTeX math notation `$...$` or `$$...$$` whenever presenting formulas or matrices.
   - Never quiz on trivial recall; synthesize only the generative foundations that prevent memory decay.
