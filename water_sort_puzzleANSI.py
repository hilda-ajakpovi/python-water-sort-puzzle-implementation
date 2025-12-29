
from bqueue import BQueue
from bstack import BStack
from random_chemicals_generator import main1
import os
MAX_SAME_CHEMICALS = 3
MAXIMUM = 4 # max number of chemicals per flask and flask per row
ANSI = {
"RED": "\033[31m",
"GREEN": "\033[32m",
"BLUE": "\033[34m",
"HRED": "\033[41m",
"HGREEN": "\033[42m",
"HBLUE": "\033[44m",
"UNDERLINE": "\033[4m",
"RESET": "\033[0m",
"CLEARLINE": "\033[0K"
}

def read_file(filename: str) -> list:
    '''
    Takes in a filename, reads the file and returns a list of all the lines in the file
    '''
    file = open(filename, 'r')
    text = file.read()
    file.close()
    
    text = text.splitlines()
    return text

def create_all_flasks_dict(text:list) -> dict:
    '''
    Creates and returns a dictionary of all the bounded stacks needed for each flask
    '''
    all_flasks = {}
    if text[0][2] == ' ':
        num_of_flasks = int(text[0][0]+text[0][1])
    else:
        num_of_flasks = int(text[0][0])
        
    for i in range(1, num_of_flasks+1):
        all_flasks[str(i)] = BStack(MAXIMUM, MAX_SAME_CHEMICALS)
    return all_flasks
    
def sort_chemicals(text, bqueue_of_chemicals, all_flasks):
    '''
    Takes the chemicals from the list from the text, enqueues them to a bounded 
    queue of capacity 4 and when called for dequeues the chemical from the bounded 
    queue to the bounded stack coresponding to the flask number the text calls for
    '''
    for item in text[1:]:
        # enqueueing chemicals
        if not item[0].isnumeric(): # checking if we're dealing with a chemical or instructions
            try:
                bqueue_of_chemicals.enqueue(item)
                
            except:
                pass
        # dequeueing and pushing chemicals
        else:
            for j in range(int(item[0])):
                try:
                    try: 
                        temp = item[3]
                        flask_num = item[2]+item[3]
                    except:
                        flask_num = item[2] 
                    finally:
                        chemical = bqueue_of_chemicals.dequeue()
                        all_flasks[flask_num].push(chemical) 
                except:
                    pass
                
def display_flasks(all_flasks, row_num, flasks_per_row, exit):
    '''
    display the flasks with the chemicals in it
    Input: disctionary of bounded stacks containing the chemicals
    '''
    chemical_colors = {
    'AA': ANSI["HRED"],
    'BB': ANSI["HBLUE"],
    'CC': ANSI["HGREEN"],
    'DD': '\033[48:5:208m',
    'EE': '\033[38:5:232m'+'\033[48:5:226m',
    'FF': '\033[48:5:164m',
    'GG': '\033[48:5:57m',
    'HH': '\033[48:5:88m',
    'II': '\033[38:5:232m'+'\033[48:5:189m',
    'JJ': '\033[48:5:59m',
    'KK': '\033[48:5:204m',
    'LL': '\033[48:5:69m',
    'OO': '\033[38:5:232m'+'\033[48:5:78m',
    'MM': '\033[38:5:232m'+'\033[48:5:231m',
    'NN': '\033[48:5:236m'
    }
    
    row = ''  
    num_of_rows = 6
    last_row_index = 5
    if not exit:
        for i in range(num_of_rows):
            #for j in range(1, len(all_flasks)+1):
            for j in range(1+row_num*flasks_per_row, (1+flasks_per_row)+row_num*flasks_per_row): # for the keys of all_flasks or flask number
                if str(j) in all_flasks:
                    # for the base of flasks
                    if i == MAXIMUM:
                        row += '+--+  '
                    elif i == last_row_index:
                        row += '{:^4}  '.format(j)
                        
                    # for flasks
                    else:
                        #print(all_flasks[str(7)].isSealed())
                        if not all_flasks[str(j)].isSealed():
                            try:
                                row += f'|{chemical_colors[all_flasks[str(j)].display()[i]]}{all_flasks[str(j)].display()[i]}{ANSI["RESET"]}|  '
                            except KeyError:
                                row += f'|{all_flasks[str(j)].display()[i]}|  '
                        else:
                            if i == 0:
                                row += '+--+  '
                            else:
                                try:
                                    row += f'|{chemical_colors[all_flasks[str(j)].display()[i-1]]}{all_flasks[str(j)].display()[i-1]}{ANSI["RESET"]}|  ' 
                                except KeyError:
                                    row += f'|{all_flasks[str(j)].display()[i-1]}|  ' 
                                
            row += '\n'
    return row + '\n'
    #print('\033[6;0{:}'.format(row))
    
