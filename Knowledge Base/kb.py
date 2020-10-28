# a4.py - Jeff Wang - 301309384 - CMPT310
# cd mnt/c/users/17789/desktop/310/HW/a4
# python3 a4.py



# Global varibale "loaded" stores the KB rules as a 2D list
# Global variable "matrix" stores the atoms of each rule as a 2D list (0 - false/ 1 - true)
# Global variable "atom" stores a list of non KB atoms set to True
loaded = []
matrix = []
atoms = []



# Description:   True if, and only if, string s is a valid variable name
def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])



# Description:   True if, and only if, char s is a valid letter
def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"



# Description   Attempt to load KB "fname", returns a valid 2D list if loaded, else returns empty list,
#               Printing is set to True if we want to print, else it's set to False
def load(fname, printing):
    a = []

    # Try to open file fname
    try:
        f = open(fname, 'r')
        with f:
            # Pharse file strings into 2D list
            for line in f:
                if line.strip():
                    a.append(line.split())
            f.close()

            # Check all edge cases for valid KB rules
            for i in range(len(a)):
                count = 0
                # Check rules contains 3 or more strings
                if len(a[i]) < 3 and printing:
                    print('Error: "{}" is not a valid knowledge base'.format(fname))
                    print("        KB rules must contain one or more atoms\n")
                    return []
                # Check rules contain an odd number of strings
                if len(a[i]) % 2 == 0 and printing:
                    print('Error: "{}" is not a valid knowledge base'.format(fname))
                    print("        KB rules must have \"&\" between two atoms\n")
                    return []

                for j in range(len(a[i])):
                    # Check that every 2nd string of each rule is "<--"
                    if j == 1 and a[i][j] != "<--" and printing:
                        print('Error: "{}" is not a valid knowledge base'.format(fname))
                        print("        KB rules must have \"<--\" as the second string\n")
                        return []
                        # Check that every even string after the 3rd string is "&"
                    elif j % 2 == 1 and j >= 3 and a[i][j] != "&" and printing:
                        print('Error: "{}" is not a valid knowledge base'.format(fname))
                        print("        KB rules must contain a \"&\" between each atom\n")
                        return []
                        # Check that every odd string is a vaild atom (must be a letter or "_")
                    elif j % 2 == 0 and is_atom(a[i][j]) == False and printing:
                        print('Error: "{}" is not a valid knowledge base'.format(fname))
                        print("        KB must contain valid atoms\n")
                        return []
    # Exception: file not found or cannot be opened
    except OSError:
        if printing:
            print('Error: load failed, could not open/read file "{}"\n'.format(fname))
        return []

    if printing:
        # If fuction has not exited yet, Print values of a[]
        for k in a:
            count = count + 1
        print(" ", count, "definite clauses read in: ")

        for k in a:
            print("   ", end = "")
            print(' '.join(k))
        print()
    return a



# Description:   Takes valid rules from "loaded" and initializes a "matrix" of the same size (Set to all atoms to 0 - false)
def loadMatrix():
    global matrix
    global loaded

    for i in range(len(loaded)):
        b = []
        for j in range(len(loaded[i])):
            b.append(0)
        matrix.append(b)
    return



# Description:   Set each valid atom to True in the KB matrix
#                printing is set to True if we want to print, else it's set to False
def tell(comsplit, printing):
    global matrix
    global loaded
    global atoms

    # For each string after the tell command compare to the rules in the loaded matrix
    for k in range(1, len(comsplit)):
        hit = 0
        for i in range(len(loaded)):
            for j in range(0, len(loaded[i]), 2):
                # Check if its a valid atom in the loaded matrix
                if comsplit[k] == loaded[i][j]:
                    # Check matrix it has been set to True
                    if matrix[i][j] == 0:
                        matrix[i][j] = 1
                        if hit == 0 and printing:
                            print('   "{}" added to KB'.format(comsplit[k]))
                    elif hit == 0 and printing:
                        print('   atom "{}" already known to be true'.format(comsplit[k]))
                    hit = 1

        # If tell string wasn't found in the loaded matrix, check it's a valid atom
        if hit == 0 and is_atom(comsplit[k]) and printing:
            # If atom is not in list atoms[] append to the list
            if comsplit[k] in atoms:
                print('   atom "{}" already known to be true'.format(comsplit[k]))
            else:
                print('   "{}" added to KB'.format(comsplit[k]))
                atoms.append(comsplit[k])
        elif hit == 0 and printing:
            print('Error: "{}" is not a valid atom'.format(comsplit[k]))

    if printing:
        print()
    return



