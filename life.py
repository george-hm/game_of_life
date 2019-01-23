import random
import time
import os


class Map(object):
	on = "1"
	off = " "

	def __init__(self, seed=None, size=None):  # generate map
		if not seed or seed == "":  # seeding
			seed = random.random()
		if not size:  # sizing
			size = 100

		self.size = size
		self.seed = seed

		random.seed(seed)  # set the seed
		self.map_sheet = []  # the map
		# generate map
		for y in range(0, (int(size/2))):  # y axis
			self.map_sheet.append([])  # add new row
			for x in range(0, size):  # x axis
				if random.random() < 0.25:  # alive
					self.map_sheet[y].append(self.on)
				else:  # dead
					self.map_sheet[y].append(self.off)

		# need to do the check before printing in case we generate an invalid life grid
		print(self.printMap())

	def printMap(self):
		ret_ar = []
		for x in range(0, len(self.map_sheet)):  # go through each row
			# join everything, for easy showing
			ret_ar.append("".join(self.map_sheet[x]))

		return "\n".join(ret_ar)  # the map!

	def performCheck(self):  # neighbor checks, the big one
		def gridCheck(row, column):  # actual neighbor check
			to_app = []

			def checkLooped(x_type=None, y_type=None):  # less repetition
				# this is used to check if we looped (e.g. array[-1])
				if x_type:
					if row+(-x) == -1:
						return True

				if y_type:
					if column+(-y) == -1:
						return True

				return False

			def checkErrors(x_type=None, y_type=None):  # less repetition
				# check cell with + or - values
				if x_type:
					x_type = -x
				else:
					x_type = x

				if y_type:
					y_type = -y
				else:
					y_type = y

				try:
					if self.map_sheet[row+(x_type)][column+(y_type)] == self.on:
						to_app.append(True)
					else:
						to_app.append(False)
				except IndexError:
					to_app.append(False)

			for x in range(0, 2):  # for loop to check surrounding cell
				for y in range(0, 2):  # ^ same as above, we need a nested
					if x == 0 and y == 0:  # this is our cell, skip
						continue

					if x == 1 and y == 1:  # if the last step, we also need -x, y and x, -y
						if checkLooped(x_type=True):  # are we looped?
							to_app.append(False)  # we are, fail
						else:
							# otherwise, check as normal
							checkErrors(x_type=True)

						if checkLooped(y_type=True):
							to_app.append(False)
						else:
							checkErrors(y_type=True)

					checkErrors()  # check with two positive values

					if checkLooped(x_type=True, y_type=True):  # check with double negative
						to_app.append(False)
					else:
						checkErrors(x_type=True, y_type=True)

			return to_app  # return the results of surrounding cells

		new_map = []  # building a new map so no changes are made until complete
		for row in range(0, len(self.map_sheet)):  # go through each row
			new_map.append([])  # create new row in new map
			# go through each column
			for column in range(0, len(self.map_sheet[row])):
				check = gridCheck(row, column)  # get neighbor checks
				# the cell itself (is it alive or dead?)
				cell = self.map_sheet[row][column]
				# the rules of life
				if cell == self.on and check.count(True) < 2:
					new_map[row].append(self.off)
				elif cell == self.on and check.count(True) > 1 and check.count(True) < 4:
					new_map[row].append(self.on)
				elif cell == self.on and check.count(True) > 3:
					new_map[row].append(self.off)
				elif check.count(True) == 3:
					new_map[row].append(self.on)
				else:
					new_map[row].append(self.off)

		self.map_sheet = new_map  # new map assembled

	def playLife(self):  # play!
		count = 1
		while True:  # infinite loop, wait, check, print, repeat
			count += 1
			self.performCheck()
			time.sleep(0.750)
			os.system('cls')
			print(self.printMap())
			print("Generation:", count)
			print("Seed:", self.seed)
			print(f"Size: {self.size}x{int(self.size/2)}")

# PLAY LIFE
test = Map(input("Enter a seed, or leave blank for a random seed.\n> "), int(input("Enter a size.\n> ")))
test.playLife()
