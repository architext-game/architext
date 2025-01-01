import { v4 as uuidv4 } from 'uuid';
import { setupSocket } from './util';
import { Socket } from "socket.io-client";
import { 
  signup, SignupParams,
  login, LoginParams,
  authenticate, AuthenticateParams,
} from "./architextSDK"


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

  test("Signup event should create a user", async () => {
    const params: SignupParams = {
      name: username,
      email: email,
      password: password,
    }

    const response = await signup(socket, params)

    expect(response).toBeDefined();
    expect(response.success).toBe(true);
    expect(response.data?.user_id).toBeDefined();
  });

  test("Login event should return a JWT token", async () => {
    const loginParams: LoginParams = {
      email: email,
      password: password,
    };

    const response = await login(socket, loginParams)
    expect(response).toBeDefined();
    expect(response.success).toBe(true);
    expect(response.data?.jwt_token).toBeDefined();
    jwt_token = response.data?.jwt_token
  });


  test("Authenticate event should return user_id", async () => {
    const authenticateInput: AuthenticateParams = {
      jwt_token: jwt_token ?? "bad_token", // Replace with a valid token
    };

    const response = await authenticate(socket, authenticateInput)
    expect(response).toBeDefined();
    expect(response.success).toBe(true);
    expect(response.data).toHaveProperty("user_id");
  });
});
