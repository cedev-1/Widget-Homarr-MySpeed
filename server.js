const express = require('express');
const { exec } = require('child_process');

const app = express();
const port = 3000;

let latestResult = null;

// Fonction pour exécuter speedtest-cli
function runSpeedtest() {
    console.log('Exécution du Speedtest...');
    exec('speedtest-cli --json', (error, stdout, stderr) => {
        if (error) {
            console.error(`Erreur lors de l'exécution de speedtest-cli : ${error.message}`);
            latestResult = { error: 'Impossible d\'exécuter le Speedtest' };
            return;
        }
        if (stderr) {
            console.error(`Stderr : ${stderr}`);
        }
        try {
            latestResult = JSON.parse(stdout);
            console.log('Speedtest terminé avec succès.');
        } catch (parseError) {
            console.error(`Erreur de parsing des résultats : ${parseError.message}`);
            latestResult = { error: 'Erreur lors du traitement des résultats' };
        }
    });
}

// Exécuter un test au démarrage
runSpeedtest();

// Planifier un Speedtest toutes les 5 minutes
setInterval(runSpeedtest, 5 * 60 * 1000);

// Endpoint pour afficher le dernier résultat
app.get('/speedtest', (req, res) => {
    if (!latestResult) {
        return res.json({ message: 'Aucun résultat disponible pour le moment. Réessayez dans quelques secondes.' });
    }
    res.json(latestResult);
});

// Lancer le serveur
app.listen(port, () => {
    console.log(`Serveur lancé sur http://localhost:${port}`);
});
