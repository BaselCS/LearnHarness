import urllib.request
import json

URL = "http://127.0.0.1:8765"

arabic_cards = [
    {
        "id": 1793151388488,
        "Text": "في FastAPI، يعمل مسار {{c1::<code>async def</code>}} مباشرة على مسار الـ Event Loop الأحادي، وأي عملية حاجبة بداخله تجمد السيرفر.",
        "Extra": "لذلك لا يجب وضع أي كود متزامن (blocking) داخل <code>async def</code> دون تفويضه."
    },
    {
        "id": 1793151415312,
        "Text": "لتشغيل دالة متزامنة حاجبة داخل مسار async def دون تجميد الـ Event Loop، يجب تغليفها باستخدام {{c1::<code>await run_in_threadpool(func, *args)</code>}} أو {{c1::<code>await asyncio.to_thread(func, *args)</code>}}.",
        "Extra": "يقوم هذا بنقل التنفيذ الحاجب إلى الـ Threadpool الخاص بـ AnyIO مع إبقاء الـ Event Loop حراً."
    },
    {
        "id": 1793151415462,
        "Text": "في FastAPI، يعمل مسار async def بتعاون تشاركي ولا يفسح المجال للمهام الأخرى إلا عند وجود {{c1::نقاط <code>await</code> صريحة}} فقط.",
        "Extra": "غياب نقاط الـ await في مسار async def يجعل المهمة تحتكر الخيط الرئيسي بالكامل وتمنع معالجة باقي الطلبات."
    },
    {
        "id": 1793151415611,
        "Text": "عند تعريف مسار في FastAPI باستخدام دالة {{c1::<code>def</code> عادية (بدون async)}}، يقوم السيرفر تلقائياً بتشغيلها داخل {{c2::مجمع خيوط معالجة منفصل (Threadpool via AnyIO)}}.",
        "Extra": "هذا يحمي الـ Event Loop الرئيسي من التجميد حتى لو كانت الدالة تستخدم دوال حاجبة مثل <code>time.sleep</code> أو <code>requests</code>."
    },
    {
        "id": 1793151415762,
        "Text": "لتشغيل عدة دوال coroutines مستقلة بالتوازي واختصار وقت الاستجابة لأطول طلب فقط، نمررها دون await إلى {{c1::<code>await asyncio.gather(coro1, coro2, ...)</code>}}.",
        "Extra": "تحذير: لا تضع await على الدوال داخل gather، لأن ذلك سيجعلها تنفذ بالتتابع قبل استدعاء gather أصلاً."
    },
    {
        "id": 1793151415912,
        "Text": "استخدام مشغلات قواعد البيانات المتزامنة مثل <code>psycopg2</code> داخل async def يجمد السيرفر؛ والحل السليم معها هو استخدام {{c1::<code>def</code> عادية}} بدلاً من async.",
        "Extra": "إذا أردت استخدام مسارات async def فيجب استخدام مشغلات غير متزامنة مثل <code>asyncpg</code> مع <code>AsyncSession</code>."
    },
    {
        "id": 1793151416062,
        "Text": "في FastAPI، القاعدة المعمارية: استخدم <code>async def</code> للمكتبات {{c1::غير المتزامنة أصلاً (مثل <code>httpx</code>)}}، واستخدم <code>def</code> عادية للمكتبات {{c2::المتزامنة الحاجبة (مثل <code>requests</code> و <code>boto3</code>)}}.",
        "Extra": "وللعمليات الحسابية الثقيلة (CPU-bound)، استخدم <code>ProcessPoolExecutor</code> لتجاوز قفل الـ GIL."
    }
]

for card in arabic_cards:
    payload = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": card["id"],
                "fields": {
                    "Text": card["Text"],
                    "Extra": card["Extra"]
                }
            }
        }
    }
    req = urllib.request.Request(URL, data=json.dumps(payload).encode("utf-8"))
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f"Updated note {card['id']}: error={res.get('error')}")

print("Done updating cards with <code> tags!")
