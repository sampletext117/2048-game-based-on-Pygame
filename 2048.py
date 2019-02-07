import pygame, sys, time
from pygame.locals import *
from random import *



colour_dict = { 0: (242, 232, 201), 2: (242, 205, 184),
				4: (149, 123, 141), 8: (108, 146, 175),
				16: (59, 131, 189) , 32: (28, 169, 201),
				64: (127, 143, 24), 128: (181, 121, 0),
				256: (204, 119, 34), 512: (217, 80, 48),
				1024: (220, 20, 60), 2048: (155, 47, 31),
				4096: (111, 0, 53), 8192: (83, 26, 80),
				16384: (255, 0, 255), 32768: (154, 206, 235)}

total_points = 0
default_score = 2


pygame.init()
width, height = 600, 700
surface = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("2048")

common_font = pygame.font.SysFont("calibri", 26)
score_font = pygame.font.SysFont("calibri", 52)
big_font = pygame.font.SysFont("calibri", 86)
medium_font = pygame.font.SysFont("calibri", 40)


matrix = []

# for i in range(field_size):
# 	matrix.append([])
# 	for j in range(field_size):
# 		matrix[i].append(0)


previous_matrix = []


def start_screen(loaded_game = False):

	surface.fill((242, 232, 201))

	pygame.draw.rect(surface, (255, 136, 0), (20, 500, 100, 100))
	pygame.draw.rect(surface, (255, 136, 0), (170, 500, 100, 100))
	pygame.draw.rect(surface, (255, 136, 0), (320, 500, 100, 100))
	pygame.draw.rect(surface, (255, 136, 0), (470, 500, 100, 100))

	labell = common_font.render("4X4", 1, (0, 0, 0))
	label2 = common_font.render("5X5", 1, (0, 0, 0))
	label3 = common_font.render("6X6", 1, (0, 0, 0))
	label4 = common_font.render("8X8", 1, (0, 0, 0))
	label_name = big_font.render("2048", 1, (0, 0, 0))
	label_6 = medium_font.render("Select your board size:", 1, (0, 0, 0))


	surface.blit(labell, (50, 535))
	surface.blit(label2, (200, 535))
	surface.blit(label3, (350, 535))
	surface.blit(label4, (500, 535))
	surface.blit(label_name, (210, 100))
	surface.blit(label_6, (120, 400))

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if not loaded_game:

				if event.type == MOUSEBUTTONDOWN and event.button == 1 and click_on_rect(event.pos,
																							(20, 110), (500, 600)):
					main(4)

				if event.type == MOUSEBUTTONDOWN and event.button == 1 and click_on_rect(event.pos,
																					 (170, 260), (500, 600)):
					main(5)

				if event.type == MOUSEBUTTONDOWN and event.button == 1 and click_on_rect(event.pos,
																					 (320, 410), (500, 600)):
					main(6)

				if event.type == MOUSEBUTTONDOWN and event.button == 1 and click_on_rect(event.pos,
																						 (470, 560), (500, 600)):
					main(8)

			else:

				if event.type == MOUSEBUTTONDOWN and event.button == 1 and click_on_rect(event.pos,
																						 (20, 110), (500, 600)):
					main(4, True)

				if event.type == MOUSEBUTTONDOWN and event.button == 1 and click_on_rect(event.pos,
																						 (170, 260), (500, 600)):
					main(5, True)

				if event.type == MOUSEBUTTONDOWN and event.button == 1 and click_on_rect(event.pos,
																						 (320, 410), (500, 600)):
					main(6, True)

				if event.type == MOUSEBUTTONDOWN and event.button == 1 and click_on_rect(event.pos,
																						 (470, 560), (500, 600)):
					main(8, True)

		pygame.display.update()




def click_on_rect(pos, rect_dx, rect_dy):
	if ((pos[0] - rect_dx[0]) * (pos[0] - rect_dx[1])) <= 0 and ((pos[1]
							- rect_dy[0])* (pos[1] - rect_dy[1])) <= 0:
		return True
	else:
		return False

