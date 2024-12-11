import { io, Socket } from "socket.io-client";
import { v4 as uuidv4 } from 'uuid';
import { LoginParams, LoginResponse, SignupParams, SignupResponse } from "./types";


const SERVER_URL = "http://localhost:5000"; // Replace with your server's URL

export function setupSocket(){
  const socket = io(SERVER_URL, { transports: ["websocket"] });
  
  socket.on("connect", () => {
    console.log("Connected to the server");
  });
  
  socket.on("connect_error", (err) => {
    console.error("Connection failed:", err.message);
  });

  return socket
}

export interface User {
  name: string,
  email: string,
  password: string,
  jwt_token: string,
  socket: Socket
}

export async function setupUser(name: string): Promise<User>{
  const socket = setupSocket()

  const email = `${name}${uuidv4()}@example.com`
  const username = `${name}${uuidv4()}`.slice(0, 10)
  const password = "password123"

  const params: SignupParams = {
    name: username,
    email: email,
    password: password,
  }

  await emitPromise<SignupResponse>(socket, "signup", params)

  const loginParams: LoginParams = {
    email: email,
    password: password,
  };

  const loginResponse = await emitPromise<LoginResponse>(socket, "login", loginParams)

  return {
    name: username,
    email: email,
    password: password,
    jwt_token: loginResponse.data?.jwt_token || '',
    socket: socket
  }
}

export async function emitPromise<T>(socket: Socket, event: string, data: unknown): Promise<T> {
  return new Promise((resolve, reject) => {
    socket.emit(event, data, (response: T) => {
      resolve(response)
    });
  });
}
