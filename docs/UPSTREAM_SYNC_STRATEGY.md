# دليل تحديث وتزامن LearnHarness مع المصدر الأصلي (Upstream) بدون كسر التعديلات

هذا الدليل يوضح الطريقة القياسية للحفاظ على تعديلاتك (التعريب، البرومبت، السلاسل غير المتصلة Unconnected Chains، والتطويرات الخاصة) عند قيام المطور الأصلي (Maintainer) بتحديث التطبيق.

---

## 1. الفصل المعماري للتعديلات (Architecture Separation)

أفضل حماية ضد التعارضات هي عدم لمس ملفات المصدر عند توفر بديل رسمي داخل الكود:

### أ) البرومبت والنظام (System Prompts)
- **لا تعدل مباشرة** في `desktop/src/agent/system-prompt.md`.
- **البديل الرسمي المدمج**: الناظم يدعم خاصية `PROMPTS_OVERRIDE_DIR` في مسار `desktop/data/prompts/`.
- انسخ أي جزء ترغب بتعديله إلى مجلد `data/prompts/` بنفس الهيكلية (مثل `data/prompts/system-prompt.md` أو `data/prompts/teacher/...`).
- عند تحديث المطور لملفات الكود، ملفاتك في `data/prompts/` تبقى معزولة وتأخذ الأولوية تلقائياً دون أي تعارض برمجي.

### ب) السلاسل والبيانات وشبكة المعرفة (Chains & Graph Data)
- بيانات السلاسل (`chains.jsonl`، `nodes.jsonl`) والإعدادات موجودة في `desktop/data/` (أو المسار المحدد بـ `LH_DATA_DIR`).
- هذا المجلد معزول بطبيعته عن الكود المصدري ولن يمسّه أي تحديث من المطور.

### ج) التعريب والواجهة (Localization / Translation)
- لتفادي تعارض دمج الأكواد (Merge Conflicts) داخل ملفات الـ React/TSX:
  1. يُفضل عزل نصوص الواجهة في ملف قاموس وسيط (مثل `locales/ar.json` أو ثوابت نصوص).
  2. أو الاعتماد على دمج Git ثلاثي الأطراف (3-way merge) كما هو مشروح أدناه.

---

## 2. المسار الأساسي: إدارة التحديث عبر Git (Upstream Branching Strategy)

هذه الطريقة الأضمن والأسهل للمشاريع مفتوحة المصدر:

### الخطوة 1: تهيئة المستودع وربطه بالأصل
```bash
cd /home/basel/Work/LearnHarness
git init
git remote add upstream https://github.com/amosblomqvist/learnharness.git
git fetch upstream
```

### الخطوة 2: إنشاء فرع التعديلات المخصصة
```bash
# إنشاء فرع خاص بتعديلاتك معتمداً على آخر نسخة مستقرة من المطور
git checkout -b custom-ar upstream/main

# أضف ملفاتك وتعديلاتك
git add .
git commit -m "feat: add arabic localization, anki bridge, and custom prompts"
```

### الخطوة 3: التحديث عند إصدار المطور لنسخة جديدة
عندما يطلق المطور تحديثاً جديداً:
```bash
# 1. جلب التحديثات الجديدة من المطور
git fetch upstream

# 2. التأكد من أنك على فرع تعديلاتك
git checkout custom-ar

# 3. دمج التحديثات
git merge upstream/main
```

- **في حالة عدم وجود تعارض في نفس الأسطر**: سينتهي الدمج تلقائياً وبنجاح.
- **في حالة وجود تعارض (Conflict)**: يقوم Git بتحديد الأسطر المتعارضة بوضوح (`<<<<<<< HEAD`)، فتقوم بحفظ تعديلك وحذف العلامات ثم:
  ```bash
  git add .
  git commit -m "chore: merge upstream updates into custom-ar"
  ```

---

## 3. المسار الاحتياطي: نظام رقع التعديلات (Git Patch Workflow)

إذا كنت لا تريد إدارة فروع Git معقدة، يمكنك استخراج كل تعديلاتك كملف "رقعة" (Patch):

### استخراج تعديلاتك كملف Patch:
```bash
git diff upstream/main > my_customizations.patch
```

### عند قدوم تحديث جديد:
1. سحب كود المطور الجديد بالكامل.
2. تطبيق رقعتك بضغطة زر:
```bash
git apply --reject --whitespace=fix my_customizations.patch
```
- إذا واجه تعديل ما مشكلة في سطر معين، يولد Git ملف `.rej` يوضح مكان التعديل بدقة لتركيبه يدوياً دون أن تفقد بقية التعديلات.

---

## ملخص سريع للقواعد الذهبية
1. أي تعديل إعدادات أو برومبت -> ضعه في `desktop/data/`.
2. أي ميزة إضافية (مثل `anki_bridge.py`) -> اتركها كملفات وسيطة ومستقلة وتستدعى كأدوات.
3. التعديلات داخل كود الواجهة -> احفظها عبر فرع `custom-ar` واعمل `git merge upstream/main` عند كل تحديث.
