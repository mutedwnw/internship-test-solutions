import base64
import re
from pathlib import Path


folder = Path(__file__).resolve().parent
path = folder / "2" / "apiajax_113069.js_"

text = path.read_text(encoding="utf-8-sig")

match = re.search(
    r"var\s+_0I1\s*=\s*'([^']+)'",
    text
)

if match is None:
    raise ValueError("Строка _0I1 не найдена")

encoded = match.group(1)

reversed_text = encoded[::-1]

decoded = base64.b64decode(reversed_text).decode("utf-8")

print(decoded)

numbers = [
    116, 96, 110, 41, 103, 106, 110, 111, 111, 100,
    98, 99, 111, 98, 100, 109, 103, 41, 109, 112
]

domain = ""

for number in numbers:
    domain += chr(number + 5)

print("Домен из папки 4:", domain)

prefix = "\150\164\164\160\072\057\057"
path = "\057" + "ctd" + "\057\163\143\162\151\160\164\163\056\152\163"

print(prefix)
print(path)