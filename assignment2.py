#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211_Assignment2"""

import urllib2
import logging
import argparse
import datetime
import csv
import sys

def main():
    """This is the main function where the assignment2 will use
	the following url as data.
    https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv
	This week's assignment is very challenging as I am using ananconda
    with spyder at version 2.7 and Ananconda python prompt at 3.6.3.
    Both versions supports different syntax.  Had did some extensive
    researching online to sort out all the different errors from
    print statements to urllib2 not supported in Python 3.6.3 which 
    resolves to from urllib.request import urlopen if running urllib
    in python 3.6.3.
    """
    def downloadData(url):
        """A function to download the contents located at the url and return
		to the caller.
        """
        get_url = urllib2.urlopen(url)
        return get_url

    def processData(contents):
        """A function that retrieves the content of the file as the first parameter.
		processes the file line by line and returns a dictionary that maps
		a person's ID to a tuple of the form in a date format of dd/mm/yyyy.
        """
        my_dictionary = {}
        csv_file=csv.reader(contents)
        csv_file.next()

        for row in csv_file:
            try:
                row[2] = datetime.datetime.strptime(row[2], "%d/%m/%Y").date()
            except ValueError:
                number = int(row[0])
                line = int(row[0])+1
                logger = logging.getLogger("assignment 2")
                logger.error("Error processing line#{} for ID #{}.".format(line, number))
            my_dictionary[int(row[0])] = (row[1], row[2])
        return my_dictionary

    def displayPerson(id, personData):
        """A function given the id, it will display the
		personData index 0 as name,
		personData index 1 as the birthday
		"""
        try:
            response = "Person ID #{idnum} is {name} with a birthday of {date}"
            print(response.format(idnum=id, name=personData[id][0], date=personData[id][1]))
        except KeyError:
            print("There is an error on Person ID # entered.")

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to csv file.")
    args = parser.parse_args()
    logging.basicConfig(filename="errors.log", level=logging.ERROR)

    if args.url:
        csvData = downloadData(args.url)
        personData = processData(csvData)
        msg = "Please enter ID number or type 0 or a negative # to exit. "

        while True:
            try:
                user = int(raw_input(msg))
            except ValueError:
                print("Please try a different ID # or type 0 or a negative # to exit.")
                continue
            if user > 0:
                print("You have entered: "), user
                displayPerson(user, personData)
            else:
                print("You have entered: "), user
                print("Program will now exit.")
                sys.exit()
    else:
        print("Please enter URL.")

if __name__ == "__main__":
    main()
