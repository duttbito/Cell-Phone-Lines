"""
File:    network.py
Author:  Timmy Nguyen
Date:    12/17/23
Section: Section 32
E-mail:  tnguye34@umbc.edu
Description:
  connect phones with each other and to start + end calls
"""

"""
maybe
import json
import csv
"""
import json
import copy

HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'




def connect_switchboards(switchboards, area_1, area_2):
    #check if the two area codes are in the switchboard
    if (str(area_1) in switchboards) and (str(area_2) in switchboards):
        #check if they are not already connected with each other
        if str(area_2) not in switchboards[str(area_1)]['switch_connect']:
            switchboards[str(area_1)]['switch_connect'].append(str(area_2))
            switchboards[str(area_2)]['switch_connect'].append(str(area_1))
        else:
            print("The area codes are already connected")

    else:
        print("the entered area code(s) is not in the switchboard")


def add_switchboard(switchboards, area_code):
    #dictionary that will be the switchboard
    dict = {
        'switch_connect': [],
        'phone_list_connected': {},
    }

    #check if the area code is not already inside of the switchboard
    if str(area_code) not in switchboards:
        switchboards[str(area_code)] = dict
    else:
        print("area code was already in the switchboards")




def add_phone(switchboards, area_code, phone_number):
    #check if the area code is in the switchboard
    if str(area_code) in switchboards:
        #check if the phone number is not already in the switchboard
        if phone_number not in switchboards[str(area_code)]['phone_list_connected']:
            switchboards[str(area_code)]['phone_list_connected'][phone_number] = ''
        else:
            print("The entered phone number is already in the phone list")
    else:
        print("the entered area code is not in the switchboard")





def save_network(switchboards, file_name):
    #Need to hang up all the phone connections before saving the network
    temp_switchboards = copy.deepcopy(switchboards)

    hang_up_all_the_phone_connections(temp_switchboards)

    saved_file = open(file_name, 'w')

    json.dump(temp_switchboards, saved_file)
    saved_file.close()


def load_network(file_name):
    """
    :param file_name: the name of the file to load.
    :return: you must return the new switchboard network.  If you don't, then it won't load properly.
    """

    loaded_file = open(file_name)
    loaded_switchboards = json.load(loaded_file)
    loaded_file.close()

    return loaded_switchboards



def start_call(switchboards, start_area, start_number, end_area, end_number):
    #check if starting area is not in the switchboard
    if str(start_area) not in switchboards:

        print("Start area is not in the switchboard")
    #checking if ending area is not in the switchboard
    elif str(end_area) not in switchboards:
        print("End area is not in the switchboard")
    #check if the start number is not in the switchboard
    elif start_number not in switchboards[str(start_area)]['phone_list_connected']:
        print("Starting number is not in the switchboard")
    #check if the ending number is not in the switchboard
    elif end_number not in switchboards[str(end_area)]['phone_list_connected']:
        print("Ending number is not in the switchboard")
    else:
        if switchboards[str(start_area)]['phone_list_connected'][start_number] != '':
            print("This phone is already connected")
        else:
            if is_there_a_path(switchboards, str(start_area), str(end_area)):
                switchboards[str(start_area)]['phone_list_connected'][start_number] = end_number
                switchboards[str(end_area)]['phone_list_connected'][end_number] = start_number
                print(start_number + " and " + end_number + ' are now connected.')
            else:
                print(start_number + " and " + end_number + ' were not connected.')




def end_call(switchboards, area_code, phone_number):
    #check if the area is in the switchboard
    if str(area_code) in switchboards:
        #check if the phone number is not found in the switch board
        if phone_number not in switchboards[str(area_code)]['phone_list_connected']:
            print("Unable to disconnect")
        else:
            #check if any phone is connected to the phone the user is trying to disconnect
            if switchboards[str(area_code)]['phone_list_connected'][phone_number] == '':
                print("No phone is currently connected to this phone.")

            else:
                #disconnects the phone from each other
                connected_phone = switchboards[str(area_code)]['phone_list_connected'][phone_number]
                print("Hanging up...")
                #takes out the first phone number they added to disconnect
                switchboards[str(area_code)]['phone_list_connected'][phone_number] = ''
                #takes out the second phone number they added to disconnect

                connected_phone_list = connected_phone.split("-")
                switchboards[connected_phone_list[0]]['phone_list_connected'][connected_phone] = ''

                print("Connection Terminated.")
    else:
        print("Please enter a valid phone number")




