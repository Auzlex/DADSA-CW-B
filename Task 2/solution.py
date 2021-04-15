"""
    Imports
"""
from os import path                     # ensures csv file can be found in same directory on an operating system
from datetime import date, datetime     # allows conversion of string DOB dd/mm/yy datetime datatype used for age
from math import ceil                   # allows a number to be rounded up always, used in printing to display page numbers
import csv                              # used for reading csv files

"""
    Variables && Properties
"""
global PATIENTS # global constant variable named patients
global PRIORITY_REFERRAL_PATIENTS # list of patients that meet the priority referral
global LOW_PRIORITY_REFERRAL_PATIENTS # list of patients that meet the priority referral
PRIORITY_REFERRAL_PATIENTS = [] # set priority patients to empty list
LOW_PRIORITY_REFERRAL_PATIENTS = [] # set low priority patients to empty list
PATIENTS = []   # set patients to empty list

"""
    Functions: determine_classification && calculate_bodymass_index && calculate_dob_to_age
"""

# calculate_bodymass_index::takes in object type Patient, gets weight and height from patient object
# returns float body mass index
def calculate_bodymass_index(patient):
    return patient.weight / patient.height**2 # calculate the BMI BMI = weight(kgs) / height^2 (m)

# determine_classification::takes in object type Patient::returns string classification
def determine_classification(patient): 

    # depending on the body build we change the overweight_to_obese_threshold :: seems to be only factor changing
    if patient.body_build.lower() == "slim": # slim body type
        overweight_to_obese_threshold = 28
    elif patient.body_build.lower() == "regular": # regular body type
       overweight_to_obese_threshold = 29
    elif patient.body_build.lower() == "athletic": # regular body type
        overweight_to_obese_threshold = 30
    else: 
        return "unknown body build" # always expect the unexpected

    # depending on the patient BMI and the overweight_to_obese_threshold
    # return the classification of this patient which is assigned in patient class
    if(patient.bmi < 18.5):
        return "underweight"
    elif(patient.bmi > 18.5 and patient.bmi < 25):
        return "normal"
    elif(patient.bmi > 25 and patient.bmi < overweight_to_obese_threshold):
        return "overweight"
    elif(patient.bmi > overweight_to_obese_threshold):
        return "obese"

# calculate_dob_to_age::takes in object type Patient::returns int age of patient
def calculate_dob_to_age(patient):
    datenow = date.today() # get the current date now
    born = patient.dob # get the patient born date of birth
    # calculate the difference from datenow and the born date from the patient :: return int year
    return datenow.year - born.year - ((datenow.month, datenow.day) < (born.month, born.day))

# determine_conditions::takes in object type Patient::returns true if they need to be referred to a dietitian
# passing in Patient object allows us to access and get all the patient information
def determine_conditions(patient):

    total_conditions_found = 0 # track the number of conditions a patient may have

    # condition "obese" OR "underweight"
    if patient.classification == "obese" or patient.classification == "underweight":
        total_conditions_found += 1 # increment condition found

    # condition if patient has hypertension
    if patient.hypertension:
        total_conditions_found += 1 # increment condition found

    # condition if patient is asthmatic
    if patient.asthmatic:
        total_conditions_found += 1 # increment condition found

     # condition if patient is a smoker
    if patient.smoker:
        total_conditions_found += 1 # increment condition found

    # condition NJT or NGR :: nasogastric_tube
    if patient.nasogastric_tube:
        total_conditions_found += 1 # increment condition found

    # condition renal replacement therapy
    if patient.renal_rt:
        total_conditions_found += 1 # increment condition found

    # condition ileostomy
    if patient.ileostomy:
        total_conditions_found += 1 # increment condition found

    # condition parenteral nutrition
    if patient.parenteral_nutrition:
        total_conditions_found += 1 # increment condition found

    return total_conditions_found # return the number of conditions found

"""
    Classes
"""
class Patient: # patient class is responsible for holding patient information
    
    # constructor for class patient :: takes in multiple arguments with data relating to patient
    def __init__( self, id_name, date_of_birth, is_female, height, weight, body_build, smoker, asthmatic, nasogastric_tube, hypertension , renal_rt, ileostomy, parenteral_nutrition):
        
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

        self.age = calculate_dob_to_age(self)                       # calculate the age of the patient
        self.number_of_conditions = determine_conditions(self)      # determines number of condition a patient has
        self.need_dietitian_referral = (self.number_of_conditions > 0)     # if the patient has more than 1 condition they need referral

    def __repr__(self): # method used to represent this class object as a string :: we print name, age, bmi rounded to the 2nd decimal place, and bmi classification
        #return "NAME: {0} | AGE: {1} | BMI: {2} | BMI-C: {3} | CONDITIONS: {4} | GENDER: {5} | REFER D: {6}".format(self.identity_name, self.age, round(self.bmi,2), self.classification, self.number_of_conditions, str(self.is_female).lower().replace("false","Male").replace("true","Female"), self.need_dietitian_referral)
        return "n: {0}, age:{9}, bmi:{10}, bb:{1}, conditions:{11}, smoke:{2}, asthmatic:{3}, NJR:{4}, hyp:{5}, renal:{6}, ileo:{7}, pn:{8}".format( self.identity_name, self.body_build, self.smoker, self.asthmatic, self.nasogastric_tube, self.hypertension, self.renal_rt, self.ileostomy, self.parenteral_nutrition, self.age, round(self.bmi,2), self.number_of_conditions )

