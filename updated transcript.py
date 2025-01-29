# This work is done by group 10:
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
    # Lists to store selected student levels and degrees
    stdLevel = []
    stdDegree = []

    # Welcome message
    print("\033[1mWelcome to the PUP Student Transcript Generation System!\033[0;0m")

    # Main loop to handle the student level selection
    while True:
        # Display student level options
        print("=" * 55)
        print("Select Student Level:")
        print("U: Undergraduate")
        print("G: Graduate")
        print("B: Both Undergraduate and Graduate")
        print("=" * 55)

        # Prompt user to select a student level
        stdLevelInput = input("Select student level (Enter to start over): ").upper().strip()

        # Restart the process if input is empty
        if stdLevelInput == "":
            clearOutput(0)  # Clears the screen/output
            startFeature()  # Restart the feature
            return  # Exit the current instance of the function

        # Validate the user input for student level
        if stdLevelInput in ['U', 'G', 'B']:
            if stdLevelInput == 'U':  # Undergraduate level selected
                stdLevel.append('U')
                stdDegree.append('BS1')  # Default undergraduate degree
            elif stdLevelInput == 'G':  # Graduate level selected
                stdLevel.append('G')
            elif stdLevelInput == 'B':  # Both levels selected
                stdLevel.extend(['U', 'G'])  # Add both undergraduate and graduate levels
                stdDegree.append('BS1')  # Add undergraduate degree for both levels
        else:
            # Handle invalid input for student level
            print("\033[1mInvalid student level. Please try again.\033[0;0m")
            print()
            continue  # Re-prompt the user for a valid student level

        # If Graduate level or Both levels are selected
        if stdLevelInput in ['G', 'B']:
            while True:
                # Display degree level options
                print("\nSelect Degree Level: ")
                print("M: Master")
                print("D: Doctorate")
                print("B0: Both Master and Doctorate")
                print("=" * 55)

                # Prompt user to select a degree level for graduate studies
                stdDegreeInput = input("For Graduate level, select the degree (Enter to start over): ").upper().strip()

                # Restart the process if input is empty
                if stdDegreeInput == "":
                    clearOutput(0)  # Clears the screen/output
                    startFeature()  # Restart the feature
                    return  # Exit the current instance of the function

                # Validate the user input for graduate degree
                if stdDegreeInput in ['M', 'D', 'B0']:
                    if stdDegreeInput == 'M':  # Master's degree selected
                        stdDegree.append('M1')  # Add Master's degree
                    elif stdDegreeInput == 'D':  # Doctorate degree selected
                        stdDegree.append('D1')  # Add Doctorate degree
                    elif stdDegreeInput == 'B0':  # Both degrees selected
                        stdDegree.extend(['M1', 'D1'])  # Add both Master's and Doctorate degrees
                    break  # Exit the loop once valid input is provided
                else:
                    # Handle invalid input for degree level
                    print("\033[1mInvalid student degree. Please try again.\033[0;0m")
                    print()

        # Attempt to load student data from the CSV file
        try:
            dataFrame = pd.read_csv("studentDetails.csv")
        except FileNotFoundError:
            print("Error: 'studentDetails.csv' file not found. Please ensure it is in the same directory.")
            sys.exit(1)

        # Loop for validating student ID
        # Loop to handle user input for Student ID
        while True:
            try:
                # Prompt user to enter their Student ID
                user_input = input("\nEnter Student ID (Enter to start over): ")

                # Restart the process if input is empty
                if user_input == "":
                    clearOutput(0)  # Clears the screen/output
                    startFeature()  # Restart the feature
                    return  # Exit the current instance of the function

                # Convert the user input to an integer for validation
                stdID = int(user_input)

                # Check if the entered Student ID exists in the database
                df_results = dataFrame[dataFrame["stdID"] == stdID]

                if not df_results.empty:  # If the ID exists in the database
                    # Extract the student's level and degree(s) from the record
                    studentLevel = df_results['Level'].tolist()  # Get all levels as a list
                    studentDegree = df_results['Degree'].tolist()  # Get all degrees as a list

                    # Validate the selected student level against the student's record
                    if stdLevelInput not in studentLevel and stdLevelInput != 'B':
                        # Display error if the level doesn't match
                        print(
                            f"\033[1mError: Selected level '{stdLevelInput}' does not match student record level '{', '.join(studentLevel)}'.\033[0;0m\n")
                        continue  # Re-prompt the user for a valid ID

                    # Additional validation if both Undergraduate and Graduate levels are selected
                    if stdLevelInput == 'B' and not all(level in studentLevel for level in ['U', 'G']):
                        # Display error if both levels are not found
                        print(
                            "\033[1mError: Both Undergraduate and Graduate levels do not match the student record.\033[0;0m\n")
                        continue  # Re-prompt the user for a valid ID

                        # Validate the selected degree(s) against the student's record only if "U" wasn't selected
                    if stdLevelInput != 'U':
                        if stdDegreeInput == 'M' and 'M1' not in studentDegree:
                            # Display error if Master's degree doesn't match
                            print(
                                "\033[1mError: Selected degree 'Master' does not match student record.\033[0;0m\n")
                            continue

                        if stdDegreeInput == 'D' and 'D1' not in studentDegree:
                            # Display error if Doctorate degree doesn't match
                            print(
                                "\033[1mError: Selected degree 'Doctorate' does not match student record.\033[0;0m\n")
                            continue

                        if stdDegreeInput == 'B0' and not all(degree in studentDegree for degree in ['M1', 'D1']):
                            # Display error if both Master's and Doctorate degrees don't match
                            print(
                                "\033[1mError: Both Master and Doctorate degrees do not match student record.\033[0;0m\n")
                            continue

                    # If all validations pass
                    print("\nStudent ID validated. Proceeding to the menu...\n")
                    clearOutput(3)  # Clear the screen before proceeding
                    menuFeature(stdLevel, stdDegree, stdID)  # Navigate to the menu feature
                    break  # Exit the loop after successful validation
                else:
                    # If the ID does not exist in the database
                    print("\nInvalid ID. Please try again.")

            # Handle non-numeric input for Student ID
            except ValueError:
                print("\nInvalid input. Please enter a valid numeric Student ID.")