def display_flask_rows(all_flasks, flasks_per_row, exit):
    '''
    Check if the number of flasks is divisible by 4 (This will tell if an extra 
    row is needed after int divion). Then interavily display the row of flasks 
    each containing 4 flasks
    '''
    output = ''
    num_of_rows = 2
    for row_num in range(num_of_rows): # iteravaly run the display_flasks to get 4 flasks per row
        output += display_flasks(all_flasks, row_num, flasks_per_row, exit) 
    print(f'\033[6;0H{output}')

def get_user_input(flask, all_flasks, row):
    '''
    Gets and returns user input and validates whether it's one of the flasks or 
    exit and if the user can pour from or into that flask
    Input: string telling whether the function is dealing with the source or destination flask; a dictionary or bounded stacks (flasks)
    '''
    
    # validates if user entered a flask or exit
    print(f"\033[{row};0HSelect {flask} Flask: ", end='')  
    #print(f'\033[{row}; {len(phrase)}H')
    user_input = input().rstrip().lower()
    while user_input not in all_flasks and user_input != 'exit':
        user_input = process_invalid_input(row, flask, 'Invalid input. Try again')                          
        
    if user_input != 'exit':
        
        if flask == 'Source':
            user_input = check_valid_flasks('empty', row, flask, all_flasks, user_input, 'Cannot pour from that flask. Try again.')
            '''
            while all_flasks[user_input].isEmpty() or all_flasks[user_input].isSealed():
                user_input = process_invalid_input(row, flask, 'Cannot pour from that flask. Try again')
                
                while user_input not in all_flasks and user_input != 'exit':
                    user_input = process_invalid_input(row, flask, 'Invalid input. Try again.')  
                    '''
                    
        elif flask == 'Destination':
            user_input = check_valid_flasks('full', row, flask, all_flasks, user_input, 'Cannot pour into that flask. Try again.')
            '''
            while all_flasks[user_input].isFull() or all_flasks[user_input].isSealed():
                user_input = process_invalid_input(row, flask, 'Cannot pour into that flask. Try again.') 
                
                while user_input not in all_flasks and user_input != 'exit':
                    user_input = process_invalid_input(row, flask, 'Invalid input. Try again')
                    '''
    
    return user_input

def process_invalid_input(row, flask, error):
    '''
    Display the appropriate error message, clears the line and moves the cursor back to where it needs 
    '''
    print(f'\033[5;0H{error}', end='')        
    print(f"\033[{row};0HSelect {flask} Flask: ", end='') 
    print(ANSI["CLEARLINE"], end='')        
    user_input = input()
    print(f'\033[5;0H{" "*len(error)}', end='') 
    return user_input

