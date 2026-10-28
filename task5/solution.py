import csv
import ipaddress
import re
from pathlib import Path

import tldextract
import xlwt

folder = Path(__file__).resolve().parent

source_path = folder / "domains.txt"
csv_path = folder / "domains_result.csv"
xls_path = folder / "domains_result.xls"

extract = tldextract.TLDExtract(
    suffix_list_urls=(),
    cache_dir=None,
    include_psl_private_domains=False
)


assert (
    extract("safeboard.kaspersky.com").top_domain_under_public_suffix
    == "kaspersky.com"
)

assert (
    extract("news.domain.com.au").top_domain_under_public_suffix
    == "domain.com.au"
)

book = xlwt.Workbook(encoding="utf-8")
header_style = xlwt.easyxf("font: bold on;")

sheet = None
sheet_number = 0

row_number = 65536

saved = 0
removed_www = 0
skipped = 0
without_result = 0

with source_path.open(encoding="utf-8-sig") as source_file:
    with csv_path.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "original_domain",
            "second_level_domain"
        ])

        for line in source_file:
            domain = line.strip()

            if not domain or domain.startswith(("#", "!")):
                continue

            if domain.lower().startswith("www"):
                removed_www += 1
                continue

            if domain.startswith("||") and domain.endswith("^"):
                domain = domain[2:-1]

            if domain.lower().startswith("www"):
                removed_www += 1
                continue

            original_domain = domain
            normalized_domain = domain.lower().rstrip(".")

            try:
                ipaddress.ip_address(normalized_domain)
            except ValueError:
                pass
            else:
                skipped += 1
                continue

            if not re.fullmatch(
                r"(?:[a-z0-9_](?:[a-z0-9_-]*[a-z0-9_])?\.)+"
                r"[a-z][a-z0-9-]*",
                normalized_domain
            ):
                skipped += 1
                continue

            parts = extract(normalized_domain)
            second_level_domain = (
                parts.top_domain_under_public_suffix
            )

            if not second_level_domain:
                without_result += 1

            if row_number == 65536:
                if sheet is not None:
                    sheet.flush_row_data()

                sheet_number += 1
                sheet = book.add_sheet(
                    f"Domains_{sheet_number}"
                )

                sheet.col(0).width = 60 * 256
                sheet.col(1).width = 40 * 256

                sheet.write(
                    0, 0, "original_domain", header_style
                )
                sheet.write(
                    0, 1, "second_level_domain", header_style
                )

                row_number = 1

            writer.writerow([
                original_domain,
                second_level_domain
            ])

            sheet.write(row_number, 0, original_domain)
            sheet.write(row_number, 1, second_level_domain)

            row_number += 1
            saved += 1

            if row_number % 5000 == 0:
                sheet.flush_row_data()

if sheet is None:
    sheet = book.add_sheet("Domains_1")
    sheet.write(0, 0, "original_domain", header_style)
    sheet.write(0, 1, "second_level_domain", header_style)

book.save(str(xls_path))

print("Сохранено строк:", saved)
print("Удалено строк с www:", removed_www)
print("Пропущено технических записей:", skipped)
print("Не удалось выделить домен:", without_result)
print("CSV:", csv_path)
print("XLS:", xls_path)