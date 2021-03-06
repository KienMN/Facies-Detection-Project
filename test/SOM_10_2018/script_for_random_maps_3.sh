bsub "python3 random_maps.py -tr 1X,2X,3X -te 4X -m 123-1345 -n 150 -s 5 -fi 10000 -si 20000 -lr 0.5 -sig 3 -c 1,2,3,4,5 > result/123_random_weighted_features_random_map_150_5_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 1X,2X,3X -te 4X -m 123-1345 -n 200 -s 5 -fi 10000 -si 20000 -lr 0.5 -sig 3 -c 1,2,3,4,5 > result/123_random_weighted_features_random_map_200_5_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 1X,2X,3X -te 4X -m 123-1345 -n 150 -s 4 -fi 10000 -si 20000 -lr 0.5 -sig 2 -c 1,2,3,4,5 > result/123_random_weighted_features_random_map_150_4_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 1X,2X,3X -te 4X -m 123-1345 -n 200 -s 4 -fi 10000 -si 20000 -lr 0.5 -sig 2 -c 1,2,3,4,5 > result/123_random_weighted_features_random_map_200_4_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 1X,2X,3X -te 4X -m 123-1345 -n 200 -s 3 -fi 10000 -si 20000 -lr 0.5 -sig 2 -c 1,2,3,4,5 > result/123_random_weighted_features_random_map_200_3_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 1X,2X,3X -te 4X -m 123-1345 -n 250 -s 3 -fi 10000 -si 20000 -lr 0.5 -sig 2 -c 1,2,3,4,5 > result/123_random_weighted_features_random_map_250_3_0,5.txt 2>&1"

bsub "python3 random_maps.py -tr 2X,3X,4X -te 1X -m 123-1345 -n 150 -s 5 -fi 10000 -si 20000 -lr 0.5 -sig 3 -c 1,2,3,4,5 > result/234_random_weighted_features_random_map_150_5_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 2X,3X,4X -te 1X -m 123-1345 -n 200 -s 5 -fi 10000 -si 20000 -lr 0.5 -sig 3 -c 1,2,3,4,5 > result/234_random_weighted_features_random_map_200_5_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 2X,3X,4X -te 1X -m 123-1345 -n 150 -s 4 -fi 10000 -si 20000 -lr 0.5 -sig 2 -c 1,2,3,4,5 > result/234_random_weighted_features_random_map_150_4_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 2X,3X,4X -te 1X -m 123-1345 -n 200 -s 4 -fi 10000 -si 20000 -lr 0.5 -sig 2 -c 1,2,3,4,5 > result/234_random_weighted_features_random_map_200_4_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 2X,3X,4X -te 1X -m 123-1345 -n 200 -s 3 -fi 10000 -si 20000 -lr 0.5 -sig 2 -c 1,2,3,4,5 > result/234_random_weighted_features_random_map_200_3_0,5.txt 2>&1"
bsub "python3 random_maps.py -tr 2X,3X,4X -te 1X -m 123-1345 -n 250 -s 3 -fi 10000 -si 20000 -lr 0.5 -sig 2 -c 1,2,3,4,5 > result/234_random_weighted_features_random_map_250_3_0,5.txt 2>&1"