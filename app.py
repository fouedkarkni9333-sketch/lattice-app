import math
import os
import random
import time
import zlib
from flask import Flask, render_template_string, request

app = Flask(__name__)


class SemanticLatticeEngine:
  """محرك الهندسة الترددية والضغط الرياضي الذكي (Semantic Lattice Core v6)"""

  def __init__(self):
    self.learned_lattice_patterns = []
    self.execution_metrics = []

  def analyze_patterns(self, raw_data: str) -> dict:
    start_time = time.time()
    total_chars = len(raw_data)
    unique_chars = len(set(raw_data))

    entropy_index = (
        math.log2(unique_chars) if unique_chars > 0 else 0
    ) * total_chars
    self.learned_lattice_patterns.extend(list(set(raw_data)))

    elapsed = time.time() - start_time
    return {
        "total_length": total_chars,
        "unique_elements": unique_chars,
        "mathematical_entropy": round(entropy_index, 2),
        "analysis_time_ms": round(elapsed * 1000, 4),
    }

  def genetic_optimize_lattice(self, raw_data: str) -> tuple:
    byte_data = raw_data.encode("utf-8")
    best_strategy = None
    min_size = float("inf")
    mutation_generations = [1, 5, 9]

    for level in mutation_generations:
      compressed_candidate = zlib.compress(byte_data, level=level)
      candidate_size = len(compressed_candidate)

      if candidate_size < min_size:
        min_size = candidate_size
        best_strategy = (level, compressed_candidate)

    orig_size = len(byte_data)
    ratio = round((1 - (min_size / orig_size)) * 100, 2) if orig_size > 0 else 0

    self.execution_metrics.append({
        "strategy_level": best_strategy[0],
        "original_size": orig_size,
        "compressed_size": min_size,
        "efficiency_ratio_percent": ratio,
    })

    return best_strategy

  def synthesize_new_lattice(self, length: int = 60) -> str:
    if not self.learned_lattice_patterns:
      return "النواة تحتاج إلى إدخال بيانات أولية لتبني البصمة."
    return "".join(random.choices(self.learned_lattice_patterns, k=length))

  def encode_lattice(self, raw_data: str) -> bytes:
    if not raw_data:
      raise ValueError("البيانات المدخلة فارغة.")
    _, optimal_lattice = self.genetic_optimize_lattice(raw_data)
    return optimal_lattice

  def decode_lattice(self, compressed_lattice: bytes) -> str:
    decompressed_bytes = zlib.decompress(compressed_lattice)
    return decompressed_bytes.decode("utf-8")

  def apply_xor_cipher(self, data: bytes, secret_key: int) -> bytes:
    return bytes([b ^ secret_key for b in data])


engine = SemanticLatticeEngine()

HTML_UI = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>محرك الهندسة الترددية - Semantic Lattice</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: #1e293b; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h1 { text-align: center; color: #38bdf8; font-size: 22px; }
        textarea { width: 100%; height: 100px; background: #0f172a; color: #fff; border: 1px solid #334155; border-radius: 8px; padding: 10px; margin-top: 10px; resize: none; box-sizing: border-box; }
        button { background: #0ea5e9; color: white; border: none; padding: 12px; width: 100%; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px; transition: 0.3s; }
        button:hover { background: #0284c7; }
        .result-box { background: #0f172a; border: 1px solid #334155; padding: 15px; border-radius: 8px; margin-top: 15px; white-space: pre-wrap; font-family: monospace; font-size: 14px; color: #34d399; }
    </style>
</head>
<body>
    <div class="container">
        <h1>محرك الهندسة الترددية (Lattice GUI)</h1>
        <p style="font-size: 13px; color: #94a3b8; text-align: center;">النظام النشط للضغط الجيني والتحليل الرياضي (سحابي)</p>
        
        <form method="POST" action="/process">
            <label for="inputText">أدخل النص أو البيانات للمعالجة:</label>
            <textarea id="inputText" name="text" placeholder="اكتب نصك هنا...">{{ default_text }}</textarea>
            <button type="submit">تنفيذ الضغط والتحليل الذكي</button>
        </form>
        
        {% if result %}
        <div id="output" class="result-box">
[✓] نتائج المعالجة السحابية الحية:
----------------------------------
- الحجم الأصلي: {{ result.original_size_bytes }} بايت
- الحجم المضغوط: {{ result.compressed_size_bytes }} بايت
- نسبة السلامة: {{ 'مطابق 100% (سليم رياضياً)' if result.integrity_verified else 'خطأ' }}
- زمن التحليل: {{ result.analysis.analysis_time_ms }} ms
- أنتروبيا النظام: {{ result.analysis.mathematical_entropy }}
----------------------------------
[المخرجات المولدة رياضياً]:
{{ result.synthetic_preview }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
  sample_text = (
      "def welcome_user(name):\nprint(f'Welcome back, {name}! Cloud system"
      " lattice is active.')"
  )
  return render_template_string(HTML_UI, default_text=sample_text, result=None)


@app.route("/process", methods=["POST"])
def process():
  user_text = request.form.get("text", "")
  if not user_text.strip():
    return render_template_string(
        HTML_UI, default_text="", result={"error": "النص فارغ"}
    )

  secret_key = 123
  metrics = engine.analyze_patterns(user_text)
  lattice_code = engine.encode_lattice(user_text)
  encrypted_code = engine.apply_xor_cipher(lattice_code, secret_key)
  restored = engine.decode_lattice(lattice_code)
  is_valid = user_text == restored

  result_data = {
      "analysis": metrics,
      "original_size_bytes": len(user_text.encode("utf-8")),
      "compressed_size_bytes": len(lattice_code),
      "integrity_verified": is_valid,
      "synthetic_preview": engine.synthesize_new_lattice(length=50),
  }

  return render_template_string(
      HTML_UI, default_text=user_text, result=result_data
  )


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)
