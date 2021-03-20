"""
    Imports
"""
from os import path                     # ensures csv file can be found in same directory on an operating system
from datetime import date, datetime     # allows conversion of string DOB dd/mm/yy datetime datatype used for age
import csv                              # used for reading csv files

"""
    Variables && Properties
"""
global PATIENTS # global constant variable named patients
PATIENTS = []   # set patients to empty list

global CLASSIFICATION_TO_PRIORITY # global constant for priority values

# priority filter we convert key values to ints for our sorting algorithm to sort to this priority
# e.g. lowest number the higher priority
CLASSIFICATION_TO_PRIORITY = {

    "obese":        0,
    "underweight":  1,
    "overweight":   2,
    "normal":       3,

}

"""
    Functions: determine_classification && calculate_bodymass_index && calculate_dob_to_age
"""

# calculate_bodymass_index::takes in object type Patient, gets weight and height from patient object
# returns float body mass index
def calculate_bodymass_index(patient):
    return patient.weight / patient.height**2 # calculate the BMI BMI = weight(kgs) / height^2 (m)

# determine_classification::takes in object type Patient::returns string classification
def determine_classification(patient): 

    #TODO:: simple implementation ATM might change later, master definition of limitations????
    if patient.body_build.lower() == "slim": # slim body type
        if(patient.bmi < 18.5):
            return "underweight"
        elif(patient.bmi > 18.5 and patient.bmi < 25):
            return "normal"
        elif(patient.bmi > 25 and patient.bmi < 28):
            return "overweight"
        elif(patient.bmi > 28):
            return "obese"
    elif patient.body_build.lower() == "regular": # regular body type
        if(patient.bmi < 18.5):
            return "underweight"
        elif(patient.bmi > 18.5 and patient.bmi < 25):
            return "normal"
        elif(patient.bmi > 25 and patient.bmi < 29):
            return "overweight"
        elif(patient.bmi > 29):
            return "obese"
    elif patient.body_build.lower() == "athletic": # regular body type
        if(patient.bmi < 18.5):
            return "underweight"
        elif(patient.bmi > 18.5 and patient.bmi < 25):
            return "normal"
        elif(patient.bmi > 25 and patient.bmi < 30):
            return "overweight"
        elif(patient.bmi > 30):
            return "obese"
    else: 
        return "unknown body build" # always expect the unexpected

# calculate_dob_to_age::takes in object type Patient::returns int age of patient
def calculate_dob_to_age(patient):
    datenow = date.today() # get the current date now
    born = patient.dob # get the patient born date of birth
    # calculate the difference from datenow and the born date from the patient :: return int year
    return datenow.year - born.year - ((datenow.month, datenow.day) < (born.month, born.day))

"""
    Classes
"""
class Patient: # patient class is responsible for holding patient information
    
    # constructor for class patient :: takes in multiple arguments with data relating to patient
    def __init__( self, id_name, date_of_birth, is_female, height, weight, body_build, smoker, asthmatic, nasogastric_tube, hypertension , renal_rt, ileostomy, parenteral_nutrition):
        
        global CLASSIFICATION_TO_PRIORITY                           # reference to global variable

        self.identity_name = id_name                                # stores name code as string
        self.dob = datetime.strptime(date_of_birth, '%d/%m/%Y')     # store DOB as a datetime datatype :: string day/month/year -> datetime
        self.is_female = is_female                                  # stores a boolean value for gender (in terms of medical relevance original biological gender is binary to this date still)
        self.height = height                                        # stores height in meters as float
        self.weight = weight                                        # stores weight in kg as float
        self.body_build = body_build                                # stores body build type as string
        self.smoker = smoker                                        # store boolean Y = true blank = false
        self.asthmatic = asthmatic                                  # store boolean Y = true blank = false
        self.nasogastric_tube = nasogastric_tube                    # store boolean Y = true blank = false
        self.hypertension = hypertension                            # store boolean Y = true blank = false
        self.renal_rt = renal_rt                                    # store boolean Y = true blank = false
        self.ileostomy = ileostomy                                  # store boolean Y = true blank = false
        self.parenteral_nutrition = parenteral_nutrition            # store boolean Y = true blank = false
        
        self.bmi = calculate_bodymass_index(self)                   # calculate the BMI
        self.classification = determine_classification(self)        # assign patient classification, pass in self(object) returns string underweight/normal/obese
        self.conditionPriority = CLASSIFICATION_TO_PRIORITY[self.classification] # convert condition name into priority int :: used for sorting

        self.age = calculate_dob_to_age(self)                       # calculate the age of the patient

    def __repr__(self): # method used to represent this class object as a string :: we print name, age, bmi rounded to the 2nd decimal place, and bmi classification
        return "NAME: {0} | AGE: {1} | BMI: {2} | BMI-C: {3}".format(self.identity_name, self.age, round(self.bmi,2), self.classification)

