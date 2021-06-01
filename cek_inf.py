import math
import dice_play

import uuid


DOMAIN = 'http://static.naver.net/clova/service/native_extensions/dice'

class Directive:
    def __init__(self, namespace, name, payload):
        self.header = {
            "messageId": str(uuid.uuid4()),
            "namespace": namespace,
            "name": name,
        }
        self.payload = payload


class CEKRequest:
    def __init__(self,jsonReq):
        self.request = jsonReq["request"]
        self.context = jsonReq["context"]
        self.session = jsonReq["session"]
        print("CEK Request : ", self.request, self.session)

    def do(self, cekResponse):
        try:
            if(self.request["type"] == 'LaunchRequest'):
                return self.launchRequest(cekResponse)
            elif(self.request["type"] == 'IntentRequest'):
                return self.intentRequest(cekResponse)
            elif(self.request["type"] == 'SessionEndedRequest'):
                return self.sessionEndedRequest(cekResponse)
            else:
                raise Exception("Invalid Request")
        except Exception as e:
            print("Exception Occurs about", e)
    

    def launchRequest(self, cekResponse):
        print("launchRequest")
        cekResponse.setSimpleSpeechText('몇개의 주사위를 던질까요?')
        cekResponse.setMultiturn({
            'intent': 'ThrowDiceIntent'
        })
        
    def intentRequest(self, cekResponse):
        print("intentRequest")
        print(self.request)
        intent = self.request["intent"]["name"]
        slots = self.request["intent"]["slots"]
        print(intent, slots)

        if(intent == 'ThrowDiceIntent'):
            diceCount = 1
            if(slots):
                
                diceCountSlot = slots["diceCount"]
                
                if((len(slots)!=0) and (diceCountSlot)):
                    diceCount = int(diceCountSlot["value"])
            
                if(math.isnan(diceCount)):
                    diceCount = 1

                print(diceCount, diceCountSlot)

            cekResponse.appendSpeechText("주사위를 "+str(diceCount)+"개 던집니다.")
            cekResponse.appendSpeechText(
                {
                    "lang": "ko",
                    "type": "URL",
                    "value": DOMAIN+"/rolling_dice_sound.mp3"
                }
            )
            
            throwResult = dice_play.throwDice(diceCount)
            
            cekResponse.appendSpeechText(dice_play.resultText(throwResult))
        else:
            cekResponse.setSimpleSpeechText("주사위 한 개 던져줘, 라고 시도해보세요.")

        if(self.session["new"] == False):
            cekResponse.setMultiturn(None)

    def sessionEndedRequest(cekResponse):
        print("sessionEndedRequest")
        cekResponse.setSimpleSpeechText('주사위 놀이 익스텐션을 종료합니다.')
        cekResponse.clearMultiturn()


class CEKResponse:
    def __init__(self):
        print("CEKResponse init")
        self.response = {
            "directives": [],
            "shoudEndSession": True,
            "outputSpeech": {},
            "card": {}
        }
        self.version = "0.1.0"
        self.sessionAttributes={}

    def setMultiturn(self,sessionAttributes):
        
        self.response["shoudEndSession"] = False

        if(sessionAttributes!=None):
            self.sessionAttributes.update(sessionAttributes)

    def clearMultiturn(self):
        self.response["shoudEndSession"] = True
        self.sessionAttributes = {}

    def setSimpleSpeechText(self, outputText):
        self.response["outputSpeech"] = {
            "type": "SimpleSpeech",
            "values": {
                "type": "PlaneText",
                "lang": "ko",
                "value": outputText
            }
        }

    def appendSpeechText(self, outputText):
        print(outputText)
        outputSpeech = self.response["outputSpeech"]
        print(outputSpeech)

        if((outputSpeech == {}) or (outputSpeech["type"] != "SpeechList")):
            outputSpeech["type"] = "SpeechList"
            outputSpeech["values"] = []

        if (type(outputText) == str):
            outputSpeech["values"].append({
                "type": 'PlainText',
                "lang": "ko",
                "value": outputText
            })
        else:
            outputSpeech["values"].append(outputText)

