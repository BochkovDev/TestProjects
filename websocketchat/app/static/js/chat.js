function addUserClickListeners() {
    const userItems = document.querySelectorAll('.user-item');  
    userItems.forEach(item => {
        item.addEventListener('click', (event) => {
            const userId = item.getAttribute('data-user-id');  
            const userName = item.textContent;  
            selectUser(userId, userName, event);  
        });
    });
}

async function fetchUsers() {
    try {
        const response = await fetch('/auth/users');
        const users = await response.json();
        const userList = document.getElementById('userList');

        userList.innerHTML = '';

        const favoriteElement = document.createElement('div');
        favoriteElement.classList.add('user-item');
        favoriteElement.setAttribute('data-user-id', currentUserId);
        favoriteElement.textContent = 'Избранное';

        userList.appendChild(favoriteElement);

        users.forEach(user => {
            if (user.id !== currentUserId) {
                const userElement = document.createElement('div');
                userElement.classList.add('user-item');
                userElement.setAttribute('data-user-id', user.id);
                userElement.textContent = user.username;
                userList.appendChild(userElement);
            }
        });

        addUserClickListeners();
    } catch (error) {
        console.error('Ошибка при загрузке списка пользователей:', error);
    }
}

document.addEventListener('DOMContentLoaded', fetchUsers);
setInterval(fetchUsers, 10000); 

let selectedUserId = null;  
let socket = null;          

async function logout() {
    try {
        const response = await fetch('/auth/logout', { 
            method: 'POST', 
            credentials: 'include' 
        });

        if (response.ok) {
            window.location.href = '/auth'; 
        } else {
            console.error('Ошибка при выходе'); 
        }
    } catch (error) {
        console.error('Ошибка при выполнении запроса:', error);
    }
}


async function selectUser(userId, userName, event) {
    selectedUserId = userId;  
    document.getElementById('chatHeader').innerHTML = `<span>Чат с ${userName}</span><button class="logout-button" id="logoutButton">Выход</button>`;
    document.getElementById('messageInput').disabled = false; 
    document.getElementById('sendButton').disabled = false;   

    document.querySelectorAll('.user-item').forEach(item => item.classList.remove('active')); 
    event.target.classList.add('active'); 

    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = '';  
    messagesContainer.style.display = 'block'; 

    document.getElementById('logoutButton').onclick = logout;  

    await loadMessages(userId);  
    connectWebSocket();
}

async function loadMessages(userId) {
    try {
        const response = await fetch(`/chat/messages/${userId}`); 
        const messages = await response.json();  

        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = messages.map(message =>
            createMessageElement(message.content, message.recipient_id)  
        ).join('');  
    } catch (error) {
        console.error('Ошибка загрузки сообщений:', error);  
    }
}

function connectWebSocket() {
    if (socket) socket.close(); 

    socket = new WebSocket(`ws://${window.location.host}/chat/ws/${selectedUserId}`);  

    socket.onopen = () => console.log('WebSocket соединение установлено');  
    console.log('My ID is ', currentUserId)
    console.log('Selected User ID is ', selectedUserId)

    socket.onmessage = (event) => {
        const incomingMessage = JSON.parse(event.data);  
        if (incomingMessage.recipient_id === currentUserId) {  
            console.log('Incoming message: ', incomingMessage.content, incomingMessage.recipient_id)
            addMessage(incomingMessage.content, incomingMessage.recipient_id);  
        }
    };

    socket.onclose = () => console.log('WebSocket соединение закрыто');  
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();  

    if (message && selectedUserId) {  
        const payload = {recipient_id: selectedUserId, content: message}; 

        try {
            await fetch('/chat/messages', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)  
            });

            socket.send(JSON.stringify(payload));  
            addMessage(message, selectedUserId);  
            messageInput.value = '';  
        } catch (error) {
            console.error('Ошибка при отправке сообщения:', error); 
        }
    }
}

function addMessage(text, recipient_id) {
    console.log('func addMessage: recipient_id=', recipient_id)
    const messagesContainer = document.getElementById('messages');
    messagesContainer.insertAdjacentHTML('beforeend', createMessageElement(text, recipient_id));  
    messagesContainer.scrollTop = messagesContainer.scrollHeight;  
}

function createMessageElement(text, recipient_id) {
    console.log('func createMessageElement: recipient_id=', recipient_id)
    const userID = parseInt(selectedUserId, 10);
    console.log('func createMessageElement: userID=', userID)
    const messageClass = userID == recipient_id ? 'my-message' : 'other-message';  
    return `<div class="message ${messageClass}">${text}</div>`; 
}

document.querySelectorAll('.user-item').forEach(item => {
    item.onclick = event => selectUser(item.getAttribute('data-user-id'), item.textContent, event); 
});

document.getElementById('sendButton').onclick = sendMessage; 

document.getElementById('messageInput').onkeypress = async (e) => {
    if (e.key === 'Enter') {  
        await sendMessage(); 
    }
};