"""
    Functions: selection_sort 
"""
# selection_sort :: takes in python list of patient objects sorts them by condition priority
def selection_sort(array, sort_via_bmi = False, low_to_high = True):

    for i in range(0, len(array)): # for every element in the list named array
        # Finding the smallest number in the subarray
        min = i

        # for every element in the array from i + 1 we compare the condition values
        for j in range(i+1,len(array)):

            if sort_via_bmi: # sorts via BMI if argument is provided, default is false
                # sorts the BMI low to high by default if set to false the ternary operators will switch the sort order to high to low
                if ((array[min].bmi > array[j].bmi) if low_to_high else (array[min].bmi < array[j].bmi) ): 
                    min = j # set min from j index found
            else:
                if array[min].conditionPriority > array[j].conditionPriority: # conditionPriority is a int value set on creation of patient
                    min = j # set min from j index found

        if (min != i):
            ## swap
            temp = array[i]
            array[i] = array[min]
            array[min] = temp

"""
    Functions: datafile_name && read_datafile && display_all_patients && display_worst_patients_via_gender_and_mode
"""
def datafile_name(): # used to store the data file csv name to read in
    # get the directory of this file to find the CSV file
    dir_path = path.dirname(path.realpath(__file__))   
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
                        row[0], # identity name
                        row[1], # dob
                        (True if (row[2].lower() == "f") else False), # if the sex lowercase is equal to f then we return true else false
                        float(row[3]), # height
                        float(row[4]), # weight
                        row[5], # body build
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
    # we will perform a selection_sort(ARRAY: Patients) takes in array of patients to sort via the filter defined at the top 
    # from CLASSIFICATION_TO_PRIORITY
    selection_sort(PATIENTS)

def display_all_patients(): # called when we want to print all patients in sets of 10
    view_limit = 10 # max display of patients
    count = 0 # count is set to 0 :: tracks line prints
    page = 1 # track the number of pages viewed
    for patient in PATIENTS: # for every patient object in patients list
        
        if(count >= view_limit): # of the line count is greater or equal to 10
            n = str(input("Hit enter to continue...")) # breaks
            count = 0 # reset line count to 0
            page = page + 1 # page number
            print("\n") # create a line break to separate prints of patients
        
        if(count == 0): # only print on first line
            print(f"____________________[ Page: {page}/{round(len(PATIENTS)/view_limit)} ]____________________")

        print(patient) # print out the patient

        # increment count
        count = count + 1

# display_worst_patients_via_gender_and_mode :: is called when we want to display most obese/most underweight top 5 patients via gender
# female_only if true prints only female patients and vice versa
# underweight mode determines which sort order the selection_sort orders BMI by 
def display_worst_patients_via_gender_and_mode(female_only, underweight_mode):

    global PATIENTS # global reference to patients list

    # sort the patients using BMI mode using High to low mode e.g. used to find the higheste BMI patients
    # selection_sort( PATIENTS_LIST, Should We Sort Via BMI?, Low to High?  )
    selection_sort(PATIENTS, True, underweight_mode)

    # auto construct title depending on given modes :: Bless Ternary Operators!!!
    title = ("Underweight" if underweight_mode else "Obese") + " " + ("Female" if female_only else "Male") + " Patients"

    # display what we are printing
    print(f"____________________[ Most { title } ]____________________")

    count = 0 # track number of displayed prints
    # for every patient in the PATIENTS LIST
    for patient in PATIENTS: # increment X from 0 to 5
        if patient.is_female == female_only: # check if we want to display male or female results only
            count = count + 1 # increment count
            print(patient, "| GENDER: " + str(patient.is_female).lower().replace("false","Male").replace("true","Female"))
        
        if count >= 5: # if count is greater or equal to five
            break # stop the for loop we found our five patients

# called when we want to output the worse patients for obese and underweight
def display_all_worst_patients():

    display_worst_patients_via_gender_and_mode(False, True) # for males, underweight_mode = True
    print("\n") # line break
    display_worst_patients_via_gender_and_mode(False, False) # for males, underweight_mode = False

    n = str(input("Hit enter to continue...")) # wait for user to continue
    print("\n\n") # double line break

    display_worst_patients_via_gender_and_mode(True, True) # for females only, underweight_mode = True
    print("\n")  # line break
    display_worst_patients_via_gender_and_mode(True, False) # for females only, underweight_mode = False

"""
    Execute::Main
"""

# read the patients data file
# this will convert our CSV into list of patient objects
# and sort them according to the CLASSIFICATION_TO_PRIORITY
read_datafile()

# display all patients to fullfil task 1 of display print
# in general we are only going to print all the patients because we sorted them to the specified task requirements
display_all_patients()

n = str(input("Hit enter to continue...")) # breaks
print("\n\n")

display_all_worst_patients()

# prevent terminal closing so fast on windows
n = str(input("Hit enter to close..."))