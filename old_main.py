import random

AICards = []
AllCards = {'A':4, '2':4, '3':4, '4':4, '5':4, '6':4, '7':4, '8':4, '9':4, '10':4, 'J':4, 'Q':4, 'K':4}
DealerCards = []
weights = [0.70,0.70]
trainingWeight = 0.02
timesTrained = 5

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
        print("AI's First Card: ", AICard1)
        AICards.append(AICard2)
        print("AI's Second Card:", AICard2)
        DealerCards.append(DealerCard)
        print("Dealer's First Card: ", DealerCard)
        print("Dealer's Hidden Card: ", DealerHidden)
        removeCards(AICards)
        removeCards(DealerCards)
        print("AI has: ", AICards)
        print("Dealer has: ", DealerCards)
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
            print(i)
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

def aceConvertRestrained(sum, iteration, numAce):
    if(numAce>=iteration and sum>21):
        sum -= 10
        return aceConvertRestrained(sum, iteration+1, numAce)
    else:
        return sum

def numCards():
    totalCards = 0
    for key,val in AllCards.items():
        totalCards += val
    return totalCards

#HIDDEN NEURON #1
def breaking_probability(Cards):
    sum = 0
    sum2 = 0
    distance = 21
    breakingCards = 0
    safeCards = 0
    probabilitySafe = 0

    sum = sumList(Cards)
    sum2 = sum - numAce(Cards)*10
    distance = distance - sum2

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
    sum2 = 0
    dealerSum = 0
    dealerSum2 = 0
    distanceFromDealer = 0
    dealerDistance = 0
    betterCards = 0
    worseCards=0
    over21 = 0
    under21 = 0
    probabilityGreater = 0

    sum = sumList(PlayerCards)
    #print("(DEBUG) SUM BEFORE ACECONVERT: ", sum)
    sum2 = aceConvertRestrained(sum, 1, numAce(PlayerCards))
    #print("(DEBUG) SUM AFTER ACECONVERT: ", sum2)
    dealerSum = sumList(DealCards)
    #print("(DEBUG) DEALERSUM BEFORE ACECONVERT: ", dealerSum)
    dealerSum2 = aceConvertRestrained(dealerSum, 1, numAce(DealCards))
    #print("(DEBUG) DEALERSUM AFTER ACECONVERT: ", dealerSum2)

    distanceFromDealer = sum2-dealerSum2
    dealerDistance = 21-dealerSum2
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
    dealerHit = 'n'
    dealerNewCard = '2'
    dealerNewSum = 0
    newCard = '2'
    doesHit = False
    doesHit = chooseHit(PlayerCards, DealCards, weight)
    
    if(doesHit):
        newAICard = getCard()
        print("HIT! New card is: ", newAICard)
        addToAICards(newAICard)
        newSum = sumList(AICards)
        if(newSum>21 and newCard is 'A'):
            newSum -= 10
    else:
        print("STAND!")
        newSum = sumList(AICards)
    
    dealerHit = input("Did the dealer hit? (y/n): ")
    if(dealerHit is 'y'):
        dealerNewCard = getCard()
        print("Dealer's new card: ", dealerNewCard)
        addToDealerCards(dealerNewCard)
    elif(dealerHit=='quit'):
        print("SYSTEM EXITED")
        raise SystemExit

    dealerNewSum = sumList(DealerCards)

    if(dealerNewSum>21 and dealerNewCard is 'A'):
        newSum -= 10

    #print("Updated sum: ", newSum)
    #print("Updated dealer sum: ", dealerNewSum)
    #print(AICards)
    #print(DealerCards)
    

    

    if(not doesHit and dealerHit is not 'y'):
        addToDealerCards(setup(2))
        dealerNewSum = sumList(DealerCards)
        #print("Dealer cards with hidden added: ", DealerCards)
        #print("Sum adjusted for dealer's new card: ", dealerNewSum)
        if(newSum>21):
            weights[0] -= trainWeight
            print("AI loses! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
            return
        if(dealerNewSum>21):
            weights[0] += trainWeight
            print("AI wins! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
            return
        if(dealerNewSum>newSum):
            print("AI loses! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
            weights[1] += trainWeight
            return
        elif(newSum>dealerNewSum):
            print("AI wins! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
            weights[1] -= trainWeight
            return
        elif(newSum==dealerNewSum):
            print("Push! Dealer Sum: ", dealerNewSum, ", AI Sum: ", newSum)
            return
    else:
        #print(AICards, DealerCards, weight, trainWeight)
        trainFunc(AICards, DealerCards, weight, trainWeight)
        return

#print("Cards in deck:")
#for key,val in AllCards.items():
#        print(key, "--", val)

#PREDICTIVE FUNCTIONS







for i in range(timesTrained):
    print("\n\n")
    print("Training loop: ",i+1)
    reset()
    trainFunc(AICards, DealerCards, weights, trainingWeight)
    print(weights)

print(weights)