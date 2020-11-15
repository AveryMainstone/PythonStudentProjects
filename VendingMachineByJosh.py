# Imports
import logging
import time;
import uuid
import datetime;

# Global Variables


global runDebug
runDebug = False;
# Names of Items and Price
global items;

global currentSymbol;

# The currency the machine is using
currentSymbol = "£";
# The default amount of each item the machine has in stock
stockOfEachItem = 2;
# The list of items and their properties in an array
items = [["Coke", currentSymbol + "1.00", stockOfEachItem], ["Water", currentSymbol + "0.50", stockOfEachItem],
         ["Orange", currentSymbol + "0.20", stockOfEachItem],
         ["Apple", currentSymbol + "0.50", stockOfEachItem]];


# START OF Functions
def debug(msg):
    if runDebug:
        # Shows debug messages when enabled
        print('\033[93m [DEBUG MESSAGE] {} \033[0m'.format(msg));


def findItemIndex(chkItem):
    # Making chkItem lowercase
    chkItem = chkItem.lower();
    # Setting counter to 0
    countGetItem = 0;
    # Accessing and looping through the 2D array
    for tempX in items:
        debug("Accessing: " + str(tempX))
        debug(tempX[0]);
        # Checking if value found matches check value.
        if (tempX[0].lower() == chkItem.lower()):
            debug("FOUND {} AT INDEX: ".format(chkItem) + str(countGetItem));
            return countGetItem;
        else:
            countGetItem = int(countGetItem) + 1;
            debug("NOT FOUND {} AT INDEX: ".format(chkItem) + str(countGetItem));
    return -1;


# Get Item Information
def getItemLocation(item):
    # If value is number search for item by number ID
    if str(item).isnumeric():
        debug(str(item) + "is numeric");
        # Checks if item is in array
        if int(selItem) < 0 or (int(selItem) + 1) > maxBound:
            # Display item is not found
            return -1;
        else:
            return int(item);

    # If value is not number search by name
    else:
        debug(str(item) + " not numeric");
        # Check if item is in list
        try:
            debug("Looking for {}.".format(item));
            # Calls function to find the item location within the machine
            return findItemIndex(item);
        except Exception as err:
            # prints the error if something goes wrong
            print(err)
            return -1;


def cls():
    # Makes a bunch of blank lines
    i = 0;
    while i < 100:
        print("\n")
        i = i + 1;


def callbackRun():
    print("Finishing up previous request... Please wait...");
    # Sleeps for 10 seconds
    time.sleep(10);
    # Clears the previous users input.
    cls();
    # Calls the main code again
    run();


def purchaseItem(item, price, inStock, pos):
    # Removes the currency symbol
    price = price.replace(currentSymbol, "");
    if inStock.lower() != "not in stock":

        #  print("Placing order");
        # Creates a transaction ID for the purchase.
        transactionID = str(uuid.uuid4());
        # Asks for the money to be input
        moneyInput = input("Please input how much money was inserted in the format (\"xx.xx\"):");
        # Removes currency symbol so it does not interfere with maths.
        moneyInput = moneyInput.replace(currentSymbol, "");
        changeGiven = 0;
        changeGivenArray = [""];
        if moneyInput.replace(".", "").isnumeric():
            # Changes data type
            moneyInput = float(moneyInput);
            if float(moneyInput) >= float(price):

                if float(moneyInput) - float(price) <= 0:
                    # Gives a success message and transaction information
                    print(
                        "Purchase successful. Your transaction id: {transactionX}".format(transactionX=transactionID));
                    # Creates log of transaction
                    createLog(str(transactionID), str(item), str(price), 0);
                else:
                    # Works out the change
                    changeGiven = str(round(float(moneyInput) - float(price), 2));
                    # Formats the change so it can split the pound from the pennies
                    changeGivenArray = changeGiven.split(".")

                    #  print("Change Given Size: " + str(len(changeGivenArray)));
                    # Checks to see if change includes pennies
                    if (len(changeGivenArray) > 1):
                        # Gives a success message and transaction information
                        print(
                            "Purchase successful. Your transaction id: {transactionX}".format(
                                transactionX=transactionID));
                        print("Change given: {currency}{pounds}.{pennies}".format(currency=currentSymbol,
                                                                                  pounds=changeGivenArray[0],
                                                                                  pennies=changeGivenArray[1]));
                        items[pos][2] = items[pos][2] - 1;
                        createLog(str(transactionID), str(item), str(price), str(changeGiven));
                    else:
                        if (len(changeGivenArray) < 3):
                            if (changeGivenArray == ""):
                                changeGivenArray[0] = 0;
                            # Gives a success message and transaction information
                            print(
                                "Purchase successful. Your transaction id: {transactionX}".format(
                                    transactionX=transactionID));
                            print("Change given: {currency}{pounds}.{pennies}".format(currency=currentSymbol,
                                                                                      pounds=changeGivenArray[0],
                                                                                      pennies="00"));
                            items[pos][2] = items[pos][2] - 1;
                            createLog(str(transactionID), str(item), str(price), str(changeGiven));
                        else:
                            pass;

            else:
                print("Insufficient Funds Available");
                purchaseItem(item, price, inStock, pos);
    else:
        # Something went wrong
        print("Not enough stock.")
        callbackRun();