def menuFeature(stdLevel, stdDegree, stdID):
    requestCounter = 0  # Initialize a counter to track the number of requests made during the session

    while True:
        # Display the menu header with bold formatting
        print("       \033[1mStudent Transcript Generation System Menu\033[0;0m")
        print("=" * 55)

        # Display available menu options
        print("1. Student details")
        print("2. Statistics")
        print("3. Transcript based on major courses")
        print("4. Transcript based on minor courses")
        print("5. Full transcript")
        print("6. Previous transcript requests")
        print("7. Select Another student")
        print("8. Terminate the system")
        print("=" * 55)

        # Get the user's menu choice
        choice = input("\033[1mEnter your feature: \033[0;0m")

        # Handle user input and call the corresponding feature function
        if choice == "1":
            requestCounter += 1  # Increment request counter for tracking
            featureRequests("Student Details", stdID)  # Log request type
            detailsFeature(stdID, stdLevel, stdDegree)  # Display student details

        elif choice == "2":
            requestCounter += 1  # Increment request counter
            featureRequests("Statistics", stdID)  # Log request type
            statisticsFeature(stdID, stdDegree, stdLevel)  # Display statistics

        elif choice == "3":
            requestCounter += 1  # Increment request counter
            featureRequests("Major Transcript", stdID)  # Log request type
            majorTranscriptFeature(stdID, stdDegree, stdLevel)  # Generate major courses transcript

        elif choice == "4":
            requestCounter += 1  # Increment request counter
            featureRequests("Minor Transcript", stdID)  # Log request type
            minorTranscriptFeature(stdID, stdDegree, stdLevel)  # Generate minor courses transcript

        elif choice == "5":
            requestCounter += 1  # Increment request counter
            featureRequests("Full Transcript", stdID)  # Log request type
            fullTranscriptFeature(stdID, stdDegree, stdLevel)  # Generate full transcript

        elif choice == "6":
            requestCounter += 1  # Increment request counter
            featureRequests("Previous Request", stdID)  # Log request type
            previousRequestsFeature(stdID, stdDegree, stdLevel)  # Show previous transcript requests

        elif choice == "7":
            requestCounter += 1  # Increment request counter
            newStudentFeature()  # Functionality to select a new student
            break  # Exit the menu loop to allow a new student selection

        elif choice == "8":
            terminateFeature(requestCounter)  # Handle termination logic and log total requests
            break  # Exit the menu loop and terminate the system

        else:
            print("Invalid input. Please try again.")  # Handle invalid input