def main(n, loaded_game = False):
	global field_size
	field_size = int(n)
	for i in range(field_size):
		matrix.append([])
		for j in range(field_size):
			matrix[i].append(0)

	if not loaded_game:
		set_initial_tile()
		set_initial_tile()

	set_matrix()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if can_go() == True:
				if event.type == KEYDOWN:
					if pressed_arrow_or_wasd(event.key):
						rotations = get_rotations(event.key)

						add_to_moves()

						for i in range(0, rotations):
							rotate_to_clockwise()

						if can_move():
							move_tiles()
							merge_tiles()
							set_initial_tile()

						for j in range(0, (4 - rotations) % 4):
							rotate_to_clockwise()

						set_matrix()
			else:
				set_game_over_labels()

			if event.type == KEYDOWN:

				if event.key == pygame.K_r:
					reset()

				if 50 < event.key and 56 > event.key:
					field_size = event.key - 48
					reset()

				if event.key == pygame.K_F1:
					save_game()
				elif event.key == pygame.K_l:
					load_game()
				elif event.key == pygame.K_u:
					to_previous_move()

		pygame.display.update()

def set_matrix():

	surface.fill((242, 232, 201))


	for i in range(0, field_size):
		for j in range(0, field_size):
			pygame.draw.rect(surface, colour_dict[matrix[i][j]],
							 (i*(width/field_size), j*(width/field_size) + 100,
							  (width/field_size) - 5, (width/field_size) - 5))


			if matrix[i][j] == 0:
				label = common_font.render('', 1, (255,255,255))
			else:
				label = common_font.render(str(matrix[i][j]), 1, (255, 255, 255))

			label2 = score_font.render("Score:" + str(total_points), 1, (0, 0, 0))

			if matrix[i][j] < 9:
				surface.blit(label, ((i * (width / field_size) + ((width / field_size) / 2.5)),
									 ((j * ((height - 100) / field_size)) +
									  ((((height - 100) / field_size)) / 3.2) + 100)))
				# surface.blit(label, (i * (width / field_size) + 30, j * (400 / field_size) + 130))
			elif matrix[i][j] > 9 and matrix[i][j] < 65:
				surface.blit(label,((i * (width / field_size) + ((width / field_size) / 3)),
									((j * ((height - 100) / field_size)) +
									 ((((height - 100) / field_size)) / 3.2) + 100)))
				# surface.blit(label, (i * (width / field_size) + 25, j * (400 / field_size) + 130))
			elif matrix[i][j] > 65 and matrix[i][j] < 512:
				surface.blit(label, ((i * (width / field_size) + ((width / field_size) / 6)),
									 ((j * ((height - 100) / field_size)) +
									  ((((height - 100) / field_size)) / 3.2) + 100)))
				# surface.blit(label, (i * (width / field_size) + 15, j * (400 / field_size) + 130))
			else:
				surface.blit(label, ((i * (width / field_size) + ((width / field_size) / 10)),
									 ((j * ((height - 100) / field_size)) +
									  ((((height - 100) / field_size)) / 3.2) + 100)))
				# surface.blit(label, (i * (width / field_size) + 10, j * (400 / field_size) + 130))
			surface.blit(label2, (10, 20))

def set_game_over_labels():
	global total_points

	surface.fill((242, 232, 201))

	label = score_font.render("Game Over!", 1, (0, 0, 0))
	label2 = score_font.render("Your score is " + str(total_points), 1, (0, 0, 0))
	label3 = common_font.render("Press "R" to restart!", 1, (0, 0, 0))

	surface.blit(label, (50, 100))
	surface.blit(label2, (50, 200))
	surface.blit(label3, (50, 300))

def set_initial_tile():
	count = 0
	for i in range(0, field_size):
		for j in range(0, field_size):
			if matrix[i][j] == 0:
				count += 1

	k = make_round(random() * field_size * field_size)

	while matrix[make_round(k / field_size)][k % field_size] != 0:
		k = make_round(random() * field_size * field_size)

	matrix[make_round(k / field_size)][k % field_size] = 2

