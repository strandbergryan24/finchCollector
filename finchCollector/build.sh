#Install dependencies
pip3 install -r requirements.txt
#Run migrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input