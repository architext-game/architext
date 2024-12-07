import { io, Socket } from "socket.io-client";
import { 
  SignupParams, SignupResponse,
  LoginParams, LoginResponse,
  AuthenticateParams, AuthenticateResponse,
  GetCurrentRoomResponse,
  CreateConnectedRoomParams, CreateConnectedRoomResponse,
  TraverseExitParams, TraverseExitResponse,

} from "./types"

const SERVER_URL = "http://localhost:5000"; // Replace with your server's URL
let jwt_token: string | undefined;

describe("Socket.IO End-to-End Tests", () => {
  let clientSocket: Socket;


  beforeAll((done) => {
    // Connect to the server before tests
    clientSocket = io(SERVER_URL, { transports: ["websocket"] });

    clientSocket.on("connect", () => {
      console.log("Connected to the server");
      done();
    });

    clientSocket.on("connect_error", (err) => {
      console.error("Connection failed:", err.message);
      done(err);
    });
  });

  afterAll(() => {
    // Disconnect after tests
    if (clientSocket.connected) {
      clientSocket.disconnect();
    }
  });


  test("Signup event should create a user", (done) => {
    const params: SignupParams = {
      name: "newuser",
      email: "newuser@example.com",
      password: "password123",
    }

    clientSocket.emit("signup", params, (response: SignupResponse) => {
      try {
        expect(response).toBeDefined();
        expect(response.success).toBe(true);
        expect(response.data?.user_id).toBeDefined();
        done();
      } catch (error) {
        done(error);
      }
    });
  });

  test("Login event should return a JWT token", (done) => {
    const loginParams: LoginParams = {
      email: "newuser@example.com",
      password: "password123",
    };

    clientSocket.emit("login", loginParams, (response: LoginResponse) => {
      try {
        expect(response).toBeDefined();
        expect(response.success).toBe(true);
        expect(response.data?.jwt_token).toBeDefined();
        jwt_token = response.data?.jwt_token
        done();
      } catch (error) {
        console.log("Error: " + response.error)
        done(error);
      }
    });
  });

  test("Authenticate event should return user_id", (done) => {
    const authenticateInput: AuthenticateParams = {
      jwt_token: jwt_token ?? "bad_token", // Replace with a valid token
    };

    clientSocket.emit("authenticate", authenticateInput, (response: AuthenticateResponse) => {
      try {
        expect(response).toBeDefined();
        expect(response.success).toBe(true);
        expect(response.data).toHaveProperty("user_id");
        done();
      } catch (error) {
        console.log("Error: " + response.error)
        done(error);
      }
    });
  });


  test("Get current room event should return room data", (done) => {
    clientSocket.emit("get_current_room", {}, (response: GetCurrentRoomResponse) => {
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

  test("Create connected room event should return room creation data", (done) => {
    const roomInput: CreateConnectedRoomParams = {
      name: "Nueva sala",
      description: "molona",
      exit_to_new_room_name: "ja",
      exit_to_new_room_description: "ja",
      exit_to_old_room_name: "ja",
      exit_to_old_room_description: "ja"
    }

    clientSocket.emit("create_connected_room", roomInput, (response: CreateConnectedRoomResponse) => {
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

    clientSocket.emit("traverse_exit", traverseInput, (response: TraverseExitResponse) => {
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

  test("Get current room event should show the new room", (done) => {
    clientSocket.emit("get_current_room", {}, (response: GetCurrentRoomResponse) => {
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
});
