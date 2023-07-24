#!/bin/bash

# Generate messages
python generate_messages.py 10 1 >msgs10
python generate_messages.py 10 10 >msgs100
python generate_messages.py 100 10 >msgs1k
python generate_messages.py 1000 10 >msgs10k
python generate_messages.py 1000 25 >msgs25k

# Run SINGLE TESTS
echo "_______________RUNNING SINGLE TESTS_______________"
python test_single_insert.py msgs10
python test_single_insert.py msgs100
#python test_single_insert.py msgs1k
#python test_single_insert.py msgs10k
#python test_single_insert.py msgs25k

# Run BULK TESTS
echo -e "\n_______________RUNNING BULK TESTS_______________"
python test_bulk_insert.py msgs10
python test_bulk_insert.py msgs100
python test_bulk_insert.py msgs1k
python test_bulk_insert.py msgs10k
python test_bulk_insert.py msgs25k

# Run test_query.py
echo -e "\n_______________RUNNING QUERY TESTS_______________"
python test_query.py quest_queries
