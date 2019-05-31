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


->
Abstractions
  Programming Model
    Relational algebra is a very frequent approach
    Collection-at-a-time
      vs low-level code dealing with records and paralellism
    Automatic optimization
      No need to code for it
      Correct decisions are made for every case (ideally)
  Computational Model
    Data-parallel distributed algorithms
    Falut tolerance
    Other performance approaches
      On-disk vs In-Memory
      Indexes
      Transactions
      ...
  [insert Data Model (from above) here?]

<-


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


################################################################################

Consistent Hashing
    ...
Vector Clocks
    ...

Configurable consistency
    R: min nodes for successful read
    W: min nodes for successful write
    R+W > N => consistency
    R+W < N => low latency

Schema-on-
  Read (Hadoop, etc.)
    No need to do a huge ETL process upfront
  Write (RDBMS, etc.)
    The system handles the schema and storage for optimal querying

################################################################################

Document Stores and Extensible Record Stores
    CouchDB
        Howe's classification
            Scales to 1000s: Yes
            Primary idx: Yes
            Secondary idxs: Yes
            Transactions: Record
            Joins/Analytics: MapReduce
            Integrity constraints: No
            Views: Yes
            Language/Algebra: No
            Data model: Document
            Howe's label: filter/MapReduce
        Data model: Document
            List of attributes _allowing nesting_
        Lock free concurrency: Optimistic approach
            Updates on data that has changed fails
        No multi-row transactions
        MapReduce instead of joins
        Views
            Materialization of MapReduce results, emitted as other documents, allowing custom keying => re-indexing
    Google's BigTable (OS equivalent: HBase)
        Howe's classification
            Scales to 1000s: Yes
            Primary idx: Yes
            Secondary idxs: Yes
            Transactions: Record
            Joins/Analytics: Google's MapReduce compatible
            Integrity constraints: Some
            Views: No
            Language/Algebra: No
            Data model: Extensible record
            Howe's label: filter/MapReduce
        Data model: "sparse, distributed, persistent multi-dimensional sorted map"
            Allows fast random access
                (row, col, timestamp) -> cell content
            Sorted: lexicographically by row key
            Tablets
                Contain a key range (lexicographically continuous?)
                Unit of distribution:
                    Good when querying contiguous keys
                    If most queried data pertains to some particular ranges, few servers will get most of the load
                        (in contrast, e.g. Teradata's hashing distributes data evenly, so access is naturally load-balanced)
            Families: Groups of columns
                Basic unit for access control and memory and disk accounting
Extended NoSQL systems
    Google's Megastore: evolution over BigTable
        Howe's classification
            Scales to 1000s: Yes
            Primary idx: Yes
            Secondary idxs: Yes
            Transactions: Entity group
            Joins/Analytics: No
            Integrity constraints: Some
            Views: No
            Language/Algebra: Some
            Data model: Tables
            Howe's label: filter
        Argues that loose consistency models complicate application programming
            Implement transactions over entity groups
                Entity groups: Records accessed together
            Synchronous replications
    Spanner
        Comes from complaints on BigTable
            BigTable not good for
                Complex, evolving schemas
                Strong consistency in the presence of wide-area replication
            Spanner's solution: Distributed transactions
                Programmers better address performance problems as bottlenecks arise, rather than coding around the lack of transactions
        Howe's classification
            Scales to 1000s: Yes
            Primary idx: Yes
            Secondary idxs: Yes
            Transactions: Yes
            Joins/Analytics: ?
            Integrity constraints: Yes
            Views: Yes
            Language/Algebra: Yes
            Data model: Tables
            Howe's label: SQL-like
        Data model: Directory: set of contiguous keys with a shared prefix
            Tables are interleaved to create a hierarchy
                Like pre-DB models
                    Same performance gains, in some particular query path
                    Same problem: different query paths are problematic
        TODO: video: Spanner cont'd, Google Systems

Google File System (GFS)
  Like HDFS but for Google's Map Reduce
  Successor: Colosus

################################################################################

 PIG
  Programming model
    RA-like but with nested types
      Optimizer using RA
  Computational Model
    MapReduce/Hadoop
  Data model
    Schema-on-read
    Non-relational
    Types and operations
      Types: atom, tuple, bag, map
        Accepts nesting
      Operations: programing lang like (see Language below)
  Language
    Shows clearly the underlying Relational Algebra concepts
    Commands
      Regular: load, filter, group, distinct, foreach, flatten...
      Analytics: cogroup, join, skew...

################################################################################

Spark
  Storage
    Resilient Distributed Dataset (RDD)
      Distributed collection of key-values
      Memory cached
        Goes to disk mainly for fault-tolerance reasons
    Programming model
      Program directly in a host language (Java/Scala, Python, others?)
      Transformations (operations)
        Map & Reduce
        Also: flatMap, filter, join, partitionBy, zip, etc.
      Actions: Return values to the host language
    Computational model
      Lazy execution
        Actions trigger lazily executed transformations
      In-memory execution









################################################################################


TODO: make sense of this hinted classification:
  Analytics
  Low-latency micro-updates
  Analytics with iteration (Pregel)

TODO: Create graph of all tech (check vids: 17.3 Spanner cont'd, 17.4 MapReduce-based Systems)

TODO: Extract the tech classification table!
