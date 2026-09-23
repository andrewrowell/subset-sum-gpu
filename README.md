# knapsack-gpu - filling many backpacks faster via the hardware designed for parallel computing

## Motivation
- It's pretty obvious that using hardware designed to run a bunch of the same calculations concurrently will... run a bunch of the same calculations concurrently, faster than more general-purpose computing hardware, but...
  - This example is simple enough to make "moving the problem to GPU" less intimidating
  - But... this is a real example! I have seen a commercial use case of solving a large number of knapsack problems.
- There has been a massive deployment of GPU hardware (source?)
- While a lot of the excitement about this hardware is related to LLMs, there are all sorts of problems that can be solved faster by throwing a bunch of parallel computing power at them.
- If the LLM/AI bubble bursts, there could be a bunch of cheap GPU hardware ready to use in the cloud

## The Problems
TODO: Store the problems in files, give a brief summary of them here

## Running It
The local environment is managed by [uv](https://docs.astral.sh/uv/)

```bash
uv sync
uv run jupyter lab macbook.ipynb
```

`colab.ipynb` is opened in Colab rather than locally. It clones this repo to get `problems.py` and installs its own dependencies there.

## Testing Method

## Results
| Device                                                                                                                           | Implementation                                                        | Run Time |
|----------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|----------|
| [M4 Macbook Air](https://everymac.com/systems/apple/macbook-air/specs/macbook-air-m4-10-core-cpu-10-core-gpu-13-2025-specs.html) | Python, [Google OR-Tools](https://github.com/google/or-tools), on CPU | ???      |
| [M4 Macbook Air](https://everymac.com/systems/apple/macbook-air/specs/macbook-air-m4-10-core-cpu-10-core-gpu-13-2025-specs.html) | Metal                                                                 | ???      |
| Colab T4                                                                                                                         | Python, [Google OR-Tools](https://github.com/google/or-tools), on CPU | ???      |
| Colab T4                                                                                                                         | PyCUDA                                                                | ???      |