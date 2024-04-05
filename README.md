# Quelques commandes utilisées durant ce TP

HADOOP:
docker container cp ./app/csv namenode:/
hadoop fs -mkdir /app
hdfs dfs -put ./csv /app

// Nettoyage des Données avec Hadoop
cat app/csv/dataset_sismique_villes.csv | python myhadoop/main.py > app/csv/clean_data.csv

SPARK:
docker exec -it spark-master bash
PATH=$PATH:/spark/bin
spark-submit app/analyse_pred.py 