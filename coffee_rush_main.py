'''
Coffee rush
Generate all possible routes of (3 + n) movements from initial position, with or without diagonals.
Dismiss illegal routes like moving off edges or ending with another player.
Gather ingredients along the route, applying acquired upgrades.
Check which orders can be completed with gathered ingredients.
'''
#============================== IMPORTS =========================================

import dataclasses
import itertools

#==================== CONSTANTS =================================================

# INGREDIENTS
NONE = 0
COFFEE = 1
MILK = 2
STEAM = 3
ICE = 4
CHOCOLATE = 5
TEA = 6
WATER = 7
CARAMEL = 8

# Ingredient dictionary for strings
INGRED_DICT = {
NONE: "None",
COFFEE: "Coffee",
MILK: "Milk",
STEAM: "Steam",
ICE: "Ice",
CHOCOLATE: "Chocolate",
TEA: "Tea",
WATER: "Water",
CARAMEL: "Caramel"}

# CARDS
'''
Cards have constant name and ingredients
'''

@dataclasses.dataclass
class Card:
	name:			str # Name of the card
	ingredients:	list # Card ingredients
	have:			bool # Do I have the card?

# RISTRETTO =			Card("Ristretto",				[COFFEE, STEAM],					True)
# AMERICANO =			Card("Americano",				[COFFEE, WATER, STEAM],				False)
# AMERICANO_HEL =		Card("Americano helado",		[COFFEE, WATER, ICE],				False)
# COLD_BREW =			Card("Cold brew",				[COFFEE, WATER, ICE],				False)
# LATTE_MAC =			Card("Latte macchiato",			[COFFEE, MILK, STEAM],				False)
# EINSPANNER =		Card("Einspanner",				[COFFEE, MILK, STEAM],				False)
# LATTE_HEL =			Card("Latte helado",			[COFFEE, MILK, ICE],				False)
# FREDDO_CAR =		Card("Cafe Freddo caramelo",	[COFFEE, CARAMEL, ICE],				False)
# ESPRESSO_DOP =		Card("Espresso doppio",			[COFFEE, COFFEE, STEAM],			True)
# TE_NEGRO =			Card("Te negro",				[TEA, WATER, STEAM],				False)
# TE_VERDE =			Card("Te verde",				[TEA, WATER, STEAM],				False)
# TE_LECHE =			Card("Te con leche",			[TEA, MILK, STEAM],					False)
# TE_NEGRO_HEL =		Card("Te negro helado",			[TEA, WATER, ICE],					False)
# TE_VERDE_HEL =		Card("Te verde helado",			[TEA, WATER, ICE],					False)
# LATTE_CHOC =		Card("Latte chocolate",			[CHOCOLATE, MILK, STEAM],			False)
# COCOA =				Card("Cocoa",					[CHOCOLATE, MILK, STEAM],			False)
# COCOA_HEL =			Card("Cocoa helado",			[CHOCOLATE, MILK, ICE],				False)
# BAT_CHOCOLATE =		Card("Batido de chocolate",		[CHOCOLATE, MILK, ICE],				False)
# MOCHACCINO =		Card("Mochaccino",				[COFFEE, CHOCOLATE, MILK, STEAM],	False)
# MOCHACCINO_HEL =	Card("Mochaccino helado",		[COFFEE, CHOCOLATE, MILK, ICE],		False)
# MOCHA_HEL =			Card("Mocha helado",			[COFFEE, CHOCOLATE, MILK, ICE],		False)
# FRAPPE_CAR =		Card("Frappe caramelo",			[COFFEE, CARAMEL, MILK, ICE],		True)
# CAR_MACCHIATO =		Card("Caramel macchiato",		[COFFEE, CARAMEL, MILK, STEAM],		False)

