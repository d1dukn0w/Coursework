# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 23:56:09 2023

@author: Conra
"""

import numpy as np
import matplotlib.pyplot as plt

#given probability = prob of seeing a head, we are working with a fair coin here

prob=.5
max=25
av=np.zeros(len(range(2,11)))     #create numpy arrays to be edited as neeeded
stder=np.zeros(len(range(2,11)))
for i in range(9):                #we do these repeated simulations for powers of 2 flips
    ntry=2**(i+2)                    #number of trials per simulation
    nsim=1000                    #number of simulations
    skip=0                      #how many results did we ignore?
    strklst =[]
    for simulation in range(0,nsim): #for all the simulations
      streak = 0                     #create variables to keep track of steaks and the maximum for each run
      maxstreak=0
      hitlist = []                   #create a list to store the truth values for the previous flips True=Heads False=Tails
      for attempt in range(ntry):    #Instead of doing the while loop, I opted to use if statements such that after each flip, the program returns to the start of the for loop
          if attempt==0:             #create a starting flip, there are no truth values prior, so don't check hitlist on first run.
              hit = (np.random.random()<prob) #flip the coin <---- WE FLIP HERE
              hitlist.append(hit)  #add the truth value of whatever the flip was to hitlist
              streak=1             #no matter if we flipped heads or tails we start a streak of 1
          else:                      #if this is not the first flip
              if (np.random.random()<prob):  #we flip a coin and get heads <---- WE FLIP HERE
                  hit = True
                  hitlist.append(hit)       #count the heads and add it to the list
                  if hitlist[attempt-1]==True: #if the last flip was also a heads
                      streak+=1                #continue the streak
                  else:                        #if the last flip was tails
                      streak=1                 #reset the streak
                  if maxstreak < streak:       #if we got a higher streak than our current max
                      maxstreak = streak      #set our current streak as our max
              else:                        #we flip a coin and get tails <---- WE FLIP HERE
                  hit=False
                  hitlist.append(hit)           #count the tails
                  if hitlist[attempt-1]==False:  # if the previous flip was tails
                      streak+=1                  #continue the streak
                  else:                          #if the previous flip was heads
                      streak=1                   #reset the streak
                  if maxstreak < streak:         #if we got a higher streak than our current max
                      maxstreak = streak        #set our current streak as our max
      if maxstreak<max+1:                      #if our streak is below our 'absurd streak value'
          strklst.append(maxstreak)            #we count it because it's normal
      else:                                    #if our streak is beyond our 'absurd streak value'
          skip+=1                              #throw it out because it's weird
    
    strklst=np.array(strklst)                  #turn our max streak list into a numpy array
    average=np.average(strklst)                #take an average of that numpy array
    av[i]=average                              #update the array that stores the average for the corresponding number of flips
    var=np.var(strklst)                        #take the variance of our streak list
    stderr=np.std(strklst)/np.sqrt(nsim)       #take the standard error of our streak list
    stder[i]=stderr                            #update the array that stores the average for the corresponding number of flips
    print("Skipped {}% of data".format((skip/(nsim*ntry))*100)) #print the percentage of data we skipped
                      
    print(average)
print(av)
def nrun(N): #we define our function for our approximation fo our longest run of coins
    return np.log2(N)

trylist=[]              #this for loop is meant to generate the list of the number of flips for each value of N
for k in range(2,11): 
    trylist.append(2**k) #they were all powers of 2

xvlus=np.array(trylist)

#plotting
plt.plot(xvlus, av, 'b.', label='Simulated Data')
plt.plot(xvlus,nrun(xvlus), 'r-', label='fit')
plt.errorbar(xvlus, av, yerr = 2.98*stder,fmt='.', color='b')
plt.xlabel('Number of Flips')
plt.ylabel('Average Largest Streak')
plt.legend(loc='best')
plt.yticks(ticks=np.arange(2,12,step=1),minor=True)
plt.xticks(ticks=np.arange(0,1.1*trylist[8], step=50),minor=True)
plt.ylim(2,12)
plt.xlim(0,1.1*trylist[8])
plt.title('Largest Average Streak of Heads or Tails from N fair coin tosses')
