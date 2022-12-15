# Traffic Engineering Simulator

## Prerequisite

Python 3.7+

## Getting started

1. Clone the repository

```
git clone https://github.com/zitengshu/traffic-engineering-simulator.git
cd traffic-engineering-simulator
```

2. Install required Python library

```
pip install -r requirements.txt
```

3. Run an example. We provide an input configuration file `input.ymal` in `example` folder.

```
python3 simulator.py -f example/input.yaml
```

We also provide predefined examples.

```
python3 simulator.py -e clos
```



## Input File

| Name                    | Description                                                  | Type                   |
| ----------------------- | ------------------------------------------------------------ | ---------------------- |
| topology                | The desired data center network topology. Can be clos or block2block. | string                 |
| numberOfServer          | Number of servers                                            | int                    |
| numberOfLeaf            | Number of leaf nodes(aggregate blocks)                       | int                    |
| numberOfSpine           | Number of spine blocks                                       | int                    |
| numberOfServersPerLeaf  | Number of servers per aggregate block                        | int                    |
| capacityList            | Possible capacity size of each link                          | list                   |
| numberOfSource          | Number of source nodes. It will randomly select a given number of nodes and set them as the source of traffic. | int                    |
| numberofSink            | Number of sink nodes. It will randomly select a given number of nodes and set them as the sink of traffic. | int                    |
| block2blockCapacityList | (Optional) This is for block to block topology. It contains the possible capacity size of links between aggregate blocks. | list                   |
| drawGraph               | A flag indicates whether to output the graph.                | boolean(True or False) |



## Output Graph

Output graph is in [Cytoscape](https://manual.cytoscape.org/en/stable/index.html) JSON format.



## Example

### Clos

![theoretical-traffic-clos](../example/theoretical-traffic-clos.png)

### Block-to-Block

![theoretical-traffic-block2block](../example/theoretical-traffic-block2block.png)



## Command Line

| Argument       | Description                   |
| -------------- | ----------------------------- |
| -e, --example  | support `clos`, `block2block` |
| -f, --filepath | Path to the input YAML file   |

