import csv,json
from elasticsearch import helpers, Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
index="marios"

#Για να μην βγάζει σφάλματα λόγω του χαμηλού χώρου στον δίσκο τρέχω αυτό στο bash:
#curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
#και
#curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'

def load_csv(file_name):
    with open(file_name, 'r',encoding="utf8") as outfile:
        reader = csv.DictReader(outfile)
        i = 0
        for row in reader:
            #print(row)
            #print("   i=",i)
            es.index(index=index, id=i,body=json.dumps(row))
            i = i + 1
            if (i%100==0):
                print(i)
            
#load_csv('movies.csv')

def search():

    erotima=input("Παρακαλώ εισάγετε το κείμενο προς αναζήτηση:")
    query_body = {
    "query": {
        "match": {
            "title": erotima
        }
    }
    }
    result=es.search(index=index, body=query_body)
    for i in range(len(result)):
        print(result['hits']['hits'][i]['_source']['title'])
search()
