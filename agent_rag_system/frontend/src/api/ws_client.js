export function createChatSocket(onMessage) {
  const socket = new WebSocket('ws://localhost:8000/ws/chat')
  socket.onmessage = (event) => onMessage(JSON.parse(event.data))
  return socket
}
