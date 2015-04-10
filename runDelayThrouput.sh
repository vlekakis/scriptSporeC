#!/usr/bin/env bash

python experimentRunner.py -b /Users/lex/Work/IdeaProjects/YCSB/bin/ycsb -i /Users/lex/Work/IdeaProjects/YCSB/sporeWorkloads/ -o edgeMultipleThreadsUnlimited -w update50read50 -c redis -f 8 80 800  -m load run loadSS runSS --thread 5;
sleep 1;
python experimentRunner.py -b /Users/lex/Work/IdeaProjects/YCSB/bin/ycsb -i /Users/lex/Work/IdeaProjects/YCSB/sporeWorkloads/ -o edgeMultipleThreadsTarget -w update50read50 -c redis -f 250  -m load run loadSS runSS --thread 5 --target 100 1000 5000 10000 20000;