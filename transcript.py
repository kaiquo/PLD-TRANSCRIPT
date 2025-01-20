import csv
import sys
import time
import os

def startFeature():
    stdLevel = input("Select what level you are in (i.e U, G, B): ")
    if stdLevel == "B":
        stdLevel = ["U","G"]
        if stdLevel == ["U","G"]:
            stdDegree = input("Specify what degree are you in (i.e M, D, B0): ")
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
            stdDegree = input("Specify what degree are you in (i.e M, D, B0): ")
            if stdDegree == "B0":
                stdDegree = ["M","D"]
            elif stdDegree == "M":
                stdDegree = "M"
            elif stdDegree == "D":
                stdDegree = "D"

    # Asks the user for their student ID
    stdID = int(input("Enter Student ID (i.e. 202006000): "))

    # Checks whether the user's input of student ID is in the database
    dataFrame = pd.read_csv("studentDetails.csv")
    df_results = dataFrame[dataFrame["stdID"] == stdID]

    # Tells the user if their student ID is invalid which means that their student ID is not in the databas
    if df_results.empty:
        print("Invalid ID")
        return stdID

    # Returns to the menu feature after sleeping
    return menuFeature(stdLevel, stdDegree, stdID)
    time.sleep(4)
