import nltk
import re
import csv
from sympy.solvers import solve
from sympy import Symbol
import json

# #####  #code is not clean and may have some redundant loops
# #####  #there is a scope for optimisation if we use maps instead of lists


data_file = "kinematics_questions.csv"
out_file = 'kinematics_populated.csv'
final_list = []

metrics = {
    "distance": ["km", "m", "cm", "kilometers", "meters", "centimeters"],
    "time": ["hours", "hour", "minute", "minutes", "seconds", "second", "s"],
    "velocity": ["km/hr", "m/s"],
    "acceleration": ["m/s2"]
}


def solve_equation(extracted_question_data):
    # create variable dynamically for tofind from csv
    tofind = Symbol(extracted_question_data['tofind'])

    equation_after_putting_values = extracted_question_data['formula']
    for data in extracted_question_data:

        # logic to replace variables in equations with numbers
        if " "+data+" " in extracted_question_data['formula'] and extracted_question_data[data] != '?' and data != '':
            equation_after_putting_values = equation_after_putting_values.replace(
                " " + data +" ", str(extracted_question_data[data]))
    solved = solve(equation_after_putting_values, tofind)
    if len(solved) > 0:
        return solved[0]


def randomizer(given_data):
    for multiplier in range(1, 100):
        extracted_question_data = {}
        question_breakup = given_data['question'].split(" ")
        for index, word in enumerate(question_breakup):
            word = word.strip('?.!,:')
            for metric in metrics:
                if word in metrics[metric]:

                    # logic to multiply numbers in question
                    question_breakup[index-1] = str(float(question_breakup[index-1]) * multiplier)
                    extracted_question_data['question'] = " ".join(question_breakup)

        for item in given_data:
            if item not in extracted_question_data:
                # filling out remaining data in extracted data, from given data.
                extracted_question_data[item] = given_data[item]

            if item != 'question_type' and item != 'question' and item != 'answer' \
                    and item != 'formula' and item != 'tofind' and extracted_question_data[item] != '?' \
                    and extracted_question_data[item] != "":

                # rounding off floats for 0.00 precision
                extracted_question_data[item] = "{0:.2f}".format(round(multiplier * float(extracted_question_data[item]),2))

        extracted_question_data['answer'] = solve_equation(extracted_question_data)

        # final list should contain ~100x items than your original csv
        final_list.append(extracted_question_data)


with open(data_file) as csv_file:
    reader_cursor = csv.reader(csv_file, delimiter=',')
    for row in reader_cursor:
        if len(row[1].split(" ")) > 1:
            question_data = dict()
            question_data['question_type'] = row[0]
            question_data['question'] = row[1]
            question_data['d'] = row[2]
            question_data['u'] = row[3]
            question_data['v'] = row[4]
            question_data['t'] = row[5]
            question_data['a'] = row[6]
            question_data['tofind'] = row[7]
            question_data['formula'] = row[8]
            question_data['answer'] = row[9]
            randomizer(question_data)


def write_csv(filename, final_list):
    with open(filename, 'w') as output_csv:
        field_names = ['question_type', 'question', 'd', 'u', 'v', 't', 'a', 'tofind', 'formula', 'answer']
        writer = csv.DictWriter(output_csv, fieldnames=field_names)
        print "CSV Writing Started."
        writer.writeheader()
        for each_question in final_list:
            writer.writerow({
                'question_type': each_question['question_type'],
                'question': each_question['question'],
                'd': each_question['d'],
                'u': each_question['u'],
                'v': each_question['v'],
                't': each_question['t'],
                'a': each_question['a'],
                'tofind': each_question['tofind'],
                'formula': each_question['formula'],
                'answer': each_question['answer']
            })

        print "CSV Writing Completed."

write_csv(out_file, final_list)

# for __question in final_list:
#     print __question