def detailsFeature(stdID, stdLevel, stdDegree):
    # Reads the student details from the CSV file into a DataFrame
    dataFrame = pd.read_csv("studentDetails.csv")

    # Filters the DataFrame to find the specific student by their ID
    stdDetail = dataFrame[dataFrame["stdID"] == stdID]

    stdDetail_txt = ""  # Initialize an empty string to store student details
    term = ""  # Initialize an empty string to store the terms
    rowLen = len(stdDegree)  # Determine the number of degree levels associated with the student

    # Concatenate terms based on the number of degree levels
    for i in range(rowLen):
        if i == 0:
            term += str(stdDetail.Terms.iloc[0])  # Add the first term
        else:
            term += ", " + str(stdDetail.Terms.iloc[i])  # Add subsequent terms with a comma separator

    # Construct a formatted string containing the student's details
    stdDetail_txt += (f"Name: {stdDetail.Name.iloc[0]}\n"
                      f"stdID: {stdID}\n"
                      f"Level(s): {', '.join(stdLevel)}\n"
                      f"Number of Terms: {term}\n"
                      f"College(s): {stdDetail.College.iloc[0]}\n"
                      f"Department(s): {stdDetail.Department.iloc[0]}\n")

    # Print the student details to the console
    print("\n" + stdDetail_txt)

    # Write the student details to a text file named after the student's ID
    with open(f"{stdID}details.txt", "w") as f:
        f.write(stdDetail_txt)  # Save the details
        f.close()  # Close the file (not strictly necessary as 'with open' handles it)

    # Clears the screen, waits for a short duration (5 seconds), and returns to the menu feature
    clearOutput(5)


def statisticsFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data from a CSV file named after the student's ID
        dataFrame = pd.read_csv(f"{stdID}.csv")
    except FileNotFoundError as e:
        # Handle case where the file does not exist
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

    stat_txt = ""  # Initialize a string to store statistics data

    # Process each degree associated with the student
    for degree in stdDegree:
        # Filter data for the current degree
        degreeDf = dataFrame[dataFrame["Degree"].str.contains(degree, na=False)]

        if degreeDf.empty:
            # Handle case where no data is found for the specified degree
            print(f"No data found for degree: {degree}")
            continue

        # Determine the correct student level type (Undergraduate or Graduate)
        if "U" in stdLevel and degree == "BS1":
            level_type = "Undergraduate"
        elif "G" in stdLevel:
            # Map degree codes to readable names
            degree_map = {"M1": "M", "D1": "D"}
            degree_label = degree_map.get(degree, degree)  # Default to original if not mapped
            level_type = f"Graduate ({degree_label})"
        else:
            level_type = "Unknown Level"

        # Create a section header for the statistics report
        stat_txt += f"""
{'=' * 63}
*******************   {level_type} Level   *******************
{'=' * 63}
"""

        # Compute overall and term-wise averages for grades
        try:
            overall_avg = round(statistics.mean(degreeDf["Grade"]), 2)  # Calculate overall average grade
            stat_txt += f"Overall Average (major and minor) for all terms: {overall_avg}\n"
            stat_txt += f"Average (major and minor) of each term:\n"

            # Compute term-wise averages
            for term in degreeDf["Term"].unique():
                termDf = degreeDf[degreeDf["Term"] == term]
                term_avg = round(statistics.mean(termDf["Grade"]), 2)
                stat_txt += f"\tTerm {term}: {term_avg}\n"
        except KeyError as e:
            # Handle missing column errors for grade computation
            print(f"Missing column in data: {e}")
            return

        # Identify repeated courses within the degree
        try:
            repeated_courses = degreeDf[degreeDf["courseName"].duplicated()]
            repeated_info = (
                f"Yes, {', '.join(repeated_courses['courseName'].unique())}"
                if not repeated_courses.empty
                else "No"
            )
        except KeyError as e:
            # Handle missing column errors for course names
            print(f"Missing column in data: {e}")
            return

        # Find the highest and lowest grades obtained
        try:
            max_grade_row = degreeDf.loc[degreeDf["Grade"].idxmax()]  # Get row with highest grade
            min_grade_row = degreeDf.loc[degreeDf["Grade"].idxmin()]  # Get row with lowest grade

            stat_txt += f"""
Maximum grade(s) and in which term(s): Term {max_grade_row['Term']}, Grade {max_grade_row['Grade']}
Minimum grade(s) and in which term(s): Term {min_grade_row['Term']}, Grade {min_grade_row['Grade']}
Do you have any repeated course(s)?: {repeated_info}
"""
        except KeyError as e:
            # Handle missing column errors for grade and term retrieval
            print(f"Missing column in data: {e}")
            return

    # Print the generated statistics report
    print(stat_txt)

    # Save the statistics to a text file named after the student's ID
    try:
        with open(f"{stdID}Statistics.txt", "w") as f:
            f.write(stat_txt)
    except Exception as e:
        # Handle errors that may occur while writing to the file
        print(f"Error writing to file: {e}")

    # Call a function to clear the output (assuming it's defined elsewhere)
    clearOutput(10)


def majorTranscriptFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data from the student's CSV file
        dataFrame = pd.read_csv(f"{stdID}.csv")
        # Load general student details from a separate CSV file
        studentDetails = pd.read_csv("studentDetails.csv")
    except FileNotFoundError as e:
        # Handle missing file error
        print(f"Error: {e}")
        return

    # Filter student details based on the given student ID
    student = studentDetails[studentDetails["stdID"] == stdID]
    if student.empty:
        # Handle case where student details are not found
        print(f"No details found for student ID: {stdID}")
        return

    # Prepare the transcript header with formatted student details
    transcript_txt = f"""
Name: {student['Name'].iloc[0]:<26} stdID: {stdID:<15}
College: {student['College'].iloc[0]:<23} Department: {student['Department'].iloc[0]:<15}
Major: {student['Major'].iloc[0]:<25} Minor: {student['Minor'].iloc[0]:<15}
Level: {', '.join(stdLevel):<25} Number of terms: {student['Terms'].iloc[0]:<15}
"""

    overall_major_sum = 0  # Sum of major course grades across all terms
    total_terms = 0  # Counter for total terms processed
    term_averages = []  # List to store term averages for major courses

    # Process each level (Undergraduate or Graduate) separately
    for level in stdLevel:
        # Filter only major courses for the given level
        level_courses = dataFrame[(dataFrame["Level"] == level) & (dataFrame["courseType"] == "Major")]
        if level_courses.empty:
            continue  # Skip processing if no major courses exist for this level

        # Process transcript data term by term
        for term in level_courses.Term.unique():
            termDf = level_courses[level_courses["Term"] == term]  # Filter courses for the specific term

            # Add term header to transcript
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"{'':^9} {'Term ' + str(term):^35} {'':^9}\n"
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"Course ID   Course Name            Credit Hours   Grade\n"
            transcript_txt += f"{'-' * 55}\n"

            # Add course details to transcript
            for _, course in termDf.iterrows():
                transcript_txt += (
                    f"{course['courseID']:<12}{course['courseName']:<23}"
                    f"{course['creditHours']:<16}{course['Grade']}\n"
                )

            # Compute the term's major course average
            if not termDf.empty:
                term_major_avg = round(statistics.mean(termDf["Grade"]), 2)
                term_averages.append(term_major_avg)  # Store term average
                overall_major_sum += sum(termDf["Grade"])  # Add term grades to overall sum
                total_terms += 1  # Increment term counter
            else:
                term_major_avg = 0  # Set default value if no major courses exist in the term

            # Compute the overall major course average across all terms
            overall_avg = round(statistics.mean(term_averages), 2) if term_averages else 0

            # Add term and overall averages to the transcript
            transcript_txt += f"\nMajor Average = {term_major_avg:<15} Overall Average = {overall_avg}\n"

        # Add a footer for the current level transcript
        transcript_txt += f"{'=' * 55}\n"
        transcript_txt += f"{'**** End of Transcript for Level (' + level + ') ****':^55}\n"
        transcript_txt += f"{'=' * 55}\n\n\n\n"

    # Print the generated transcript
    print(transcript_txt)

    # Save the transcript to a file named after the student's ID
    with open(f"{stdID}MajorTranscript.txt", "w") as f:
        f.write(transcript_txt)

    # Return to the main menu after a short delay (assumes clearOutput is defined elsewhere)
    clearOutput(10)


def minorTranscriptFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data from CSV files
        dataFrame = pd.read_csv(f"{stdID}.csv")  # Contains student's grades and course details
        studentDetails = pd.read_csv("studentDetails.csv")  # Contains general student information
    except FileNotFoundError as e:
        # Handle missing file error
        print(f"Error: {e}")
        return

    # Extract student details using stdID
    student = studentDetails[studentDetails["stdID"] == stdID]
    if student.empty:
        # Handle case where student ID is not found in details file
        print(f"No details found for student ID: {stdID}")
        return

    # Format transcript header with student details
    transcript_txt = f"""
Name: {student['Name'].iloc[0]:<26} stdID: {stdID:<15}
College: {student['College'].iloc[0]:<23} Department: {student['Department'].iloc[0]:<15}
Major: {student['Major'].iloc[0]:<25} Minor: {student['Minor'].iloc[0]:<15}
Level: {', '.join(stdLevel):<25} Number of terms: {student['Terms'].iloc[0]:<15}
"""

    # Initialize variables for storing minor course averages
    overall_minor_sum = 0  # Sum of all grades for minor courses
    total_terms = 0  # Number of terms that include minor courses
    term_averages = []  # List to store the average for each term

    # Process transcript data for each academic level (e.g., Undergraduate, Graduate)
    for level in stdLevel:
        # Filter courses for the given level that are classified as "Minor"
        level_courses = dataFrame[(dataFrame["Level"] == level) & (dataFrame["courseType"] == "Minor")]
        if level_courses.empty:
            continue  # Skip if no minor courses exist for this level

        # Process each academic term within the current level
        for term in sorted(level_courses["Term"].unique()):
            termDf = level_courses[level_courses["Term"] == term]  # Filter data for the term

            # Format the term header in the transcript
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

            # Compute the term's minor course average
            if not termDf.empty:
                term_minor_avg = round(statistics.mean(termDf["Grade"]), 2)  # Calculate average
                term_averages.append(term_minor_avg)  # Store term average for later use
                overall_minor_sum += sum(termDf["Grade"])  # Update overall minor sum
                total_terms += 1  # Increase count of terms with minor courses
            else:
                term_minor_avg = 0  # No minor courses in the term

            # Compute the overall minor course average across all terms so far
            overall_avg = round(statistics.mean(term_averages), 2) if term_averages else 0

            # Append term and overall averages to the transcript
            transcript_txt += f"\nMinor Average = {term_minor_avg:<15} Overall Average = {overall_avg}\n"

        # Mark the end of the transcript for the current level
        transcript_txt += f"{'=' * 55}\n"
        transcript_txt += f"{'**** End of Transcript for Level (' + level + ') ****':^55}\n"
        transcript_txt += f"{'=' * 55}\n\n\n\n"

    # Print the generated transcript
    print(transcript_txt)

    # Save the transcript to a text file
    try:
        with open(f"{stdID}MinorTranscript.txt", "w") as f:
            f.write(transcript_txt)
    except Exception as e:
        # Handle any errors that may occur while saving the file
        print(f"Error writing transcript to file: {e}")

    # Clear the output after a delay (assuming clearOutput is defined elsewhere)
    clearOutput(10)


