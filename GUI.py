import pandas as pd
import sys, urllib3
import certifi
from PIL import Image
import requests
from PyQt5 import QtGui, QtCore, QtWidgets

pokedex = pd.read_csv('Pokedex.csv')
pokedex['type'] = pokedex[pokedex.columns[6:8]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
pokedex.drop('type_1',axis=1,inplace= True)
pokedex.drop('type_2',axis=1,inplace=True)
col =['id', 'type','pokemon', 'species_id', 'height', 'weight', 'base_experience',
       'attack', 'defense', 'hp', 'special_attack', 'special_defense', 'speed',
       'ability_1', 'ability_2', 'ability_hidden', 'color_1', 'color_2',
       'color_f', 'egg_group_1', 'egg_group_2', 'url_image', 'generation_id',
       'evolves_from_species_id', 'evolution_chain_id', 'shape_id', 'shape']
pokedex=pokedex[col]
pokedex=pokedex.set_index('id')


class PokeDex(QtWidgets.QWidget):
    
    def __init__(self):
        super(PokeDex, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        '''Initial UI'''
        
        #Grid Layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        
        #Parse JSON for DataFrame
        self.df = pokedex
        
        #Drop Down
        self.dropdown = QtWidgets.QComboBox(self)
        self.names = self.df['pokemon'].values
        self.dropdown.addItems(self.names)
        self.grid.addWidget(self.dropdown, 0,0,1,1)
        
        #Search Button
        self.btn = QtWidgets.QPushButton('Search', self)
        self.btn.clicked.connect(self.runSearch)      
        self.grid.addWidget(self.btn, 0,1,1,1)
        
        #Image
        self.img = QtWidgets.QLabel(self)
        self.grid.addWidget(self.img, 1,1,1,1)
        
        #Data
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('\nName:\n\nType:\n\nHP:\n\nAttack\n\nSp. Attack\n\n Defense:\n\nSp. Defense:\n\nSpeed:\n\nTotal:')
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.label, 1,0,1,1)
        
        #Customize Widgets
        self.resize(500, 250)
        self.center()
        self.setWindowTitle('PokeDex')    
        self.show()
        
    def runSearch(self):
        '''Event for run button'''
        
        #Parse value
        index = self.dropdown.currentIndex()
        val= str(self.names[index])
        cond = self.df['pokemon']== val
        
        #Image
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        base = 'http://img.pokemondb.net/artwork/'
        img_url = base + val.lower() + '.jpg'
        r = requests.get(img_url)
        image = QtGui.QImage()
        image.loadFromData(r.content)
        self.img.setPixmap(QtGui.QPixmap(image))
        #Set values
        name = 'Name:\t\t\t'+val+'\n\n'
        ty = 'Type:\t\t\t'+ str(self.df[cond]['type'].values[0])+'\n\n'
        hp = 'HP:\t\t\t'+ str(self.df[cond]['hp'].values[0])+'\n\n'
        atk = 'Attack:\t\t\t'+str(self.df[cond]['attack'].values[0])+'\n\n'
        satk = 'Sp. Attack:\t\t'+str(self.df[cond]['special_attack'].values[0])+'\n\n'
        deff = 'Defense:\t\t\t'+str(self.df[cond]['defense'].values[0])+'\n\n'
        sdef = 'Sp.Defense:\t\t'+str(self.df[cond]['special_defense'].values[0])+'\n\n'
        speed = 'Speed:\t\t\t'+str(self.df[cond]['speed'].values[0])+'\n\n'
        
        #Add text
        final = name+ty+hp+atk+satk+deff+sdef+speed
        self.label.setText(final)
        
    def center(self):
        '''Center Widget on screen'''
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
def main():
    '''Codes for running GUI'''
    
    #Create Application object to run GUI
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    
    #Run GUI
    gui = PokeDex()
    #Exit cleanly when closing GUI
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()