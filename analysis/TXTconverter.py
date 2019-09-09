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

def array2file(spec_data, spec_name, runnum): 
    
    '''Function to write spectra arrays into txt format'''      
    
    if not os.path.exists(f"./{runnum}/"):
        os.makedirs(f"./{runnum}/")
    f= open(f"./{runnum}/{runnum}_{spec_name}.txt", "w")
    #f.write(string)
    
    for num in spec_data:
        print("%i" %(num), file=f)
    
    f.close()

def import_spectra(filename, run_number, array, size):
    ''' Function to import all spectra from 
        single file into separate .spe files'''
        
    for i in array:  
        array[i]= unpack_spectra(filename, i, size)
        array2file(array[i], i, run_number)