"""
    Functions: selection_sort 
"""
# selection_sort :: takes in python list of patient objects sorts them by condition priority if sort_via_bmi is false
# if sort via bmi is true then low_to_high determines the sorting order of the BMI values
def selection_sort(array, sort_via_bmi = False, low_to_high = True, sort_via_age = False):

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
                if sort_via_age: # sorts via age
                    # sorts the BMI low to high by default if set to false the ternary operators will switch the sort order to high to low
                    if ((array[min].age > array[j].age) if low_to_high else (array[min].age < array[j].age) ): 
                        min = j # set min from j index found
                else: # if no other boolean values are specified sort by the number of conditions
                    if ((array[min].number_of_conditions > array[j].number_of_conditions) if low_to_high else (array[min].number_of_conditions < array[j].number_of_conditions) ): # conditionPriority is a int value set on creation of patient
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
    global PRIORITY_REFERRAL_PATIENTS # global reference to priority referral
    global LOW_PRIORITY_REFERRAL_PATIENTS # global reference to low priority referral list

    # open the datafile and access it via variable named csvfile
    with open(datafile_name()) as csvfile:
        line_count = 0 # tracks the lines
        spamreader = csv.reader(csvfile, delimiter=',') # perform a csv reader and split by ,
        for row in spamreader: # for every row
            if(line_count != 0): # if the line count is not 0 e.g. header of the CSV then
                # create a new patient on new row data
                new_patient = Patient(
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
                
                # If a patient is asthmatic OR a smoker and is over 55, OR Obese & suffers from hypertension or any patient with more than 2 conditions
                if ((new_patient.asthmatic or new_patient.smoker) and new_patient.age >= 55) or (new_patient.classification == "obese" and new_patient.hypertension) or new_patient.number_of_conditions > 2:
                    PRIORITY_REFERRAL_PATIENTS.append(new_patient) # append priority referral patient
                else: # if the patient does not meet the requirements for priority then shove them into the original patients list
                    if new_patient.number_of_conditions > 0: # do one last check for low priority referrals
                        LOW_PRIORITY_REFERRAL_PATIENTS.append(new_patient) # append to low priority list
                    else: # not important
                        PATIENTS.append(new_patient) # append non referral patients to the normal pool

            line_count += 1 # increment line count
        
        # close csv file
        csvfile.close()
    
    print("number of patients",line_count-1)
    print(len(PRIORITY_REFERRAL_PATIENTS))
    print(len(LOW_PRIORITY_REFERRAL_PATIENTS))
    print(len(PATIENTS))
    total = len(PRIORITY_REFERRAL_PATIENTS) + len(LOW_PRIORITY_REFERRAL_PATIENTS) + len(PATIENTS)
    print(total)

    # after reading the file and placing patients in their respective lists for dietition referral
    # sort all those lists by age from high to low
    selection_sort(PATIENTS,False,False,True)
    selection_sort(PRIORITY_REFERRAL_PATIENTS,False,False,True)
    selection_sort(LOW_PRIORITY_REFERRAL_PATIENTS,False,False,True)

def display_all_priority_referral_patients(): # called when we want to print all patients in sets of 10
    
    global PRIORITY_REFERRAL_PATIENTS # list of patients that meet the priority referral
  
    view_limit = 10 # max display of patients
    count = 0 # count is set to 0 :: tracks line prints
    page = 1 # track the number of pages viewed

    for patient in PRIORITY_REFERRAL_PATIENTS: # for every patient object in patients list
        if(count >= view_limit): # of the line count is greater or equal to 10
            n = str(input("Hit enter to continue...")) # breaks
            count = 0 # reset line count to 0
            page = page + 1 # page number
            print("\n") # create a line break to separate prints of patients
        
        if(count == 0): # only print on first line
            print(f"____________________[ Priority Referral Patients, Page: {page}/{ceil(len(PRIORITY_REFERRAL_PATIENTS)/view_limit)} ]____________________")

        print(patient) # print out the patient

        # increment count
        count = count + 1

def display_all_low_priority_referral_patients(): # called when we want to print all patients in sets of 10

    global LOW_PRIORITY_REFERRAL_PATIENTS

    view_limit = 10 # max display of patients
    count = 0 # count is set to 0 :: tracks line prints
    page = 1 # track the number of pages viewed

    for patient in LOW_PRIORITY_REFERRAL_PATIENTS: # for every patient object in patients list

        if(count >= view_limit): # of the line count is greater or equal to 10
            n = str(input("Hit enter to continue...")) # breaks
            count = 0 # reset line count to 0
            page = page + 1 # page number
            print("\n") # create a line break to separate prints of patients
        
        if(count == 0): # only print on first line
            print(f"____________________[ Low Priority Referral Patients, Page: {page}/{ceil(len(LOW_PRIORITY_REFERRAL_PATIENTS)/view_limit)} ]____________________")

        print(patient) # print out the patient

        # increment count
        count = count + 1

def display_all_no_referral_patients(): # called when we want to print all patients in sets of 10

    global PATIENTS

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
            print(f"____________________[ Patients that don't need referral, Page: {page}/{ceil(len(PATIENTS)/view_limit)} ]____________________")

        print(patient) # print out the patient

        # increment count
        count = count + 1

"""
    Execute::Main
"""

# read the patients data file
# this will convert our CSV into list of patient objects
# and sort them according to the WEIGHT_CLASSIFICATION_TO_PRIORITY
read_datafile()

# display_all_priority_referral_patients
# displays all the priority referral patients
display_all_priority_referral_patients()

n = str(input("Hit enter to continue...")) # breaks
print("\n\n")

# displays all the non priority referrals
display_all_low_priority_referral_patients()

n = str(input("Hit enter to continue...")) # breaks
print("\n\n")

# displays all the non priority referrals
display_all_no_referral_patients()

# prevent terminal closing so fast on windows
n = str(input("Hit enter to close..."))