# Makes the secret draw and encodes it so nobody can read it from the page.
import random, json, base64, unicodedata
people = ["Hanna", "Maja", "Wiktoria", "Julia", "Nikola"]
banned = {("Hanna", "Maja"), ("Maja", "Hanna")}
def ok(a):
    return all(g != r and (g, r) not in banned for g, r in a.items())
while True:
    shuffled = people[:]; random.SystemRandom().shuffle(shuffled)
    draw = dict(zip(people, shuffled))
    if ok(draw): break
def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").strip().lower()
def h36(s):
    h = 5381
    for c in s: h = (h * 33 + ord(c)) & 0xFFFFFFFF
    d = "0123456789abcdefghijklmnopqrstuvwxyz"; out = ""
    while h: out = d[h % 36] + out; h //= 36
    return out or "0"
enc = {}
for g, r in draw.items():
    key = (norm(g) + "|ff2026").encode()
    b = bytes(x ^ key[i % len(key)] for i, x in enumerate(r.encode()))
    enc[h36(norm(g))] = base64.b64encode(b).decode()
t = open("template.html").read().replace("__DRAW__", json.dumps(enc))
open("index.html", "w").write(t)
print("draw sealed:", len(enc), "entries (assignments not shown)")
