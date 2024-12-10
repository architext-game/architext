import { setupUser, User } from './util';
import { 
  GetCurrentRoomResponse,
  CreateConnectedRoomParams, CreateConnectedRoomResponse,
  TraverseExitParams, TraverseExitResponse,
  OtherLeftRoomData,
  OtherEnteredRoomData
} from "./types"
import { Socket } from 'socket.io-client';

describe("Socket.IO End-to-End Tests", () => {
  let alice: User;
  let bob: User;
  let charlie: User;
  let dave: User;

  beforeAll(async () => {
    // Connect to the server before tests
    alice = await setupUser('alice');
    bob = await setupUser('bob');
    charlie = await setupUser('cha');
    dave = await setupUser('dave');
  });

  afterAll(() => {
    // Disconnect after tests
    if (alice.socket.connected) {
      alice.socket.disconnect();
    }
    if (bob.socket.connected) {
      bob.socket.disconnect();
    }
    if (charlie.socket.connected) {
      charlie.socket.disconnect();
    }
    if (dave.socket.connected) {
      dave.socket.disconnect();
    }
  });

  test("Get current room event should return room data", (done) => {
    alice.socket.emit("get_current_room", {}, (response: GetCurrentRoomResponse) => {
      try {
        expect(response).toBeDefined();
        expect(response.success).toBe(true);
        expect(response.data?.name).toBeDefined();
        done();
      } catch (error) {
        done(error);
      }
    });
  });


  function emitCreateConnectedRoom(socket: Socket, params: CreateConnectedRoomParams, callback: (response: CreateConnectedRoomResponse) => void){
    socket.emit('create_connected_room', params, callback)
  }

  function onOtherLeftRoom(socket: Socket, callback: (event: OtherLeftRoomData) => void){
    socket.on('other_left_room', callback)
  }

  test("Create connected room event should return room creation data", (done) => {
    const roomInput: CreateConnectedRoomParams = {
      name: "Nueva sala",
      description: "molona",
      exit_to_new_room_name: "ja",
      exit_to_new_room_description: "ja",
      exit_to_old_room_name: "ja",
      exit_to_old_room_description: "ja"
    }

    alice.socket.emit("create_connected_room", roomInput, (response: CreateConnectedRoomResponse) => {
      try {
        expect(response).toBeDefined();
        expect(response.success).toBe(true);
        expect(response.data?.name).toBe("Nueva sala");
        done();
      } catch (error) {
        done(error);
      }
    });
  });

  test("Traverse exit event should return traversal data", (done) => {
    const traverseInput: TraverseExitParams = {
      exit_name: "ja",
    };

    alice.socket.emit("traverse_exit", traverseInput, (response: TraverseExitResponse) => {
      try {
        expect(response).toBeDefined();
        expect(response.success).toBe(true);
        expect(response.data).toBeDefined();
        expect(response.data?.new_room_id).toBeDefined();
        done();
      } catch (error) {
        done(error);
      }
    });
  });

  test("User gets notified when another user leaves the room", async () => {
    const traverseInput: TraverseExitParams = {
      exit_name: "ja",
    };

    const spy = jest.fn((x: OtherLeftRoomData) => {})
    
    const expectedEventPromise =  new Promise<void>((resolve) => {
      dave.socket.on("other_left_room", (event: OtherLeftRoomData) => {
        if(event.user_name == charlie.name){
          spy(event);
          resolve();
        }
      });
    });

    charlie.socket.emit("traverse_exit", traverseInput);
    await expectedEventPromise

    expect(spy).toHaveBeenCalled();
    expect(spy.mock.calls[0][0]).toBeDefined();
    expect(spy.mock.calls[0][0].user_name).toBe(charlie.name);
  });

  test("User gets notified when another user enters the room", async () => {
    const traverseInput: TraverseExitParams = {
      exit_name: "ja",
    };

    const spy = jest.fn((x: OtherLeftRoomData) => {})
    
    const expectedEventPromise =  new Promise<void>((resolve) => {
      charlie.socket.on("other_entered_room", (event: OtherEnteredRoomData) => {
        if(event.user_name == dave.name){
          spy(event);
          resolve();
        }
      });
    });

    dave.socket.emit("traverse_exit", traverseInput);
    await expectedEventPromise

    expect(spy).toHaveBeenCalled();
    expect(spy.mock.calls[0][0]).toBeDefined();
    expect(spy.mock.calls[0][0].user_name).toBe(dave.name);
  });
});
