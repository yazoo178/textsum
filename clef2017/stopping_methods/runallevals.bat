python .\eval\evalulate_curve.py -s 3 -c .\Test_Data_Sheffield-run-2_int_scores_3 -t .\Test_Data_Sheffield-run-2_int_scores_1 -m lower -o shef_lin_3 
python .\eval\evalulate_curve.py -s 3 -c .\Test_Data_Sheffield-run-2_int_scores_3 -t .\Test_Data_Sheffield-run-2_int_scores_1 -m upper -o shef_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\Test_Data_Sheffield-run-2_int_scores_3 -t .\Test_Data_Sheffield-run-2_int_scores_1 -o shef_lin_3

python .\eval\evalulate_curve.py -s 3 -c .\A-rank-cost_int_scores_3 -t .\A-rank-cost_int_scores_1 -m lower -o waterloo_A_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\A-rank-cost_int_scores_3 -t .\A-rank-cost_int_scores_1 -m upper -o waterloo_A_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\A-rank-cost_int_scores_3 -t .\A-rank-cost_int_scores_1 -o waterloo_A_lin_3

python .\eval\evalulate_curve.py -s 3 -c .\B-rank-cost_int_scores_3 -t .\B-rank-cost_int_scores_1 -m lower -o waterloo_B_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\B-rank-cost_int_scores_3 -t .\B-rank-cost_int_scores_1 -m upper -o waterloo_B_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\B-rank-cost_int_scores_3 -t .\B-rank-cost_int_scores_1 -o waterloo_B_lin_3

python .\eval\evalulate_curve.py -s 3 -c .\run-1_int_scores_3 -t .\run-1_int_scores_1 -m lower -o auth_1_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\run-1_int_scores_3 -t .\run-1_int_scores_1 -m upper -o auth_1_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\run-1_int_scores_3 -t .\run-1_int_scores_1 -o auth_1_lin_3

python .\eval\evalulate_curve.py -s 3 -c .\run-2_int_scores_3 -t .\run-2_int_scores_1 -m lower -o auth_2_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\run-2_int_scores_3 -t .\run-2_int_scores_1 -m upper -o auth_2_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\run-2_int_scores_3 -t .\run-2_int_scores_1 -o auth_2_lin_3

python .\eval\evalulate_curve.py -s 3 -c .\run_fulltext_test_int_scores_3 -t .\run_fulltext_test_int_scores_1 -m lower -o ucl_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\run_fulltext_test_int_scores_3 -t .\run_fulltext_test_int_scores_1 -m upper -o ucl_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\run_fulltext_test_int_scores_3 -t .\run_fulltext_test_int_scores_1 -o ucl_lin_3

python .\eval\evalulate_curve.py -s 3 -c .\test_ranked_run_1_int_scores_3 -t .\test_ranked_run_1_int_scores_1 -m lower -o ntu_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\test_ranked_run_1_int_scores_3 -t .\test_ranked_run_1_int_scores_1 -m upper -o ntu_lin_3
python .\eval\evalulate_curve.py -s 3 -c .\test_ranked_run_1_int_scores_3 -t .\test_ranked_run_1_int_scores_1 -o ntu_lin_3