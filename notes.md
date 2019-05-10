PIG         Relational Algebra on Hadoop
HIVE        SQL on Hadoop
HBase       Indexing on Hadoop
Dietrich    Schemas and Indexing on Hadoop
?           Transactions in HBase (VoltDB, other NewSQL)

gartner


Paradigms of Science
    Traditional three:
        Empirical: Test and describe
        Theoretical: Embraces abstract modeling
        Computational: Embraces simulations
            Data acquisition coupled to hypothesis
    New fourth paradigm?
        eScience: Acquire massive datasets from field (new cheaper collection methods or simulations) and
            Massive data acquisition, potentially in support of many hypotheses
            Equivalent in academia to DataScience in business


Bags: Contain data that can be repeated
Sets: Contain unique data


3D Data Management: Volume, Velocity and Variety
    Volume: Size of data
    Velocity: Processing latency
        In the context of a growing demand for interactivity (real-time conclusions)
    Variety: Diversity of sources, formats, quality, etc.



Big data: "any data that is expensive to manage and hard to extract value from" => more like "challenging" than big.




Data Model
    Examples: Files, Spreadsheets, Tables, Key-value, Graphs...
    Components:
        Structures. e.g:
            Rows and columns
            Nodes and edges
            Key-value pairs
            Byte sequences
            ...
        Constraints. e.g:
            All rows have same number of cols
            All values of row have same type
            Child cannot have more than one parent
            ...
        Operations. e.g:
            Index values from keys
            Filter rows
            Slice byte sequences
            ...

RDBMS Systems:
    Pre-relational solutions:
        "Network (proto)databases": Files with "file position pointers" to other records
            Whenever one record type changes in length, it pushes all records below, so references need to be updated
            Custom solutions (like back-referencing) need to be developed a-priori in the model to support the kind of queries needed, so new needs could mean restructuring all the DB
            Also, changing the model implies changing the programs that access the data
        Hierarchical structures
            Divides the above problems in "segments", but the problems are still there (right? ;p)
    Key motivations:
        Allow unforeseen data exploitation
        Physical data independence: Insulate users (human or apps) from changing when the underlying data changes
            RDBMS's solution: provide the user of an _algebraic structure_ (of tables or relations) allowing reasoning and manipulation independently of physical data representation
    Other benefits
        Automatic algebraic optimization and query planning


Relational Algebra:
    ...

SQL:
    ...
    Query plans
        Optimization
            ...


Scalability
    Meanings
        Operationally
            Past: Works even if data doesn't fit in memory (read a bit, calc., clear memory and read a bit, calc., etc.)
                In-core: all data in memory
                Out-of-core: use the disk to off-load ram
            Now: Parallelizable: can use 1000s of cheap computers
        Algorithmically
            Past: For n items, perform less than n^m operations (polynomial time, in contrast to e.g. exponential times)
            Now: For n items, perform less than (n^m)/k (large k) operations (parallelized polinomial algorithms)
            Soon: For n items, perform less than n*log(n) (stream processing: n is for the one pass, log(n) if for maybe indexing or something related to trees)

Algorithmic complexity
    ...

MapReduce
    ...

NoSQL