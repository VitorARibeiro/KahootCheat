import requests as req
# b84f489e-c4a1-4eed-b185-173caada4fd0

def RequestQuestion():
    GameId = input("Indique o Game-ID")
    r  = req.get(f"https://play.kahoot.it/rest/kahoots/{GameId}") 
    return r.json().get("questions")

def Parser(input):
    FinalDictionary = dict()
    for QuestionNumber in input:
        Questions = QuestionNumber.get("question")
        if Questions is not None:
            Choices = QuestionNumber.get("choices") 
            CorrectAnswers = [
                Option.get("answer") 
                for Option in Choices 
                if Option.get("correct") is True
            ]
            FinalDictionary[Questions] = CorrectAnswers
    return FinalDictionary

print(Parser(RequestQuestion()))