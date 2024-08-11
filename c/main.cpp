#include <iostream>
#include <vector>
#include <chrono>
#include <thread>
#include "ortools/algorithms/knapsack_solver.h"

void solveKnapsack(const int64_t* values, const int64_t* weights, int64_t capacity, int num_items, int64_t* result) {
    operations_research::KnapsackSolver solver(
        operations_research::KnapsackSolver::KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER,
        "KnapsackExample");

    std::vector<int64_t> values_vec(values, values + num_items);
    std::vector<int64_t> weights_vec(weights, weights + num_items);
    std::vector<std::vector<int64_t>> weights_vecs = {weights_vec};
    std::vector<int64_t> capacities = {capacity};

    solver.Init(values_vec, weights_vecs, capacities);
    *result = solver.Solve();
}

int main() {
    const int NUMBER_OF_TRIALS = 100;

    // Problem setup for 10,000 problems
    const int num_problems = 10000;
    const int64_t max_capacity = 50;
    const int num_items_per_problem = 3;

    // Randomly generate values and weights for each problem
    srand(42);
    int64_t values[num_problems][num_items_per_problem];
    int64_t weights[num_problems][num_items_per_problem];
    int64_t capacities[num_problems];
    int64_t results[num_problems];

    for (int i = 0; i < num_problems; ++i) {
        for (int j = 0; j < num_items_per_problem; ++j) {
            values[i][j] = rand() % 99 + 1;
            weights[i][j] = rand() % 49 + 1;
        }
        capacities[i] = rand() % max_capacity + 1;
    }

    long long totalExecutionTime = 0;

    for (int k = 0; k < NUMBER_OF_TRIALS; ++k) {
        // Measure execution time
        auto startTime = std::chrono::high_resolution_clock::now();

        // Solve all knapsack problems using threads
        std::vector<std::thread> threads;
        for (int i = 0; i < num_problems; ++i) {
            threads.emplace_back([=, &results]() {
                solveKnapsack(values[i], weights[i], capacities[i], num_items_per_problem, &results[i]);
            });
        }

        // Wait for all threads to finish
        for (auto& t : threads) {
            t.join();
        }

        auto endTime = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();
        totalExecutionTime += duration;
    }

    std::cout << "Average C++ execution time: " << (totalExecutionTime / NUMBER_OF_TRIALS) / 1000.0 << " seconds" << std::endl;

    // Print the results for the first 10 problems
    std::cout << "First 10 results:" << std::endl;
    for (int i = 0; i < 10; ++i) {
        std::cout << "Final Result for Problem " << i + 1 << ": Maximum value = " << results[i] << std::endl;
    }

    return 0;
}

