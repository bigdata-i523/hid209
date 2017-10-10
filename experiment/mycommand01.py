from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.mycommand01.api.manager import Manager
from date_parsing import DateParsing


class Mycommand01Command(PluginCommand):
    # noinspection PyUnusedLocal
    @command
    def do_mycommand01(self, args, arguments):
        """
        ::

          Usage:
                mycommand01 -f FILE
                mycommand01 -g DIR
                mycommand01 list

          This command does some useful things.

          Arguments:
              FILE   a file name
              DIR    a file directory

          Options:
              -f      specify the file
              -g      generate all yaml files

        """

        arguments.is_FILE = arguments['-f'] or None
        arguments.is_generate = arguments['-g'] or None

        print(arguments)

        m = Manager()

        if arguments.is_FILE:
            print("option a")
            m.list(arguments.FILE)

            # all variables/counters declaration
            my_path = arguments.FILE

            # define global variables
            all_sections = ["Logistic", "Theory", "Practice", "Writing",
                            "Meetings"]  # this is for a completely notebook file
            all_meetings_date = ["170825", "170901", "170908", "170915",
                                 "170922"]  # all meetings that a student need to attend

            dp = DateParsing(all_sections, all_meetings_date)
            dp.run_single_file(my_path)

        elif arguments.is_generate:
            print("option b")
            m.list(arguments.DIR)

            # all variables/counters declaration
            my_dir = arguments.DIR
            my_files_name = "notebook*.md"

            # define global variables
            all_sections = ["Logistic", "Theory", "Practice", "Writing",
                            "Meetings"]  # this is for a completely notebook file
            all_meetings_date = ["170825", "170901", "170908", "170915",
                                 "170922"]  # all meetings that a student need to attend

            dp = DateParsing(all_sections, all_meetings_date)
            dp.run_all_files(my_dir + my_files_name)

        elif arguments.list:
            print("option c")
            m.list("just calling list without parameter")
