from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'  # Ändere das unbedingt für deine Anwendung!

def generiere_code():
    return ''.join(random.choice('1234567890') for _ in range(4))

def vergleiche_code(gegebener_code, echter_code):
    if gegebener_code == echter_code:
        return "Korrekt!"
    feedback = ""
    for i in range(4):
        if gegebener_code[i] == echter_code[i]:
            feedback += "•"  # Richtige Zahl an der richtigen Stelle
        elif gegebener_code[i] in echter_code:
            feedback += "o"  # Richtige Zahl an der falschen Stelle
    return feedback if feedback else "Keine Übereinstimmung"

def gib_laufenden_hinweis(gegebener_code, echter_code):
    try:
        letzte_ziffer_gegeben = int(gegebener_code[-1])
        letzte_ziffer_echt = int(echter_code[-1])
        if letzte_ziffer_gegeben < letzte_ziffer_echt:
            return "Die letzte Ziffer ist höher."
        elif letzte_ziffer_gegeben > letzte_ziffer_echt:
            return "Die letzte Ziffer ist niedriger."
        else:
            return "Die letzte Ziffer ist richtig."
    except (ValueError, IndexError):
        return None

@app.route('/', methods=['GET', 'POST'])
def rate_code():
    if 'echter_code' not in session:
        session['echter_code'] = generiere_code()
        session['versuche'] = []
        session['anzahl_versuche'] = 0
        session['hinweis_aktiv'] = False

    hinweis = None
    if request.method == 'POST':
        geratener_code = request.form['code']
        spezial_code = request.form.get('spezialcode')

        if geratener_code:
            session['anzahl_versuche'] += 1
            ergebnis = vergleiche_code(geratener_code, session['echter_code'])
            session['versuche'].append({'code': geratener_code, 'ergebnis': ergebnis})
            if ergebnis == "Korrekt!":
                return render_template('ergebnis.html', versuche=session['versuche'], anzahl_versuche=session['anzahl_versuche'], echter_code=session['echter_code'])

        if spezial_code and spezial_code.lower() == 'rolex':
            session['hinweis_aktiv'] = True

        if session.get('hinweis_aktiv'):
            hinweis = gib_laufenden_hinweis(geratener_code, session['echter_code'])

    return render_template('raten.html', versuche=session['versuche'], anzahl_versuche=session['anzahl_versuche'], hinweis=hinweis)

@app.route('/reset')
def reset_spiel():
    session.pop('echter_code', None)
    session.pop('versuche', None)
    session.pop('anzahl_versuche', None)
    session.pop('hinweis_aktiv', None)
    return redirect(url_for('rate_code'))

if __name__ == '__main__':
    app.run(debug=True)