#  Definition:  Prints all the atoms that can currently be inferred by the rules in the KB
def infer():
    global matrix
    global loaded
    global atoms
    new = []
    known = set(atoms)
    repeat = True

    # Append new True atoms from KB matrix into known set of atoms[]
    for i in range(len(matrix)):
        for j in range(2, len(matrix[i]), 2):
            if matrix[i][j] == 1:
                known.add(loaded[i][j])

    # Infer head atoms from rules, Repeat when newly inferred head atom is needed to infer another rule
    while repeat:
        repeat = False

        # For every rule in KB matrix
        for i in range(len(matrix)):
            # If the head has not been infered AND all the atoms in the rule adds up correctly
            if matrix[i][0] == 0 and (len(matrix[i]) - 3)/2 + 1 == sum(matrix[i]):
                repeat = True
                matrix[i][0] = 1
                # Append head atom into newly infered list AND run tell command on head atom
                new.append(loaded[i][0])
                tell(["", loaded[i][0]], False)

    # Print list of newly infered atoms
    print("   Newly inferred atoms:")
    if len(new) == 0:
        print("      <none>")
    else:
        print("      ", end = "")
        print(', '.join(new))

    # Print list of known atoms
    print("   Atoms already known to be true:")
    if len(known) == 0:
        print("      <none>")
    else:
        print("      ", end = "")
        print(', '.join(known))

    print()
    return



# Main function
if __name__ == "__main__":
    print("Interactive Interpreter Commands: ")
    print("   load - Loads into memory the KB stored in the file someKB.txt  (e.g: load someKB.txt)")
    print("   tell - Adds the atoms atom_1 to atom_n to the current KB  (e.g: tell atom_1 atom_2 ... atom_n )")
    print("   infer_all - Prints all the atoms that can currently be inferred by the rules in the KB  (e.g: infer_all)")
    print("   quit - Exits interactive interpreter  (e.g: quit)\n\n")

    # Loop interpreter until user quits
    while True:
        com = input("kb> ")
        comsplit = com.split()

        # Check command has valid length
        if len(comsplit) > 0:

            # Load Command
            if comsplit[0] == "load":
                # If load command is valid,
                if len(comsplit) == 2:
                    # If load succeeds, delete old load and replace with new load (resets all other KB lists)
                    if len(load(comsplit[1], True)) != 0:
                        loaded = []
                        matrix = []
                        atoms = []
                        loaded = load(comsplit[1], False)
                        loadMatrix()
                else:
                    print("Error: Incorrect formating for \"load\" command")
                    print("       Command \"load\" is followed by \"someKB.txt\"\n")

            # Tell Command
            elif comsplit[0] == "tell":
                if len(comsplit) > 1:
                    tell(comsplit, True)
                else:
                    print("Error: Incorrect formating for \"tell\" command")
                    print("       Command \"tell\" is followed by at least one atom\n")

            # InferAll Command
            elif comsplit[0] == "infer_all":
                if len(comsplit) == 1:
                    infer()
                else:
                    print("Error: Incorrect formating for \"infer_all\" command")
                    print("       Command \"infer_all\" is not followed by any command\n")

            # Quit Command
            elif comsplit[0] == "quit" and len(comsplit) == 1:
                exit()

            # Unknown Command entered
            else:
                print('Error: Unknown command "{}"\n'.format(com))

        # No Command entered
        else:
            print("Error: No command entered\n")
