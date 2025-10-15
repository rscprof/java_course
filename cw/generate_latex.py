#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт формирует красивый LaTeX-файл из структурированного списка вопросов.
Входной файл: list.txt
Формат:
  Заголовок
  вопрос 1
  вопрос 2
  ===
  Следующий заголовок
  вопрос 1
  ...
Выход: output.tex
"""

from pathlib import Path

INPUT_FILE = Path("list.txt")
OUTPUT_FILE = Path("output.tex")

def parse_blocks(text: str):
    """Разделяет текст на блоки по '==='."""
    blocks = []
    current = []
    for line in text.splitlines():
        line = line.strip()
        if line == "===":
            if current:
                blocks.append(current)
                current = []
        elif line:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


def make_latex(blocks):
    """Создаёт тело документа LaTeX."""
    result = []
    for block in blocks:
        if not block:
            continue
        title, *questions = block
        if not questions:
            continue  # пропускаем пустые секции
        result.append(f"\\section*{{{title}}}\n\\begin{{enumerate}}")
        for q in questions:
            q = q.replace("&", "\\&")  # базовая защита от спецсимволов
            q = q.replace("#", "\\#")  # базовая защита от спецсимволов
            result.append(f"  \\item {q}")
        result.append("\\end{enumerate}\n")
    return "\n".join(result)


def make_document(body):
    """Формирует полноценный LaTeX-документ."""
    return f"""\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[russian]{{babel}}
\\usepackage[a4paper,margin=2cm]{{geometry}}
\\usepackage{{enumitem}}
\\setlist[enumerate]{{itemsep=3pt,topsep=3pt}}

\\begin{{document}}

{body}

\\end{{document}}
"""


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")
    blocks = parse_blocks(text)
    body = make_latex(blocks)
    doc = make_document(body)
    OUTPUT_FILE.write_text(doc, encoding="utf-8")
    print(f"LaTeX-файл успешно создан: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
