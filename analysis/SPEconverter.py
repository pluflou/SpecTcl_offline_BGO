import numpy as np
import os, sys

def unpack_spectra(filename, key, size):
    
    """Function to unpack all saved spectra from text file 
       and import them as a single array of counts for each BGO """
    
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    counts_array=[0 for i in range(0,size)] #array size of 6554

    for i, line in enumerate(lines):
        
        #split each line at " symbol to find the spectrum name
        if (len(line.split('"'))>1) and (line.split('"')[1] == key):
            #skip the rows of text until you reach where data starts
            i=i+6
            #record count number at each channel until you reach the last entry with channel (-1)
            
            while (lines[i].split(" ")[0] != "(-1)"):
                i=i+1
                channel_num= int(lines[i].split(" ")[0].split(")")[0].split("(")[1])
                #print(channel_num, counts)
                
                if (channel_num==-1):
                    #print(f"Imported {key}.")
                    break
                else:
                    counts= int(lines[i].split(" ")[1])
                    #taking the channel number in file as index for count array
                    counts_array[channel_num]= counts                       
        else: 
            
            continue
            
    return counts_array

def txt2spe(spec_data, spec_name, run_number): 
    
    '''Function to write spectra arrays into .spe format'''

    speclen= len(spec_data) - 1
            
    string=     ( "$SPEC_ID:          \n"
                 f"Description: {run_number} {spec_name}\n"
                  "$MEAS_TIM:         \n"
                  "666 666            \n"
                  "$DATE_MEA:         \n"
                  "01/01/2019 12:00:00.0\n"
                  "$DATA:             \n"
                 f"0 {speclen}        \n")
    
    
    if not os.path.exists(f"./{run_number}/"):
        os.makedirs(f"./{run_number}/")
    f= open(f"./{run_number}/{run_number}_{spec_name}.spe", "w")
    f.write(string)
    
    for num in spec_data:
        print("%i" %(num), file=f)
    
    f.close()

def import_spectra(filename, run_number, array, size):
    ''' Function to import all spectra from 
        single file into separate .spe files'''
        
    for i in array:  
        array[i]= unpack_spectra(filename, i, size)
        txt2spe(array[i], i, run_number)