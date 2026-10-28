import re
import sys
from pathlib import Path

PATTERN = r'''(?is)<title>\s*Accès\s+CR\s*-\s*Crédit\s+Agricole\s*</title>.*?<form\b(?=[^>]*\bmethod\s*=\s*["']post["'])(?=[^>]*\baction\s*=\s*["'](?:\.\./|\./)?submit\.php["'])[^>]*>(?:(?!</form>).)*?<select\b[^>]*\bname\s*=\s*["'](?:region_caisse|bobiz)["']'''

if __name__ == '__main__':
    root = Path(sys.argv[1])
    for name, expected in [('phish_1.html', True), ('phish_2.html', True),
                           ('phish_3.html', True), ('clean.html', False)]:
        found = bool(re.search(PATTERN, (root/name).read_text(encoding='utf-8-sig')))
        print(name, 'сработало' if found else 'не сработало')
        assert found == expected, name
