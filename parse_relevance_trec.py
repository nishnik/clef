# directory: /net/work/people/saleh/clir_experiments/resources/new_data_split/data

path = 'qrels_dev_train.txt'
with open(path, 'r') as f:
    data = f.readlines()

for i in range(len(data)):
    data[i] = data[i].strip().split(' ')

topic_wise = {}

for a in data:
    if a[0] in topic_wise.keys():
        topic_wise[a[0]][a[3]].append(a[2])
    else:
        topic_wise[a[0]] = {}
        topic_wise[a[0]]['0'] = []
        topic_wise[a[0]]['1'] = []

# Checked that topics are same
# docs = set()
# for a in data:
#     docs.add(a[2])

# for a in docs:
#     print (a)

# print (len(docs)) # = 13137


#################################
# len(data) = 15571
# len(topic_wise[list(topic_wise.keys())[0]]['0']) = 179
# len(topic_wise[list(topic_wise.keys())[0]]['1']) = 21
# len(topic_wise[list(topic_wise.keys())[1]]['1']) = 29
# len(topic_wise[list(topic_wise.keys())[2]]['1']) = 59
# len(topic_wise[list(topic_wise.keys())[2]]['0']) = 152
