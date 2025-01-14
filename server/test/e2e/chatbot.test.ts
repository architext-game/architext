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
    let out = ""
    onChatbotServerMessage(alice.socket, (event) => {
      out += event.text + "\n"
    })
    sockets.push(alice.socket)
    await chatbotMessage(alice.socket, { message: 'look' })
    await chatbotMessage(alice.socket, { message: 'build' })
    await chatbotMessage(alice.socket, { message: "Alice's cool room" })
    await chatbotMessage(alice.socket, { message: "You see the ultimate gaming rig." })
    await chatbotMessage(alice.socket, { message: `A door that reads: "${alice.name}'s"` })
    await chatbotMessage(alice.socket, { message: `Exit door` })
    await chatbotMessage(alice.socket, { message: `look` })
    await chatbotMessage(alice.socket, { message: `go ${alice.name}'s` })
    console.log(out)
    expect(out.includes(`You start building a new room.`))
    expect(out.includes(`Your new room is ready. Good work!`))
    expect(out.includes(`Alice's cool room`))
    expect(out.includes(`You see the ultimate gaming rig`))
    expect(out.includes(`Alice's cool room`))
    expect(out.includes(`You see the ultimate gaming rig`))

  });

});