def itemsForPurchaseMSG():
    # Sets count
    count = 1;
    # Create the message of what is avaliable and in stock to purchase.
    fullList = "----------------------------------------\n       Items avaliable to purchase   \n\n";
    for p in items:
        # Gets item name
        name = p[0]
        # Gets item price
        price = p[1]
        # Gets item stock level
        stock = p[2]
        if (stock > 0):
            fullList = fullList + str(count) + " - " + name + "\n";
            count = int(count) + 1;
        else:
            fullList = fullList + str(count) + " - " + name + " [OUT OF STOCK] " + "\n";
            count = int(count) + 1;
    return fullList + "\n----------------------------------------";


def createLog(transactionID, item, price, changeGiven):
    # Accesses the logging functions
    logging.basicConfig(filename="transactions.log", level=logging.INFO)
    # Logs the transaction
    logging.info(
        " {dateAndTime} | Transaction ID: {transactionIDf} - {itemf} was purchased for {pricef} and {currentSymbolf} {changeGivenf}\n".format(
            dateAndTime=datetime.datetime.now(),
            transactionIDf=str(transactionID), itemf=str(item), pricef=str(price), currentSymbolf=str(currentSymbol),
            changeGivenf=str(changeGiven)));


def run():
    # Welcome Message
    vendingMachineWelcomeMessage = "\n\n\n" + itemsForPurchaseMSG();

    # Print Welcome Message
    print(vendingMachineWelcomeMessage);

    # Which item are you selecting?
    global selItem;
    selItem = input("Select item: ");

    # Changes to human counting standard;
    if str(selItem).isnumeric():
        selItem = int(selItem) - 1;
        selItem = int(selItem);

    # Declare max boundary
    global maxBound;
    maxBound = len(items);

    # Prints output of what item is selected and the price
    global matrixLoc;
    matrixLoc = getItemLocation(selItem);
    # print(matrixLoc);
    if int(matrixLoc) >= 0:
        # print("Name: " + items[matrixLoc][0] + " \nPrice: " + items[matrixLoc][1]);
        global isAvailable;
        isAvailable = "";
        # Format of item info message
        formatOfItemInfoMSG = "\033[95m-=-=-=-=- SELECTION INFORMATION -=-=-=-=-\nName {itemName}\nPrice: {itemPrice}\nItem Available: {availableStatus}.\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\033[0m"
        if items[matrixLoc][2] > 0:
            # Sets message to show in stock
            isAvailable = "Item in stock";
            # Fill in the missing fields in the Item Info Message
            formattedItemInfoMSG = formatOfItemInfoMSG.format(itemName=str(items[matrixLoc][0]),
                                                              itemPrice=str(items[matrixLoc][1]),
                                                              availableStatus=str(isAvailable));
        else:
            # Sets message to show out of stock
            isAvailable = "Not in Stock";
            # Fill in the missing fields in the Item Info Message
            formattedItemInfoMSG = formatOfItemInfoMSG.format(itemName=str(items[matrixLoc][0]),
                                                              itemPrice=str(items[matrixLoc][1]),
                                                              availableStatus=str(isAvailable));
        print(formattedItemInfoMSG);
        if (isAvailable):
            purchaseItem(items[matrixLoc][0], items[matrixLoc][1], isAvailable, matrixLoc);
        callbackRun();

    else:
        if str(selItem).isnumeric():
            print("\033[31mThe item {} was not found. \033[0m".format("you selected"));
            callbackRun();
        else:
            print("\033[31mThe item \"{}\" was not found. \033[0m".format(selItem));
            callbackRun();


print(
    "\nNOTICE: Colours will not display correctly, and will show as random text unless code is run within PyCharm or a terminal that supports ANSI\n")
# Waits for 1 second
time.sleep(1);
# Displays startup message
print("Machine starting up... please wait...")
# Waits for 3 seconds
time.sleep(3);
# Calls main code
run();
