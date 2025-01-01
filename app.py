from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Configurarea aplicației Flask
app = Flask(__name__)
# Configurarea URL-ului bazei de date
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:andrey11@localhost/muzicadb'
# Dezactivarea track-modifications pentru a economisi resurse
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Cheia secretă pentru sesiuni
app.secret_key = 'secret_key'

# Inițializarea extensiei SQLAlchemy
db = SQLAlchemy(app)

# Modele pentru baza de date
class Melodii(db.Model):
    id_melodie = db.Column(db.Integer, primary_key=True)
    titlu = db.Column(db.String(45), nullable=False)
    gen = db.Column(db.String(45), nullable=False)
    an_lansare = db.Column(db.Integer, nullable=False)

class Muzicieni(db.Model):
    id_muzician = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(45), nullable=False)
    prenume = db.Column(db.String(45), nullable=False)
    instrument = db.Column(db.String(45), nullable=False)
    data_nasterii = db.Column(db.Date, nullable=False)

class Album(db.Model):
    idalbum = db.Column(db.Integer, primary_key=True)
    id_muzician = db.Column(db.Integer, db.ForeignKey('muzicieni.id_muzician'), nullable=False)
    id_melodie = db.Column(db.Integer, db.ForeignKey('melodii.id_melodie'), nullable=False)
    rol_muzician = db.Column(db.String(45), nullable=False)

# Rute pentru aplicație
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/melodii')
def melodii():
    # Preluarea tuturor înregistrărilor din tabelul Melodii
    melodii = Melodii.query.all()
    return render_template('melodii.html', melodii=melodii)

@app.route('/muzicieni')
def muzicieni():
    # Preluarea tuturor înregistrărilor din tabelul Muzicieni
    muzicieni = Muzicieni.query.all()
    return render_template('muzicieni.html', muzicieni=muzicieni)

@app.route('/albume')
def albume():
    # Inner join între tabelele Album, Muzicieni și Melodii
    albume = db.session.query(
        Album.idalbum, 
        Album.rol_muzician,
        Muzicieni.nume, 
        Muzicieni.prenume, 
        Muzicieni.instrument, 
        Melodii.titlu, 
        Melodii.gen, 
        Melodii.an_lansare
    ).join(Muzicieni, Album.id_muzician == Muzicieni.id_muzician) \
     .join(Melodii, Album.id_melodie == Melodii.id_melodie).all()

    return render_template('albume.html', albume=albume)

# Rute pentru tabelă Melodii
@app.route('/adauga_melodie', methods=['GET', 'POST'])
def adauga_melodie():
    if request.method == 'POST':
        # Preluarea datelor din formular
        titlu = request.form['titlu']
        gen = request.form['gen']
        an_lansare = request.form['an_lansare']
        # Crearea unui obiect Melodii
        melodie = Melodii(titlu=titlu, gen=gen, an_lansare=an_lansare)
        # Adăugarea obiectului în sesiunea de bază de date
        db.session.add(melodie)
        # Confirmarea modificărilor în baza de date
        db.session.commit()
        # Redirecționarea către pagina melodii
        return redirect(url_for('melodii'))
    # Renderizarea template-ului adauga_melodie.html pentru metode GET
    return render_template('adauga_melodie.html')

@app.route('/sterge_melodie/<int:id>')
def sterge_melodie(id):
    # Căutarea melodiei după id, sau returnarea unei erori 404 dacă nu este găsită
    melodie = Melodii.query.get_or_404(id)
    # Ștergerea obiectului din sesiunea de bază de date
    db.session.delete(melodie)
    # Confirmarea modificărilor în baza de date
    db.session.commit()
    # Redirecționarea către pagina melodii
    return redirect(url_for('melodii'))

@app.route('/modifica_melodie/<int:id>', methods=['GET', 'POST'])
def modifica_melodie(id):
    # Căutarea melodiei după id, sau returnarea unei erori 404 dacă nu este găsită
    melodie = Melodii.query.get_or_404(id)
    if request.method == 'POST':
        # Preluarea datelor din formular și actualizarea obiectului Melodii
        melodie.titlu = request.form['titlu']
        melodie.gen = request.form['gen']
        melodie.an_lansare = request.form['an_lansare']
        # Confirmarea modificărilor în baza de date
        db.session.commit()
        # Redirecționarea către pagina melodii
        return redirect(url_for('melodii'))
    # Renderizarea template-ului modifica_melodie.html pentru metode GET
    return render_template('modifica_melodie.html', melodie=melodie)

