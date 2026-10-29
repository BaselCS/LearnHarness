import json
import time

chat_id = "chat_test_arabic_matrix"
test_markdown = """# اختبار تعريب الواجهة والمحتوى (Localization & BiDi Test Suite)

مرحباً بك في اختبار بيئة العرض ثنائية الاتجاه (BiDi Test Suite). نختبر هنا جميع التراكيب المعقدة:

---

## 1. القرآن الكريم مع نص إنجليزي وتشكيل كثيف (Quran & Tashkeel)
قال تعالى: ﴿ اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ ۝ خَلَقَ الْإِنْسَانَ مِنْ عَلَقٍ ۝ اقْرَأْ وَرَبُّكَ الْأَكْرَمُ ۝ الَّذِي عَلَّمَ بِالْقَلَمِ ﴾ [العلق: 1-4]
*Translation: "Read! In the Name of your Lord, Who has created. Has created man from a clot. Read! And your Lord is the Most Generous. Who has taught by the pen."*

آية أخرى مع علامات وقف وأرقام:
﴿ وَقُل رَّبِّ زِدْنِي عِلْمًا ﴾ [طه: 114]
بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ (تأكد من عدم اقتطاع الحركات العلوية والسفلية بسبب الـ `line-height`).

---

## 2. الرياضيات والمعادلات (LaTeX & KaTeX)
معادلة تفاضلية في سياق عربي:
إذا كانت الدالة $f(x) = x^2 + 2x + 1$، فإن المشتقة الأولى هي:
$$f'(x) = \\lim_{\\Delta x \\to 0} \\frac{f(x + \\Delta x) - f(x)}{\\Delta x} = 2x + 2$$

حساب التكامل المحدد:
$$\\int_{0}^{\\pi} \\sin(x) \\, dx = [-\\cos(x)]_{0}^{\\pi} = 2$$

صيغة المصفوفات:
$$A = \\begin{pmatrix} a_{11} & a_{12} \\\\ a_{21} & a_{22} \\end{pmatrix}, \\quad \\det(A) = a_{11}a_{22} - a_{12}a_{21}$$

قيمة ثابت الدائرة تقريباً $\\pi \\approx 3.14159$ ونسبة الخطأ أقل من $0.001\\%$.

---

## 3. الأرقام والنسب والتواريخ والعملات (Numbers, Dates, Percentages & Currencies)
- نطاق السنوات: تم تطوير المشروع بين عامي 1990-2026 م.
- نطاق زمني: من الساعة 09:00 إلى 17:30 بتوقيت مكة المكرمة.
- النسب المئوية: حقق النموذج دقة تصنيف بلغت 98.5% مع هامش خطأ ±0.2%.
- العملات والمبالغ: بلغت التكلفة $45.20 دولار (ما يعادل 169.50 ر.س).
- عناوين IP والمنافذ: اتصل بالخادم المحلي عبر `127.0.0.1:2949` أو المنفذ `8080`.
- أرقام هواتف وصيغ دولية: رقم الدعم الفني الدولي هو `+966 50 123 4567`.

---

## 4. علامات الترقيم والأقواس المحايدة في أطراف السطر (Neutral Punctuation & Brackets)
- جملة عربية تنتهي بكلمة إنجليزية ونقطة: تم إطلاق النموذج بالاعتماد على محرك vLLM.
- جملة عربية تنتهي بقوس: تم تحديث قواعد البيانات (الإصدار الأخير رقم 4).
- جملة عربية داخل أقواس مختلفة: [تنبيه رقم 1]، (ملاحظة 2)، {مفتاح: "قيمة"}، و «اقتباس عربي».
- جملة تنتهي بعلامة استفهام إنجليزية وعربية: هل هذا النموذج يدعم RTL؟ وماذا عن LTR Support?

---

## 5. المسارات البرمجية وعناوين الويب (Paths, URLs & RegEx)
- مسار الملف المحلي: `/home/basel/Work/LearnHarness/src/core/i18n.ts`
- مسار نسبي: `../../components/ui/button.tsx`
- عنوان ويب كامل مع استعلام: `https://learnharness.local/api/search?q=ذكاء_اصطناعي&lang=ar#section-2`
- تعبير نمطي (RegEx): `/^[a-zA-Z0-9_\u0600-\u06FF]+$/g` للتحقق من الكلمات العربية والإنجليزية.

---

## 6. الأسهم والاتجاهات واختصارات لوحة المفاتيح (Directional Arrows & Shortcuts)
- تسلسل منطقي: الخطوة أ -> الخطوة ب -> الخطوة ج (تأكد من عدم انعكاس السهم).
- أسهم يونيكود: سهم لليسار ← وسهم لليمين → وسهم للأسفل ↓.
- اختصارات المفاتيح:
  - اضغط `Ctrl + Shift + Enter` أو `⌘ + Enter` لإرسال الرسالة.
  - اضغط `Ctrl + K` أو `⌘ + K` لفتح نافذة البحث السريع.
  - اضغط `Alt + F4` أو `Ctrl + W` للإغلاق.

---

## 7. كتل الأكواد والأكواد المضمنة المتتالية (Inline Code & Code Fences)
- تسلسل أوامر متتالية في نفس السطر: نفذ أمر `git checkout -b feat/ar` ثم `git add .` ثم `git commit -m "feat: arabic"` وأخيراً `git push origin`.
- كود بايثون مع تعليقات عربية:
```python
def calculate_accuracy(tp: int, tn: int, fp: int, fn: int) -> float:
    # حساب نسبة الدقة الكلية: (TP + TN) / Total
    total = tp + tn + fp + fn
    if total == 0:
        return 0.0
    accuracy = (tp + tn) / total
    return round(accuracy * 100, 2)

print(f"نسبة الدقة: {calculate_accuracy(95, 90, 5, 10)}%")
```

- كود تايب سكريبت مع نسخ LTR:
```typescript
export interface LocalizationConfig {
  locale: "ar" | "en";
  direction: "rtl" | "ltr";
  version: number;
}
```

---

## 8. خلط العربية مع اللغات الشرقية (Arabic + Chinese & Japanese)
- المصطلح الصيني للذكاء الاصطناعي: 人工智能 (Rén'gōng zhìnéng).
- المصطلح الياباني للتعلم العميق: ディープラーニング (Deep Learning) أو بالكانجي 人工知能 (Jinkō chinō).
- جملة مشتركة: في طوكيو (東京) وبكين (北京)، يجتمع باحثو الذكاء الاصطناعي (AI Researchers).

---

## 9. تنسيقات الخط العريض والمائل وماركداون المتقدم (Bold, Italic & Advanced MD)
- **نص عربي عريض جداً (Bold)** للتركيز.
- *نص عربي مائل (Italic)* للتأكيد.
- ***عريض ومائل معاً (Bold & Italic)***.
- ~~نص مشطوب (Strikethrough)~~ للعناصر المحذوفة.
- مصطلح إنجليزي عريض داخل سياق عربي: يعتبر **Self-Attention Mechanism** أساس هندسة النماذج.
- مصطلح إنجليزي مائل داخل سياق عربي: تعتمد الخوارزمية على *Stochastic Gradient Descent (SGD)*.
- اقتباس متعدد التنسيقات (Blockquote):
  > **ملاحظة معمارية:** هذا *اقتباس مركب* يحتوي على `inline-code` ورابط [وثائق المشروع](https://learnharness.local).

---

## 10. الجداول المنسقة ثنائية الاتجاه (BiDi Markdown Tables)
| الرقم | اسم الأداة (Tool) | المسار (Path) | التكلفة (USD) | النسبة (%) | الحالة |
| :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | `DeepSeek-V3` | `/models/deepseek` | $0.14 | 99.2% | نشط (Active) |
| 2 | `Gemini-Flash` | `/models/gemini` | $0.35 | 98.7% | قيد الانتظار |
| 3 | `Claude-Sonnet` | `/models/claude` | $3.00 | 97.5% | متوقف |

---

## 11. القوائم المنسدلة والمهام المتداخلة (Nested Lists & Tasklists)
- [x] إعداد هيكل اللغة العربية وتفعيل `dir="rtl"`.
- [x] ضبط عزل معادلات KaTeX لتكون LTR دائماً.
- [ ] فحص موضع أزرار النسخ في زاوية كتل الأكواد (يجب أن تكون باليسار في RTL أو باليمين المناسب).
- [ ] التأكد من محاذاة أزرار المحادثة والـ Composer.
  1. القائمة الفرعية الأولى:
     - تفصيل أ (Item A)
     - تفصيل ب (Item B)
  2. القائمة الفرعية الثانية:
     * نقطة هامة `CodeSpan` مع نص عربي.

---

## 12. الوسائط والصور والفيديو (Media, Images & Video)
شعار النظام:
![شعار التطبيق](/favicon.ico)

فيديو توضيحي:
[مشاهدة الفيديو التوضيحي (Tutorial Video)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
"""

chat_data = {
    "id": chat_id,
    "title": "اختبار مصفوفة اللغة العربية والـ BiDi",
    "createdAt": "2026-10-30T00:35:00.000Z",
    "updatedAt": "2026-10-30T00:35:00.000Z",
    "messages": [
        {
            "id": "u_test_1",
            "role": "user",
            "content": "هل يمكنك استعراض جميع حالات النصوص المعقدة باللغة العربية مع الرياضيات والرموز والأكواد والترقيم والتنسيقات؟",
            "timestamp": int(time.time() * 1000)
        },
        {
            "id": "a_test_1",
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": test_markdown
                }
            ],
            "api": "openai-completions",
            "provider": "openrouter",
            "model": "deepseek-v4.1-flash",
            "usage": {
                "input": 150,
                "output": 1650,
                "cacheRead": 0,
                "cacheWrite": 0
            },
            "stopReason": "endTurn",
            "timestamp": int(time.time() * 1000) + 100
        }
    ]
}

with open("data/chats/chat_test_arabic_matrix.json", "w", encoding="utf-8") as f:
    json.dump(chat_data, f, ensure_ascii=False, indent=2)

print("Generated full test matrix chat successfully.")
