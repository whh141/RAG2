export function createChatSocket(onMessage) {
  const baseUrl = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000'
  const socket = new WebSocket(`${baseUrl}/ws/chat`)
  socket.onmessage = (event) => onMessage(JSON.parse(event.data))
  return socket
}
