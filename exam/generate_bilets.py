import os
import random
import argparse

def load_questions(file_path):
    """Load non-empty questions from a file, one per line."""
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_tasks_from_file(practice_file):
    """Load practical tasks from practice.txt, split by '==='."""
    with open(practice_file, "r", encoding="utf-8") as f:
        content = f.read()
    raw_tasks = [task.strip() for task in content.split("===") if task.strip()]
    return raw_tasks

def escape_latex(text):
    """Escape basic LaTeX special characters."""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '#': r'\#',
        '_': r'\_',
        '^': r'\^{}',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def generate_tickets(
    tickets_template_path,
    ticket_template_path,
    questions_1,
    questions_2,
    tasks,
    num_tickets,
    output_path
):
    # Проверка достаточности данных
    max_tickets = min(len(questions_1), len(questions_2), len(tasks))
    if num_tickets > max_tickets:
        raise ValueError(f"Запрошено {num_tickets} билетов, но доступно только {max_tickets} (ограничено вопросами или заданиями).")

    # Перемешиваем вопросы независимо
    shuffled_q1 = random.sample(questions_1, len(questions_1))
    shuffled_q2 = random.sample(questions_2, len(questions_2))
    shuffled_tasks = random.sample(tasks, len(tasks))  # можно и не перемешивать, но для разнообразия — да

    # Загружаем шаблоны
    with open(tickets_template_path, "r", encoding="utf-8") as f:
        tickets_template = f.read()
    with open(ticket_template_path, "r", encoding="utf-8") as f:
        ticket_template = f.read()

    # Генерация билетов
    tickets_content = []
    for i in range(num_tickets):
        q1 = escape_latex(shuffled_q1[i])
        q2 = escape_latex(shuffled_q2[i])
        q3 = escape_latex(shuffled_tasks[i])  # Экранируем всё задание как текст

        ticket = (
            ticket_template
            .replace("@num@", str(i + 1))
            .replace("@q1@", q1)
            .replace("@q2@", q2)
            .replace("@q3@", q3)
        )
        tickets_content.append(ticket)

    full_content = tickets_template.replace("@content@", "\n\n".join(tickets_content))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"Сгенерировано {num_tickets} билетов в {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Генератор экзаменационных билетов")
    parser.add_argument("--num", type=int, default=25, help="Количество билетов (по умолчанию: 31)")
    parser.add_argument("--output", type=str, default="generated_tickets.tex", help="Имя выходного файла")
    args = parser.parse_args()

    # Пути к файлам
    questions_1_path = "questions_1.txt"
    questions_2_path = "questions_2.txt"
    practice_file = "practice.txt"
    tickets_template_path = "tickets.tex"
    ticket_template_path = "ticket.tex"

    # Загрузка данных
    questions_1 = load_questions(questions_1_path)
    questions_2 = load_questions(questions_2_path)
    tasks = load_tasks_from_file(practice_file)

    # === ДИАГНОСТИКА ===
    print(f"Загружено из {questions_1_path}: {len(questions_1)} вопросов")
    print(f"Загружено из {questions_2_path}: {len(questions_2)} вопросов")
    print(f"Загружено из {practice_file}: {len(tasks)} практических заданий")

    # Проверка наличия файлов и непустоты
    if not questions_1:
        raise ValueError(f"Файл {questions_1_path} пуст или не содержит непустых строк!")
    if not questions_2:
        raise ValueError(f"Файл {questions_2_path} пуст или не содержит непустых строк!")
    if not tasks:
        raise ValueError(f"Файл {practice_file} пуст или не содержит заданий (нет блоков между '===')!")

    max_tickets = min(len(questions_1), len(questions_2), len(tasks))
    print(f"Максимально возможное количество билетов: {max_tickets}")

    if args.num > max_tickets:
        print("\n❌ ОШИБКА: Невозможно сгенерировать запрошенное количество билетов!")
        print(f"   Запрошено: {args.num}")
        print(f"   Ограничено:")
        print(f"     - questions_1.txt: {len(questions_1)}")
        print(f"     - questions_2.txt: {len(questions_2)}")
        print(f"     - practice.txt:    {len(tasks)}")
        raise ValueError(
            f"Недостаточно данных для генерации {args.num} билетов. "
            f"Максимум: {max_tickets} (минимум по трём спискам)."
        )

    # Генерация
    generate_tickets(
        tickets_template_path=tickets_template_path,
        ticket_template_path=ticket_template_path,
        questions_1=questions_1,
        questions_2=questions_2,
        tasks=tasks,
        num_tickets=args.num,
        output_path=args.output
    )

if __name__ == "__main__":
    main()