# Rute pentru tabelă Muzicieni
@app.route('/adauga_muzician', methods=['GET', 'POST'])
def adauga_muzician():
    if request.method == 'POST':
        # Preluarea datelor din formular
        nume = request.form['nume']
        prenume = request.form['prenume']
        instrument = request.form['instrument']
        data_nasterii = request.form['data_nasterii']
        # Crearea unui obiect Muzicieni
        muzician = Muzicieni(nume=nume, prenume=prenume, instrument=instrument, data_nasterii=data_nasterii)
        # Adăugarea obiectului în sesiunea de bază de date
        db.session.add(muzician)
        # Confirmarea modificărilor în baza de date
        db.session.commit()
        # Redirecționarea către pagina muzicieni
        return redirect(url_for('muzicieni'))
    # Renderizarea template-ului adauga_muzician.html pentru metode GET
    return render_template('adauga_muzician.html')

@app.route('/sterge_muzician/<int:id>')
def sterge_muzician(id):
    # Căutarea muzicianului după id, sau returnarea unei erori 404 dacă nu este găsit
    muzician = Muzicieni.query.get_or_404(id)
    # Ștergerea obiectului din sesiunea de bază de date
    db.session.delete(muzician)
    # Confirmarea modificărilor în baza de date
    db.session.commit()
    # Redirecționarea către pagina muzicieni
    return redirect(url_for('muzicieni'))

@app.route('/modifica_muzician/<int:id>', methods=['GET', 'POST'])
def modifica_muzician(id):
    # Căutarea muzicianului după id, sau returnarea unei erori 404 dacă nu este găsit
    muzician = Muzicieni.query.get_or_404(id)
    if request.method == 'POST':
        # Preluarea datelor din formular și actualizarea obiectului Muzicieni
        muzician.nume = request.form['nume']
        muzician.prenume = request.form['prenume']
        muzician.instrument = request.form['instrument']
        muzician.data_nasterii = request.form['data_nasterii']
        # Confirmarea modificărilor în baza de date
        db.session.commit()
        # Redirecționarea către pagina muzicieni
        return redirect(url_for('muzicieni'))
    # Renderizarea template-ului modifica_muzician.html pentru metode GET
    return render_template('modifica_muzician.html', muzician=muzician)

# Rute pentru tabelă Albume
@app.route('/adauga_album', methods=['GET', 'POST'])
def adauga_album():
    # Preluarea muzicienilor și melodiilor din baza de date pentru a le afișa în formular
    muzicieni = Muzicieni.query.all()  # Preluarea muzicienilor din baza de date
    melodii = Melodii.query.all()  # Preluarea melodiilor din baza de date

    if request.method == 'POST':
        # Preluarea datelor din formular
        id_muzician = request.form['id_muzician']
        id_melodie = request.form['id_melodie']
        rol_muzician = request.form['rol_muzician']
        # Crearea unui obiect Album
        album = Album(id_muzician=id_muzician, id_melodie=id_melodie, rol_muzician=rol_muzician)
        # Adăugarea obiectului în sesiunea de bază de date
        db.session.add(album)
        # Confirmarea modificărilor în baza de date
        db.session.commit()
        # Redirecționarea către pagina albume
        return redirect(url_for('albume'))
    # Renderizarea template-ului adauga_album.html pentru metode GET
    return render_template('adauga_album.html', muzicieni=muzicieni, melodii=melodii)

@app.route('/sterge_album/<int:id>')
def sterge_album(id):
    # Căutarea albumului după id, sau returnarea unei erori 404 dacă nu este găsit
    album = Album.query.get_or_404(id)
    # Ștergerea obiectului din sesiunea de bază de date
    db.session.delete(album)
    # Confirmarea modificărilor în baza de date
    db.session.commit()
    # Redirecționarea către pagina albume
    return redirect(url_for('albume'))

@app.route('/modifica_album/<int:id>', methods=['GET', 'POST'])
def modifica_album(id):
    # Căutarea albumului după id, sau returnarea unei erori 404 dacă nu este găsit
    album = Album.query.get_or_404(id)
    # Preluarea muzicienilor și melodiilor din baza de date pentru a le afișa în formular
    muzicieni = Muzicieni.query.all()  # Preluarea muzicienilor din baza de date
    melodii = Melodii.query.all()  # Preluarea melodiilor din baza de date

    if request.method == 'POST':
        # Preluarea datelor din formular și actualizarea obiectului Album
        album.id_muzician = request.form['id_muzician']
        album.id_melodie = request.form['id_melodie']
        album.rol_muzician = request.form['rol_muzician']
        # Confirmarea modificărilor în baza de date
        db.session.commit()
        # Redirecționarea către pagina albume
        return redirect(url_for('albume'))
    # Renderizarea template-ului modifica_album.html pentru metode GET
    return render_template('modifica_album.html', album=album, muzicieni=muzicieni, melodii=melodii)

if __name__ == '__main__':
    # Pornirea aplicației Flask în modul debug
    app.run(debug=True)
