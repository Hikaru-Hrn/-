import csv
import re

import pdfplumber

headers = [
    "Дата и время операции",
    "Дата списания",
    "Сумма в валюте операции",
    "Сумма операции в валюте карты",
    "Описание операции",
    "Номер карты",
]
all_data = []

table_settings = {
    "vertical_strategy": "explicit",
    "explicit_vertical_lines": [55, 110, 190, 270, 360, 490, 530],
    "horizontal_strategy": "lines",
}

with pdfplumber.open("Справка о движении средств.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        search_area = page.crop((0, 250, page.width, page.height)) if i == 0 else page
        table = search_area.extract_table(table_settings)

        if table:
            for row in table:
                clean_row = [" ".join(cell.split()) if cell else "" for cell in row]
                if any(clean_row) and re.search(r"\d{2}\.\d{2}\.\d{4}", clean_row[0]):
                    all_data.append(clean_row)

        # Для дебага
        # im = page.to_image(resolution=150)
        # im.debug_tablefinder(table_settings)
        # im.show()

with open("report.csv", "w", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(all_data)
