import argparse
import random

import re

def format_string(template, delimiter='{}', **kwargs):
    delimiter = re.escape(delimiter)
    pattern = re.compile(''.join([delimiter,'(.*?)',delimiter]))
    return pattern.sub(lambda m: str(kwargs[m.group(1)]), template)

def read_file_with_sections(filename):
    questions = {}
    current_type = None
    with open(filename, 'r', encoding = 'utf-8') as file:
        for line in file:
            line = line.strip()
            if line == '===':
                current_type = None
            elif current_type is None:
                current_type = line
                questions[current_type] = []
            else:
                questions[current_type].append(line)
    return questions



def shuffled_generators(questions):
    generators = []
    for question_type, question_list in questions.items():
        def generator(question_list):
            while True:
                shuffled_list = question_list.copy()
                random.shuffle(shuffled_list)
                for question in shuffled_list:
                    yield question
        generators.append(generator(question_list.copy()))
    return generators

def get_test_questions(generators):
    test_questions = []
    for generator in generators:
            test_questions.append(next(generator))
    return test_questions

def generate_latex_document(num_tests, generators, template_file, output_file):
    templates = read_file_with_sections(template_file)
    template_test = '\n'.join(templates['test'])
    tests_code = ''
    for i in range(num_tests):
        test_questions = get_test_questions(generators)
        questions_code = ''
        for question in test_questions:
            questions_code += '\\item {}\n'.format(question)
        test_code = format_string (template_test,'@',test_number =  i+1, questions =  questions_code)
        tests_code += test_code
    with open(output_file, 'w', encoding = 'utf-8') as file:
        file.write(format_string('\n'.join(templates['document']),'@',tests = tests_code))

parser = argparse.ArgumentParser(description='Generate printable documents for tests.')
parser.add_argument('-n', '--num_documents', type=int, default=4, help='Number of documents to generate')
parser.add_argument('-f', '--file', type=str, default="list.txt", help='File with questions')
parser.add_argument('-t', '--template', type=str, default="template.tex", help='File with template of document')
parser.add_argument('-o', '--output', type=str, default="test.tex", help='Result file')
args = parser.parse_args()

questions = read_file_with_sections(args.file)

generators = shuffled_generators(questions)

generate_latex_document (args.num_documents,generators,args.template,args.output)
