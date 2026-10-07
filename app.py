import math
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
MAX_H = math.log2(26)


def count_letters(text):
    """Đếm 26 chữ cái a-z, không phân biệt hoa thường, bỏ ký tự khác."""
    counts = [0] * 26
    for ch in text.lower():
        if 'a' <= ch <= 'z':
            counts[ord(ch) - ord('a')] += 1
    return counts


def frequencies(counts):
    total = sum(counts)
    if total == 0:
        return [0.0] * 26
    return [c / total for c in counts]


def entropy(probs):
    """H = -sum(p * log2 p), bỏ qua p = 0."""
    h = 0.0
    for p in probs:
        if p > 0:
            h -= p * math.log2(p)
    return h


def caesar_counts(counts, k):
    """Bản mã = (chữ + k) mod 26: số đếm của chữ i chuyển sang ô (i+k) mod 26."""
    out = [0] * 26
    for i in range(26):
        out[(i + k) % 26] = counts[i]
    return out


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    text = data.get("text", "")
    try:
        k = int(data.get("k", 0)) % 26
    except (TypeError, ValueError):
        k = 0

    plain_counts = count_letters(text)
    cipher_counts = caesar_counts(plain_counts, k)
    plain_freq = frequencies(plain_counts)
    cipher_freq = frequencies(cipher_counts)

    return jsonify({
        "letters": list(ALPHABET),
        "total": sum(plain_counts),
        "k": k,
        "plain_freq": plain_freq,
        "cipher_freq": cipher_freq,
        "plain_entropy": entropy(plain_freq),
        "cipher_entropy": entropy(cipher_freq),
        "max_entropy": MAX_H,
        "uniform": 1 / 26,
    })


if __name__ == "__main__":
    app.run(debug=True)
