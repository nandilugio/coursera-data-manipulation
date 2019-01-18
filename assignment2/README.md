# Data Manipulation at Scale: Systems and Algorithms

## Assignment 2: SQL for Data Science Assignment

### Bootstrap

```bash
docker image build -t coursera-data-manipulation-assignment2 .
```

### Running solutions

#### Problem 1: Inspecting the Reuters Dataset and Basic Relational Algebra

```bash
docker container run --rm -v $PWD/materials:/root/materials -it coursera-data-manipulation-assignment2 sqlite3 /root/materials/reuters.db
```

```sql
-- Part a: select
SELECT count(*) FROM ( SELECT * FROM frequency WHERE docid="10398_txt_earn" );
-- 138

-- Part b: select project
SELECT count(*) FROM ( SELECT term FROM frequency WHERE docid="10398_txt_earn" AND count=1 );
-- 110

-- Part c: union
SELECT count(*) FROM ( SELECT term FROM frequency WHERE docid="10398_txt_earn" AND count=1 UNION SELECT term FROM frequency WHERE docid="925_txt_trade" AND count=1 ); -- Note the UNION removes duplicates (11 in this case)
-- 324

-- Part d: count
SELECT count(*) FROM ( SELECT DISTINCT docid FROM frequency WHERE term IN ("law", "legal") );
-- 58

-- Part e: big documents
-- Answer to the question as described in the instructions (taking into account duplicates):
SELECT count(*) FROM ( SELECT docid, sum(count) AS total_terms FROM frequency GROUP BY docid HAVING total_terms > 300 );
-- 107
-- Answer to the graded question (_not_ taking into account duplicates; see https://www.coursera.org/learn/data-manipulation/programming/nkglo/sql-for-data-science-assignment/discussions/threads/LokkyEkVEeeqVwpT36CBzg):
SELECT count(*) FROM ( SELECT docid, count(*) AS total_terms FROM frequency WHERE count > 0 GROUP BY docid HAVING total_terms > 300 );
-- 11

-- Part f: two words
SELECT count(*) FROM ( SELECT DISTINCT f1.docid FROM frequency AS f1 INNER JOIN frequency AS f2 ON f1.term="transactions" AND f2.term="world" AND f1.docid=f2.docid );
-- 3
```

#### Problem 2: Matrix Multiplication in SQL

```bash
docker container run --rm -v $PWD/materials:/root/materials -it coursera-data-manipulation-assignment2 sqlite3 /root/materials/matrix.db
```

```sql
-- Part g: multiply
SELECT value FROM ( SELECT a.row_num, b.col_num, sum(a.value * b.value) AS value FROM a INNER JOIN b ON a.col_num = b.row_num GROUP BY a.row_num, b.col_num ) WHERE row_num=2 AND col_num=3;
-- 2874
```

#### Problem 3: Working with a Term-Document Matrix

```bash
docker container run --rm -v $PWD/materials:/root/materials -it coursera-data-manipulation-assignment2 sqlite3 /root/materials/reuters.db
```

```sql
-- Part h: similarity matrix
SELECT value FROM ( SELECT a.docid AS a_docid, b.docid AS b_docid, sum(a.count * b.count) AS value FROM frequency a INNER JOIN frequency b ON a.term = b.term WHERE a.docid < b.docid GROUP BY a.docid, b.docid ) WHERE a_docid="10080_txt_crude" AND b_docid="17035_txt_earn";
-- 19

-- Part i: keyword search
CREATE TEMPORARY VIEW frequency_and_query AS SELECT * FROM frequency UNION SELECT 'q' as docid, 'washington' as term, 1 as count UNION SELECT 'q' as docid, 'taxes' as term, 1 as count UNION SELECT 'q' as docid, 'treasury' as term, 1 as count;
SELECT a_docid, value FROM ( SELECT a.docid AS a_docid, b.docid AS b_docid, sum(a.count * b.count) AS value FROM frequency_and_query a INNER JOIN frequency_and_query b ON a.term = b.term WHERE a.docid < b.docid GROUP BY a.docid, b.docid ) WHERE b_docid = "q" and a_docid != "q" ORDER BY value DESC LIMIT 10;
-- 16094_txt_trade|6   <-- Max score = 6
-- 16357_txt_trade|6
-- 19775_txt_interest|6
-- 10623_txt_trade|5
-- 5964_txt_trade|5
-- 12774_txt_interest|4
-- 12848_txt_trade|4
-- 16214_txt_interest|4
-- 16681_txt_interest|4
-- 1711_txt_crude|4
```