def make_round(n):
	return int(n - (n % 1))

def move_tiles():
	for i in range(0, field_size):
		for j in range(0, field_size - 1):
			while matrix[i][j] == 0 and sum(matrix[i][j:]) > 0:
				for k in range(j, field_size - 1):
					matrix[i][k] = matrix[i][k + 1]
				matrix[i][field_size - 1] = 0

def can_go():
	for i in range(0, field_size ** 2):
		if matrix[make_round(i / field_size)][i % field_size] == 0:
			return True

	for i in range(0, field_size):
		for j in range(0, field_size - 1):
			if matrix[i][j] == matrix[i][j + 1]:
				return True
			elif matrix[j][i] == matrix[j + 1][i]:
				return True

	return False



def merge_tiles():
	global total_points

	for i in range(0, field_size):
		for k in range(0, field_size - 1):
				if matrix[i][k] == matrix[i][k + 1] and matrix[i][k] != 0:
					matrix[i][k] = matrix[i][k] * 2
					matrix[i][k + 1] = 0
					total_points += matrix[i][k]
					move_tiles()


def reset():
	global total_points
	global matrix

	total_points = 0
	surface.fill((242, 232, 201))

	matrix = [[0 for i in range(0, field_size)] for j in range(0, field_size)]
	start_screen()


def can_move():

	for i in range(0, field_size):
		for j in range(1, field_size):
			if matrix[i][j-1] == 0 and matrix[i][j] > 0:
				return True
			elif (matrix[i][j-1] == matrix[i][j]) and matrix[i][j-1] != 0:
				return True

	return False


def save_game():
	f = open("savedata", "w")

	line1 = " ".join([str(matrix[make_round(_ / field_size)][_ % field_size])
					  for _ in range(0, field_size ** 2)])

	f.write(line1 + "\n")
	f.write(str(field_size)  + "\n")
	f.write(str(total_points))
	f.close()


def load_game():
	global field_size
	global total_points
	global matrix

	f = open("savedata", "r")

	mat = (f.readline()).split(' ', field_size ** 2)
	field_size = int(f.readline())
	total_points = int(f.readline())

	for i in range(0, field_size ** 2):
		matrix[make_round(i / field_size)][i % field_size] = int(mat[i])

	f.close()

	start_screen(True)


def rotate_to_clockwise():
	for i in range(0, int(field_size/2)):
		for j in range(i, field_size - i - 1):
			temp1 = matrix[i][j]
			temp2 = matrix[field_size - 1 - j][i]
			temp3 = matrix[field_size - 1 - i][field_size - 1 - j]
			temp4 = matrix[j][field_size - 1 - i]

			matrix[field_size - 1 - j][i] = temp1
			matrix[field_size - 1 - i][field_size - 1 - j] = temp2
			matrix[j][field_size - 1 - i] = temp3
			matrix[i][j] = temp4


def pressed_arrow_or_wasd(k):
	return(k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT
		   or k == pygame.K_w or k == pygame.K_s or k == pygame.K_a or k == pygame.K_d)


def get_rotations(k):
	if k == pygame.K_UP or k == pygame.K_w:
		return 0
	elif k == pygame.K_DOWN or k == pygame.K_s:
		return 2
	elif k == pygame.K_LEFT or k == pygame.K_a:
		return 1
	elif k == pygame.K_RIGHT or k == pygame.K_d:
		return 3


def previous_game_data():
	mat = []

	for i in range(0, field_size ** 2):
		mat.append(matrix[make_round(i / field_size)][i % field_size])

	mat.append(total_points)

	return mat


def add_to_moves():
	previous_matrix.append(previous_game_data())


def to_previous_move():
	if len(previous_matrix) > 0:
		mat = previous_matrix.pop()

		for i in range(0, field_size ** 2):
			matrix[make_round(i / field_size)][i % field_size] = mat[i]

		global total_points
		total_points = mat[field_size ** 2]

		set_matrix()

start_screen()