def check_valid_flasks(flask_condition, row, flask, all_flasks, user_input, message):
    '''
    Validate that the user does not choose a flask that is empty or full
    '''
    
    if flask_condition == 'full':
        boolean = all_flasks[user_input].isFull()
    elif flask_condition == 'empty':
        boolean = all_flasks[user_input].isEmpty()
       
    while boolean or all_flasks[user_input].isSealed():
        user_input = process_invalid_input(row, flask, message) 
        
        while user_input not in all_flasks and user_input != 'exit':
            user_input = process_invalid_input(row, flask, 'Invalid input. Try again')
           
        if flask_condition == 'full':
            boolean = all_flasks[user_input].isFull()
        elif flask_condition == 'empty':
            boolean = all_flasks[user_input].isEmpty()  
         
    return user_input

def update_flasks(all_flasks, source_flask, destination_flask, moves):
    '''
    Updates the appropriate stacks by popping a chemical from the sources stack/flask 
    and pushing it onto the destination. Also updates the user_manipulated attribute 
    by calling the userManipulated method so that the flask can be sealed if need be
    '''
    all_flasks[source_flask].userManipulated()        
    chemical = all_flasks[source_flask].pop()
    
    all_flasks[destination_flask].userManipulated()        
    all_flasks[destination_flask].push(chemical)
    
    return moves+1
    
def update_sealed_flasks(flask, sealed_flasks, all_flasks):
    '''
    Updates the number of sealed flasks if a flask has been sealed
    '''
    if all_flasks[flask].isSealed():
        sealed_flasks += 1  
    return sealed_flasks
 
def main():
    os.system('')
    # Local Variables
    bqueue_of_chemicals = BQueue(MAXIMUM)
    text = read_file('random_chemicals.txt')
    all_flasks = create_all_flasks_dict(text)
    exit = False
    won = False
    sealed_flasks = 0 
    ddigit_flasks = False
    
    if text[0][2] == ' ':
        ddigit_flasks = True
        flasks_per_row = int(text[0][0]+text[0][1])//2
        
        try:
            num_of_chemicals = int(text[0][3] + text[0][4])
        except:
            num_of_chemicals = int(text[0][3])
    else:
        num_of_chemicals = int(text[0][2])
        
        flasks_per_row = int(text[0][0])//2
    
    sort_chemicals(text, bqueue_of_chemicals, all_flasks)
    
    #display_flask_rows(all_flasks, flasks_per_row)
    moves = 0
    
    while not won and not exit:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.sytem('clear')
            
        print(f"Water Sort Puzzle {moves}\n")
        
        print('Select Source Flask: ')
        print('Select Destination Flask: ')
        display_flask_rows(all_flasks, flasks_per_row, exit)
        
        
        source_flask = get_user_input('Source', all_flasks, 3)
        
        if source_flask == 'exit':
            exit = True
            
        if not exit:
            destination_flask = get_user_input('Destination', all_flasks, 4)
            if destination_flask == 'exit':
                exit = True
            
            if not exit:
                while source_flask == destination_flask:
                    print('\033[5;0HCannot pour into the same flask. Try again. ', end='') 
                    print('\033[4;0HSelect Destination Flask: ',  end='')
                    print(ANSI["CLEARLINE"], end='')                                                
                    destination_flask = get_user_input('Destination', all_flasks, 4)
                    if destination_flask == 'exit':
                        exit = True  
                #display_flask_rows(all_flasks)                
                    
                if not exit:
                    moves = update_flasks(all_flasks, source_flask, destination_flask, moves)
                    
                    sealed_flasks = update_sealed_flasks(source_flask, sealed_flasks, all_flasks)
                    sealed_flasks = update_sealed_flasks(destination_flask, sealed_flasks, all_flasks)
                    
                    display_flask_rows(all_flasks, flasks_per_row, exit)
                    
                    if sealed_flasks == num_of_chemicals:
                        print('You Win!')
                        play_again = input('Play Again?(y/n) ').strip().lower()
                        valid_inputs = ('y', 'n')
                        while play_again not in valid_inputs:
                            play_again = input('Invalid input. Try again.' )
                            
                        if play_again == 'y':
                            for i in all_flasks:
                                all_flasks[i].changeSealed(False)
                            main1()
                            main()
                        else:
                            won = True       
        
        
    
main()