AMERICANO =			Card("Americano",				[COFFEE, WATER, STEAM],				False)
AMERICANO_HEL =		Card("Americano helado",		[COFFEE, WATER, ICE],				False)
BATIDO_CHOC =		Card("Batido de chocolate",		[CHOCOLATE, MILK, ICE],				False)
CAR_MACCHIATO =		Card("Caramel macchiato",		[COFFEE, CARAMEL, MILK, STEAM],		False)
COCOA =				Card("Cocoa",					[CHOCOLATE, MILK, STEAM],			False)
COCOA_HEL =			Card("Cocoa helado",			[CHOCOLATE, MILK, ICE],				False)
COLD_BREW =			Card("Cold brew",				[COFFEE, WATER, ICE],				False)
EINSPANNER =		Card("Einspanner",				[COFFEE, MILK, STEAM],				False)
ESPRESSO_DOP =		Card("Espresso doppio",			[COFFEE, COFFEE, STEAM],			False)
FRAPPE_CAR =		Card("Frappe caramelo",			[COFFEE, CARAMEL, MILK, ICE],		False)
FREDDO_CAR =		Card("Cafe Freddo caramelo",	[COFFEE, CARAMEL, ICE],				False)
LATTE_CHOC =		Card("Latte chocolate",			[CHOCOLATE, MILK, STEAM],			False)
LATTE_HEL =			Card("Latte helado",			[COFFEE, MILK, ICE],				False)
LATTE_MAC =			Card("Latte macchiato",			[COFFEE, MILK, STEAM],				False)
MOCHA_HEL =			Card("Mocha helado",			[COFFEE, CHOCOLATE, MILK, ICE],		False)
MOCHACCINO =		Card("Mochaccino",				[COFFEE, CHOCOLATE, MILK, STEAM],	False)
MOCHACCINO_HEL =	Card("Mochaccino helado",		[COFFEE, CHOCOLATE, MILK, ICE],		False)
RISTRETTO =			Card("Ristretto",				[COFFEE, STEAM],					False)
TE_LECHE =			Card("Te con leche",			[TEA, MILK, STEAM],					False)
TE_NEGRO =			Card("Te negro",				[TEA, WATER, STEAM],				False)
TE_NEGRO_HEL =		Card("Te negro helado",			[TEA, WATER, ICE],					False)
TE_VERDE =			Card("Te verde",				[TEA, WATER, STEAM],				False)
TE_VERDE_HEL =		Card("Te verde helado",			[TEA, WATER, ICE],					False)

# Card list sorted by number of ingredients, common ingredients first
CARD_LIST = [RISTRETTO, AMERICANO, AMERICANO_HEL, COLD_BREW, LATTE_MAC, EINSPANNER,
			LATTE_HEL, FREDDO_CAR, ESPRESSO_DOP, TE_NEGRO, TE_VERDE, TE_LECHE,
			TE_NEGRO_HEL, TE_VERDE_HEL, LATTE_CHOC, COCOA, COCOA_HEL,
			BATIDO_CHOC, MOCHACCINO, MOCHACCINO_HEL, MOCHA_HEL, FRAPPE_CAR, CAR_MACCHIATO]

# BOARD
'''
BOARD = [[ICE,	  CARAMEL, STEAM,	  COFFEE],
		 [COFFEE, MILK,	   ICE,		  WATER],
		 [TEA,	  STEAM,   MILK,	  COFFEE],
		 [MILK,	  ICE,	   CHOCOLATE, STEAM]]
'''

BOARD = [[MILK, TEA, COFFEE, ICE],
		[ICE, STEAM, MILK, CARAMEL],
		[CHOCOLATE, MILK, ICE, STEAM],
		[STEAM, COFFEE, WATER, COFFEE]]

CORNER_LIST = [[0,0],[0,3],[3,0],[3,3]]

# POSITION
X = 0
Y = 1

# MOVEMENTS
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
NE = 4
NW = 5
SE = 6
SW = 7

moves = [NORTH, SOUTH, EAST, WEST, NE, NW, SE, SW]
MOVES_DICT = {NORTH: "N", SOUTH: "S", EAST: "E", WEST: "W", NE: "NE", NW: "NW", SE: "SE", SW: "SW"}

BASE_MOVES = 3

#======================== PARAMETERS =================================================

MEEPLE_POS =	[[0, 1], [1, 1], [1, 0]] # Position of other players' meeples

# Initial position
Pos = [0,0]
Position = Pos.copy() # Auxiliary position variable

# CUPS
# Current ingredients in your cups
CUPS = [[NONE, NONE, NONE, NONE],
		[NONE, NONE, NONE, NONE],
		[NONE, NONE, NONE, NONE]]

# STATS
MOVE_TOKENS = 0

# UPGRADES (Stackable, effects add up)
DIAGONAL = False # Allows to move diagonally
MEEPLES = True # Double ingredient from spaces with meeples
CORNERS = True # Double ingredient from corners
SPECIALS = True # Double ingredient from special spaces

cardsEnable = True

#========================= AUXILIARY VARIABLES =========================================
routes = [] # Generated routes
Ingredients = [] # Gathered ingredients

RoutesList = [] # Feasible routes, filtered from 'routes'
IngredientsList = [] # Ingredient lists for each feasible route
CompletedCardsList = [] # Completed cards for each feasible route

#=======================FUNCTIONS==================================

def MoveNorth():
	Position[Y] += 1

def MoveSouth():
	Position[Y] -= 1

def MoveEast():
	Position[X] += 1

def MoveWest():
	Position[X] -= 1

