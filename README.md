# pyTLEX: An NLP library for Timeline Extraction. 

## What is pyTLEX?

pyTLEX is a Python Library developed for implementing the TLEX (TimeLine EXtraction) Algorithm on TimeML Files. The TLEX Algorithm was first developed by Mustafa Ocal and Dr. Mark Finlayson. It was then adapted into a Python Library by multiple students across several semesters at Florida International University.

## Installation

User must also install certain packages using the requirements.txt file:

`pip install -r requirements.txt`

A corpus containing freely available TimeML files can be found at: https://catalog.ldc.upenn.edu/LDC2006T08

Before being able to download the corpus for free, the user must register and read the user agreement at the aforementioned address. Afterwards, save the TimeML files inside the _/pyTLEX/pytlex_data/TimeBankCorpus/_ directory.



## Getting Started

### How to create a TimeML Graph
#### From a TimeML File (must provide a valid TimeML file or filepath):

`timeML_graph = Graph('wsj_0555.tml')` 

#### Using TimeML text (must be in the correct TimeML format):

```
timeML_graph = Graph("<TimeML
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="../../dtd/timeml_1.2.1.xsd">
    </TimeML>")
```
    
 
#### Using the graph definition (a set of nodes and links):

```
node1 = TimeX(50, "FUTURE_REF", True, "next wednesday")
node2 = TimeX(51, "FUTURE_REF", True, "next thursday")
node3 = TimeX(52, "FUTURE_REF", True, "next friday")
link1 = Link(50, "TLINK", "BEFORE", node1, node2)
link2 = Link(51, "TLINK", "BEFORE", node2, node3)
timeML_nodes = set()
timeML_nodes.add(node1)
timeML_nodes.add(node2)
timeML_nodes.add(node3)
timeML_links.add(link1)
timeML_links.add(link2)
timeML_graph = Graph(timeML_nodes, timeML_links)
```


#### Accessing a graph's partitions (main and subordination partitions):

```
timeML_graph = Graph('wsj_0555.tml')
timeML_graph.main_partitions
timeML_graph.subordination_parittions
```

#### Accessing a graph's timeline:
```
timeML_graph = Graph('wsj_0555.tml')
timeML_graph.timeline
```

For a more throughout look on graphs and other useful methods, please refer to the PyTLEX User Manual.pdf located on _/pyTLEX/_.

## Credits
_Dr. Mark Finlayson_: TLEX Algorithm developer  
_Mustafa Ocal_: TLEX Algorithm developer  
_Jared Hummer_: contributed to  
_Ismael Clark_: contributed to  
_Victoria Fernandez_: contributed to Event.py, Instance.py, Link.py, Signal.py, TimeMLParser.py, and tests  
_Leandro Estevez_: contributed to  
_Felipe Arce Rivera_: contributed to  
_Akul Singh_: contributed to Event.py, Sanity_Check.py, and tests  
_Kevin Fontela_: contributed to Signal.py, and tests  
_Raul Garcia Breijo_: contributed to Instance.py  
_Jorge Segredo_: contributed to TimeX.py, and tests  
_Sage Pages_: contributed to TimeX.py, Sanity_Check.py, tests, and GitHub upload  
_Gerardo Parra_: contributed to Inconsistency_detector.py, IndeterminacyDetector.py, Sanity_Check.py, and tests  
_Ivan Parra Sanz_: contributed to Connectivity_Increaser.py, Partitioner.py, TimeMLParser.py, TCSP_solver.py, Sanity_Check.py, and tests  
_Carlos Pimentel_: contributed to  
_Franklin Bello Romero_: contributed to  
_Tony Erazo_: contributed to  
_Hector Borges_: contributed to  
