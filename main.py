import random
import csv

f = open('test1.csv','w', newline='')
writer = csv.writer(f)

row1 = ["Trial", "Weight 1", "Weight 2", "Success", "Wins","Win Rate"]

writer.writerow(row1)


AICards = []
AllCards = {'A':4, '2':4, '3':4, '4':4, '5':4, '6':4, '7':4, '8':4, '9':4, '10':4, 'J':4, 'Q':4, 'K':4}
DealerCards = []
weights = [0.92,1.8]
trainingWeight = 0.001
timesTrained = 10000

#GAMEPLAY
deck = ['A', 'A', 'A', 'A', '2', '2', '2', '2', '3', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']
random.shuffle(deck)

def getCard():
    global deck
    return deck.pop()

#MUTATORS
def setWeights(newList):
    weights = newList

def addToAICards(newCard):
    AICards.append(newCard)
    removeCards(newCard)

def addToDealerCards(newCard):
    DealerCards.append(newCard)
    removeCards(newCard)

#ACCESSORS
def getWeights():
    return weights

#GENERAL FUNCTIONS
def setup(numberused):
    global DealerHidden
    if(numberused==1):
        AICard1 = getCard()
        AICard2 = getCard()
        DealerCard = getCard()
        DealerHidden = getCard()

        AICards.append(AICard1)
        #print("AI's First Card: ", AICard1)
        AICards.append(AICard2)
        #print("AI's Second Card:", AICard2)
        DealerCards.append(DealerCard)
        #print("Dealer's First Card: ", DealerCard)
        #print("Dealer's Hidden Card: ", DealerHidden)
        removeCards(AICards)
        removeCards(DealerCards)
        #print("AI has: ", AICards)
        #print("Dealer has: ", DealerCards)
        #print("(DEBUG): ", AllCards)
    if(numberused==2):
        return DealerHidden

def reset():
    global AllCards
    global deck
    AICards.clear()
    DealerCards.clear()
    AllCards = {'A':4, '2':4, '3':4, '4':4, '5':4, '6':4, '7':4, '8':4, '9':4, '10':4, 'J':4, 'Q':4, 'K':4}
    deck = ['A', 'A', 'A', 'A', '2', '2', '2', '2', '3', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']
    random.shuffle(deck)
    setup(1)

def sumList(Cards):
    sum = 0
    for i in range(len(Cards)):
        sum += charToNum(Cards[i])
    return sum

def sumListAI(Cards):
    sum = sumList(Cards)
    for i in range(numAce(Cards)):
        if(sum>21):
            sum -= 10
    return sum


def sumListDealer(Cards, hidden):
    CardSum = sumList(Cards)
    sum = 0
    sum += charToNum(hidden)
    if(CardSum+sum>21 and sum == 11):
        sum = 1
    
    for i in range(numAce(Cards)):
        if(CardSum+sum>21):
            CardSum -= 10
    
    return  CardSum + sum


def higherCards(inputnum):
    greaterCards = 0
    lowerCards = 0

    for i in range(1, 11):
        if(i>inputnum):
            greaterCards += AllCards[numToChar(i)]
        else:
            lowerCards += AllCards[numToChar(i)]
    
    if(10>inputnum):
        greaterCards += AllCards[numToChar(11)]
        greaterCards += AllCards[numToChar(12)]
        greaterCards += AllCards[numToChar(13)]
    else:
        lowerCards += AllCards[numToChar(11)]
        lowerCards += AllCards[numToChar(12)]
        lowerCards += AllCards[numToChar(13)]
    
    return greaterCards, lowerCards


def charToNum(inputchar):
    if(inputchar=='A'):
        return 11
    if(inputchar=='J' or inputchar=='Q' or inputchar=='K'):
        return 10
    else:
        return int(float(inputchar))
    print("Custom Error: no charToNum instance picked")
    return 0

def numToChar(inputnum):
    if(inputnum==1):
        return 'A'
    elif(inputnum==2):
        return '2'
    elif(inputnum==3):
        return '3'
    elif(inputnum==4):
        return '4'
    elif(inputnum==5):
        return '5'
    elif(inputnum==6):
        return '6'
    elif(inputnum==7):
        return '7'
    elif(inputnum==8):
        return '8'
    elif(inputnum==9):
        return '9'
    elif(inputnum==10):
        return '10'
    elif(inputnum==11):
        return 'J'
    elif(inputnum==12):
        return 'Q'
    elif(inputnum==13):
        return 'K'
    return inputnum
    

def removeCards(Cards):
    if(isinstance(Cards, list)):
        for i in range(len(Cards)):
            #print(i)
            AllCards[Cards[i]] = AllCards[Cards[i]] - 1
    if(isinstance(Cards, str)):
        AllCards[Cards] = AllCards[Cards] - 1

def numAce(Cards):
    aceCount=0
    for i in range(len(Cards)):
        if(Cards[i]=='A'):
            aceCount += 1
    #print("Number of Aces: ", aceCount)
    return aceCount

def numCards():
    totalCards = 0
    for key,val in AllCards.items():
        totalCards += val
    return totalCards

#HIDDEN NEURON #1
def breaking_probability(Cards):
    sum = 0
    distance = 21
    breakingCards = 0
    safeCards = 0
    probabilitySafe = 0

    sum = sumListAI(Cards)
    distance = distance - sum

    #print(distance)

    removeCards(AICards)
    removeCards(DealerCards)
    
    """
    for i in range(1, 11):
        if(i>distance):
            breakingCards += AllCards[numToChar(i)]
        else:
            safeCards += AllCards[numToChar(i)]
    
    if(10>distance):
        breakingCards += AllCards[numToChar(11)]
        breakingCards += AllCards[numToChar(12)]
        breakingCards += AllCards[numToChar(13)]
    else:
        safeCards += AllCards[numToChar(11)]
        safeCards += AllCards[numToChar(12)]
        safeCards += AllCards[numToChar(13)]
    """
    breakingCards, safeCards = higherCards(distance)
    probabilitySafe = safeCards/numCards()
    """
    print("Total: ", numCards())
    print("Breaking: ", breakingCards)
    print("Safe: ", safeCards)
    """
    #print("How Safe: ", probabilitySafe*100, "%")
    return probabilitySafe

#HIDDEN NEURON #2
def betterCard_probability(PlayerCards, DealCards):
    sum = 0
    dealerSum = 0
    distanceFromDealer = 0
    dealerDistance = 0
    betterCards = 0
    worseCards=0
    over21 = 0
    under21 = 0
    probabilityGreater = 0

    sum = sumListAI(PlayerCards)
    #print("(DEBUG) SUM BEFORE ACECONVERT: ", sum)
    #print("(DEBUG) SUM AFTER ACECONVERT: ", sum2)
    dealerSum = sumListAI(DealCards)
    #print("(DEBUG) DEALERSUM BEFORE ACECONVERT: ", dealerSum)
    #print("(DEBUG) DEALERSUM AFTER ACECONVERT: ", dealerSum2)

    distanceFromDealer = sum-dealerSum
    dealerDistance = 21-dealerSum
    #print("(DEBUG) DISTANCE: ", distanceFromDealer)
    betterCards, worseCards = higherCards(distanceFromDealer)
    over21, under21 = higherCards(dealerDistance)
    betterCards -= over21
    #print("(DEBUG) BETTER CARDS: ", betterCards)
    #print("(DEBUG) WORSE CARDS: ", worseCards)
    probabilityGreater = betterCards/numCards()
    #print("Probability Greater Card: ", probabilityGreater*100, "%")
    
    return probabilityGreater

#OUTPUT NODE
def chooseHit(PlayerCards, DealCards, weightList):
    node1 = 0
    node2 = 0
    hitChoice = 0
    
    node1 = breaking_probability(PlayerCards)
    node2 = betterCard_probability(PlayerCards, DealCards)

    hitChoice = (weightList[0]*node1)+(weightList[1]*node2)
    #print(hitChoice)
    if(hitChoice>=1):
        return True
    else:
        return False



#TRAINING PART
def trainFunc(PlayerCards, DealCards, weight, trainWeight):
    global DealerHidden
    newSum = 0
    dealerHit = 'y'
    dealerNewCard = '2'
    dealerNewSum = 0
    newCard = '2'
    doesHit = False
    doesHit = chooseHit(PlayerCards, DealCards, weight)

    while(doesHit and newSum <= 21):
        newAICard = getCard()
        #print("HIT! New card is: ", newAICard)
        addToAICards(newAICard)
        newSum = sumListAI(AICards)
        if(newSum>21 and newCard=='A'):
            newSum -= 10
        doesHit = chooseHit(PlayerCards, DealCards, weight)
    
    #print("STAND!")
    newSum = sumListAI(AICards)

    
    #dealerHit = input("Did the dealer hit? (y/n): ")

    dealerNewSum = sumListDealer(DealerCards, setup(2))
    #print("I think the dealer has ", dealerNewSum)
    while(dealerHit=='y' and dealerNewSum<17):
        dealerNewCard = getCard()
        #print("HIT! Dealer's new card: ", dealerNewCard)
        addToDealerCards(dealerNewCard)
        dealerNewSum = sumListDealer(DealerCards, setup(2))
        #print("I think the dealer has ", dealerNewSum)
        #dealerHit = input("Did the dealer hit? (y/n): ")
    
    if(dealerHit=='quit'):
        print("SYSTEM EXITED")
        raise SystemExit

    dealerNewSum = sumListDealer(DealerCards, setup(2))
    #print("Dealer cards with hidden added: ", DealerCards)
    #print("Sum adjusted for dealer's new card: ", dealerNewSum)
    if(newSum>21):
        weights[0] -= trainWeight
        #print("AI loses! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
        return False
    if(dealerNewSum>21):
        weights[0] += trainWeight
        #print("AI wins! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
        return True
    if(dealerNewSum>newSum):
        #print("AI loses! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
        weights[1] += trainWeight
        return False
    elif(newSum>dealerNewSum):
        #print("AI wins! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
        weights[1] -= trainWeight
        return True
    elif(newSum==dealerNewSum):
        #print("Push! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
        return True

    return

result = False
row = ""
wins = 0
for i in range(timesTrained):
    #print("\n\n")
    #print("Training loop: ",i+1)
    reset()
    result = trainFunc(AICards, DealerCards, weights, trainingWeight)
    if(result):
        wins += 1
    row = [i, weights[0], weights[1], result, wins, wins/(i+1)]
    writer.writerow(row)
    #print(weights)

print(weights)
