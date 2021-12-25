#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: lfox, nasharaf, lkota
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time
import random
import copy

ANY_EXP = ['xxx','zzz']


# Assign users based on passed in preference list, the current best assigment group based
# on cost and hashmap used to capture current team so we do not process again
def assign_groups(assignment_pref_list, best_assignment_group, eval_states):
    all_users = [assignment_pref.user for assignment_pref in assignment_pref_list]
    #Initial assignment
    best_assignment_group_found = best_assignment_group
    if best_assignment_group is None:
        assignment_teams = []
        eval_states = {}
        for assignment_pref in assignment_pref_list:
            assignment_teams.append(AssignmentTeam([assignment_pref.user]))
        cost = calculate_cost(assignment_teams, assignment_pref_list)
        best_assignment_group_found = AssignmentGroup(assignment_teams, cost)
        eval_states[hash(str(best_assignment_group_found.assignment_teams))] = assignment_teams
        return (best_assignment_group_found, eval_states)
    # Build an arbitrary number of groups based off users
    # If we have not seen this group config before calculate cost
    # Replace best assignment group found if cost is less
    # Otherwise continue
    for i in range(0,100000):
        assignment_teams = assign_teams_inc(best_assignment_group_found) #assign_teams_randomly(all_users)
        group_str = ""
        for assignment_team in assignment_teams:
            group_str += "-".join(assignment_team.users)
            group_str += " "
        hash_val = hash(group_str)
        if hash_val not in eval_states:
            eval_states[hash_val] = assignment_teams
            cost = calculate_cost(assignment_teams, assignment_pref_list)
            if cost < best_assignment_group_found.cost:
                best_assignment_group_found = AssignmentGroup(assignment_teams, cost)
    return (best_assignment_group_found, eval_states)


def assign_teams_inc(best_assignment_group):
    # Randomly pick number of changes between 1 and 4
    assignment_teams = copy.deepcopy(best_assignment_group.assignment_teams)
    for i in range(1, random.randint(1, 4)):
        # Grab a random team
        # Move the user to a random team or a new team
        # If user is only one in team delete team
        assignment_team = random.choice(assignment_teams)
        user_to_move = random.choice(assignment_team.users)
        if len(assignment_team.users) == 1:
            assignment_teams.remove(assignment_team)
        else:
            assignment_team.users.remove(user_to_move)
        choice_to_make = random.randint(1,3)
        if choice_to_make == 1:
            assignment_teams.append(AssignmentTeam([user_to_move]))
        else:
            random.shuffle(assignment_teams)
            user_matched = False
            for team_to_assign in assignment_teams:
                if len(team_to_assign.users) < 3:
                    team_to_assign.users.append(user_to_move)
                    user_matched = True
                    break
            if not user_matched:
                assignment_teams.append(AssignmentTeam([user_to_move]))
    return assignment_teams


# Calculate cost of assignment team
def calculate_cost(assignment_teams, assignment_pref_list):
    total_cost = 0
    for assignment_team in assignment_teams:
        total_cost += calculate_cost_team(assignment_team, assignment_pref_list)
    total_cost += len(assignment_teams) * 5
    return total_cost


# Calculate Cost of team
def calculate_cost_team(assignment_team, assigned_pref_list):
    cost_for_team = 0
    for user in assignment_team.users:
        assignment_pref = get_assignment_pref(assigned_pref_list, user)
        for other_user in assignment_team.users:
            if user != other_user:
                if assignment_pref.is_no_pref_user(other_user):
                    cost_for_team += 10
        if len(assignment_team.users) != len(assignment_pref.pref_group):
            cost_for_team += 2
        if not assignment_pref.all_prefer_users_added(assignment_team):
            cost_for_team += 3
    return cost_for_team


# Find preference for user
def get_assignment_pref(assigned_pref_list, user):
    for pref in assigned_pref_list:
        if user == pref.user:
            return pref
    return None


# Class to capture Assignment Group
class AssignmentGroup:
    def __init__(self, assignment_teams, cost):
        self.assignment_teams = assignment_teams
        self.cost = cost


# Class to capture Assignment Team
class AssignmentTeam:
    def __init__(self, users):
        self.users = users


# Class to capture Assignment Preference
class AssignmentPref:
    def __init__(self, user, pref_group, no_pref_group):
        self.user = user
        self.pref_group = pref_group
        self.no_pref_group = no_pref_group

    def is_pref_user(self, pref_user):
        return pref_user in self.pref_group

    def is_no_pref_user(self, no_pref_user):
        return no_pref_user in self.no_pref_group

    def all_prefer_users_added(self, assignment_team):
        for pref_user in self.pref_group:
            if pref_user not in ANY_EXP and pref_user not in assignment_team.users:
                return False
        return True


# Return dictionary with result from assignment group
def get_assignment_group_summary(assignment_group):
    team_array = []
    for assignment_team in assignment_group.assignment_teams:
        team_array.append("-".join(assignment_team.users))
    return {"assigned-groups": team_array, "total-cost": assignment_group.cost}


def parse_file(input_file):
    assignment_pref_list = []
    with open(input_file) as lines:
        for ln in lines:
            if len(ln) >0:
                entries = ln.split()
                assignment_pref_list.append(AssignmentPref(entries[0], entries[1].split('-'), entries[2].split(',')))
    return assignment_pref_list


def solver(input_file):
    # Parse the input file and create a list ossignment preferences
    data = parse_file(input_file)
    # Create Initial best guess at assignment group
    assignment_group, eval_states = assign_groups(data, None, [])

    # First we yield a quick solution
    yield(get_assignment_group_summary(assignment_group))
    #
    # # Then we think a while and return another solution:
    time.sleep(10)
    assignment_group, eval_states = assign_groups(data, assignment_group, eval_states)
    # Generate a slightly better solution
    yield(get_assignment_group_summary(assignment_group))
    #
    # # This solution will never befound, but that's ok; program will be killed eventually by the
    # #  test script.
    while True:
        assignment_group, eval_states = assign_groups(data, assignment_group, eval_states)
        yield(get_assignment_group_summary(assignment_group))

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
