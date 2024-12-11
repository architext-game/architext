import { v4 as uuidv4 } from 'uuid';
import { setupSocket } from './util';
import { io, Socket } from "socket.io-client";
import { 
  SignupParams, SignupResponse,
  LoginParams, LoginResponse,
  AuthenticateParams, AuthenticateResponse,
  GetCurrentRoomResponse,
  CreateConnectedRoomParams, CreateConnectedRoomResponse,
  TraverseExitParams, TraverseExitResponse,
} from "./types"


describe("Socket.IO End-to-End Tests", () => {
  let socket: Socket
  let jwt_token: string | undefined
  const email = `${uuidv4()}@example.com`
  const username = uuidv4().slice(0, 10)
  const password = "password123"

  beforeAll(() => {
    socket = setupSocket()
  });

  afterAll(() => {
    if (socket.connected) {
      socket.disconnect();
    }
  });

  test("Signup event should create a user", (done) => {
    const params: SignupParams = {
      name: username,
      email: email,
      password: password,
    }

    socket.emit("signup", params, (response: SignupResponse) => {
      try {
        console.log(response)
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
      email: email,
      password: password,
    };

    socket.emit("login", loginParams, (response: LoginResponse) => {
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

    socket.emit("authenticate", authenticateInput, (response: AuthenticateResponse) => {
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
});
