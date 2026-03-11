'''Jonathan Goohs
CS3001
Project 1
'''

### BEGIN RESTATING PROBLEM ###
'''
The problem as it is currently defined is one that takes one input, the desired end string of a derivative applying MIU rules.
The output of the problem is the optimal means to achieve that derivative.
The four rules that can be applied are:
1. Rule 1: If a string ends with "I", you can add a "U" at the end.
    Then, the rule 1 symbol |-1 is added as well as the resulting new string.
2. Rule 2: If "III" exists in a string, you can replace it with "U".
    This can apply to numerous IIIs throughout the string like MIIII or MIIIIIU. Each version must be checked.
    Then, the rule 2 symbol |-2 is added as well as the resulting new string.
3. Rule 3: If "UU" exists in a string, you can remove it.
    This rule can apply to numerous instances of UU, like MUUI or MUUUI. Each version must be checked.
    Then, the rule 3 symbol |-3 is added as well as the resulting new string.
4. Rule 4: If "M" is the first character in the string, the characters after "M" are duplicated and appended to the string.
    Then, the rule 4 symbol |-4 is added as well as the resulting new string.

By starting with a constant value of "MI" and applying all four rules if possible, the program outputs 
a set of each rule applied for a particular step. Another routine will check each item in the set from the rule application
in succession until the goal string is formed.
'''
### END RESTATING PROBLEM ###

### BEGIN IMPORTS ###
import time
### END IMPORTS ###

class MIU:
    """
    This class implements the MIU system, which applies a set of transformation
    rules to strings starting with "MI" to derive new strings ending when a goal string is met or attempts run out.
    """

    def __init__(self, goal):
        """
        Initialize the MIU system. All derivations start with "MI".
        """
        self.initial_string = "MI"
        self.goal = goal
        self.steps = set()
        
    def r_one(self, string):
        """
        Applies the first MIU rule: xI → xIU
        If the string ends with "I", append "U" to it.
        Args:
            string (str): The input string to apply the rule to.
        Returns:
            set: A set containing the resulting string if the rule applies,
                 or an empty set if the rule doesn't apply.
        """
        result_set = set()
        # Check if the string ends with "I"
        if string[-1] == "I":
            new_string = string + "U"
            result_set.add(new_string)

        return result_set
        
    def r_two(self,string):
        """
        Applies the second MIU rule: Replace "III" with "U".
        This can apply to multiple instances of "III" in the string.
        Args:
            string (str): The input string to apply the rule to.
        Returns:
            set: A set containing all possible resulting strings.
        """
        result_set = set()
        start_index = 0
        transformation_applied = False
        while True:
            #find the first instance of iii starting at the 0th index
            valid_index = string.find("III",start_index)
            #the return value for not found is -1 for find module
            if valid_index == -1:
                break
            #we have found a valid case to transform, so new string is the beginning to that found instance + U + the rest
            new_string = string[:valid_index] + "U" + string[valid_index + 3:]
            transformation_applied = True
            result_set.add(new_string)
            #increment the starting index to catch more instances of III
            start_index = valid_index + 1
        if transformation_applied == False:
            return result_set
        return result_set

    def r_three(self,string):
        """
        Applies the third MIU rule: Remove "UU".
        This can apply to multiple instances of "UU" in the string.
        Args:
            string (str): The input string to apply the rule to.
        Returns:
            set: A set containing all possible resulting strings.
        """
        result_set = set()
        start_index = 0
        transformation_applied = False
        while True:
            valid_index = string.find("UU",start_index)
            #if theres no UU in the string exit, then no transformation is
            if valid_index == -1:
                break
            #if the string is just UU, the set with a blank string should be returned
            if valid_index == 0:
                new_string = string[valid_index+2:]
                transformation_applied = True
            else: 
                new_string = string[:valid_index] + string[valid_index+2:]
                transformation_applied = True
            result_set.add(new_string)
            start_index = valid_index + 1
        #if the rules for UU didnt apply then just add the original string to the set
        if not transformation_applied:
            return result_set
        return result_set
    
    def r_four(self,string):
        """
        Applies the fourth MIU rule: Duplicate the string after "M".
        If "M" is the first character, duplicate the rest of the string and append it.
        Args:
            string (str): The input string to apply the rule to.
        Returns:
            set: A set containing the resulting string if the rule applies,
                 or the original string if the rule doesn't apply.
        """
        result_set = set()
        transformation_applied = False
        if string[0] == "M":
            new_string = string[0] + string[1:] + string[1:]
            result_set.add(new_string)
            transformation_applied = True
        if transformation_applied == False:
            result_set.add(string)
        return result_set      

    def derive(self, string):
        """
        Applies all four MIU rules to a given string and generates a set of results.
        Each result is stored as a tuple containing the rule identifier and the resulting string.
        Args:
            string (str): The input string to apply the rules to.
        Returns:
            set: A set of tuples, where each tuple contains a rule identifier and a resulting string.
        """
        result_set = set()
        # Apply Rule 1
        for result in self.r_one(string):
            if result != string:
                result_set.add(("|-1", result))
        # Apply Rule 2
        for result in self.r_two(string):
            if result != string:
                result_set.add(("|-2", result))
        # Apply Rule 3
        for result in self.r_three(string):
            if result != string:
                result_set.add(("|-3",result))
        # Apply Rule 4
        for result in self.r_four(string):
            if result != string:
                result_set.add(("|-4",result))
        return result_set

    def check(self):
        """
        Checks if the goal string can be derived from the initial string using the MIU rules.
        Tracks the path of derivations and prints the steps if the goal is found.
        Returns:
            bool: True if the goal is found, False otherwise.
        """
        # Initial derivation from the starting string
        derivation_from_mi = MIU.derive(self, self.initial_string)
        all_possible_derivatives = set(derivation_from_mi)
        max_attempts = 1000
        attempts = 0

        # Dictionary to track the path (string -> (rule, parent string))
        path_map = {}
        for rule, result in derivation_from_mi:
            path_map[result] = (rule, self.initial_string)

        # Loop until the goal is found in the derivations if possible (see internal holding for excessive runtime)
        while True:
            # Check if the goal is in the current derivations
            goal_found = False
            for rule, result in all_possible_derivatives:
                if result == self.goal:
                    goal_found = True
                    break

            if goal_found:
                # Trace back the path from the goal to the initial string
                path = []
                current = self.goal
                while current != self.initial_string:
                    rule, parent = path_map[current]
                    path.append((rule, current))
                    current = parent
                path.reverse()  # Reverse the path to start from the initial string
                #now add the initial string back in for printing at the end
                path = [self.initial_string] + path
                print(path)

                print(f"Goal '{self.goal}' found!")
                print("Path to goal:")
                for step in path:
                    print(f"{step[0]} {step[1]}")
                return True

            # Generate new derivations
            new_derivations = set()
            
            for rule, result in all_possible_derivatives:
                # Apply the derive method to the result
                derived_set = MIU.derive(self, result)
                attempts += 1
                if attempts == max_attempts:
                    print(f"Sorry, {self.goal} is not attainable given the current rule set for MIU...Exiting now.")
                    return False
                for new_rule, new_result in derived_set:
                    if new_result not in path_map:  # Avoid overwriting existing paths
                        path_map[new_result] = (new_rule, result)
                new_derivations.update(derived_set)  # Add new derivations to the set

            # Update the main set with the new derivations
            all_possible_derivatives.update(new_derivations)
            

def main():
    goal = input("Welcome to the MIU algorithm tester. Please input a string you would like to test for processing: ")
    init = MIU(goal)
    init.check()

if __name__ == "__main__":
    main()