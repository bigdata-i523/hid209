import yaml
import sys
from pprint import pprint
import glob
import errno

# all variables/counters declaration
path = 'notebook*.md'  # find all notebook files in the current directory
files = glob.glob(path)
file_number = 1

dict = {}
dict["Logistic"] = {}
dict["Logistic"]["Date"] = []
dict["Logistic"]["Content"] = []
dict["Theory"] = {}
dict["Theory"]["Date"] = []
dict["Theory"]["Content"] = []
dict["Practice"] = {}
dict["Practice"]["Date"] = []
dict["Practice"]["Content"] = []
dict["Writing"] = {}
dict["Writing"]["Date"] = []
dict["Writing"]["Content"] = []
dict["Meetings"] = {}
dict["Meetings"]["Date"] = []
dict["Meetings"]["Content"] = []

find_logistic = False
find_theory = False
find_practice = False
find_writing = False
find_meetings = False

counter = 0


# convert the input data format
def convert_format(input_lines):
    output_lines = []
    for new_line in input_lines:
        new_line = new_line.replace("*", "-")
        new_line = new_line.replace("# ", "")
        new_line = new_line.replace("\t", "    ")
        output_lines.append(new_line)

    return output_lines


# split each line of data into {content:[], date[]} format
def split_str(title, input_line):
    # if there exist a range of time
    if input_line[11:12] == "-":
        dict[title]["Date"].append(input_line[2:21])  # include two dates
        dict[title]["Content"].append(input_line[22:(len(input_line) - 1)].replace("\n", ""))

    # no range of time, just a single date
    else:
        dict[title]["Date"].append(input_line[2:10])  # each date has 8 characters
        dict[title]["Content"].append(input_line[11:(len(input_line) - 1)].replace("\n", ""))


def clear_lists(titles):
    for title in titles:
        dict[title]["Date"] = []
        dict[title]["Content"] = []


if __name__ == '__main__':
    for my_file in files:
        try:
            print(my_file)

            # read notebook*.md files
            with open(my_file, "r") as f:
                read_lines = f.readlines()
                converted_lines = convert_format(read_lines)
                # print(converted_lines)

                # Loop through all the lines
                for converted_line in converted_lines:
                    # search for titles
                    if converted_line.startswith("Logistic\n"):
                        find_logistic = True
                        continue
                    elif converted_line.startswith("Theory\n"):
                        find_theory = True
                        continue
                    elif converted_line.startswith("Practice\n"):
                        find_practice = True
                        continue
                    elif converted_line.startswith("Writing\n"):
                        find_writing = True
                        continue
                    elif converted_line.startswith("Meetings\n"):
                        find_meetings = True
                        continue

                    # read the data between two '\n's
                    if find_logistic:
                        if converted_line != "\n":
                            split_str("Logistic", converted_line)
                        if converted_line.startswith("\n"):
                            counter = counter + 1
                    elif find_theory:
                        if converted_line != "\n":
                            split_str("Theory", converted_line)
                        if converted_line.startswith("\n"):
                            counter = counter + 1
                    elif find_practice:
                        if converted_line != "\n":
                            split_str("Practice", converted_line)
                        if converted_line.startswith("\n"):
                            counter = counter + 1
                    elif find_writing:
                        if converted_line != "\n":
                            split_str("Writing", converted_line)
                        if converted_line.startswith("\n"):
                            counter = counter + 1
                    elif find_meetings:
                        if converted_line != "\n":
                            split_str("Meetings", converted_line)
                        if converted_line.startswith("\n"):
                            counter = counter + 1

                    # when counter=2, means it has reached to another title
                    if counter == 2:
                        counter = 0
                        find_logistic = False
                        find_theory = False
                        find_practice = False
                        find_writing = False
                        find_meetings = False

                # print(dict)
                # print(dict["Logistic"])
                # print(dict["Theory"])
                # print(dict["Practice"])
                # print(dict["Writing"])
                # print(dict["Meetings"])

                # define the output file name (yaml file), correspond to input file name
                out_str = 'data_parsing_' + my_file + '.yaml'
                print(out_str)

                # write file with yaml data format
                stream = file(out_str, "w")
                yaml.dump(dict, stream)  # write a yaml representation of data to 'data_parsing.yaml'
                print(yaml.dump(dict))

                # clear all sub-lists for the new file
                clear_lists(["Logistic", "Theory", "Practice", "Writing", "Meetings"])

            file_number = file_number + 1

        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
