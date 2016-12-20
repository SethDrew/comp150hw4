#Simulating Power Usage in a IOT-based Smart Home Lighting
##Ashton Knight, Carter Casey, Chase Conley, Seth Drew, Thomas Rind, and Walton Lee

To run the simulation, run one of the following scripts:

        ./run_simple_cloud.sh
        ./run_one_person.sh
        ./run_control.sh

This will generate a fresh copy of the associated config and event files and
run the simulation. To run the simulation on different files:

        python simulation.py [config.json] [events.json]
        
Make sure to have Python v2.7 installed.
        
See IOSpecs.md for how to run the generator
