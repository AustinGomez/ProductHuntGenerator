from __future__ import print_function

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from keras.models import model_from_json
from sqlalchemy import create_engine
from sqlalchemy import text
from services.utils import generate_text, load_data
from models.models import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)

NUMBER_TO_GENERATE = 5
# Creating training data
X, y, VOCAB_SIZE, ix_to_char = load_data('./services/producthunt.txt', 100)

# Either load the model or create it.
# Loading the trained weights
print('Loading model')
json_file = open('model.json', 'r', encoding='utf-8')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights('checkpoint_layer_2_hidden_500_epoch_40.hdf5')
print("Loaded model from disk")

generated = generate_text(model, NUMBER_TO_GENERATE, VOCAB_SIZE, ix_to_char)

for string in generated:
    name = string.split(":")[0]
    tagline = ''.join(string.split(":")[1:])

    db.session.add(Product(name=name, tagline=tagline))

db.session.commit()


