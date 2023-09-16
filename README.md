
###### Wordwand AI ######


### Installation


# Install Python

Python 3.10.5

https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe


# Clone a repository

Run command in terminal

git clone https://github.com/CreativeBufferOfficial/zendesk_word_want.git

# Create and Activate virtual environment

For Windows run:

1. py -m pip install --upgrade pip

2. py -m pip --version

3. py -m pip install --user virtualenv

4. py -m venv word_env

5. .\word_env\Scripts\activate

For Unix/macOS run:

1. python3 -m pip install --user --upgrade pip

2. python3 -m pip --version

3. python3 -m pip install --user virtualenv

4. python3 -m venv word_env

5. source word_env/bin/activate


For Ubuntu run:

1. sudo apt install python3-venv

2. python3 -m venv word_env

3. source word_env/bin/activate



# Install requirement.txt file

Run command in terminal

pip install -r requirements.txt



# Migrate database

To migrate the database you have to run this command

python manage.py migrate

# Run server

To run the server you have to run this command

python manage.py runserver