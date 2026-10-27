# تقرير جاهزية التنفيذ البرمجي (Stage 9: Implementation Readiness Audit Report)

* **المستند المستهدف:** `/home/basel/Work/LearnHarness/docs/designs/learnharness_architecture.md`
* **النطاق المفحوص:** DetailedRange (الأسطر 200–237: خطة التنفيذ التفصيلية)
* **المراجع:** `egm-implementation-readiness` (قائد تقني ومهندس تنفيذ)
* **التاريخ:** 2026-10-27

---

## 1. التقييم العام (Status: BLOCKED)
الخطة تتضمن خطوات جيدة ولكنها **تحتوي فجوات تقنية تمنع كتابة الكود فوراً** دون ترك قرارات تصميمية للمبرمج. يجب توفير تواقيع الواجهات البرمجية (TypeScript Interfaces)، وتحديد خطة الاختبارات والتحقق، وإكمال جدول الملفات.

---

## 2. الملاحظات المصنفة حسب الأولوية

### 🔴 [Blocker 1] غياب كامل لخطة الاختبار وأوامر التحقق البرمجية
- **المشكلة:** لا يوجد أي ذكر لاختبارات الوحدة (Unit Tests)، التكامل (Integration Tests)، أو الواجهة (E2E). لا يوجد إطار عمل محدد (Vitest / Playwright)، وتنعدم أوامر الطرفية الصريحة للتحقق من سلامة البناء وعمل الخدمات.
- **التوجيه العلاجي:**
  - إضافة قسم `ج. خطة التحقق والاختبار (Verification & Test Plan)`.
  - تحديد Vitest لاختبارات الخدمات (Anki & Model Router).
  - توثيق أوامر التحقق الصريحة:
    - `npm run test:unit`
    - `npm run build`
    - أمر فحص اتصال AnkiConnect عبر الطرفية (`curl -X POST http://127.0.0.1:8765 -d '{"action": "version", "version": 6}'`).

### 🔴 [Blocker 2] تحديد مصدر المشروع المصدري وهيكل `auth.json`
- **المشكلة:**
  - لم يحدد المسار المصدري لاستنساخ هيكل LearnHarness الأساسي إلى مجلد `desktop`.
  - ملف `auth.json`: لم يتم توثيق الـ TypeScript Schema الخاصة به.
- **التوجيه العلاجي:**
  - تحديد المسار المصدري: النسخ المباشر من المستودع المستنسخ في `/tmp/learnharness_repo` إلى `/home/basel/Work/LearnHarness/desktop`.
  - كتابة Interface صريح لـ `auth.json`:
    ```typescript
    interface AppAuthConfig {
      geminiApiKey: string;
      localFallback?: {
        baseUrl: string; // e.g. http://127.0.0.1:11434
        modelName: string;
      };
    }
    ```

### 🔴 [Blocker 3] غياب مواصفات AnkiConnect وهيكل طابور المزامنة
- **المشكلة:** مهمة `src/services/anki.ts` لم تحدد أسماء عمليات AnkiConnect المستهدفة (`canAddNotes`, `addNote`)، ونوع البطاقة واسم الـ Deck، وبنية ملف `pending_cards.json`.
- **التوجيه العلاجي:** توثيق توقيعات دوال `AnkiService` ونوع البطاقة الافتراضي (`Cloze` لمعادلات الجبر الخطي و `Basic` للأسئلة المباشرة) ورزمة `LearnHarness::AI`.

### 🟡 [Major 1] غياب واجهة موجه النماذج (Model Router) وشروط التحويل
- **المشكلة:** عدم تحديد الـ SDK المعتمد للاتصال بـ Gemini وشروط التحويل عند أخطاء 429.
- **التوجيه العلاجي:** اعتماد مكتبة `@google/genai` الرسمية، وتحديد مهلة الطلب (5000ms للـ Flash و 15000ms للـ Pro).

### 🟡 [Major 2] نقص ملفات معمارية جوهرية في جدول التأثير
- **المشكلة:** غياب ملف واجهة D3 (`src/components/KnowledgeGraphView.tsx`)، وملف وسيط Electron Preload (`electron/preload.cjs`)، وملفات الاختبارات.
- **التوجيه العلاجي:** إدراج هذه الملفات صراحة في جدول التأثير.

### 🟡 [Major 3] آلية مزامنة D3 غير محددة
- **المشكلة:** كيف تستقبل لوحة D3 تحديث `knowledge_graph.json`؟
- **التوجيه العلاجي:** تحديد قناة IPC مخصصة (`graph:updated`) أو حدث SSE.

### 🟢 [Nit] عدم وجود معايير الانتهاء (Definition of Done)
- **التوجيه العلاجي:** إضافة قائمة تحقق (Acceptance Criteria checklist) لكل مهمة.
