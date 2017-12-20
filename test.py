import flask
import boto3
import s3fs
import tendo

test = flask.Flask(__name__)

@test.route('/')
def hello_world():
	s1 = flask.__version__
	s2 = boto3.__version__
	s3 = s3fs.__version__
	s4 = tendo.__version__
	return "success" + ' ' + s1 + ' ' + s2 + ' ' + s3 + ' ' + s4

if __name__ == "__main__":
	test.run(host = "0.0.0.0")