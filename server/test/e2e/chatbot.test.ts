import { setupUser, setupRoom } from './util';
import { 
  chatbotMessage, onChatbotServerMessage
} from "./architextSDK"
import { Socket, io } from 'socket.io-client';
import { v4 as uuidv4 } from 'uuid';

describe("Socket.IO End-to-End Tests", () => {
  const sockets: Socket[] = []

  afterAll(() => {
    sockets.forEach(s => s.disconnect())
  })

  test("Smoke test", async () => {
    const alice = await setupUser('alice')
    onChatbotServerMessage(alice.socket, (event) => {
      console.log(event.text)
    })
    sockets.push(alice.socket)
    await chatbotMessage(alice.socket, { message: 'look' })
    await chatbotMessage(alice.socket, { message: 'build' })
    await chatbotMessage(alice.socket, { message: "Alice's cool room" })
    await chatbotMessage(alice.socket, { message: "You see the ultimate gaming rig." })
    await chatbotMessage(alice.socket, { message: `A door that reads: "Alice's"` })
    await chatbotMessage(alice.socket, { message: `Exit door` })
    await chatbotMessage(alice.socket, { message: `look` })
    await chatbotMessage(alice.socket, { message: `go A door that reads: "Alice's"` })
  });

});
