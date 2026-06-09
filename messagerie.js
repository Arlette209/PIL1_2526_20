const USER_ID = 1;           
const CONVERSATION_ID = 1;  
const DESTINATAIRE_ID = 2;   
const socket = io('http://localhost:5001');
socket.on('connect', () => {
    socket.emit('rejoindre', { user_id: USER_ID });
    socket.emit('charger_messages', { conversation_id: CONVERSATION_ID });
    socket.emit('marquer_comme_lu', {
        conversation_id: CONVERSATION_ID,
        user_id: USER_ID
    });
});
socket.on('historique_messages', (data) => {
    const liste = document.getElementById('liste-messages');
    liste.innerHTML = '';
    data.messages.forEach(msg => afficherMessage(msg));
});
socket.on('nouveau_message_recu', (msg) => {
    afficherMessage(msg);
});
socket.on('messages_lus_notification', (data) => {
    console.log('Messages lus par', data.lecteur_id);
});
function envoyerMessage() {
    const input = document.getElementById('input-message');
    const texte = input.value.trim();
    if (!texte) return;
    socket.emit('envoyer_message', {
        conversation_id: CONVERSATION_ID,
        expediteur_id: USER_ID,
        destinataire_id: DESTINATAIRE_ID,
        contenu: texte
    });
    afficherMessage({ expediteur_id: USER_ID, contenu: texte, date_envoi: new Date().toLocaleTimeString() });
    input.value = '';
}
function afficherMessage(msg) {
    const liste = document.getElementById('liste-messages');
    const div = document.createElement('div');
    div.classList.add('message');
    div.classList.add(msg.expediteur_id == USER_ID ? 'message-moi' : 'message-autre');
    div.innerHTML = `<p>${msg.contenu}</p><span>${msg.date_envoi || ''}</span>`;
    liste.appendChild(div);
    liste.scrollTop = liste.scrollHeight; 
}
async function envoyerFichier(messageId, fichier) {
    const formData = new FormData();
    formData.append('fichier', fichier);
    formData.append('message_id', messageId);

    const res = await fetch('/api/upload_piece_jointe', {
        method: 'POST',
        body: formData
    });
    const data = await res.json();
    console.log('Fichier uploadé :', data.chemin);
}