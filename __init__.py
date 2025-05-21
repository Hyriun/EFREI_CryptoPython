from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template
import base64

app = Flask(__name__)

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"

@app.route('/decrypt/<string:token_chiffre>')
def decryptage(token_chiffre):
    token_bytes = token_chiffre.encode()
    try:
        valeur_dechiffree_bytes = f.decrypt(token_bytes)
        return f"Valeur déchiffrée : {valeur_dechiffree_bytes.decode()}"
    except Exception as e:
        return f"Erreur de déchiffrement : {str(e)}. Assurez-vous que le token est correct et que la clé utilisée pour le chiffrement est la même."

@app.route('/encryptkey/<key>/<valeur>')
def encrypt_personal(key, valeur):
    try:
        key_bytes = key.encode()
        fernet_perso = Fernet(key_bytes)
        token = fernet_perso.encrypt(valeur.encode())
        return f"Valeur encryptée : {token.decode()}"
    except Exception as e:
        return f"Erreur de chiffrement : {str(e)}", 400

@app.route('/decryptkey/<key>/<token>')
def decrypt_personal(key, token):
    try:
        key_bytes = key.encode()
        fernet_perso = Fernet(key_bytes)
        valeur = fernet_perso.decrypt(token.encode())
        return f"Valeur déchiffrée : {valeur.decode()}"
    except InvalidToken:
        return "Clé incorrecte ou token invalide", 403
    except Exception as e:
        return f"Erreur de déchiffrement : {str(e)}", 400

if __name__ == "__main__":
    app.run(debug=True)
