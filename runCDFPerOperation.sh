#!/bin/bash



python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/load_redis_update50read50_5.txt redisVSredisSS_2015-03-14_key512Breakdown/load_redisSS_update50read50_5.txt -l insert -o i5.pdf -f 5;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/load_redis_update50read50_50.txt redisVSredisSS_2015-03-14_key512Breakdown/load_redisSS_update50read50_50.txt -l insert -o i50.pdf -f 50;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/load_redis_update50read50_100.txt redisVSredisSS_2015-03-14_key512Breakdown/load_redisSS_update50read50_100.txt -l insert -o i100.pdf -f 100;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/load_redis_update50read50_250.txt redisVSredisSS_2015-03-14_key512Breakdown/load_redisSS_update50read50_250.txt -l insert -o i250.pdf -f 250;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/load_redis_update50read50_500.txt redisVSredisSS_2015-03-14_key512Breakdown/load_redisSS_update50read50_500.txt -l insert -o i500.pdf -f 500;


python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_5.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_5.txt -l read -o r5.pdf -f 5;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_50.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_50.txt -l read -o r50.pdf -f 50;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_100.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_100.txt -l read -o r100.pdf -f 100;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_250.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_250.txt -l read -o r250.pdf -f 250;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_500.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_500.txt -l read -o r500.pdf -f 500;

python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_5.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_5.txt -l update -o u5.pdf -f 5;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_50.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_50.txt -l update -o u50.pdf -f 50;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_100.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_100.txt -l update -o u100.pdf -f 100;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_250.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_250.txt -l update -o u250.pdf -f 250;
python cdfGen.py -i redisVSredisSS_2015-03-14_key512Breakdown/run_redis_update50read50_500.txt redisVSredisSS_2015-03-14_key512Breakdown/run_redisSS_update50read50_500.txt -l update -o u500.pdf -f 500;
