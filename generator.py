import random
from pythonds.basic.stack import Stack

def RandomInfoInput():
    global random_base
    global random_weight
    global random_number
    global random_neg
    global random_type

    while True:
        try:
            random_base   = int(input("Please input the BASE of the randoms : "))
            if random_base in [2, 10, 16]:
                break
        except ValueError:
            continue
        else:
            print("Error 000 : The base is illegality for the moment.")
            continue

    while True:
        try:
            random_weight = int(input("Please input the WEIGHT of the randoms : "))
            if random_weight > 0:
                break
        except ValueError:
            continue

    while True:
        try:
            random_number = int(input("Please input the NUMBER of the randoms : "))
            if random_number > 0:
                break
        except ValueError:
            continue

    while True:
        random_neg    = input("Generate negtive random?(y/n) : ")
        if random_neg in ["y", "n"]:
            break

    while True:
        random_type   = input("Please input the type of random(int/int list/int tuple) : ")
        if random_type in ["int", "int list", "int tuple"]:
            break


def BaseConversion(origin_number, random_base, random_weight):
    digits = "0123456789ABCDEF"
    target_number = ""
    S = Stack()

    if origin_number < 0:
        neg_flag = True
        if random_base in [10, 16]:
            origin_number = - origin_number
        else:
            origin_number = - (origin_number + 1)
    else:
        neg_flag = False
    
    while True:
        number = origin_number // random_base
        rem    = origin_number %  random_base
        bit    = str(digits[int(rem)])
        S.push(bit)
        # print(bit)
        if number == 0:
            break
        origin_number = number

    while not S.isEmpty():
        target_bit = S.pop()

        if neg_flag == True and random_base == 2:
            if target_bit == "0":
                target_bit == "1"
            else:
                target_bit == "0"

        target_number = target_number + target_bit

    while True:
        if len(target_number) < random_weight and random_base == 2:
            if neg_flag == True:
                target_number = "1" + target_number
            else:
                target_number = "0" + target_number
        else:
            break

    if random_base in [10, 16]:
        if neg_flag == True:
            target_number = "-" + target_number
        else:
            target_number = " " + target_number

    return target_number


def RandomGenerator():
    global random_weight
    global random_base
    global random_number
    global random_type
    global random_neg


    if random_type in ["int list", "int tuple"]:
        if random_type == "int list":
            print("[" ,end="")
        elif random_type =="int tuple":
            print("(" ,end="")


    for i in range(random_number):
        
        if random_type in ["int list", "int tuple"] and i > 0:
            print(", " ,end="")
        
        # generate integer
        if random_type in ["int", "int list", "int tuple"]:
            
            # check the weight of the random
            if random_weight == 0:
                weight = random.randint(1,9)
            else:
                weight = random_weight
            
            # check the negtive enable flag
            
            max_range = int(random_base**weight)
            if random_neg == "n":
                min_range = 0
                max_range = max_range - 1
            else:
                min_range = - max_range
                max_range = max_range - 1

            number = random.randint(min_range, max_range)

            # print(number)
            target_number = BaseConversion(number, random_base, weight)
            print(target_number, end=" ")
        i = i + 1

    if random_type in ["int list", "int tuple"]:
        if random_type == "int list":
            print("]", end="")
        elif random_type == "int tuple":
            print(")", end="")

    print("")


def menu():
    print("-----------------------------------------------------------------")
    print("    1. Random numbers generator")
    print("-----------------------------------------------------------------")
    while True:
        menu_choice = input("Please press your choice : ") 
        if menu_choice in ["1"]:
            break
    
    if menu_choice == "1":
        global random_weight
        global random_number
        global random_base
        global random_type
        global random_neg

        RandomInfoInput()
        RandomGenerator()

random_weight   = 0         # 0 means random
random_number   = 10     
random_base     = 10
random_type     = "int"     # int 
random_neg      = "n"       # y-positive and negtive n-only positive

menu()
