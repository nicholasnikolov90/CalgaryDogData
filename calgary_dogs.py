import pandas as pd
import numpy as np
# calgary_dogs.py
# Nick Nikolov
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 git repository.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.


def main():

    # Import data here
    dog_data = pd.read_excel(r"./CalgaryDogBreeds.xlsx") #read entire excel data 
    dog_breeds = dog_data['Breed'].unique() #extract only dog breeds to compare user input
    years = dog_data['Year'].unique() #extract all valid years
    dog_data_df = pd.DataFrame(dog_data) #create initial dataframe of all data
    
    
    #create a multi-index pandas dataframe, all breeds included
    dog_data_df = dog_data_df.set_index(['Breed', 'Year', 'Month'])
    dog_data_df = dog_data_df.sort_index() #sort the indices

    print("ENSF 592 Dogs of Calgary")

    # User input stage
    while (True): 
        try:
            current_dog_breed =  str(input("Please enter a dog breed: ")).upper() #force the user input to upper to match the data file. User can input any case and it will be compared correctly.
            if current_dog_breed in dog_breeds: #if user input is a correct breed
                break # stop asking for user input once they input a correct breed
            else: #otherwise raise error if incorrect dog breed entered
                raise KeyError ("Dog breed not found in the data. Please try again.") #key error raised if incorrect dog breed is entered
        except KeyError:
            print("Dog breed not found in the data. Please try again.")

    # Data anaylsis stage
    # create an index slice containing only the current dog breed data
    idx = pd.IndexSlice
    current_dog_data = dog_data_df.loc[idx[current_dog_breed]] #dataframe containing only user input breed data

    #total registrations for all dog breeds
    total_registrations = dog_data_df.groupby(level='Year').sum()

    current_dog_yearly_registrations = current_dog_data.groupby(level='Year').sum() # find the total registrations for the current input dog for each year
    current_dog_registrations = current_dog_data.sum() # total registrations of the current dog 
    top_years = current_dog_data.index.get_level_values('Year').unique().tolist() #extract only the years that the dog was in the top breed list
    top_years = ' '.join(map(str, top_years)) #join the list by spaces to format it correctly
   
    print(f"""The {current_dog_breed} was found in the top breeds for years: {top_years}""")
    print(f"""There have been {int(current_dog_registrations)} {current_dog_breed} dogs registered in total.""")

    #prints the data percentage of total registrations that the current dog comprises, for each year it was in the data set
    #this is inside a try except block in case the dog was not in the list of popular breeds that year, it will default to 0.0%
    for i in years: 
        try: #If the dog breed was in the popular breed list, print the percentage of total registrations it made up
            current_percent = (current_dog_yearly_registrations.loc[i] / total_registrations.loc[i]) * 100
            print(f"""The {current_dog_breed} was {round(float(current_percent), 6)}% of top breeds in {i}.""")
        except: #print 0% if the dog was not in the most popular breeds that year
            print(f"""The {current_dog_breed} was 0.0% of top breeds in {i}.""")
    
    #find the percentage of the current dog breed across all years of recorded data
    total_percent = current_percent = (current_dog_yearly_registrations.sum() / total_registrations.sum()) * 100
    print(f"""The {current_dog_breed} was {round(float(total_percent), 6)}% of top breeds accross all years.""")

    #find the most popular month to register the current dog
    months = dog_data_df.loc[current_dog_breed].groupby(level=1).size().reset_index(level='Month', name='count') #creates a series that groups the repeated numbers of months, into a column called 'count'
    max_num = months['count'].max() #find max number of repeated months
    popular_months = months[months['count'] == max_num] #use masked array to find most repeated months
    print(popular_months)
    popular_months = popular_months['Month'].tolist() # convert array to a list, easier for printing
    popular_months = ' '.join(map(str, popular_months)) #used for formatting output only, convert the list to space separated values and join

    print(f"""Most popular month(s) for  {current_dog_breed} dogs: {popular_months}""")

if __name__ == '__main__':
    main()
 