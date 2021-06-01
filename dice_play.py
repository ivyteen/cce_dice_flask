import numpy as np


def resultText(throwResult):
    if ( throwResult["diceCount"] == 1):
        return "결과는 "+str(throwResult["sum"])+"입니다"
    elif ( throwResult["diceCount"] < 4 ):
        return "결과는 "+throwResult["midText"]+"이며 합은 "+str(throwResult["sum"])+"입니다"
    else :
        return "주사위 "+str(throwResult["diceCount"])+"개의 합은 "+str(throwResult["sum"])+"입니다"


def throwDice(diceCount):

    midText = ''
    sum = 0

    print("throw {} times".format(diceCount))

    #for i in range(diceCount):
    rand = np.random.randint(1,7,size=diceCount)
    sum = rand.sum()
    midText = str(rand).replace("[","")
    midText = midText.replace("]","")

    return {"midText":midText, "sum":sum, "diceCount":diceCount}
