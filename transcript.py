# This work is done by group __:
# Llegue, Tim Kaiser L.     2024-04875-MN-0, 25%
# Alindogan, Hanniel II D.  2024-02554-MN-0, 25%
# Monreal, Xancho Bryan G.  2024-01561-MN-0, 25%
# Antiquera, Simeon III B.  2024-05025-MN-0, 25%

import sys
import os
import statistics
import pandas as pd
import time
from datetime import datetime, date

def startFeature():
    print("\033[1mWelcome to the PUP Student Transcript Generation System!\033[0;0m") # Display the welcome message
    
    while True: 
        # Display menu for selecting student level 
        print("=" * 55)
        print("Select Student Level:")
        print("U: Undergraduate")
        print("G: Graduate")
        print("B: Both Undergraduate and Graduate")
        print("=" * 55)
        
        # Input for student level selection
        stdLevel = input("Select student level (Enter to start over): ").upper().strip()
        
        # Restart the feature if input is empty
        if stdLevel == "":
            clearOutput(0)
            startFeature()
        
        # Validate student level input
        if stdLevel not in ["U", "G", "B"]:
            print("\033[1mInvalid student level. Please try again.\033[0;0m")
            continue
        
        # If "B" is selected, prompt for graduate degree levels
        if stdLevel == "B":
            stdLevel = ["U", "G"]          
            if stdLevel == ["U", "G"]:
                print("\nSelect Degree Level: ")
                print("M: Master")
                print("D: Doctorate")
                print("B0: Both Master and Doctorate")
                print("=" * 55)
                
                # Input for degree level selection 
                stdDegree = input("For Graduate level, select the degree (Enter to start over): ").upper().strip()
                if stdDegree == "":# Restart the feature if input is empty
                    clearOutput(0)
                    startFeature()
                    
                if stdDegree not in ["M", "D", "B0"]:  # Validate degree level input
                    print("\033[1mInvalid student level. Please try again.\033[0;0m")
                    continue
                    
                if stdDegree == "B0": # Assign degree levels based on user input
                    stdDegree = ["B", "M", "D"]
                elif stdDegree == "M":
                    stdDegree = ["B", "M"]
                elif stdDegree == "D":
                    stdDegree = ["B", "D"]
        
        # If "U" is selected, assign undergraduate level and default degree
        elif stdLevel == "U":
            stdLevel = ["U"]
            stdDegree = ["BS1"]
        
        # If "G" is selected, prompt for graduate degree levels
        elif stdLevel == "G":
            stdLevel = ["G"]
            if stdLevel == ["G"]:
                print("\nSelect Degree Level: ")
                print("M: Master")
                print("D: Doctorate")
                print("B0: Both Master and Doctorate")
                print("=" * 55)
                
                # Input for degree level selection
                stdDegree = input("For Graduate level, select the degree (Enter to start over): ").upper().strip()
                 
                if stdDegree == "": # Restart the feature if input is empty
                    clearOutput(0)
                    startFeature()
                
                if stdDegree not in ["M", "D", "B0"]: # Validate degree level input
                    print("\033[1mInvalid student level. Please try again.\033[0;0m")
                    continue  
                # Assign degree levels based on user input
                if stdDegree == "B0":
                    stdDegree = ["M", "D"]
                elif stdDegree == "M":
                    stdDegree = ["M"]
                elif stdDegree == "D":
                    stdDegree = ["D"]

        # Attempt to load student data from the CSV file
        try:
            dataFrame = pd.read_csv("studentDetails.csv")
        except FileNotFoundError:
            print("Error: 'studentDetails.csv' file not found. Please ensure it is in the same directory.")
            sys.exit(1)

        # Loop for validating student ID
        while True:
            try:         
                user_input = input("\nEnter Student ID (Enter to start over): ")
                if user_input == "": # Restart the feature if input is empty
                    clearOutput(0)
                    startFeature()
                stdID = int(user_input)
                df_results = dataFrame[dataFrame["stdID"] == stdID] # Check if the student ID exists in the database

                if not df_results.empty:  # Valid student ID
                    print("\nStudent ID validated. Proceeding to the menu...\n")
                    clearOutput(3)
                    menuFeature(stdLevel, stdDegree, stdID)
                    break  # Exit loop once ID is validated
                else:
                    print("\nInvalid ID. Please try again.")  # No ID found
            except ValueError:
                print("\nInvalid input. Please enter a valid numeric Student ID.")  # Invalid input message


