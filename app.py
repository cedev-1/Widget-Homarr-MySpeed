from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # URL de l'API pour récupérer les tests de vitesse
    url = "http://192.168.0.9:5216/api/speedtests?hours=24"
    
    # Faire la requête à l'API
    response = requests.get(url)
    
    # Si la réponse n'est pas OK, renvoyer une erreur
    if response.status_code != 200:
        return "Erreur lors de la récupération des données de l'API", 500
    
    data = response.json()
    
    # Filtrer les résultats pour n'inclure que ceux qui n'ont pas d'erreur
    valid_results = [result for result in data if 'error' not in result]
    
    if not valid_results:
        return "Aucun test valide trouvé.", 500
    
    # Récupérer les données du dernier test valide
    last_result = valid_results[0]  # Utiliser le dernier résultat valide

    # Extraire les informations de téléchargement, d'upload et de ping
    download = last_result.get('download', 'N/A')
    upload = last_result.get('upload', 'N/A')
    ping = last_result.get('ping', 'N/A')

    return render_template('medium.html', download=download, upload=upload, ping=ping)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)
