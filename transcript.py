# This work is done by group __:
# Llegue, Tim Kaiser L.     2024-04875-MN-0, 25%
# Alindogan, Hanniel II D.  2024-02554-MN-0, 25%
# Monreal, Xancho Bryan G.  2024-01561-MN-0, 25%
# Antiquera, Simeon III B.  2024-05025-MN-0, 25%

import pandas as pd
import sys
import time
import os
import statistics

def startFeature():
    print("\033[1mWelcome to the PUP Student Transcript Generation System!\033[0;0m")
    while True:
        print("=" * 55)
        print("Select Student Level:")
        print("U: Undergraduate")
        print("G: Graduate")
        print("B: Both Undergraduate and Graduate")
        print("=" * 55)
        stdLevel = input("Select student level: ").upper().strip()
        if stdLevel not in ["U", "G", "B"]:
            print("\033[1mInvalid student level. Please try again.\033[0;0m")
            continue
        if stdLevel == "B":
            stdLevel = ["U","G"]
            if stdLevel == ["U","G"]:
                print("\nSelect Degree Level: ")
                print("M: Master")
                print("D: Doctorate")
                print("B0: Both Master and Doctorate")
                print("=" * 55)
                stdDegree = input("For Graduate level, select the degree: ").upper().strip()
                if stdDegree not in ["M", "D", "B0"]:
                    print("\033[1mInvalid student level. Please try again.\033[0;0m")
                    continue
                if stdDegree == "B0":
                    stdDegree = ["B","M","D"]
                elif stdDegree == "M":
                    stdDegree = ["B","M"]
                elif stdDegree == "D":
                    stdDegree = ["B","D"]
        elif stdLevel == "U":
            stdLevel = "U"
            stdDegree = "B"
        elif stdLevel == "G":
            stdLevel = "G"
            if stdLevel == "G":
                print("M: Master")
                print("D: Doctorate")
                print("B0: Both Master and Doctorate")
                stdDegree = input("For Graduate level, select the degree: ").upper()
                if stdDegree not in ["M", "D", "B0"]:
                    print("\033[1mInvalid student level. Please try again.\033[0;0m")
                    continue
                if stdDegree == "B0":
                    stdDegree = ["M","D"]
                elif stdDegree == "M":
                    stdDegree = "M"
                elif stdDegree == "D":
                    stdDegree = "D"

                # Load the data from the CSV file
        try:
            dataFrame = pd.read_csv("studentDetails.csv")
        except FileNotFoundError:
            print("Error: 'studentDetails.csv' file not found. Please ensure it is in the same directory.")
            sys.exit(1)

        while True:
            try:
                # Ask the user for their student ID
                stdID = int(input("\nEnter Student ID: "))

                # Check whether the student's ID exists in the database
                df_results = dataFrame[dataFrame["stdID"] == stdID]

                if not df_results.empty:  # If the ID is valid
                    print("\nStudent ID validated. Proceeding to the menu...\n")
                    clearOutput(-2)
                    menuFeature(stdLevel, stdDegree, stdID)
                    break  # Exit the loop once a valid ID is provided
                else:
                    # If the ID is invalid
                    print("\nInvalid ID. Please try again.")
            except ValueError:
                print("\nInvalid input. Please enter a valid numeric Student ID.")

def menuFeature(stdLevel, stdDegree, stdID):
    requestCounter = 0
    while True:
        print("       \033[1mStudent Transcript Generation System Menu\033[0;0m")
        print("=" * 55)
        print("1. Student details")
        print("2. Statistics")
        print("3. Transcript based on major courses")
        print("4. Transcript based on minor courses")
        print("5. Full transcript")
        print("6. Previous transcript requests")
        print("7. Select Another student")
        print("8. Terminate the system")
        print("=" * 55)
        choice = input("\033[1mEnter your feature: \033[0;0m")

        if choice == "1":
            requestCounter += 1
            detailsFeature(stdID, stdLevel, stdDegree)
        elif choice == "2":
            requestCounter += 1
            statisticsFeature(stdID, stdDegree, stdLevel)  # Ensure parameters are passed correctly
        elif choice == "3":
            requestCounter += 1
            majorTranscriptFeature(stdID, stdDegree, stdLevel)
        elif choice == "4":
            requestCounter += 1
            minorTranscriptFeature(stdID, stdDegree, stdLevel)
        elif choice == "5":
            requestCounter += 1
            fullTranscriptFeature(stdID, stdDegree, stdLevel)
        elif choice == "6":
            requestCounter += 1
            previousRequestsFeature()
        elif choice == "7":
            requestCounter = 0
            newStudentFeature()
            break  # Exit the menu loop for a new student
        elif choice == "8":
            terminateFeature(requestCounter)
            break  # Exit the menu loop and end the program
        else:
            print("Invalid input. Please try again.")