# Move the meeple in the desired direction
# Dir	Direction to move, may be diagonal
def Move(Dir):
	
	match Dir:
		case Dir if ((Dir == NORTH)):	MoveNorth()
		case Dir if ((Dir == SOUTH)):	MoveSouth()
		case Dir if ((Dir == EAST)):	MoveEast()
		case Dir if ((Dir == WEST)):	MoveWest()
		case Dir if ((Dir == NE)):
			MoveNorth()
			MoveEast()
		case Dir if ((Dir == NW)):
			MoveNorth()
			MoveWest()
		case Dir if ((Dir == SE)):
			MoveSouth()
			MoveEast()
		case Dir if ((Dir == SW)):
			MoveSouth()
			MoveWest()
		case _:	print("Movement error")

# Generate all possible routes, considering used move tokens and diagonal upgrade
def GenRoutes():
	global routes

	reps = BASE_MOVES + MOVE_TOKENS # repetitions for product()

	# Generate all possible combinations of n movements, with or without diagonals
	if DIAGONAL:
		routes = list(itertools.product(moves, repeat=reps))
	else:
		routes = list(itertools.product(moves[0:4], repeat=reps))

# Move along the generated routes, gathering ingredients along the way, discard route if not valid.
def WalkRoutes():
	global Position

	TempIngredients = []

	for route in routes:
		for idx in range(len(route)):
			Move(route[idx])

			# Cannot exit board bounds
			if any(((p > 3) or (p < 0)) for p in Position):
				#print("Out of bounds " + str(Position))
				break
			# Cannot end route in space with another meeple
			elif ((idx == (len(route) - 1)) and (Position in MEEPLE_POS)):
				#print("Meeple at end " + str(Position))
				break
			else:
				GetIngredients(TempIngredients)
		else: # Executed if no break was reached, route completed
			TempIngredients.sort()
			IngredientsList.append(TempIngredients)
			RoutesList.append(route)

		# Always restart position and temp ingredients
		Position = Pos.copy()
		TempIngredients = []

# Get ingredients from current position, applying upgrades
# List	Temporary list to fill with gathered ingredients
def GetIngredients(List: list):
	global Position

	numIngredients = 1

	# Duplicate ingredient with upgrades
	if ((MEEPLES) and (Position in MEEPLE_POS)):
		numIngredients *= 2

	if ((CORNERS) and (Position in CORNER_LIST)):
		numIngredients *= 2

	if ((SPECIALS) and (BOARD[Position[X]][Position[Y]] > 4)):
		numIngredients *= 2

	for i in range(numIngredients):
		List.append(BOARD[Position[X]][Position[Y]])

# Check which order cards can be completed with gathered ingredients, including ingredients in each cup, no duplicates
def CompleteOrders():

	for i in range(len(IngredientsList)):
		CompletedCardsList.append([])

		for j in range(len(CUPS)):
			for k in range(len(CARD_LIST)):
				# Check a card only if I have it and it is not yet in list to avoid duplicates
				if ((CARD_LIST[k].have) and (CARD_LIST[k].name not in CompletedCardsList[i])):
					tempIng = IngredientsList[i].copy() + CUPS[j]
					tempCard = CARD_LIST[k].ingredients.copy()

					if (CheckOrders(tempIng, tempCard)):
						CompletedCardsList[i].append(CARD_LIST[k].name)

# Check if an order card can be completed with given set of ingredients
# ings	gathered ingredients, plus ingredients in a cup
# card	list of ingredients of a specific card
def CheckOrders(ings: list, card: list):
	for ing in card:
		if (ing in ings):
			ings.remove(ing)
			continue
		else:
			#print("ing not found")
			return False
	else:
		#print("Card complete")
		return True

# Print possible routes with gathered ingredients and which cards can be completed
def PrintResults():
	routeStr = []
	ingStr = []

	for i in range(len(RoutesList)):
		for j in range(len(RoutesList[i])):
			routeStr.append(MOVES_DICT[RoutesList[i][j]])

		for j in range(len(IngredientsList[i])):
			ingStr.append(INGRED_DICT[IngredientsList[i][j]])

		print(str(routeStr) + " " + str(ingStr) + " " + str(CompletedCardsList[i]))

		routeStr = []
		ingStr = []
	
	print("\n" + str(len(RoutesList)) + " routes generated from position " + str(Pos))
		
# Enable or disable all cards at once
def EnableCards(enable: bool):
	for i in range(len(CARD_LIST)):
		CARD_LIST[i].have = enable

#=======================MAIN FUNCTION==================================

def main():
	EnableCards(cardsEnable)
	GenRoutes()
	WalkRoutes()
	CompleteOrders()
	PrintResults()

#========================MAIN CALL=====================================

if __name__ == '__main__':
	main()
