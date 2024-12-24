import { setupUser, User, setupRoom, Room, emitPromise } from './util';
import { 
  getCurrentRoom,
  createConnectedRoom, CreateConnectedRoomParams,
  traverseExit, TraverseExitParams,
  OtherLeftRoomNotification,
  OtherEnteredRoomNotification
} from "./types"
import { Socket, io } from 'socket.io-client';
import { v4 as uuidv4 } from 'uuid';

describe("Socket.IO End-to-End Tests", () => {
  const sockets: Socket[] = []

  afterAll(() => {
    sockets.forEach(s => s.disconnect())
  })

  test("Get current room event should return room data", async () => {
    const alice = await setupUser('alice')
    sockets.push(alice.socket)
    const response = await getCurrentRoom(alice.socket, null)
    expect(response).toBeDefined();
    expect(response.success).toBe(true);
    expect(response.data?.current_room?.name).toBeDefined();
  });

  test("Create connected room event should return room creation data", async () => {
    const alice = await setupUser('alice')
    sockets.push(alice.socket)

    const uuid = uuidv4()
    const room_name = `${uuid}`.slice(0, 30)
    const exit_name = `${uuid}`.slice(0, 10)
    const return_name = `back${uuid}`.slice(0, 10)

    const roomInput: CreateConnectedRoomParams = {
      name: room_name,
      description: "Bot made this",
      exit_to_new_room_name: exit_name,
      exit_to_new_room_description: "Bot made this",
      exit_to_old_room_name: return_name,
      exit_to_old_room_description: "Bot made this"
    }

    const response = await createConnectedRoom(alice.socket, roomInput)
    expect(response).toBeDefined();
    expect(response.success).toBe(true);
    expect(response.data?.room_id).toBeDefined();
  });

  test("Traverse exit event should return traversal data", async () => {
    const alice = await setupUser('alice')
    sockets.push(alice.socket)

    const room = await setupRoom('', alice)

    const traverseInput: TraverseExitParams = {
      exit_name: (await room).exit_name,
    };

    const response = await traverseExit(alice.socket, traverseInput)
    expect(response).toBeDefined();
    expect(response.success).toBe(true);
    expect(response.data).toBeDefined();
    expect(response.data?.new_room_id).toBe(room.id);
  });

  test("User gets notified when another user leaves the room", async () => {
    const alice = await setupUser('alice');
    const bob = await setupUser('bob');

    sockets.push(alice.socket)
    sockets.push(bob.socket)

    const room = await setupRoom('leaves', alice)
    const traverseInput: TraverseExitParams = {
      exit_name: room.exit_name,
    };

    const spy = jest.fn((x: OtherLeftRoomNotification) => {})
    
    const expectedEventPromise =  new Promise<void>((resolve) => {
      bob.socket.on("other_left_room", (event: OtherLeftRoomNotification) => {
        if(event.user_name == alice.name){
          spy(event);
          resolve();
        }
      });
    });

    const response = await traverseExit(alice.socket, traverseInput);
    await expectedEventPromise

    expect(spy).toHaveBeenCalled();
    expect(spy.mock.calls[0][0]).toBeDefined();
    expect(spy.mock.calls[0][0].user_name).toBe(alice.name);

    alice.socket.disconnect()
    bob.socket.disconnect()
  });

  test("User gets notified when another user enters the room", async () => {
    const alice = await setupUser('alice');
    const bob = await setupUser('bob');

    sockets.push(alice.socket)
    sockets.push(bob.socket)

    const room = await setupRoom('leaves', alice)
    const traverseInput: TraverseExitParams = {
      exit_name: room.exit_name,
    };
    await traverseExit(alice.socket, traverseInput);
    
    const spy = jest.fn((x: OtherLeftRoomNotification) => {})
    
    const expectedEventPromise =  new Promise<void>((resolve) => {
      bob.socket.on("other_entered_room", (event: OtherEnteredRoomNotification) => {
        if(event.user_name == alice.name){
          spy(event);
          resolve();
        }
      });
    });

    await traverseExit(alice.socket, {exit_name: room.there_exit_name});

    const response = await traverseExit(alice.socket, traverseInput);
    await expectedEventPromise

    expect(spy).toHaveBeenCalled();
    expect(spy.mock.calls[0][0]).toBeDefined();
    expect(spy.mock.calls[0][0].user_name).toBe(alice.name);

    alice.socket.disconnect()
    bob.socket.disconnect()
  });
});