def detailsFeature(stdID, stdLevel, stdDegree):
    # Reads the csv file and is then entered as the value of the variable dataFrame
    dataFrame = pd.read_csv("studentDetails.csv")
    stdDetail = dataFrame[dataFrame["stdID"] == stdID]

    # Initializes the txt file
    stdDetail_txt = ""

    # Initializes term text to be displayed
    term = ""
    rowLen = len(stdDegree)

    for i in range(rowLen):
        if i == 0:
            term += str(stdDetail.Terms.iloc[0])
        if i != 0:
            term += ", " + str(stdDetail.Terms.iloc[i])
    # Inputs information to the txt file
    stdDetail_txt += (f"Name: {stdDetail.Name.iloc[0]}\n"
                      f"stdID: {stdID}\n"
                      f"Level(s): {', '.join(stdLevel)}\n"
                      f"Number of Terms: {term}\n"
                      f"College(s): {stdDetail.College.iloc[0]}\n"
                      f"Department(s): {stdDetail.Department.iloc[0]}\n")

    print("\n" + stdDetail_txt)

    with open(f"{stdID}details.txt", "w") as f:
        f.write(stdDetail_txt)
        f.close()

    # Clears the screen followed by a short sleep and then proceeds to the menu feature again
    clearOutput(0)

def statisticsFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data
        dataFrame = pd.read_csv(f"{stdID}.csv")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    stat_txt = ""  # To store the statistics output text

    # Process each degree
    for degree in stdDegree:
        degreeDf = dataFrame[dataFrame["Degree"].str.contains(degree, na=False)]
        if degreeDf.empty:
            print(f"No data found for degree: {degree}")
            continue

        # Prepare the statistics header
        level_type = "Undergraduate" if stdLevel == "U" else f"Graduate({degree})"
        stat_txt += f"""
{'=' * 63}
 ******************   {level_type} Level   ******************
{'=' * 63}
"""

        # Compute overall and term averages
        try:
            overall_avg = round(statistics.mean(degreeDf["Grade"]), 2)
            overall_weighted_avg = round(sum(degreeDf["Grade"] * degreeDf["creditHours"]) / degreeDf["creditHours"].sum(), 2)
            stat_txt += f"Overall Average (major and minor) for all terms: {overall_avg}\n"
            stat_txt += f"Overall Weighted Average (major and minor) for all terms: {overall_weighted_avg}\n"
            stat_txt += f"Average (major and minor) of each term:\n"

            for term in degreeDf["Term"].unique():
                termDf = degreeDf[degreeDf["Term"] == term]
                term_avg = round(statistics.mean(termDf["Grade"]), 2)
                stat_txt += f"\tTerm {term}: {term_avg}\n"
        except KeyError as e:
            print(f"Missing column in data: {e}")
            return

        # Find repeated courses
        try:
            repeated_courses = degreeDf[degreeDf["courseName"].duplicated()]
            repeated_info = (
                f"Yes, {', '.join(repeated_courses['courseName'].unique())}"
                if not repeated_courses.empty
                else "No"
            )
        except KeyError as e:
            print(f"Missing column in data: {e}")
            return

        # Find maximum and minimum grades
        try:
            max_grade_row = degreeDf.loc[degreeDf["Grade"].idxmax()]
            min_grade_row = degreeDf.loc[degreeDf["Grade"].idxmin()]

            stat_txt += f"""
Maximum grade(s) and in which term(s): Term {max_grade_row['Term']}, Grade {max_grade_row['Grade']}
Minimum grade(s) and in which term(s): Term {min_grade_row['Term']}, Grade {min_grade_row['Grade']}
Do you have any repeated course(s)?: {repeated_info}
"""
        except KeyError as e:
            print(f"Missing column in data: {e}")
            return

    # Print the statistics
    print(stat_txt)

    # Save the statistics to a file
    try:
        with open(f"{stdID}Statistics.txt", "w") as f:
            f.write(stat_txt)
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Return to the menu
    clearOutput(5)

def majorTranscriptFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data
        dataFrame = pd.read_csv(f"{stdID}.csv")
        studentDetails = pd.read_csv("studentDetails.csv")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Filter student details
    student = studentDetails[studentDetails["stdID"] == stdID]
    if student.empty:
        print(f"No details found for student ID: {stdID}")
        return

    # Prepare the transcript header
    transcript_txt = f"""
Name: {student['Name'].iloc[0]:<26} stdID: {stdID:<15}
College: {student['College'].iloc[0]:<23} Department: {student['Department'].iloc[0]:<15}
Major: {student['Major'].iloc[0]:<25} Minor: {student['Minor'].iloc[0]:<15}
Level: {', '.join(stdLevel):<25} Number of terms: {student['Terms'].iloc[0]:<15}
"""

    overall_major_sum = 0
    total_terms = 0
    term_averages = []

    # Separate processing for undergraduate and graduate levels
    for level in stdLevel:
        level_courses = dataFrame[(dataFrame["Level"] == level) & (dataFrame["courseType"] == "Major")]
        if level_courses.empty:
            continue

        # Process each term
        for term in level_courses.Term.unique():
            termDf = level_courses[level_courses["Term"] == term]
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"{'':^9} {'Term ' + str(term):^35} {'':^9}\n"
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"Course ID   Course Name            Credit Hours   Grade\n"
            transcript_txt += f"{'-' * 55}\n"

            for _, course in termDf.iterrows():
                transcript_txt += (
                    f"{course['courseID']:<12}{course['courseName']:<23}"
                    f"{course['creditHours']:<16}{course['Grade']}\n"
                )

            # Compute the term's major average
            if not termDf.empty:
                term_major_avg = round(statistics.mean(termDf["Grade"]),2)
                term_averages.append(term_major_avg)
                overall_major_sum += sum(termDf["Grade"])
                total_terms += 1
            else:
                term_major_avg = 0

            # Compute the overall average, adjusting per term based on the mean of term averages
            overall_avg = round(statistics.mean(term_averages), 2) if term_averages else 0

            # Add averages to the transcript
            transcript_txt += f"\nMajor Average = {term_major_avg:<15} Overall Average = {overall_avg}\n"

        transcript_txt += f"{'=' * 55}\n"
        transcript_txt += f"{'**** End of Transcript for Level (' + level + ') ****':^55}\n"
        transcript_txt += f"{'=' * 55}\n\n\n\n"

    # Print the transcript
    print(transcript_txt)

    # Save the transcript to a file
    with open(f"{stdID}MajorTranscript.txt", "w") as f:
        f.write(transcript_txt)

    # Return to the menu
    clearOutput(5)

def minorTranscriptFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data
        dataFrame = pd.read_csv(f"{stdID}.csv")
        studentDetails = pd.read_csv("studentDetails.csv")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Filter student details
    student = studentDetails[studentDetails["stdID"] == stdID]
    if student.empty:
        print(f"No details found for student ID: {stdID}")
        return

    # Prepare the transcript header
    transcript_txt = f"""
Name: {student['Name'].iloc[0]:<26} stdID: {stdID:<15}
College: {student['College'].iloc[0]:<23} Department: {student['Department'].iloc[0]:<15}
Major: {student['Major'].iloc[0]:<25} Minor: {student['Minor'].iloc[0]:<15}
Level: {', '.join(stdLevel):<25} Number of terms: {student['Terms'].iloc[0]:<15}
"""

    overall_minor_sum = 0
    total_terms = 0
    term_averages = []

    # Separate processing for undergraduate and graduate levels
    for level in stdLevel:
        level_courses = dataFrame[(dataFrame["Level"] == level) & (dataFrame["courseType"] == "Minor")]
        if level_courses.empty:
            continue

        # Process each term
        for term in level_courses.Term.unique():
            termDf = level_courses[level_courses["Term"] == term]
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"{'':^9} {'Term ' + str(term):^35} {'':^9}\n"
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"Course ID   Course Name            Credit Hours   Grade\n"
            transcript_txt += f"{'-' * 55}\n"

            for _, course in termDf.iterrows():
                transcript_txt += (
                    f"{course['courseID']:<12}{course['courseName']:<23}"
                    f"{course['creditHours']:<16}{course['Grade']}\n"
                )

            # Compute the term's minor average
            if not termDf.empty:
                term_minor_avg = round(statistics.mean(termDf["Grade"]), 2)
                term_averages.append(term_minor_avg)
                overall_minor_sum += sum(termDf["Grade"])
                total_terms += 1
            else:
                term_minor_avg = 0

            # Compute the overall average, adjusting per term based on the mean of term averages
            overall_avg = round(statistics.mean(term_averages), 2) if term_averages else 0

            # Add averages to the transcript
            transcript_txt += f"\nMinor Average = {term_minor_avg:<15} Overall Average = {overall_avg}\n"

        transcript_txt += f"{'=' * 55}\n"
        transcript_txt += f"{'**** End of Transcript for Level (' + level + ') ****':^55}\n"
        transcript_txt += f"{'=' * 55}\n\n\n\n"

    # Print the transcript
    print(transcript_txt)

    # Save the transcript to a file
    with open(f"{stdID}MinorTranscript.txt", "w") as f:
        f.write(transcript_txt)

    # Return to the menu
    clearOutput(5)

def fullTranscriptFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data
        dataFrame = pd.read_csv(f"{stdID}.csv")
        studentDetails = pd.read_csv("studentDetails.csv")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Filter student details
    student = studentDetails[studentDetails["stdID"] == stdID]
    if student.empty:
        print(f"No details found for student ID: {stdID}")
        return

    # Prepare the transcript header
    transcript_txt = f"""
Name: {student['Name'].iloc[0]:<26} stdID: {stdID:<15}
College: {student['College'].iloc[0]:<23} Department: {student['Department'].iloc[0]:<15}
Major: {student['Major'].iloc[0]:<25} Minor: {student['Minor'].iloc[0]:<15}
Level: {', '.join(stdLevel):<25} Number of terms: {student['Terms'].iloc[0]:<15}
"""

    overall_major_sum = 0
    overall_minor_sum = 0
    overall_total_grades = 0
    overall_total_courses = 0
    major_term_averages = []
    minor_term_averages = []
    overall_term_averages = []

    for level in stdLevel:
        transcript_txt += f"\n{'=' * 55}\n{' Full Transcript for Level ' + level:^55}\n{'=' * 55}\n"

        # Process both major and minor courses for the level
        level_courses = dataFrame[dataFrame["Level"] == level]
        if level_courses.empty:
            continue

        # Process each term for the level
        for term in level_courses.Term.unique():
            termDf = level_courses[level_courses["Term"] == term]
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"{'':^9} {'Term ' + str(term):^35} {'':^9}\n"
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"Course ID   Course Name            Credit Hours   Grade\n"
            transcript_txt += f"{'-' * 55}\n"

            term_grades = []  # List to store all grades for the term

            for _, course in termDf.iterrows():
                transcript_txt += (
                    f"{course['courseID']:<12}{course['courseName']:<23}"
                    f"{course['creditHours']:<16}{course['Grade']:<8}\n"
                )
                term_grades.append(course['Grade'])  # Add grade to term_grades list

            # Calculate term averages for major and minor
            major_courses = termDf[termDf["courseType"] == "Major"]
            minor_courses = termDf[termDf["courseType"] == "Minor"]

            # Major average for this term
            if not major_courses.empty:
                term_major_avg = round(statistics.mean(major_courses["Grade"]), 2)
                major_term_averages.append(term_major_avg)
                overall_major_sum += sum(major_courses["Grade"])
            else:
                term_major_avg = 0

            # Minor average for this term
            if not minor_courses.empty:
                term_minor_avg = round(statistics.mean(minor_courses["Grade"]), 2)
                minor_term_averages.append(term_minor_avg)
                overall_minor_sum += sum(minor_courses["Grade"])
            else:
                term_minor_avg = 0

            # Calculate overall term average (including both major and minor courses)
            term_avg = round(statistics.mean(term_grades), 2)
            overall_term_averages.append(term_avg)
            overall_total_grades += sum(term_grades)
            overall_total_courses += len(term_grades)

            # Calculate overall average up to this term (cumulative average of all processed grades)
            overall_avg = round(overall_total_grades / overall_total_courses, 2)

            # Add term averages and overall averages to the transcript
            transcript_txt += f"\nMajor Average = {term_major_avg:<14} Minor Average = {term_minor_avg:<15}\n"
            transcript_txt += f"Term Average = {term_avg:<15} Overall Average = {overall_avg:<20}\n"

        # Add overall averages for this level after processing all terms
        transcript_txt += f"\n{'=' * 55}\n"
        transcript_txt += f"{'**** End of Transcript for Level (' + level + ') ****':^55}\n"
        transcript_txt += f"{'=' * 55}\n"

    # Print the transcript
    print(transcript_txt)

    # Save the transcript to a file
    with open(f"{stdID}FullTranscript.txt", "w") as f:
        f.write(transcript_txt)

    # Return to the menu
    clearOutput(5)

def newStudentFeature():
    print("Preparing for a new student...")
    clearOutput(-2)
    print("Redirecting you to the main menu...")
    clearOutput(-2)

def terminateFeature(requestCounter):
    print("Terminating the program. . .")
    clearOutput(-2)
    print(f"{'*' * 60}\nNumber of request: {requestCounter}\nThank you for using the Student Transcript Generation System\n{'*' * 60}")
    sys.exit()

def clearOutput(x):
    # Wait for 3 seconds
    time.sleep(5+x)
    # Clear output
    def clear(): return os.system('cls')
    clear()

startFeature()
