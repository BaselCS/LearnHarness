# دليل تحديث وتزامن LearnHarness مع المصدر الأصلي (Upstream) بدون فقدان التعديلات

تم ربط المستودع بنجاح مع حساب GitHub الخاص بك:
- **المستودع الخاص بك (Origin):** `https://github.com/BaselCS/LearnHarness`
- **المصدر الأصلي (Upstream):** `https://github.com/amosblomqvist/learnharness`

---

## 1. المعمارية المعتمدة: Git Subtree

تم عزل كود تطبيق LearnHarness داخل المجلد `desktop/` وربطه بالمستودع الأصلي باستخدام معمارية **Git Subtree**:
- مجلد `desktop/` يتتبع شجرة الكود الأصلية مباشرة من `upstream/main`.
- التعديلات المخصصة (التعريب العربي، دمج أنكي `anki.ts`، الأدوات المضافة، ملفات التوثيق وسكربتات بايثون في الجذر) محفوظة ومحمية عبر سجل التعديلات المدمج (3-Way Merge).

---

## 2. كيفية استلام التحديثات الجديدة بسهولة

عند صدور أي تحديث أو ميزة جديدة من المطور الأصلي، يمكنك جلبها ودمجها بضغطة زر واحدة:

### الطريقة السريعة (الموصى بها):
شغّل السكربت التلقائي في جذر المشروع:
```bash
./sync_upstream.sh
```

### الطريقة اليدوية:
```bash
# 1. جلب التحديثات من المطور
git fetch upstream main

# 2. دمج التحديثات داخل مجلد desktop/ مع الحفاظ على تعديلاتك
git subtree pull --prefix=desktop upstream main --squash -m "chore: sync updates from upstream main"

# 3. رفع النتيجة لمستودعك على GitHub
git push origin main
```

---

## 3. التعامل مع التعارضات في حال حدوثها (Conflict Resolution)
- إذا عدّل المطور سطراً لم تقم بتعديله -> يتم دمجه تلقائياً 100%.
- إذا عدّل المطور ملفاً قمت بتعديله (مثل نصوص تم تعريبها سابقاً) -> يضع Git علامات التعارض القياسية (`<<<<<<< HEAD`).
  1. راجع الأسطر المتعارضة في الملف.
  2. احفظ التعديل المطلوب.
  3. نفّذ:
     ```bash
     git add .
     git commit -m "chore: resolve sync merge conflicts"
     git push origin main
     ```

---

## 4. الفحص والتشغيل بعد التحديث
بعد كل تحديث:
```bash
cd desktop
npm install
npm run typecheck
cd ..
./launch_learnharness.sh
```
