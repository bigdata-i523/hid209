import errno
import glob
import os

import dateparser
import yaml


class DateParsing:
    def __init__(self, sections, meetings_date):
        self.section_list = sections
        self.meeting_list = meetings_date

    # convert the input data format
    def convert_data(self, input_lines):
        output_lines = []
        cur_sections = []

        for new_line in input_lines:
            new_line = new_line.replace("*", "-")

            if new_line.startswith("# "):
                new_line = new_line.replace("# ", "")
                cur_sections.append(new_line.replace("\n", ""))

            new_line = new_line.replace("Weeks with no progress", "Inactive")
            new_line = new_line.replace("\t", "    ")
            output_lines.append(new_line)

        return output_lines, cur_sections

    def extract_data(self, read_lines):
        counter = 0
        flag = None

        # initialize a dictionary (table) structure, which is
        # {
        #   "Section": {
        #           "Date": [],
        #           "Content": []
        #       }
        # }
        dict = {}
        for i in self.section_list:
            dict[i] = {}
            dict[i]["Date"] = []
            dict[i]["Content"] = []

        # Loop through all the lines
        for read_line in read_lines:
            # search for titles
            if read_line.startswith("Logistic\n"):
                flag = "Logistic"
                continue
            elif read_line.startswith("Theory\n"):
                flag = "Theory"
                continue
            elif read_line.startswith("Practice\n"):
                flag = "Practice"
                continue
            elif read_line.startswith("Writing\n"):
                flag = "Writing"
                continue
            elif read_line.startswith("Meetings\n"):
                flag = "Meetings"
                continue

            # read the data between two '\n's
            if flag == "Logistic":
                if read_line != "\n":
                    self.split_str(dict[flag], read_line)
                if read_line.startswith("\n"):
                    counter = counter + 1
            elif flag == "Theory":
                if read_line != "\n":
                    self.split_str(dict[flag], read_line)
                if read_line.startswith("\n"):
                    counter = counter + 1
            elif flag == "Practice":
                if read_line != "\n":
                    self.split_str(dict[flag], read_line)
                if read_line.startswith("\n"):
                    counter = counter + 1
            elif flag == "Writing":
                if read_line != "\n":
                    self.split_str(dict[flag], read_line)
                if read_line.startswith("\n"):
                    counter = counter + 1
            elif flag == "Meetings":
                if read_line != "\n":
                    self.split_str(dict[flag], read_line)
                if read_line.startswith("\n"):
                    counter = counter + 1

            # when counter=2, means it has reached to another title
            if counter == 2:
                counter = 0
                flag = None

        return dict

    # split each line of data into {content:[], date[]} format
    def split_str(self, row, content):
        # if there exist a range of time (xx/xx/xx - xx/xx/xx)
        if content[11:12] == "-":
            date1 = dateparser.parse(content[2:10]).strftime("%y%m%d")
            date2 = dateparser.parse(content[13:21]).strftime("%y%m%d")
            period = date1 + date2
            row["Date"].append(period)  # include two dates, which is a period

            content = content[22:(len(content) - 1)].replace("\n", "")
            row["Content"].append(content)

        # no range of time, just a single date
        else:
            cur_date = dateparser.parse(content[2:10]).strftime(
                "%y%m%d")  # for a single date, there are at most 8 characters
            row["Date"].append(cur_date)

            content = content[11:(len(content) - 1)].replace("\n", "")
            row["Content"].append(content)

    def check_sections(self, name, sections):
        # transfer list to set then use the reduce operation
        missed_sections = list(set(self.section_list) - set(sections))
        if missed_sections:
            print(name + " misses following sections:")

            for i in missed_sections:
                print(i)
        else:
            print(name + " does not miss any section.")

    def check_attend(self, name, meetings):
        missed_meetings = list(set(self.meeting_list) - set(meetings))
        if missed_meetings:
            print(name + " misses following meetings:")

            for i in missed_meetings:
                print(i)
        else:
            print(name + " does not miss any meeting.")

    def output_data(self, in_data, file_name):
        # write file with yaml data format
        stream = file(file_name, "w")
        yaml.dump(in_data, stream)  # write a yaml representation of data to 'data_parsing.yaml'
        print(yaml.dump(in_data))

    def display_section_date(self, dictionary, name):
        if name:
            if name not in self.section_list:
                print("Section name is wrong.")
            else:
                print(dictionary[name]["Date"])
        else:
            for i in self.section_list:
                print(dictionary[i]["Date"])

    def display_all_info(self, dictionary):
        print(dictionary)
        print(dictionary["Logistic"])
        print(dictionary["Theory"])
        print(dictionary["Practice"])
        print(dictionary["Writing"])
        print(dictionary["Meetings"])

    def run_single_file(self, file_path):
        # split the file name through a completely file path
        file_name = os.path.split(file_path)[-1]

        with open(file_path, 'r') as f:
            read_lines = f.readlines()
            (converted_lines, my_sections) = self.convert_data(read_lines)
            # print(converted_lines)

            raw_result = self.extract_data(converted_lines)

            # self.display_all_info(raw_result)

            section_name = "Meetings"
            self.display_section_date(raw_result, section_name)

            self.check_sections(file_name, my_sections)
            self.check_attend(file_name, raw_result["Meetings"]["Date"])

            # define the output file name (yaml file), correspond to input file name
            out_str = file_path + "_data_parsing" + ".yaml"
            print("\n---------------------------------" + file_name + " data---------------------------------")
            self.output_data(raw_result, out_str)

    def run_all_files(self, file_dir):
        # find all notebook files (begin with notebook) in the current directory
        files = glob.glob(file_dir)  # combine to a completely file path

        # read all files in this directory
        for my_file in files:
            try:
                print(my_file + "\n")
                file_name = os.path.split(my_file)[-1]

                # read notebook*.md files
                with open(my_file, "r") as f:
                    read_lines = f.readlines()
                    (converted_lines, my_sections) = self.convert_data(read_lines)
                    # print(converted_lines)

                    raw_result = self.extract_data(converted_lines)

                    # self.display_all_info(raw_result)

                    section_name = "Meetings"
                    self.display_section_date(raw_result, section_name)

                    self.check_sections(file_name, my_sections)
                    self.check_attend(file_name, raw_result["Meetings"]["Date"])

                    # define the output file name (yaml file), correspond to input file name
                    out_str = my_file + "_data_parsing" + ".yaml"
                    print("\n---------------------------------" + file_name + " data---------------------------------")
                    self.output_data(raw_result, out_str)

            except IOError as exc:
                if exc.errno != errno.EISDIR:
                    raise
