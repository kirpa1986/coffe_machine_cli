import questionary as qnry
import random
from dotenv import load_dotenv
import os
import time

from data.resources import resources, coins
from data.receipts import receipts

def is_enough_resources(coffee_selected):
    ingridients = receipts[coffee_selected]['ingredients']
    for ingridient in ingridients:
        if ingridients[ingridient] > resources[ingridient]:
            return (False, ingridient)
    return True
 
def get_money(coffee_selected):
    beverage_cost = receipts[coffee_selected]['cost']
    credit_options = []
    for each in coins:
        credit_options.append(each.title())
    credit_options.append("Refund")
    coins_credited = {
    "quarters": 0,
    "dimes": 0,
    "nickles": 0,
    "pennies": 0
    }
    total_amount = 0
    while beverage_cost - total_amount > 0:
        os.system('clear')
        print(f'The cost of {coffee_selected.title()} is ${beverage_cost}')
        remaining_amount = round(beverage_cost - total_amount, 2)
        print(f"Remaining amount: ${remaining_amount}")
        opt = qnry.select("Select coin:", choices=credit_options).ask()
        if opt != 'Refund':
            coins_amount = int(qnry.text(f"How many {opt.lower()}: ").ask())
            coins_credited[opt.lower()] += coins_amount
            total_amount += round(coins_amount * coins[opt.lower()]['value'], 2)
        else: 
            print("Refunding the order...")
            time.sleep(1)
            return False

    return (coins_credited, total_amount) 
              
def prepare_beverage(coffee_selected):
    ingredients = receipts[coffee_selected]['ingredients']
    for ingredient in ingredients:
        resources[ingredient] -= ingredients[ingredient]

def get_change(change, coins_used):
    if change > 0:
        print(f"Please take your change: ${change}:")
        change_coins = {}
        for each in coins_used:
            count_coins = int(change / coins[each]['value'])
            if count_coins != 0:
                if count_coins > coins_used[each]:
                    change_coins[each] = coins_used[each]
                    coins_used[each] = 0
                    change -= (change_coins[each]*coins[each]['value'])
                else:
                    change_coins[each] = count_coins
                    coins_used[each] -= count_coins
                    change -= (change_coins[each]*coins[each]['value'])
                print(f"{each}: {change_coins[each]}")
    for coin in coins_used:
        coins[coin]['count'] += coins_used[coin]    
            

def brew():
    os.system('clear')
    receipt_types = []
    for each in receipts:
        receipt_types.append(each.title())
    receipt_types.append("Nothing")
    coffee_selected = qnry.select("Select a beverage you would like!", choices = receipt_types).ask()
    
    if coffee_selected != 'Nothing':
        enough_to_prepare = is_enough_resources(coffee_selected.lower())
        if enough_to_prepare != True:
            print(f"\nWe are so sorry! There are not enough {enough_to_prepare[1]} to prepare the selected beverage!\n")
        else:
            os.system('clear')
            result = get_money(coffee_selected.lower())
            if result:
                os.system('clear')
                print(f'Please wait, I am working on your {coffee_selected.lower()}')
                prepare_beverage(coffee_selected.lower())
                time.sleep(2)
                print(f"Your {coffee_selected.lower()} is ready. Enjoy!")
                change = result[1] - receipts[coffee_selected.lower()]['cost']
                get_change(round(change, 2), result[0])


    
    qnry.text("Press Enter to continue").ask()

def show_avail_resources():
    print("Available resources:")
    avail_resources = []
    for each in resources:
        print(f"{each.title()}: {resources[each]}")  
        avail_resources.append(each.title())  
    print('-'*30)
    return avail_resources


def show_machine_balance():
    print("Coins Total:")
    total = 0
    for each in coins:
         print(f"{each.title()}: {coins[each]['count']} coins, ${coins[each]['count']*coins[each]['value']}")  
         total += coins[each]['count']*coins[each]['value']
    print(f'Total amount: {total}')
    print('-'*30)

        

def maintenance_mode():
    pwd = qnry.password("Password: ").ask()
    if  adm_pass == pwd:
        maint_mode = True
        while maint_mode:
            os.system('clear')
            print("Maintenance Mode" + '\n' + '-'*len("Maintenance Mode"))
            avail_resources = show_avail_resources()
            show_machine_balance()
            avail_resources.append("Exit Maintenance Mode")
            resource_to_add = qnry.select("Select resource to add: ", choices = avail_resources, pointer='👉 ', qmark="").ask()
            if resource_to_add == "Exit Maintenance Mode":
                print("Leaving Maintenance Mode...")
                time.sleep(1)
                maint_mode = False
            else: 
                amount = int(qnry.text("How much units to add? ", qmark="").ask())
                resources[resource_to_add.lower()] += amount
        
    

load_dotenv()
adm_pass = os.getenv("ADMIN_PASS")
money = 0

global_mode = True
while global_mode:
    os.system('clear')
    q = qnry.select("Hi! I am a coffee machine! What do you want to do?",choices=["Brew a coffee ☕", "Maintenance Mode", "Turn Off"], pointer='👉 ', qmark="").ask()

    if q == 'Brew a coffee':
        os.system('clear')
        brew()
    if q == 'Maintenance Mode':
        os.system('clear')
        maintenance_mode()
    if q == "Turn Off":
        print("Turning off...")
        time.sleep(1)
        exit()
        

    
