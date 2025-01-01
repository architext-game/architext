import { Socket } from 'socket.io-client';

export interface LoginParams {
    email: any;
    password: string;
}

export interface LoginResponse {
    success: boolean;
    data: {
        jwt_token: string;
    } | null;
    error: string | null;
}

export interface AuthenticateParams {
    jwt_token: string;
}

export interface AuthenticateResponse {
    success: boolean;
    data: {
        user_id: string;
    } | null;
    error: string | null;
}

export interface SignupParams {
    email: any;
    name: string;
    password: string;
}

export interface SignupResponse {
    success: boolean;
    data: {
        user_id: string;
    } | null;
    error: string | null;
}

export interface GetCurrentRoomResponse {
    success: boolean;
    data: {
        current_room: {
            id: string;
            name: string;
            description: string;
            exits: {
                name: string;
                description: string;
            }[];
            people: {
                id: string;
                name: string;
            }[];
        } | null;
    } | null;
    error: string | null;
}

export interface CreateConnectedRoomParams {
    name: string;
    description: string;
    exit_to_new_room_name: string;
    exit_to_new_room_description: string;
    exit_to_old_room_name: string;
    exit_to_old_room_description: string;
}

export interface CreateConnectedRoomResponse {
    success: boolean;
    data: {
        room_id: string;
    } | null;
    error: string | null;
}

export interface TraverseExitParams {
    exit_name: string;
}

export interface TraverseExitResponse {
    success: boolean;
    data: {
        new_room_id: string;
    } | null;
    error: string | null;
}

export interface OtherLeftRoomNotification {
    user_name: string;
}

export interface OtherEnteredRoomNotification {
    user_name: string;
}
export async function login(
    socket: Socket,
    params: LoginParams
): Promise<LoginResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("login", params, (response: LoginResponse) => {
            resolve(response)
        });
    });
}

export async function authenticate(
    socket: Socket,
    params: AuthenticateParams
): Promise<AuthenticateResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("authenticate", params, (response: AuthenticateResponse) => {
            resolve(response)
        });
    });
}

export async function signup(
    socket: Socket,
    params: SignupParams
): Promise<SignupResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("signup", params, (response: SignupResponse) => {
            resolve(response)
        });
    });
}

export async function getCurrentRoom(
    socket: Socket,
    params: null
): Promise<GetCurrentRoomResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("get_current_room", params, (response: GetCurrentRoomResponse) => {
            resolve(response)
        });
    });
}

export async function createConnectedRoom(
    socket: Socket,
    params: CreateConnectedRoomParams
): Promise<CreateConnectedRoomResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("create_connected_room", params, (response: CreateConnectedRoomResponse) => {
            resolve(response)
        });
    });
}

export async function traverseExit(
    socket: Socket,
    params: TraverseExitParams
): Promise<TraverseExitResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("traverse_exit", params, (response: TraverseExitResponse) => {
            resolve(response)
        });
    });
}

export function onOtherLeftRoom(
    socket: Socket,
    callback: (event: OtherLeftRoomNotification) => void
): void {
    socket.on('other_left_room', callback)
}

export function onOtherEnteredRoom(
    socket: Socket,
    callback: (event: OtherEnteredRoomNotification) => void
): void {
    socket.on('other_entered_room', callback)
}

