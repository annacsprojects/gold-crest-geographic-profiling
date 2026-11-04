import csv

#By adding a defining function, my code can be imported into other programming files, rather than having to copy and paste it several times.

def load_crime_data(filepath):

#The command 'with' closes the csv file securely after use so that the memory doesn't leak.
    with open('data/crime_scenes.csv', newline='') as csvfile:

    #Here, this program reads the first line of the csv file and each component becomes a dictionary key.
        reader = csv.DictReader(csvfile)

    #When each line is read in the csv file, each value is assigned to its row with its key.
        for row in reader:

        #The values of the selected keys are printed.
            print(row['case_name'], row['latitude'], row['longitude'])
load_crime_data('data/crime_scenes.csv')