def display(switchboards):
    #access the switchboard
    for switchboards_k, switchboards_v in switchboards.items():
        print("Switchboard with area code: " + switchboards_k)
        print("    Trunk lines are: ")
        for values in switchboards_v['switch_connect']:
            print("       Trunk line connection to: " + values)

        print("    Local phone numbers are:")
        for phone_list_connected_k, phone_list_connected_v in switchboards_v["phone_list_connected"].items():
            if is_phone_in_use(switchboards, phone_list_connected_k):

                print("       Phone with number: " + phone_list_connected_k + " is connected to " + phone_list_connected_v)
            else:
                print("       Phone with number: " + phone_list_connected_k + " is not in use.")

def hang_up_all_the_phone_connections(switchboards):
    '''
    for outer_k, outer_v in switchboards.items():
        outer_v["phone_connect"] = []
    '''

    for switchboards_k, switchboards_v in switchboards.items():
        for phone_list_connected_k, phone_list_connected_v in switchboards_v["phone_list_connected"].items():
            switchboards_v["phone_list_connected"][phone_list_connected_k] = ''



def is_phone_in_use(switchboards, phone_num):
    phone_num_slit = phone_num.split('-')

    is_in_use = False

    for switchboards_k, switchboards_v in switchboards.items():
        if switchboards_k == phone_num_slit[0]:
            for phone_list_connected_k, phone_list_connected_v in switchboards_v["phone_list_connected"].items():
                if (phone_list_connected_k == phone_num) and (phone_list_connected_v != ''):
                    is_in_use = True

    return is_in_use

def is_there_a_path(switchboards, starting_place, destination):
    visited = {}
    for place in switchboards:
        visited[place] = False

    switch_path = []
    switch_path = is_there_a_path_helper(switchboards, starting_place, destination, visited)

    if not switch_path: # No path between the switches
        return False
    else:
        return True






def is_there_a_path_helper(switchboards, starting_place, destination, visited):
    path = []  # set the path to empty at first, this will contain the path from the current place that we start to the end.


    if starting_place == destination:  # if we've reached the end, then begin constructing the path from the back.
        return [destination]
    # setting the visited to true so we don't loop back.
    visited[starting_place] = True

    '''
    for next_place in switchboards[starting_place]:
        if not visited[next_place]:
            path = is_there_a_path_helper(switchboards, next_place, destination, visited)
            if path:
                return [starting_place] + path
    '''


    for next_place in switchboards[starting_place]["switch_connect"]:
        if not visited[next_place]:
            path = is_there_a_path_helper(switchboards, next_place, destination, visited)
            if path:
                return [starting_place] + path


    visited[starting_place] = False
    # essentially this will return if no path is found, i.e. we still have  path = []
    return path



if __name__ == '__main__':
    #switchboards = None  # probably {} or []
    switchboards = {}
    s = input('Enter command: ')
    while s.strip().lower() != QUIT:
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
            area_1 = int(split_command[1])
            area_2 = int(split_command[2])
            connect_switchboards(switchboards, area_1, area_2)
        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
            add_switchboard(switchboards, int(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
            number_parts = split_command[1].split('-')
            area_code = int(number_parts[0])
            #phone_number = int(''.join(number_parts[1:]))
            add_phone(switchboards, area_code, split_command[1])
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
            save_network(switchboards, split_command[1])
            print('Network saved to {}.'.format(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
            switchboards = load_network(split_command[1])
            print('Network loaded from {}.'.format(split_command[1]))
        elif len(split_command) == 3 and split_command[0].lower() == START_CALL:
            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = int(src_number_parts[0])
            src_number = int(''.join(src_number_parts[1:]))

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = int(dest_number_parts[0])
            dest_number = int(''.join(dest_number_parts[1:]))
            start_call(switchboards, src_area_code, split_command[1], dest_area_code, split_command[2])


        elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
            number_parts = split_command[1].split(HYPHEN)
            area_code = int(number_parts[0])
            end_call(switchboards, area_code, split_command[1])


        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
            display(switchboards)

        s = input('Enter command: ')


	
