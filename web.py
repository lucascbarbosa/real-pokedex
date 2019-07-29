from flask import Flask,request, render_template,redirect,url_for
import pandas as pd
import requests
from watson_developer_cloud import VisualRecognitionV3 
import json
import ast
#Initialize Watson VR
visual_recognition = VisualRecognitionV3(
    version='2016-05-20',
    iam_apikey='2AFlJNIvEkn44rBnlaAUUwYX_4rVNEKR8tIBQQlL-BPt'
)

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='2AFlJNIvEkn44rBnlaAUUwYX_4rVNEKR8tIBQQlL-BPt')

#Preprocessing pokedex database
pokedex = pd.read_csv('Pokedex.csv')
pokedex['type'] = pokedex[pokedex.columns[6:8]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
pokedex.drop('type_1',axis=1,inplace= True)
pokedex.drop('type_2',axis=1,inplace=True)
col =['id', 'pokemon','type', 'species_id', 'height', 'weight', 'base_experience',
       'attack', 'defense', 'hp', 'special_attack', 'special_defense', 'speed',
       'ability_1', 'ability_2', 'ability_hidden', 'color_1', 'color_2',
       'color_f', 'egg_group_1', 'egg_group_2', 'url_image', 'generation_id',
       'evolves_from_species_id', 'evolution_chain_id', 'shape_id', 'shape']
pokedex=pokedex[col]
pokedex=pokedex.set_index('id')
base = 'http://img.pokemondb.net/artwork/'
#initialize flask
app = Flask(__name__)
@app.route('/<name>&<score>',methods = ['POST','GET'])
def result(name,score):
      return render_template('result.html',name=name,score=score, 
                                          type = pokedex[pokedex['pokemon']==name]['type'].values[0],
                                          hp = pokedex[pokedex['pokemon']==name]['hp'].values[0],
                                          atk = pokedex[pokedex['pokemon']==name]['attack'].values[0],
                                          satk =  pokedex[pokedex['pokemon']==name]['special_attack'].values[0],
                                          deff = pokedex[pokedex['pokemon']==name]['defense'].values[0],
                                          sdef =pokedex[pokedex['pokemon']==name]['special_defense'].values[0],
                                          speed = pokedex[pokedex['pokemon']==name]['speed'].values[0],
                                          img_url = base + name + '.jpg')


@app.route('/vr', methods = ['POST','GET']) 
def VR():
       if request.method == 'POST':
              url = request.form['img_src']
              r = requests.get(url, allow_redirects=True)
              open('tests/pokemon.jpg', 'wb').write(r.content)
              with open('tests/pokemon.jpg', 'rb') as images_file:
                     classes = visual_recognition.classify(
                     images_file,
                     threshold='0.6',
	              classifier_ids='Pok´´´´´´_794921030').get_result()
              dict1 = ast.literal_eval(json.dumps(classes, indent=2))
              res = pd.DataFrame.from_dict(dict1)
              dict2 = dict(res['images'].apply(pd.Series)['classifiers'].apply(pd.Series)[0].apply(pd.Series)['classes'].apply(pd.Series)[0].values[0])
              name = str(dict2['class']).lower()
              score = dict2['score']
              return redirect(url_for('result',name=name,score=score))

       return render_template('vr.html')


@app.route('/<name>',methods = ['POST','GET'])
def getPokemonStats(name):
       if request.method == 'POST':

              name = str(request.form['name'])
              return redirect(url_for('getPokemonStats',name=name))

       return render_template('stats.html',name= name, 
                                          type = pokedex[pokedex['pokemon']==name]['type'].values[0],
                                          hp = pokedex[pokedex['pokemon']==name]['hp'].values[0],
                                          atk = pokedex[pokedex['pokemon']==name]['attack'].values[0],
                                          satk =  pokedex[pokedex['pokemon']==name]['special_attack'].values[0],
                                          deff = pokedex[pokedex['pokemon']==name]['defense'].values[0],
                                          sdef =pokedex[pokedex['pokemon']==name]['special_defense'].values[0],
                                          speed = pokedex[pokedex['pokemon']==name]['speed'].values[0],
                                          img_url = base + name + '.jpg')

@app.route('/',methods=['POST','GET'])
def hello():
       if request.method == 'POST':
              
              name = str(request.form['name'])
              return redirect(url_for('getPokemonStats',name=name))


if __name__ == "__main__":
    app.run(debug=True)