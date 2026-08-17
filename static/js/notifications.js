const token = localStorage.getItem('access_token');

if (token) {
  // ws:// not http:// — this is a WebSocket connection, not a normal request
  const socket = new WebSocket(`ws://127.0.0.1:8000/ws/notifications/?token=${token}`);

  socket.onopen = () => {
    console.log('Notification socket connected');
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    showNotification(data.message);
  };

  socket.onerror = (err) => {
    console.error('WebSocket error:', err);
  };

  socket.onclose = () => {
    console.log('Notification socket disconnected');
  };
}

function showNotification(message) {
  const badge = document.getElementById('notif-badge');
  if (badge) {
    badge.textContent = parseInt(badge.textContent || '0') + 1;
    badge.classList.remove('d-none');
  }
  alert('🔔 ' + message);
}