# LearnHarness (نسخة مخصصة - Arabic & Anki Integrated)

بيئة تعلم تكيفية سقراطية تعتمد على الذكاء الاصطناعي مع تعريب الواجهة وربط مباشر ببرنامج Anki لإدارة التكرار المتباعد وشبكة معرفة مستمرة (2D DAG).

- **المستودع الرئيسي (Origin):** [BaselCS/LearnHarness](https://github.com/BaselCS/LearnHarness)
- **المصدر الأصلي (Upstream):** [amosblomqvist/learnharness](https://github.com/amosblomqvist/learnharness)

---

## هيكلية المشروع (Project Architecture)

- **`desktop/`**: تطبيق Electron + Next.js المستقل (مرتبط مع المستودع الأصلي عبر Git Subtree).
- **`launch_learnharness.sh`**: سكربت تشغيل التطبيق على المنفذ `12321`.
- **`sync_upstream.sh`**: سكربت مزامنة وسحب آخر تحديثات المطور الأصلي ودمجها تلقائياً دون فقدان التعديلات.
- **`anki_bridge.py`**: جسر التواصل مع بطاقات Anki عبر AnkiConnect.
- **`graph_manager.py`**: مدير قراءة وتحديث شبكة المعرفة المحلية.
- **`docs/`**: خطط التصميم ومعمارية المشروع واستراتيجية التزامن.

---

## التشغيل السريع (Quick Start)

```bash
# تشغيل تطبيق سطح المكتب
./launch_learnharness.sh
```

---

## التحديث من المصدر الأصلي (Upstream Sync)

للحصول على أي تحديثات جديدة من المستودع الأصلي مع الحفاظ التام على تعديلاتك:

```bash
./sync_upstream.sh
```
