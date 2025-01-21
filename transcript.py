import pandas as pd
import sys
import time
import os

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
            detailsFeature(stdID, stdLevel, stdDegree)
        elif choice == "2":
            statisticsFeature(stdID, stdDegree, stdLevel)  # Ensure parameters are passed correctly
        elif choice == "3":
            majorTranscriptFeature(stdID, stdDegree, stdLevel)
        elif choice == "4":
            minorTranscriptFeature(stdID, stdDegree, stdLevel)
        elif choice == "5":
            fullTranscriptFeature()
        elif choice == "6":
            previousRequestsFeature()
        elif choice == "7":
            newStudentFeature()
            break  # Exit the menu loop for a new student
        elif choice == "8":
            terminateFeature()
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
                      f"Level(s): {stdLevel}\n"
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
    # Reads the CSV file for the student
    try:
        dataFrame = pd.read_csv(f"{stdID}.csv")
    except FileNotFoundError:
        print(f"Error: File for student ID {stdID} not found.")
        return

    stat_txt = ""  # To store the statistics output text

    # Handling undergraduate statistics
    if stdLevel == "U":
        for degree in stdDegree:
            degDf = dataFrame.loc[dataFrame["Degree"].str.contains(degree)]
            stat_txt += f"""
            ======================================================
            **********   Undergraduate Level   **********
            ======================================================
            Overall Average (major and minor) for all terms: {round(degDf.Grade.mean(), 2)}
            Average (major and minor) of each term: {round(degDf.Grade.sum() / degDf.creditHours.sum(), 2)}
            """

            terms = degDf.Term.unique()
            for term in terms:
                average = round(degDf[degDf["Term"] == term]["Grade"].mean(), 2)
                stat_txt += f'\n\tTerm {term}: {average}'

            repeatedCourses = degDf[degDf.courseName.duplicated()]
            repeated = (
                f"Yes, {repeatedCourses['courseName'].iloc[0]}"
                if not repeatedCourses.empty
                else "No"
            )

            maximumGrade = degDf[degDf["Grade"] == degDf["Grade"].max()]
            minimumGrade = degDf[degDf["Grade"] == degDf["Grade"].min()]
            stat_txt += f"""
            Maximum grade(s) and in which term(s): Term - {maximumGrade["Term"].iloc[0]}, Grade - {maximumGrade["Grade"].iloc[0]} 
            Minimum grade(s) and in which term(s): Term - {minimumGrade["Term"].iloc[0]}, Grade - {minimumGrade["Grade"].iloc[0]}  
            Do you have any repeated course(s)? {repeated}
            """

    # Handling graduate or both levels
    elif stdLevel == "G" or stdLevel == ["U", "G"]:
        for degree in stdDegree:
            degDf = dataFrame.loc[dataFrame["Degree"].str.contains(degree)]
            stat_txt += f"""
            ======================================================
            **********   Graduate ({degree}) Level   **********
            ======================================================
            Overall Average (major and minor) for all terms: {round(degDf.Grade.mean(), 2)}
            Average (major and minor) of each term: {round(degDf.Grade.sum() / degDf.creditHours.sum(), 2)}
            """

            terms = degDf.Term.unique()
            for term in terms:
                average = round(degDf[degDf["Term"] == term]["Grade"].mean(), 2)
                stat_txt += f'\n\tTerm {term}: {average}'

            repeatedCourses = degDf[degDf.courseName.duplicated()]
            repeated = (
                f"Yes, {repeatedCourses['courseName'].iloc[0]}"
                if not repeatedCourses.empty
                else "No"
            )

            maximumGrade = degDf[degDf["Grade"] == degDf["Grade"].max()]
            minimumGrade = degDf[degDf["Grade"] == degDf["Grade"].min()]
            stat_txt += f"""
            Maximum grade(s) and in which term(s): Term - {maximumGrade["Term"].iloc[0]}, Grade - {maximumGrade["Grade"].iloc[0]} 
            Minimum grade(s) and in which term(s): Term - {minimumGrade["Term"].iloc[0]}, Grade - {minimumGrade["Grade"].iloc[0]}  
            Do you have any repeated course(s)? {repeated}
            """

    print(stat_txt)

    with open(f"{stdID}statistics.txt", "w") as f:
        f.write(stat_txt)

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
{'=' * 55}
"""

    overall_major_sum = 0
    overall_major_credits = 0

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
                    f"{course['courseID']:<12}{course['courseName']:<25}"
                    f"{course['creditHours']:<14}{course['Grade']}\n"
                )

            # Compute averages
            if not termDf.empty:
                term_major_avg = round(termDf["Grade"].sum() / termDf["creditHours"].sum(), 2)
                overall_major_sum += termDf["Grade"].sum()
                overall_major_credits += termDf["creditHours"].sum()
            else:
                term_major_avg = 0

            overall_avg = round(overall_major_sum / overall_major_credits, 2) if overall_major_credits > 0 else 0

            # Add averages to the transcript
            transcript_txt += f"\nMajor Average = {term_major_avg:<15} Overall Average = {overall_avg}\n"

        transcript_txt += f"{'=' * 55}\n"
        transcript_txt += f"{'****** End of Transcript for Level (' + level + ') ******':^55}\n"
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
{'=' * 55}
"""

    overall_minor_sum = 0
    overall_minor_credits = 0

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
                    f"{course['courseID']:<12}{course['courseName']:<25}"
                    f"{course['creditHours']:<14}{course['Grade']}\n"
                )

            # Compute averages
            if not termDf.empty:
                term_minor_avg = round(termDf["Grade"].sum() / termDf["creditHours"].sum(), 2)
                overall_minor_sum += termDf["Grade"].sum()
                overall_minor_credits += termDf["creditHours"].sum()
            else:
                term_minor_avg = 0

            overall_avg = round(overall_minor_sum / overall_minor_credits, 2) if overall_minor_credits > 0 else 0

            # Add averages to the transcript
            transcript_txt += f"\nMinor Average = {term_minor_avg:<15} Overall Average = {overall_avg}\n"

        transcript_txt += f"{'=' * 55}\n"
        transcript_txt += f"{'****** End of Transcript for Level (' + level + ') ******':^55}\n"
        transcript_txt += f"{'=' * 55}\n\n\n\n"

    # Print the transcript
    print(transcript_txt)

    # Save the transcript to a file
    with open(f"{stdID}MinorTranscript.txt", "w") as f:
        f.write(transcript_txt)

    # Return to the menu
    clearOutput(5)


def clearOutput(x):
    # Wait for 3 seconds
    time.sleep(5+x)
    # Clear output
    def clear(): return os.system('cls')
    clear()

startFeature()
