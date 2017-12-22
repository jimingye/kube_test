import s3fs
import datetime
import boto3
from multiprocessing import Pool
from flask import Flask

app = Flask(__name__)
s3 = s3fs.S3FileSystem(anon = False)
ls = []
dayArray = []
today = datetime.date.today()
sqs = boto3.resource('sqs', region_name = 'us-east-1')
queue = sqs.get_queue_by_name(QueueName = 'jye-test')

def getPath(i):
    date = today - datetime.timedelta(i)
    date = date.isoformat().split('-')
    return s3.glob("hurley-insights-vault/0000/events/" + date[0] + '/' + date[1] + '/' + date[2] + "/*/video/*.data")

def group(l):
    count = 0
    for j in range(len(l)):
        if count == 10:
            queue.send_messages(Entries = l[j - count : j])
            count = 0
        l[j] = {'Id': str(count), 'MessageBody': l[j]}
        count += 1

    if count != 0 and count != 1:
        queue.send_messages(Entries = l[len(l) - count : ])

@app.route('/')
def start():
    try:
        for i in range(90):
            dayArray.append(i)

        pool = Pool(128)
        ls = pool.map(getPath, dayArray)
        pool.map(group, ls)
        pool.close()
        pool.join()

    except Exception as error:
        print error

    del ls[ : ]
    del dayArray[ : ]

    return "finished"

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
