"""
    Imports
"""
import os   
import csv

"""
    Variables
"""
global PATIENTS # global constant variable named patients
PATIENTS = []   # set patients to empty list

global CONDITION_TO_PRIORITY # global constant for priority values
# priority filter we convert key values to ints for our sorting algorithm to sort to this priority
# e.g. lowest number the higher priority
CONDITION_TO_PRIORITY = {

    "obese":0,
    "underweight":1,
    "overweight":2,
    "normal":3,

}

"""
    Classes
"""
class Patient: # patient class is responsible for holding patient information
    # constructor for class patient
    def __init__( self, id_name, date_of_birth, is_female, height, weight, body_build, smoker, asthmatic, nasogastric_tube, hypertension , renal_rt, ileostomy, parenteral_nutrition):
        
        global CONDITION_TO_PRIORITY                        # reference to global variable

        self.identity_name = id_name                        # stores name code as string
        self.dob = date_of_birth                            # stores DoB as string
        self.is_female = is_female                          # stores a boolean value for gender (since is in terms of medical relevance original biological gender is binary to this date still. )
        self.height = height                                # stores height in meters as float
        self.weight = weight                                # stores weight in kg as float
        self.body_build = body_build                        # stores body build type as string
        self.smoker = smoker                                # store boolean Y = true blank = false
        self.asthmatic = asthmatic                          # store boolean Y = true blank = false
        self.nasogastric_tube = nasogastric_tube            # store boolean Y = true blank = false
        self.hypertension = hypertension                    # store boolean Y = true blank = false
        self.renal_rt = renal_rt                            # store boolean Y = true blank = false
        self.ileostomy = ileostomy                          # store boolean Y = true blank = false
        self.parenteral_nutrition = parenteral_nutrition    # store boolean Y = true blank = false
        self.bmi = weight / height**2                       # calculate the BMI BMI = weight(kgs) / height^2 (m)

        self.conditionName = self.calculate_risk_factor()   # get the condition name from calculation of risk factor
        self.condition = CONDITION_TO_PRIORITY[self.conditionName] # convert condition name into priority int


    def calculate_risk_factor(self): # used to calculate the condition of a patient

        #TODO:: simple implementation ATM might change later, master definition of limitations????
        if self.body_build.lower() == "slim": # slim body type
            if(self.bmi < 18.5):
                return "underweight"
            elif(self.bmi > 18.5 and self.bmi < 25):
                return "normal"
            elif(self.bmi > 25 and self.bmi < 28):
                return "overweight"
            elif(self.bmi > 28):
                return "obese"
        elif self.body_build.lower() == "regular": # regular body type
            if(self.bmi < 18.5):
                return "underweight"
            elif(self.bmi > 18.5 and self.bmi < 25):
                return "normal"
            elif(self.bmi > 25 and self.bmi < 29):
                return "overweight"
            elif(self.bmi > 29):
                return "obese"
        elif self.body_build.lower() == "athletic": # regular body type
            if(self.bmi < 18.5):
                return "underweight"
            elif(self.bmi > 18.5 and self.bmi < 25):
                return "normal"
            elif(self.bmi > 25 and self.bmi < 30):
                return "overweight"
            elif(self.bmi > 30):
                return "obese"
        else: 
            return "unknown body build" # always expect the unexpected

    def __repr__(self): # function used to define pythons print to output this class object in a readable format
        return "<{14}, {13}, {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}>".format(self.identity_name, self.dob, self.is_female, self.height, self.weight, self.body_build, self.smoker, self.asthmatic, self.nasogastric_tube, self.hypertension, self.renal_rt, self.ileostomy, self.parenteral_nutrition, self.bmi, self.condition)

"""
    Selection Sort
"""
def selectionSort(array): # selection sort takes in array of patient objects
    for i in range(0, len(array)):
        # Finding the smallest number in the subarray
        min = i

        # for every element in the array from i + 1 we compare the condition values
        for j in range(i+1,len(array)):
            if array[min].condition > array[j].condition: # condition is a int value set on creation of patient
                min = j # set min from j index found

        if (min != i):
            ## swap
            temp = array[i]
            array[i] = array[min]
            array[min] = temp

"""
    Functions
"""
def datafile_name(): # used to store the data file csv name to read in
    # get the directory of this file to find the CSV file
    dir_path = os.path.dirname(os.path.realpath(__file__))   
    return  dir_path + "\\DADSA 2021 CWK B DATA COLLECTION.csv"

def read_datafile(): # called on application start when we want to read in the csv data

    global PATIENTS # global variable reference to patients

    # open the datafile and access it via variable named csvfile
    with open(datafile_name()) as csvfile:
        line_count = 0 # tracks the lines
        spamreader = csv.reader(csvfile, delimiter=',') # perform a csv reader and split by ,
        for row in spamreader: # for every row
            if(line_count != 0): # if the line count is not 0 e.g. header of the CSV then
                # append a new patient do the patients global list
                PATIENTS.append(
                    Patient(
                        row[0],
                        row[1],
                        (True if (row[2].lower() == "f") else False), # if the sex lowercase is equal to f then we return true else false
                        float(row[3]),
                        float(row[4]),
                        row[5],
                        (True if (row[6].lower() == "y") else False), # if segment is equal to lower case y return true else false
                        (True if (row[7].lower() == "y") else False), # if segment is equal to lower case y return true else false
                        (True if (row[8].lower() == "y") else False), # if segment is equal to lower case y return true else false
                        (True if (row[9].lower() == "y") else False), # if segment is equal to lower case y return true else false
                        (True if (row[10].lower() == "y") else False), # if segment is equal to lower case y return true else false
                        (True if (row[11].lower() == "y") else False), # if segment is equal to lower case y return true else false
                        (True if (row[12].lower() == "y") else False), # if segment is equal to lower case y return true else false
                    )
                )

            line_count += 1 # increment line count
        
        # close csv file
        csvfile.close()
    
    # after reading in the data file we need to sort the list of PATIENTS
    # we will perform a selectionSort(ARRAY: Patients) takes in array of patients to sort via the filter defined at the top 
    # from CONDITION_TO_PRIORITY
    selectionSort(PATIENTS)

    

# read the patients data file
# this will convert our CSV into list of patient objects
# and sort them according to the CONDITION_TO_PRIORITY
read_datafile()

# print some stuff out mate
print("sorted::")
count = 0
for patient in PATIENTS:
    print(patient.conditionName, patient)
    if(count >= 10):
        count = 0
        print("\n")
    count = count + 1

n = str(input("Hit enter to close..."))