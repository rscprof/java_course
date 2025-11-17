import os
import re

# Пути к файлам
questions_files = ["questions_1.txt", "questions_2.txt"]
practice_file = "practice.txt"
output_file = "exam_document.tex"

# Шаблон документа
latex_template = r"""
\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{amssymb}
\titleformat{\section}[block]{\normalfont\Large\bfseries}{}{0em}{}
\titleformat{\subsection}[block]{\normalfont\large\bfseries}{}{0em}{}

\title{Вопросы к экзамену по разработке мобильных приложений}
\author{}
\date{}

\begin{document}

\maketitle

В ходе практической части экзамена будет доступна документация по Java (с помощью zeal), 
по Spring Boot (с помощью zeal), 
JUnit (с помощью пользовательского контента для zeal: 
\url{https://github.com/Kapeli/Dash-User-Contributions/tree/master/docsets/JUnit5},
JavaFX (самостоятельно будет импортировано преподавателем)).

Кроме того, практическое задание можно выполнять с собственноручным конспектом.

Для Spring проектов будет предоставлен результат запуска \url{https://start.spring.io/}

По практической части задания проводится опрос; по теоретической -- наряду с вопросами билета 
задаются дополнительные (краткие) вопросы.

\textbf{В билете должно быть два теоретических и один практический вопрос}

\section*{Теоретические вопросы}
%s

\section*{Практические задания}
%s

\end{document}
"""

def escape_latex(text):
    """Экранирует базовые символы LaTeX"""
    replacements = {
        '_': r'\_',
        '%': r'\%',
        '#': r'\#',
        '&': r'\&',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# --- Теоретические вопросы ---
theoretical_sections = []
for file in questions_files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Разбиваем на отдельные вопросы по пустым строкам или переносам
        questions = [q.strip() for q in content.splitlines() if q.strip()]
        if questions:
            items = "\n".join(f"    \\item {escape_latex(q)}" for q in questions)
            theoretical_sections.append(f"\\begin{{enumerate}}[left=0pt]\n{items}\n\\end{{enumerate}}")

theoretical_section = "\n".join(theoretical_sections)

# --- Практические задания ---
practical_section = ""
if os.path.exists(practice_file):
    with open(practice_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Разделяем по === и убираем лишние пробелы
    tasks = [task.strip() for task in content.split("===") if task.strip()]
    practical_parts = []
    for i, task in enumerate(tasks, start=1):
        escaped_task = escape_latex(task)
        practical_parts.append(f"\\subsection*{{Задание {i}}}\n{escaped_task}")
    practical_section = "\n\n".join(practical_parts)

# --- Генерация итогового документа ---
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(latex_template % (theoretical_section, practical_section))

print(f"Документ сгенерирован и сохранён в {output_file}")