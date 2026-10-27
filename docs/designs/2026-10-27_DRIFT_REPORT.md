# تقرير رصد الانحراف المعماري (Drift Detection Report)

* **التاريخ:** 2026-10-27
* **المجلد المفحوص:** `/home/basel/Work/LearnHarness/docs/designs`
* **المستند الأساسي:** `learnharness_architecture.md`
* **بيئة الكود المستهدفة:** `/home/basel/Work/LearnHarness/desktop`

---

## learnharness_architecture.md

- **انحراف خدمة الربط مع Anki (Anki Integration Hook Divergence):**
  - **التصميم:** يحدد التصميم في القسم 5.ب والقسم 7.أ قيام `TeacherAgent` باستدعاء `AnkiService.addCard()` تلقائياً فور إتقان المفهوم لتوليد بطاقات ذرية وحقنها في Anki.
  - **الواقع البرمجي:** تم إنشاء الملف الأساسي `src/services/anki.ts` بشكل مستقل، لكنه لم يُربط بعد داخل دورة حياة الوكيل (`src/agent/teacher-agent.ts`) أو مسار اكتمال التحقق (`/api/activity`).

- **ملفات ومكونات لم تُنشأ بعد (Unimplemented Specified Files):**
  - ملف العميل المباشر لـ AGY: `src/services/agy-client.ts` غير موجود حالياً في الكود؛ التطبيق ما زال يعتمد الواجهة المسبقة `@earendil-works/pi-ai`.
  - ملف دوال الكتابة الذرية: `src/store/atomic-storage.ts` غير موجود؛ التطبيق يستخدم عمليات الكتابة المباشرة في `src/store/graph.ts`.
  - ملفات الاختبارات: `tests/services/anki.test.ts` المحددة في خطة التحقق لم تُكتب بعد.

- **انحراف مسار مكون الرسم البياني (Component Path Drift):**
  - **التصميم:** يذكر مسار `src/components/KnowledgeGraphView.tsx`.
  - **الواقع البرمجي:** مسار مجلد المكونات الفعلي في المشروع هو `components/graph-view.tsx` و `components/graph-canvas.ts` مباشرة تحت جذر `desktop/` وليس داخل `src/components/`.

- **انحراف المنفذ المعتمد (Port Configuration Drift):**
  - **التصميم:** يوثق التصميم الاعتماد الافتراضي على المنفذ `3000`.
  - **الواقع البرمجي:** تم تعديل ملف `package.json` بناءً على طلب المستخدم الصريح ليعمل على المنفذ المخصص `12321` لمنع تعارض المنافذ.
