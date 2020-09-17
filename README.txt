The program takes the user’s input for a Non-deterministic Finite Automaton (NFA) transition table and outputs the corresponding Deterministic Finite Automaton (DFA) tables and the DFA diagram.

1.	The user is prompted to enter all the data for the NFA table. The program records all the data to a default dictionary. defaultdict is a nested key-value structure in Python that has the following form: {key 1: {key 2: {value}}}
2.	Then the NFA table is output based on the dictionary above. 
3.	Then the DFA nested dictionary is constructed using the NFA dictionary. The key 1 field of DFA correspond to the powerset of NFA. After that, a union of sets is put to the “value” part of DFA on each key 2 (alphabet symbol). At the same time, the program fills out the intermediary DFA table based on these keys and values.
4.	The intermediary DFA table is output. 
5.	Names of all the states in the DFA are replaced by letter names.
6.	A new dictionary is created that takes the letter name as a key and the corresponding DFA state as a value (example: B: ‘q0’).
7.	Based on the alphabet dictionary and the DFA default dictionary, all the states in the intermediary DFA table are replaced by an alphabet letter.
8.	The final DFA table is output.
9.	The diagram of the DFA is output.