def fullTranscriptFeature(stdID, stdDegree, stdLevel):
    try:
        # Load student data from CSV files
        dataFrame = pd.read_csv(f"{stdID}.csv")  # Contains student's grades and course details
        studentDetails = pd.read_csv("studentDetails.csv")  # Contains general student info
    except FileNotFoundError as e:
        # Handle missing file error
        print(f"Error: {e}")
        return

    # Extract student details using stdID
    student = studentDetails[studentDetails["stdID"] == stdID]
    if student.empty:
        # Handle case where student ID is not found in details file
        print(f"No details found for student ID: {stdID}")
        return

    # Format transcript header with student details
    transcript_txt = f"""
Name: {student['Name'].iloc[0]:<26} stdID: {stdID:<15}
College: {student['College'].iloc[0]:<23} Department: {student['Department'].iloc[0]:<15}
Major: {student['Major'].iloc[0]:<25} Minor: {student['Minor'].iloc[0]:<15}
Level: {', '.join(stdLevel):<25} Number of terms: {student['Terms'].iloc[0]:<15}
"""

    # Initialize lists to store grades for computing averages later
    overall_major_grades = []  # Stores all major course grades
    overall_minor_grades = []  # Stores all minor course grades
    overall_term_grades = []  # Stores all term grades

    # Process transcript data for each academic level (e.g., Undergraduate, Graduate)
    for level in stdLevel:
        # Add a section header for the current level
        transcript_txt += f"\n{'=' * 55}\n{' Full Transcript for Level ' + level:^55}\n{'=' * 55}\n"

        # Filter courses specific to the current level
        level_courses = dataFrame[dataFrame["Level"] == level]
        if level_courses.empty:
            continue  # Skip if no courses are found for this level

        # Process each academic term within the current level
        for term in sorted(level_courses["Term"].unique()):
            termDf = level_courses[level_courses["Term"] == term]  # Filter data for the term

            # Format the term header in the transcript
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"{'':^9} {'Term ' + str(term):^35} {'':^9}\n"
            transcript_txt += f"{'=' * 55}\n"
            transcript_txt += f"Course ID   Course Name            Credit Hours   Grade\n"
            transcript_txt += f"{'-' * 55}\n"

            term_grades = []  # Stores all grades for the current term

            # Iterate through each course in the term
            for _, course in termDf.iterrows():
                transcript_txt += (
                    f"{course['courseID']:<12}{course['courseName']:<23}"
                    f"{course['creditHours']:<16}{course['Grade']:<8}\n"
                )
                term_grades.append(course['Grade'])  # Store course grade for term calculations

            # Separate major and minor courses for the current term
            major_courses = termDf[termDf["courseType"] == "Major"]
            minor_courses = termDf[termDf["courseType"] == "Minor"]

            # Compute the term's average grade for major courses
            term_major_avg = round(statistics.mean(major_courses["Grade"]), 2) if not major_courses.empty else 0
            if not major_courses.empty:
                overall_major_grades.extend(major_courses["Grade"])  # Add to overall major grades list

            # Compute the term's average grade for minor courses
            term_minor_avg = round(statistics.mean(minor_courses["Grade"]), 2) if not minor_courses.empty else 0
            if not minor_courses.empty:
                overall_minor_grades.extend(minor_courses["Grade"])  # Add to overall minor grades list

            # Compute the overall average for this term (includes both major and minor courses)
            term_avg = round(statistics.mean(term_grades), 2) if term_grades else 0
            overall_term_grades.extend(term_grades)  # Add to overall term grades list

            # Compute the cumulative overall average across all terms so far
            overall_avg = round(statistics.mean(overall_term_grades), 2) if overall_term_grades else 0

            # Append the computed averages to the transcript
            transcript_txt += f"\nMajor Average = {term_major_avg:<14} Minor Average = {term_minor_avg:<15}\n"
            transcript_txt += f"Term Average = {term_avg:<15} Overall Average = {overall_avg:<20}\n"

        # Mark the end of the transcript for the current level
        transcript_txt += f"\n{'=' * 55}\n"
        transcript_txt += f"{'**** End of Transcript for Level (' + level + ') ****':^55}\n"
        transcript_txt += f"{'=' * 55}\n"

    # Print the final transcript
    print(transcript_txt)

    # Save the transcript to a text file
    try:
        with open(f"{stdID}FullTranscript.txt", "w") as f:
            f.write(transcript_txt)
    except Exception as e:
        # Handle any errors that may occur while saving the file
        print(f"Error writing transcript to file: {e}")

    # Clear the output after a delay (assuming clearOutput is defined elsewhere)
    clearOutput(10)


