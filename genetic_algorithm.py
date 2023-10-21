import random


# Define the game of Mancala
class Mancala:
    def __init__(self):
        self.board = [4] * 6 + [0] + [4] * 6 + [0]

    def play(self, moves):
        player = 0
        position = 0
        for move in moves:
            if player == 0:
                position = (position + move) % 14
            else:
                position = (position + move + 7) % 14
            self.board[position] += 1
            if position == 6 and player == 0:
                player = 1
            elif position == 13 and player == 1:
                player = 0
            if self.board.count(0) >= 12:
                return self.score()
        return self.score()

    def score(self):
        return self.board[6] - self.board[13]


# Define the genetic algorithm
class GeneticAlgorithm:
    def __init__(self):
        self.population = [[random.randint(1, 6) for _ in range(6)] for _ in range(POPULATION_SIZE)]
        self.fitness = [0] * POPULATION_SIZE

    def evaluate_fitness(self):
        game = Mancala()
        for i in range(POPULATION_SIZE):
            self.fitness[i] = game.play(self.population[i])

    def select_parents(self):
        parents = []
        for _ in range(int(POPULATION_SIZE / 2)):
            tournament = random.sample(range(POPULATION_SIZE), 5)
            tournament_fitness = [self.fitness[i] for i in tournament]
            winner = tournament[tournament_fitness.index(max(tournament_fitness))]
            parents.append(self.population[winner])
        return parents

    def crossover(self, parents):
        children = []
        for i in range(int(POPULATION_SIZE / 2)):
            parent1 = parents[i]
            parent2_index = POPULATION_SIZE - 1 - i
            if parent2_index >= len(parents):
                parent2_index = random.randint(0, len(parents) - 1)
            parent2 = parents[parent2_index]
            crossover_point = random.randint(1, NUM_MOVES - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            children.append(child1)
            children.append(child2)
        return children

    def mutate(self, children):
        for i in range(POPULATION_SIZE):
            for j in range(NUM_MOVES):
                if random.random() < 0.1:
                    children[i][j] = random.randint(1, 6)

    def evolve(self):
        for i in range(NUM_GENERATIONS):
            self.evaluate_fitness()
            parents = self.select_parents()
            children = self.crossover(parents)
            self.mutate(children)
            self.population = parents + children

        best_individual = max(range(POPULATION_SIZE), key=lambda i: self.fitness[i])
        print("\nBest individual:", self.population[best_individual], "with fitness:", self.fitness[best_individual])


# Run the genetic algorithm
if __name__ == '__main__':
    POPULATION_SIZE = 100
    NUM_GENERATIONS = 50
    NUM_MOVES = 6
    genetic_algorithm = GeneticAlgorithm()
    genetic_algorithm.evolve()
