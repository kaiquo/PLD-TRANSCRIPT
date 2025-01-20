import pandas as pd
import sys
import time
import os

def startFeature():
    print("\033[1mWelcome to the PUP Student Transcript Generation System!\033[0;0m")
    while True:
        print("========================================================")
        print("Select Student Level:\n")
        print("U: Undergraduate")
        print("G: Graduate")
        print("B: Both Undergraduate and Graduate")
        print("========================================================")
        stdLevel = input("Select student level: ").upper()
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
                stdDegree = input("For Graduate level, select the degree: ").upper()
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
                    clearOutput()
                    menuFeature(stdLevel, stdDegree, stdID)
                    break  # Exit the loop once a valid ID is provided
                else:
                    # If the ID is invalid
                    print("\nInvalid ID. Please try again.\n")
            except ValueError:
                print("\nInvalid input. Please enter a valid numeric Student ID.\n")

def menuFeature(stdLevel, stdDegree, stdID):
    while True:
        print("\033[1mStudent Transcript Generation System Menu\033[0;0m")
        print("===================================================")
        print("1. Student details")
        print("2. Statistics")
        print("3. Transcript based on major courses")
        print("4. Transcript based on minor courses")
        print("5. Full transcript")
        print("6. Previous transcript requests")
        print("7. Select Another student")
        print("8. Terminate the system")
        print("===================================================")
        choice = input("\033[1mEnter your feature: \033[0;0m")

        if choice == "1":
            detailsFeature(stdID, stdLevel, stdDegree)
        elif choice == "2":
            statisticsFeature()
        elif choice == "3":
            majorTranscriptFeature()
        elif choice == "4":
            minorTranscriptFeature()
        elif choice == "5":
            fullTranscriptFeature()
        elif choice == "6":
            previousRequestsFeature()
        elif choice == "7":
            newStudentFeature()
        elif choice == "8":
            terminateFeature()
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

    with open(f"std{stdID}details.txt", "w") as f:
        f.write(stdDetail_txt)
        f.close()

    # Clears the screen followed by a short sleep and then proceeds to the menu feature again
    clearOutput()
    menuFeature(stdLevel, stdDegree, stdID)

def clearOutput():
    # Wait for 3 seconds
    time.sleep(5)
    # Clear output
    def clear(): return os.system('cls')
    clear()

startFeature()