def previousRequestsFeature(stdID, stdDegree, stdLevel):
    try:
        # Attempt to open the file containing previous requests for the student
        with open(f"{stdID}PreviousRequests.txt", "r") as f:
            text = f.read()  # Read the entire content of the file
            print()  # Print an empty line for readability
            print(text)  # Print the contents of the file (previous requests)
    except FileNotFoundError:
        # If the file is not found, print an error message
        print(f"No previous requests found for student ID {stdID}.")

    # Clear the output after a brief delay (helps tidy up the interface/console)
    clearOutput(5)


def newStudentFeature():
    print("Preparing for a new student...")  # Inform the user that the system is preparing for a new student
    clearOutput(3)  # Clear the output 3 times to give the user a clean interface
    print("Redirecting you to the main menu...")  # Inform the user that they are being redirected
    clearOutput(3)  # Clear the output again for a clean transition to the next screen

    # Call the startFeature() function, presumably redirecting to the main menu or initial step
    startFeature()


def terminateFeature(requestCounter):
    print("Terminating the program...")

    # Clear the output after 3 seconds
    clearOutput(3)
    # This gives the user a summary of the session
    print(
        f"{'=' * 60}\nNumber of request: {requestCounter}\nThank you for using the Student Transcript Generation System\n{'=' * 60}")

    sys.exit()  # Stops the program execution completely


def featureRequests(feature: str, stdID: int):
    # Open the file in append mode ('a+'), allowing both reading and writing
    # If the file doesn't exist, it will be created
    with open(f"{stdID}PreviousRequests.txt", "a+") as f:
        f.seek(0)  # Move the cursor to the start of the file to check its content
        content = f.read()  # Read the current content of the file

        # If the file is empty, write the header for the request log
        if not content.strip():  # Check if the content is empty or only whitespace
            header = f"{'Request':<20}{'Date':<15}{'Time':<10}\n"  # Define the header format
            separator = "=" * 45 + "\n"  # Create a separator line for neatness
            f.write(header)  # Write the header to the file
            f.write(separator)  # Write the separator line

        # Get the current date in dd/mm/yyyy format
        date_now = date.today().strftime("%d/%m/%Y")

        # Get the current time in 12-hour format with AM/PM
        time_now = datetime.now().strftime("%I:%M %p")

        # Format the request line with the feature description, date, and time
        text = f"{feature:<20}{date_now:<15}{time_now:<10}\n"
        f.write(text)  # Write the request line to the file


def clearOutput(x):
    # Wait for 'x' seconds (this helps in creating a delay before clearing the output)
    time.sleep(x)

    # Define a function to clear the console screen
    def clear():
        return os.system('cls')  # used to clear the screen in Windows

    clear()


startFeature()
