# -*- coding: utf-8 -*-
"""setup

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WCcUl4R4cD_OmyRwnRC6xNqTKY3SNGnO

#**Stock Market Simulation Game** 
## Data Science Team:
**Data Science Manager** - Anade Davis

**Lead Data Scientist** - Ragavendhra Ramanan 

**Lead Machine Learning Engineer** - Tanjeel Ahmed 

**Lead Data Science Researcher** - Hafizah Ab Rahim

**Data Scientist** - Ivy Hsu

**Data Engineer** - Brandon Oppong-Antwi

**Data Science Researcher** -  Michael Ayedun


Sources: 
https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/wall-street-survivor-stock-market-game/
shreyanshs7/Wallstreet-Django
https://github.com/Agtm48/Stock-Market-Simulator
"""

import os #Operating System
path = os.getcwd() #Create the file path from the operating system.And returns current working directory of a process
os.chdir(path) #changes the current working directory to the given path
dbpath = (str(os.getcwd()) + "\\Stocks.db") #returns the absolute path of the working directory where Python is currently running as a string for our db file
fpath = (str(os.getcwd() + "\\task4data.csv")) #returns the absolute path of the working directory where Python is currently running as a string for our Stock tickers
from time import sleep #used to simulate delays within our code
import sys #module provides information about constants, functions and methods of the interpreter
from character import BusinessPerson #import from our customerName class
from database_connection import * #establish the database connection 
stocksBought = []

#Start the initial environment 
def env_start():
    for i in range(1, 11):
        sleep(0.1)
        print("*" * i)
    print(os.getcwd())
    print("Welcome to the Stock Game. In this game, you will try to make money by buying or selling certain stocks."
          " However, make sure that you make smart investment choices or you could be bankrupt at the end")
    name = input("What is your name?")
    object_customer = BusinessPerson(name)
    print("Welcome, " + name + ".")
    print("Here are the available stocks for today.")
    objective(object_customer)

#Goes over the rules of the game and what the user can expect and connects to the database
def objective(object_customer):
    day = 1
    isInput = False
    while isInput != True:
        print("The objective of the game is to make as much money as possible in a 7 day period.")
        sleep(0.25)
        print("Each day, you will be given a list of stocks to choose from, and you can buy as many as you can"
              " You will start out with $1000")
        sleep(0.25)
        print("However, the value of the stocks will rise and fall, mimicking the behaviors of some stocks on"
              " previous accounts, taken from real data.")
        sleep(0.25)
        start = input("Are you ready to start the game? (Y/N)")
        if(start.lower() == "y"):
            break
        elif(start.lower() == "n"):
            print("The objective of the game is to make as much money as possible in a 7 day period.")
            sleep(0.25)
            print("Each day, you will be given a list of stocks to choose from, and you can buy as many as you can"
                  " possibly fit with your money constraint, which starts out with $500")
            sleep(0.25)
            print("However, the value of the stocks will rise and fall, mimicking the behaviors of some stocks on"
                  " previous accounts, taken from real life data.")
            isInput = True

        else:
            print("Invalid Input!")


    full_database()
    print("Successfully created the database")
    insert_values()
    print("The game is about to begin.")
    display_stocks(day)
    while(day <= 8):
        vchoice = input("Press 1 to view your information. \nPress 2 to see the available stocks for today. "
                        "\nPress 3 to see how many stocks you have bought. \nPress 4 to buy a stock. "
                        "\nPress 5 to sell a stock. \nPress 6 to move on to the next day.")
        if(vchoice == "1"):
            display_statistics(object_customer)
        elif(vchoice == "2"):
            display_stocks(day)
        elif(vchoice == "3"):
            display_bought()
        elif(vchoice == "4"):
            buy_stock(object_customer, day)
        elif(vchoice == "5"):
            sell_stock(object_customer, day)
        elif(vchoice == "6"):
            if day < 8:
                temp = day + 1
                print("Moving from day " + str(day) + " to " + str(temp))
                sleep(0.5)
                day = temp
                display_stocks(day)
            if day == 8:
                print("The game is over! '" + str(object_customer.name).title() + "' finished with $" + str(object_customer.money))
                break
    print("About to delete all values from the database")
    sleep(.25)
    clean_data()
    sys.exit()


#Keep track of metrics and report the actions taken to the user
def display_statistics(object_customer):
    print("Name: " + str(object_customer.name))
    print("Money Remaining: " + str(object_customer.money))

#Display what was bought
def display_bought():
    count = 1
    for item in stocksBought:
        print("Stock " + str(count) + " is " + str(item) + ".")
        count = count + 1
#Connects to the database and ask the user for information
def buy_stock(object_customer, dayofweek):
    val_input = False
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute("SELECT Ticker from Stocks")
    ticks = cur.fetchall()
    cur.execute("SELECT Name from Stocks")
    stock_name = cur.fetchall()
    cur.execute("SELECT " + str(stockDict[dayofweek]) + " from Stocks")
    stock_values = cur.fetchall()
    while(val_input != True):
        ch = input("Which stock would you like to buy?")
        for i in range(0, len(ticks)):
            if(ch.lower() in str(ticks[i]).lower()) or (ch.lower() in str(stock_name[i]).lower()):
                amt = input("How many of the stock " + parse(str(stock_name[i])) + " would you like to buy?")
                cost = float(amt) * float(parse(str(stock_values[i])))
                if cost > object_customer.money:
                    print("Sorry, you have insufficient funds in your account for you to make that transaction. ")
                    cost = 0
                object_customer.money = object_customer.money - cost
                print("Your transaction has been completed. You paid $" + str(cost) + ".")
                if cost <= object_customer.money:
                    for number in range(0, int(amt)):
                        stocksBought.append(parse(str(stock_name[i])))
                val_input = True
                break
            else:
                if i == len(ticks):
                    print("Sorry, the given stock name is not available!")
#Sell stock action and update of database
def sell_stock(object_customer, dayOfWeek):
    val_input = False
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute("SELECT Ticker from Stocks")
    ticks = cur.fetchall()
    cur.execute("SELECT Name from Stocks")
    stock_name = cur.fetchall()
    cur.execute("SELECT " + str(stockDict[dayOfWeek]) + " from Stocks")
    stock_values = cur.fetchall()
    while (val_input != True):
        ch = input("Which stock would you like to sell?")
        for i in range(0, len(ticks)):
            if (ch.lower() in str(ticks[i]).lower()) or (ch.lower() in str(stock_name[i]).lower()):
                amt = input("How many of the stock " + parse(str(stock_name[i])) + " would you like to sell?")
                benefit = float(amt) * float(parse(str(stock_values[i])))
                countVar = 0
                for item in stocksBought:
                    sv = parse(str(stock_name[i]))
                    if(sv.lower() == item.lower()):
                        countVar = countVar + 1
                if(int(amt) <= int(countVar)):
                    pass
                else:
                    print("Sorry, you do not have the required number "
                          "of stocks to successfully process that transaction.")
                    benefit = 0
                object_customer.money = object_customer.money + benefit
                print("Your transaction has been completed. You gained $" + str(benefit) + ".")
                val_input = True
                break
            else:
                if i == len(ticks):
                    print("Sorry, the given stock name is not available!")
def parse(x):
    x = str(x)
    x = x.replace("('", "")
    x = x.replace("',),", "")
    x = x.replace(",),", "")
    x = x.replace("[", "")
    x = x.replace("]", "")
    x = x.replace("(", "")
    x = x.replace(",)", "")
    x = x.replace("'", "")
    return x
env_start()

