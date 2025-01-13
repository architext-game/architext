import { manager } from "@/app/game/UserMessageHandler";

describe('UserMessageHandler', () => {
  it('handles messages', () => {
    let response = manager.handleMessage('mirar patatas fritas')
    console.log(response)
    response = manager.handleMessage('build')
    console.log(response)
    response = manager.handleMessage('una sala')
    console.log(response)
    response = manager.handleMessage('tiene patatas fritas')
    console.log(response)
  })
})