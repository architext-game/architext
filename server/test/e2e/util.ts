import { io, Socket } from "socket.io-client";
import { v4 as uuidv4 } from 'uuid';
import { LoginParams, LoginResponse, SignupParams, SignupResponse, CreateConnectedRoomParams, CreateConnectedRoomResponse } from "./types";


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

export interface Room {
  id: string,
  name: string,
  exit_name: string,
  there_exit_name: string,
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

export async function setupRoom(name: string, user: User): Promise<Room>{
  const uuid = uuidv4()
  const room_name = `${name}${uuid}`.slice(0, 30)
  const exit_name = `${name}${uuid}`.slice(0, 10)
  const return_exit_name = `return${name}${uuid}`


  const createParams: CreateConnectedRoomParams = {
    name: room_name,
    description: 'Room created automatically',
    exit_to_new_room_name: exit_name,
    exit_to_new_room_description: 'Exit created automatically',
    exit_to_old_room_name: return_exit_name,
    exit_to_old_room_description: 'Exit created automatically'
  }

  const response = await emitPromise<CreateConnectedRoomResponse>(user.socket, "create_connected_room", createParams)
  
  return {
    id: response.data?.room_id || '',
    name: room_name,
    exit_name: exit_name,
    there_exit_name: return_exit_name
  }
}

export async function emitPromise<T>(socket: Socket, event: string, data: unknown): Promise<T> {
  return new Promise((resolve, reject) => {
    socket.emit(event, data, (response: T) => {
      resolve(response)
    });
  });
}