def menuFeature(stdLevel, stdDegree, stdID):
    requestCounter = 0   # Initialize a counter to track the number of requests made during the session

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

        choice = input("\033[1mEnter your feature: \033[0;0m") # Get the user's menu choice

        # repititiom structure to display features 
        if choice == "1":
            requestCounter += 1 # Increment request counter
            featureRequests("Student Details", stdID)  
            detailsFeature(stdID, stdLevel, stdDegree)  
        elif choice == "2":
            requestCounter += 1 # Increment request counter
            featureRequests("Statistics", stdID)
            statisticsFeature(stdID, stdDegree, stdLevel)  
        elif choice == "3":
            requestCounter += 1 # Increment request counter
            featureRequests("Major Transcript", stdID)
            majorTranscriptFeature(stdID, stdDegree, stdLevel)
        elif choice == "4":
            requestCounter += 1 # Increment request counter
            featureRequests("Minor Transcript", stdID)
            minorTranscriptFeature(stdID, stdDegree, stdLevel)
        elif choice == "5":
            requestCounter += 1 # Increment request counter
            featureRequests("Full Transcript", stdID)
            fullTranscriptFeature(stdID, stdDegree, stdLevel)
        elif choice == "6":
            requestCounter += 1 # Increment request counter
            featureRequests("Previous Request", stdID)
            previousRequestsFeature(stdID, stdDegree, stdLevel)
        elif choice == "7":
            requestCounter += 1 # Increment request counter
            newStudentFeature()  # Functionality to select a new student
            break  # Exit the menu loop for a new student

        # Option 8: Terminate the system
        elif choice == "8":
            terminateFeature(requestCounter)  # Handle termination logic
            break  # Exit the menu loop and end the program
        else:
            print("Invalid input. Please try again.")


def detailsFeature(stdID, stdLevel, stdDegree):
    dataFrame = pd.read_csv("studentDetails.csv") # Reads the student details from the CSV file into a DataFrame
    stdDetail = dataFrame[dataFrame["stdID"] == stdID]# Filters the DataFrame to find the specific student by their ID
    stdDetail_txt = ""
    term = ""
    rowLen = len(stdDegree) # Number of degree levels associated with the student

    # Concatenate terms based on the number of degree levels
    for i in range(rowLen):
        if i == 0:
            term += str(stdDetail.Terms.iloc[0])  # Add the first term
        else:
            term += ", " + str(stdDetail.Terms.iloc[i])  # Add subsequent terms with a comma separator

    # Construct the student's detail string
    stdDetail_txt += (f"Name: {stdDetail.Name.iloc[0]}\n"
                      f"stdID: {stdID}\n"
                      f"Level(s): {', '.join(stdLevel)}\n"
                      f"Number of Terms: {term}\n"
                      f"College(s): {stdDetail.College.iloc[0]}\n"
                      f"Department(s): {stdDetail.Department.iloc[0]}\n")

    print("\n" + stdDetail_txt)

    # Write the student details to a text file named after the student's ID
    with open(f"{stdID}details.txt", "w") as f:
        f.write(stdDetail_txt)  # Save the details
        f.close()

    # Clears the screen, waits for a short duration, and returns to the menu feature
    clearOutput(5)


def statisticsFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data from CSV file named after student ID
        dataFrame = pd.read_csv(f"{stdID}.csv")
    except FileNotFoundError as e:
        # Handle case where file is not found
        print(f"Error: {e}")
        return
    except pd.errors.EmptyDataError as e:
        # Handle case where the file is empty
        print(f"Error: The file is empty. {e}")
        return
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return

    stat_txt = ""

    # Process each degree provided in the list
    for degree in stdDegree:
        # Filter data for the current degree
        degreeDf = dataFrame[dataFrame["Degree"].str.contains(degree, na=False)]
        if degreeDf.empty:
            # Handle case where no data is found for the degree
            print(f"No data found for degree: {degree}")
            continue

        # Prepare header based on student level (Undergraduate or Graduate)
        level_type = "Undergraduate" if stdLevel == "U" else f"Graduate({degree})"
        stat_txt += f"""
{'=' * 63}
  ******************   {level_type} Level   ******************
{'=' * 63}
"""

        # Compute overall and term averages for grades
        try:
            # Calculate overall average and overall weighted average
            overall_avg = round(statistics.mean(degreeDf["Grade"]), 2)
            overall_weighted_avg = round(
                sum(degreeDf["Grade"] * degreeDf["creditHours"]) / degreeDf["creditHours"].sum(), 2)
            stat_txt += f"Overall Average (major and minor) for all terms: {overall_avg}\n"
            stat_txt += f"Overall Weighted Average (major and minor) for all terms: {overall_weighted_avg}\n"
            stat_txt += f"Average (major and minor) of each term:\n"

            # Calculate average for each term
            for term in degreeDf["Term"].unique():
                termDf = degreeDf[degreeDf["Term"] == term]
                term_avg = round(statistics.mean(termDf["Grade"]), 2)
                stat_txt += f"\tTerm {term}: {term_avg}\n"
        except KeyError as e:
            # Handle missing columns for averages
            print(f"Missing column in data: {e}")
            return

        # Find repeated courses in the degree
        try:
            repeated_courses = degreeDf[degreeDf["courseName"].duplicated()]
            repeated_info = (
                f"Yes, {', '.join(repeated_courses['courseName'].unique())}"
                if not repeated_courses.empty
                else "No"
            )
        except KeyError as e:
            # Handle missing column for course names
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
            # Handle missing columns for grades and terms
            print(f"Missing column in data: {e}")
            return

    # Print the statistics text
    print(stat_txt)

    # Save the statistics to a text file
    try:
        with open(f"{stdID}Statistics.txt", "w") as f:
            f.write(stat_txt)
    except Exception as e:
        # Handle errors when writing to the file
        print(f"Error writing to file: {e}")

    # Call a function to clear the output (assuming it's defined elsewhere)
    clearOutput(10)

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
                term_major_avg = round(statistics.mean(termDf["Grade"]), 2)
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
    clearOutput(10)


def minorTranscriptFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data from CSV files
        dataFrame = pd.read_csv(f"{stdID}.csv")  # Student's grade and course data
        studentDetails = pd.read_csv("studentDetails.csv")  # General student details
    except FileNotFoundError as e:
        # Handle case where the file is not found
        print(f"Error: {e}")
        return

    # Filter the student details using the provided student ID
    student = studentDetails[studentDetails["stdID"] == stdID]
    if student.empty:
        # Handle case where no details are found for the student ID
        print(f"No details found for student ID: {stdID}")
        return

    # Prepare the transcript header with student and academic details
    transcript_txt = f"""
Name: {student['Name'].iloc[0]:<26} stdID: {stdID:<15}
College: {student['College'].iloc[0]:<23} Department: {student['Department'].iloc[0]:<15}
Major: {student['Major'].iloc[0]:<25} Minor: {student['Minor'].iloc[0]:<15}
Level: {', '.join(stdLevel):<25} Number of terms: {student['Terms'].iloc[0]:<15}
"""

    overall_minor_sum = 0  # Sum of all grades for minor courses
    total_terms = 0  # Number of terms with minor courses
    term_averages = []  # List to store the average for each term

    # Separate processing for undergraduate and graduate levels
    for level in stdLevel:
        # Filter courses for the given level and type "Minor"
        level_courses = dataFrame[(dataFrame["Level"] == level) & (dataFrame["courseType"] == "Minor")]
        if level_courses.empty:
            continue  # Skip if there are no minor courses for this level

        # Process each term for the current level
        for term in level_courses.Term.unique():
            termDf = level_courses[level_courses["Term"] == term]
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"{'':^9} {'Term ' + str(term):^35} {'':^9}\n"
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"Course ID   Course Name            Credit Hours   Grade\n"
            transcript_txt += f"{'-' * 55}\n"

            # List the minor courses for the current term
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
                term_minor_avg = 0  # No minor courses in the term

            # Compute the overall average for minor courses across all terms
            overall_avg = round(statistics.mean(term_averages), 2) if term_averages else 0

            # Add term and overall averages to the transcript
            transcript_txt += f"\nMinor Average = {term_minor_avg:<15} Overall Average = {overall_avg}\n"

        transcript_txt += f"{'=' * 55}\n"
        transcript_txt += f"{'**** End of Transcript for Level (' + level + ') ****':^55}\n"
        transcript_txt += f"{'=' * 55}\n\n\n\n"

    # Print the generated transcript
    print(transcript_txt)

    # Save the transcript to a text file
    with open(f"{stdID}MinorTranscript.txt", "w") as f:
        f.write(transcript_txt)

    # Call a function to clear the output (assumed to be defined elsewhere)
    clearOutput(10)


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
    clearOutput(10)


def previousRequestsFeature(stdID, stdDegree, stdLevel):
    try:
        with open(f"{stdID}PreviousRequests.txt", "r") as f:
            text = f.read()
            print()
            print(text)
    except FileNotFoundError:
        print(f"No previous requests found for student ID {stdID}.")
    clearOutput(5)


def newStudentFeature():
    print("Preparing for a new student...")
    clearOutput(3)
    print("Redirecting you to the main menu...")
    clearOutput(3)


def terminateFeature(requestCounter):
    print("Terminating the program...")
    clearOutput(3)
    print(
        f"{'=' * 60}\nNumber of request: {requestCounter}\nThank you for using the Student Transcript Generation System\n{'=' * 60}")
    sys.exit()


def featureRequests(feature: str, stdID: int):
    # Open the file in append mode and check if the header needs to be written
    with open(f"{stdID}PreviousRequests.txt", "a+") as f:
        f.seek(0)  # Move the cursor to the start of the file to check its content
        content = f.read()

        # Write header if the file is empty
        if not content.strip():
            header = f"{'Request':<20}{'Date':<15}{'Time':<10}\n"
            separator = "=" * 45 + "\n"
            f.write(header)
            f.write(separator)

        # Format the current date and time
        date_now = date.today().strftime("%d/%m/%Y")
        time_now = datetime.now().strftime("%I:%M %p")  # 12-hour format with AM/PM

        # Format the request line with proper column widths
        text = f"{feature:<20}{date_now:<15}{time_now:<10}\n"
        f.write(text)


def clearOutput(x):
    # Wait for 3 seconds
    time.sleep(x)
    # Clear output
    def clear(): return os.system('cls')
    clear()


startFeature()
