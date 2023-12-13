# Network Simulation and Analysis Instructions

## Running Simulator.py for Ping Data Generation

To generate ping data for both IPv6 and IPv4, follow these steps on Windows CMD:

```bash
python ./Simulator.py [name] [ISP]
# Example => python ./Simulator.py Shubham Airtel
# Result file as result_[name].json is created
# If it already exists, then it appends the data to it.
```

## Plotting Graphs for Ping Data

1. Navigate to `results/ping` in the WN project.
2. Add your `result.json` file to the `ping` folder.
3. Run `Graph_individual.ipynb`, specifying your result and operator.

## Wget Instructions

For Wget:

- On Linux, execute `webpage_test.py` similarly:
    ```bash
    python3 webpage_test.py [name] [ISP]
    ```

## Plotting Wget Graphs

For generating plots:

1. Move the result to `results/wget`.
2. Re-run `Wget_graphs` by specifying your values in the ipynb file.
