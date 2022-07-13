import requests
import json

#https://deckofcardsapi.com/
from PIL import ImageTk, Image
import cv2
import numpy as np

def image(url):
	response = requests.get(url, stream=True)
	response.raw.decode_content = True
	return Image.open(response.raw)

def dispimages(hand, titulo):
	imagesSrcs = []
	for a in hand:
		imagesSrcs.append(image(a['image']))
	Hori = np.concatenate(imagesSrcs, axis=1)
	cv2.imshow(titulo, Hori)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")

deckId = deck.json()['deck_id']

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    

def draw(deck, cant):
	card = requests.get("https://deckofcardsapi.com/api/deck/"+deck+"/draw/?count="+cant)
	return (card.json()['cards'])

def show(hand, titulo):
	cards =[]
	num=0
	for a in hand:
		cards.append(a['code'])
		num = num + figures(a['value'])
	dispimages(hand, titulo)
	return(cards,num)

def figures(value):
	if value in["QUEEN", "KING", "JACK"] :
		value = 10
	if value == "ACE":
		value = 1
	return int(value)



player = draw(deckId,"2")
dealer = draw(deckId,"1")

(code,num)=show(dealer, "Dealer")
dealerCards = code
dealerSum =+num
#######print ("Mesa:", dealerCards)
#######print(dealerSum)

(code,num)=show(player, "Jugador")
playerCards =[]
playerCards.append(code)
playerSum=+num
#######print ("Mano:", playerCards)
#######print(playerSum)

print("SU TURNO\n")

while input("Pedir(S | N):  ").capitalize()!="N":
	player = player + draw(deckId,"1")
	(playerCards,playerSum)=show(player, "Jugador")
#######	print ("Mano:", playerCards)
	
	if(playerSum>21):
		break
#######	print(playerSum)
	pass

for a in player:
	if a['value'] == 'ACE' and playerSum<=11:
		playerSum+=10
#######		print(playerSum)

if(playerSum<=21):
	print("TURNO DE LA MESA\n")

	while dealerSum<=17:
		dealer = dealer + draw(deckId,"1")
		(dealerCards,dealerSum)=show(dealer,"Dealer")
#######		print ("Mesa:", dealerCards)
#######		print(dealerSum)
		if(dealerSum>21):
			break
		pass

	if (playerSum>dealerSum) or (dealerSum>21):
		print("GANADOR :) !!!\n")
	else:
		if playerSum==dealerSum:
			print("EMPATE\n")
		else:	
			print("PERDIO :(\n")
else:
	print("PERDIO :(\n")

