# Data Manipulation at Scale: Systems and Algorithms

## Assignment 3: Thinking in MapReduce

### Bootstrap

```bash
# Install python 2.7 and pipenv
pipenv shell
pipenv install -d

cd solutions
```

### Running solutions

#### Problem 1:

```bash
# Run
python inverted_index.py ../materials/data/books.json

# Test
sort ../materials/solutions/inverted_index.json > /tmp/inverted_index.sorted.json; python inverted_index.py ../materials/data/books.json | sort | colordiff - /tmp/inverted_index.sorted.json
```

#### Problem 2:

```bash
# Run
python join.py ../materials/data/records.json

# Test
sort ../materials/solutions/join.json > /tmp/join.sorted.json; python join.py ../materials/data/records.json | sort | colordiff - /tmp/join.sorted.json
```

#### Problem 3:

```bash
# Run
python friend_count.py ../materials/data/friends.json

# Test
sort ../materials/solutions/friend_count.json > /tmp/friend_count.sorted.json; python friend_count.py ../materials/data/friends.json | sort | colordiff - /tmp/friend_count.sorted.json
```

#### Problem 4:

```bash
# Run
python asymmetric_friendships.py ../materials/data/friends.json

# Test
sort ../materials/solutions/asymmetric_friendships.json > /tmp/asymmetric_friendships.sorted.json; python asymmetric_friendships.py ../materials/data/friends.json | sort | colordiff - /tmp/asymmetric_friendships.sorted.json
```

#### Problem 5:

```bash
# Run
python unique_trims.py ../materials/data/dna.json

# Test
sort ../materials/solutions/unique_trims.json > /tmp/unique_trims.sorted.json; python unique_trims.py ../materials/data/dna.json | sort | colordiff - /tmp/unique_trims.sorted.json
```

#### Problem 6:

```bash
# Run
python multiply.py ../materials/data/matrix.json

# Test
sort ../materials/solutions/multiply.json > /tmp/multiply.sorted.json; python multiply.py ../materials/data/matrix.json | sort | colordiff - /tmp/multiply.sorted.json
```

