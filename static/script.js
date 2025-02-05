document.addEventListener('DOMContentLoaded', function() {
    const encodeForm = document.getElementById('encode-form');
    const decodeForm = document.getElementById('decode-form');

    if (encodeForm) {
        encodeForm.addEventListener('submit', function(event) {
            processForm(event, encodeForm);
        });
    }

    if (decodeForm) {
        decodeForm.addEventListener('submit', function(event) {
            processForm(event, decodeForm, '/decode'); // Utilisez la route /decode pour le traitement du décodage
        });
    }
});

function processForm(event, form, action = '/encode') {
    event.preventDefault();
    showLoader();

    const formData = new FormData(form);
    let outputName = formData.get('output_name'); // Récupérer le nom du fichier entré par l'utilisateur

    fetch(action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return Promise.all([response.blob(), response.headers.get('X-Decoded-File-Extension'), response.headers.get('Content-Disposition')]);
        } else {
            return response.json().then(data => {
                displayErrorAlert(data.error);  // Afficher l'alerte basée sur le message d'erreur JSON
                hideLoader();
                throw new Error('La réponse du serveur n\'est pas OK.');
            });
        }
    })
    .then(([blob, decodedFileExtension, contentDispositionHeader]) => {
        let fileName = 'default_file';
        if (action === '/decode' && decodedFileExtension) {
            // Si le décodage et une extension de fichier est fournie, ajouter l'extension au nom fourni
            fileName = outputName ? `${outputName}${decodedFileExtension}` : 'decoded_file' + decodedFileExtension;
        } else if (action === '/encode') {
            // Pour l'encodage, utilisez simplement le nom donné ou un nom par défaut
            fileName = outputName || 'encoded_image';
            fileName += '.png'; // Ajouter une extension par défaut pour l'encodage
        }
        downloadFile(blob, fileName);
        hideLoader();
    })
    .catch(error => {
        console.error('Error:', error);
        hideLoader();
    });
}
function displayErrorAlert(errorMsg) {
    // Utiliser alert pour montrer tous les messages d'erreur
    alert(errorMsg); // Ceci affichera le message d'erreur dans une alerte standard du navigateur
}


function downloadFile(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}



function showLoader() {
    document.querySelector('.loader').style.display = 'block';
    document.querySelector('.loader-backdrop').style.display = 'block';
}

function hideLoader() {
    document.querySelector('.loader').style.display = 'none';
    document.querySelector('.loader-backdrop').style.display = 'none';
}
