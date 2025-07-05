const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

let chatState = {
    step: 0,
    user: {},
    reservation: {},
    reservationId: null
};

function appendMessage(msg, sender) {
    const div = document.createElement('div');
    div.className = sender === 'user' ? 'user-msg' : 'agent-msg';
    div.textContent = msg;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function resetChat() {
    chatWindow.innerHTML = '';
    chatState = { step: 0, user: {}, reservation: {}, reservationId: null };
    agentIntro();
}

function agentIntro() {
    appendMessage('Welcome! Please enter your username:', 'agent');
}

async function agentStep(input) {
    switch (chatState.step) {
        case 0:
            chatState.user.username = input;
            appendMessage('What is your specialization?', 'agent');
            chatState.step = 1;
            break;
        case 1:
            chatState.user.specialization = input;
            appendMessage('What is your position? (Doctor, Nurse, Surgeon, Physician)', 'agent');
            chatState.step = 2;
            break;
        case 2:
            chatState.user.position = input;
            // Register user
            try {
                const res = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(chatState.user)
                });
                const data = await res.json();
                if (res.ok) {
                    chatState.user.user_id = data.user_id;
                    appendMessage('What do you need to do today? (Lab work, Patient consultation, Research)', 'agent');
                    chatState.step = 3;
                } else {
                    appendMessage('Registration failed: ' + data.message, 'agent');
                    chatState.step = 0;
                }
            } catch (err) {
                appendMessage('Error connecting to server.', 'agent');
                chatState.step = 0;
            }
            break;
        case 3:
            chatState.reservation.action = input;
            appendMessage('When do you need the space? (e.g., 2025-07-05 14:00-16:00)', 'agent');
            chatState.step = 4;
            break;
        case 4:
            chatState.reservation.time_needed = input;
            // Start booking
            try {
                const res = await fetch('/start_booking', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: chatState.user.user_id,
                        action: chatState.reservation.action,
                        time_needed: chatState.reservation.time_needed
                    })
                });
                const data = await res.json();
                if (res.ok) {
                    chatState.reservationId = data.reservation_id;
                    appendMessage(`Proposed resource: ${data.resource}. Confirm booking? (Yes/No)`, 'agent');
                    chatState.step = 5;
                } else {
                    appendMessage('Booking failed: ' + data.message, 'agent');
                    chatState.step = 3;
                }
            } catch (err) {
                appendMessage('Error connecting to server.', 'agent');
                chatState.step = 3;
            }
            break;
        case 5:
            if (/^yes$/i.test(input)) {
                // Confirm booking
                try {
                    const res = await fetch('/confirm_booking', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ reservation_id: chatState.reservationId, agree: true })
                    });
                    const data = await res.json();
                    if (res.ok) {
                        appendMessage('Booking confirmed! Thank you.', 'agent');
                        chatState.step = 6;
                    } else {
                        appendMessage('Confirmation failed: ' + data.message, 'agent');
                        chatState.step = 3;
                    }
                } catch (err) {
                    appendMessage('Error connecting to server.', 'agent');
                    chatState.step = 3;
                }
            } else {
                // Cancel booking
                try {
                    const res = await fetch('/confirm_booking', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ reservation_id: chatState.reservationId, agree: false })
                    });
                    const data = await res.json();
                    appendMessage('Booking cancelled.', 'agent');
                    chatState.step = 3;
                } catch (err) {
                    appendMessage('Error connecting to server.', 'agent');
                    chatState.step = 3;
                }
            }
            break;
        default:
            appendMessage('Start over? Type anything to restart.', 'agent');
            chatState.step = 0;
            break;
    }
}

chatForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const input = userInput.value.trim();
    if (!input) return;
    appendMessage(input, 'user');
    userInput.value = '';
    agentStep(input);
});

window.onload = agentIntro;
