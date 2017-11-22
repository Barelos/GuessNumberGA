from Constants import *
import math
import random

TARGET = 50
NUM_BITS = 15
BIT_SIZE = 4
GENERATION_SIZE = 100

chromosomes = []
fitness = []
roulette_fitness = None

CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.01
EPSILON = 0.001


######### Logistic functions #########

# turn binary to decimal form
def bin_to_dec(string):
    result = 0
    for i in range(len(string)):
        if string[i] is "1":
            result += math.pow(2, len(string) - 1 - i)
    return int(result)


# turn decimal tp binary (not in use old function)
def dec_to_bin(num):
    return str('{0:04b}'.format(num))


# generate random chromosomes to act as base generation
def generate_base_generation(n=GENERATION_SIZE, j=NUM_BITS, k=BIT_SIZE):
    # TODO test what happens if i wont allow duplicate base chromosomes
    chromosome = ""
    for i1 in range(n):
        for i2 in range(j):
            # every even place is a number, every odd place is an operation
            if i2 % 2 == 0:
                for i3 in range(k):
                    chromosome += str(random.randint(0, 1))  # chromosome is made of 0\1
            else:
                i = random.randint(0, len(operations) - 1)
                chromosome += operations[i]
        chromosomes.append(chromosome)
        chromosome = ""


# calculate the fitness of a chromosome
def calculate_fitness(num):
    # if the chromosome is a perfect match we return the winner flag
    if num == TARGET:
        return WINNER_FLAG

    # else we return the fitness function
    return 1 / math.fabs(num - TARGET)


# decifer the chromosome into a number
def calculate_expression_value(expression, num_bits=NUM_BITS, bit_size=BIT_SIZE):
    # we seperate the chromosomes into bits
    bits = []
    for i in range(num_bits):
        bit = expression[i * bit_size: i * bit_size + bit_size]
        bits.append(bit)

    # we transfer the numbers from binary to decimal
    for i in range(len(bits)):
        if i % 2 == 0:
            bits[i] = bin_to_dec(bits[i])
        else:
            val = bin_to_dec(bits[i])
            if val < BIT_SIZE:
                bits[i] = mult_s
            elif val < 2 * BIT_SIZE:
                bits[i] = div_s
            elif val < 3 * BIT_SIZE:
                bits[i] = plus_s
            elif val < 4 * BIT_SIZE:
                bits[i] = minus_s

    # whie there are still operation we evaluate them
    while len(bits) > 1:
        if mult_s in bits:
            index = bits.index(mult_s)
            bits[index - 1: index + 2] = [bits[index - 1] * bits[index + 1]]
        elif div_s in bits:
            index = bits.index(div_s)
            if bits[index + 1] == 0:
                return TARGET + DIVISION_BY_ZEOR
            bits[index - 1: index + 2] = [bits[index - 1] / bits[index + 1]]
        elif plus_s in bits:
            index = bits.index(plus_s)
            bits[index - 1: index + 2] = [bits[index - 1] + bits[index + 1]]
        elif minus_s in bits:
            index = bits.index(minus_s)
            bits[index - 1: index + 2] = [bits[index - 1] - bits[index + 1]]
    # we return the expression value
    return bits[0]


# run the program
def main():
    generate_base_generation()
    # calculate fitness
    for chromosome in chromosomes:
        fitness.append(calculate_fitness(calculate_expression_value(chromosome)))

    if WINNER_FLAG in fitness:
        print("best fit:")
        print(chromosomes[fitness.index(WINNER_FLAG)])
        print(calculate_expression_value(chromosomes[fitness.index(WINNER_FLAG)]))
        return

    # run GA until good eproximation is found
    best_fit = TARGET + 1
    # while math.fabs(best_fit - TARGET) > EPSILON:
    for i in range(1000):
        best_fit_index = create_new_generation()
        best_fit = calculate_expression_value(chromosomes[best_fit_index])
        # input(chromosomes)
        # if i % 100 == 0:
        #     print(i, best_fit)

    print("best fit:")
    print(chromosomes[best_fit_index])
    print(best_fit)
    return



######### Evolution functions #########
def make_roulette_fitness():
    global roulette_fitness
    if WINNER_FLAG in fitness:
        return WINNER_FLAG
    # make the sum of fitness normalized to 1
    total_fitness = sum(fitness)
    roulette_fitness = [x / total_fitness for x in fitness]
    return True


def pick_random_chromosome():
    partial_sum = 0
    candidate = random.random()
    for i in range(len(roulette_fitness)):
        partial_sum += roulette_fitness[i]
        if candidate <= partial_sum:
            return i
    print("ERROR")
    return False


def crossover(index1, index2):
    curr_rate = random.random()
    if curr_rate < CROSSOVER_RATE:
        i = random.randint(0, NUM_BITS * BIT_SIZE - 1)
        return chromosomes[index1][0 : i] + chromosomes[index2][i: NUM_BITS * BIT_SIZE], \
               chromosomes[index2][0: i] + chromosomes[index1][i: NUM_BITS * BIT_SIZE]
    else:
        return chromosomes[index1], chromosomes[index2]


def mutate(to_mutate):
    for chromosome in to_mutate:
        for i in range(len(chromosome)):
            if random.random() < MUTATION_RATE:
                l = list(chromosome)
                l[i] = "1" if l[i] is "0" else "0"
                chromosome = "".join(l)


def create_new_generation():
    global chromosomes
    global fitness

    # test if we have a winner if so return the index of it
    winner =  make_roulette_fitness()

    # if no winner found we make a new generation
    new_chromosomes = []
    # crossover
    for i in range(int(GENERATION_SIZE / 2)):
        ch1, ch2 = crossover(pick_random_chromosome(), pick_random_chromosome())
        new_chromosomes.append(ch1)
        new_chromosomes.append(ch2)
    # mutation
    mutate(new_chromosomes)
    # change the current generation
    chromosomes = new_chromosomes
    fitness = []
    # calculate fitness
    for chromosome in chromosomes:
        fitness.append(calculate_fitness(calculate_expression_value(chromosome)))

    if WINNER_FLAG in fitness:
        return fitness.index(WINNER_FLAG)

    return fitness.index(max(fitness))


# TODO finish genetic funcitons


for i in range(5):
    main()
    fitness = []
    chromosomes = []
    roulette_fitness = []