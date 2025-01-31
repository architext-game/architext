import { Socket } from 'socket.io-client';

export interface LoginParams {
    email: {
    };
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
    email: {
    };
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

export interface ChatbotMessageParams {
    message: string;
}

export interface ChatbotMessageResponse {
    success: boolean;
    data: null;
    error: string | null;
}

export interface GetWorldsParams {
}

export interface GetWorldsResponse {
    success: boolean;
    data: {
        worlds: {
            id: string;
            name: string;
            description: string;
            owner_name: string | null;
            connected_players_count: number;
            base_template_name: string | null;
            base_template_author: string | null;
            visibility: 'public' | 'private';
            you_authorized: boolean;
        }[];
    } | null;
    error: string | null;
}

export interface GetWorldTemplatesParams {
}

export interface GetWorldTemplatesResponse {
    success: boolean;
    data: {
        templates: WorldTemplateListItem[];
    } | null;
    error: string | null;
}

export interface GetWorldParams {
    world_id: string;
}

export interface GetWorldResponse {
    success: boolean;
    data: {
        id: string;
        name: string;
        description: string;
        owner_name: string | null;
        connected_players_count: number;
        base_template_name: string | null;
        base_template_author: string | null;
        visibility: 'public' | 'private';
        you_authorized: boolean;
    } | null;
    error: string | null;
}

export interface GetWorldTemplateParams {
    template_id: string;
}

export interface GetWorldTemplateResponse {
    success: boolean;
    data: {
        id: string;
        name: string;
        description: string;
        owner: string | null;
    } | null;
    error: string | null;
}

export interface EditWorldParams {
    world_id: string;
    name: string | null;
    description: string | null;
}

export interface EditWorldResponse {
    success: boolean;
    data: {
    } | null;
    error: string | null;
}

export interface GetMeParams {
}

export interface GetMeResponse {
    success: boolean;
    data: {
        name: string;
        email: string;
        current_world_id: string | null;
        id: string;
    } | null;
    error: string | null;
}

export interface EnterWorldParams {
    world_id: string;
}

export interface EnterWorldResponse {
    success: boolean;
    data: {
    } | null;
    error: string | null;
}

export interface CreateTemplateParams {
    name: string;
    description: string;
    base_world_id: string;
}

export interface CreateTemplateResponse {
    success: boolean;
    data: {
        template_id: string;
    } | null;
    error: string | null;
}

export interface RequestWorldImportParams {
    name: string;
    description: string;
    format: 'plain' | 'encoded';
    text_representation: string;
}

export interface RequestWorldImportResponse {
    success: boolean;
    data: {
        future_world_id: string;
    } | null;
    error: string | null;
}

export interface RequestWorldCreationFromTemplateParams {
    name: string;
    description: string;
    template_id: string;
}

export interface RequestWorldCreationFromTemplateResponse {
    success: boolean;
    data: {
        future_world_id: string;
    } | null;
    error: string | null;
}

export interface OtherLeftRoomNotification {
    user_name: string;
}

export interface OtherEnteredRoomNotification {
    user_name: string;
}

export interface Message {
    text: string;
    options: {
        display: 'wrap' | 'box' | 'underline' | 'fit';
        section: boolean;
        fillInput: string | null;
        asksForPassword: boolean;
    };
}

export interface WorldCreatedNotification {
    world_id: string;
}

export interface WorldTemplateListItem {
    id: string;
    name: string;
    description: string;
    author_name: string | null;
    author_id: string | null;
    you_authorized: boolean;
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

export async function chatbotMessage(
    socket: Socket,
    params: ChatbotMessageParams
): Promise<ChatbotMessageResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("chatbot_message", params, (response: ChatbotMessageResponse) => {
            resolve(response)
        });
    });
}

export async function getWorlds(
    socket: Socket,
    params: GetWorldsParams
): Promise<GetWorldsResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("get_worlds", params, (response: GetWorldsResponse) => {
            resolve(response)
        });
    });
}

export async function getWorldTemplates(
    socket: Socket,
    params: GetWorldTemplatesParams
): Promise<GetWorldTemplatesResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("get_world_templates", params, (response: GetWorldTemplatesResponse) => {
            resolve(response)
        });
    });
}

export async function getWorld(
    socket: Socket,
    params: GetWorldParams
): Promise<GetWorldResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("get_world", params, (response: GetWorldResponse) => {
            resolve(response)
        });
    });
}

export async function getWorldTemplate(
    socket: Socket,
    params: GetWorldTemplateParams
): Promise<GetWorldTemplateResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("get_world_template", params, (response: GetWorldTemplateResponse) => {
            resolve(response)
        });
    });
}

export async function editWorld(
    socket: Socket,
    params: EditWorldParams
): Promise<EditWorldResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("edit_world", params, (response: EditWorldResponse) => {
            resolve(response)
        });
    });
}

export async function getMe(
    socket: Socket,
    params: GetMeParams
): Promise<GetMeResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("get_me", params, (response: GetMeResponse) => {
            resolve(response)
        });
    });
}

export async function enterWorld(
    socket: Socket,
    params: EnterWorldParams
): Promise<EnterWorldResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("enter_world", params, (response: EnterWorldResponse) => {
            resolve(response)
        });
    });
}

export async function createTemplate(
    socket: Socket,
    params: CreateTemplateParams
): Promise<CreateTemplateResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("create_template", params, (response: CreateTemplateResponse) => {
            resolve(response)
        });
    });
}

export async function requestWorldImport(
    socket: Socket,
    params: RequestWorldImportParams
): Promise<RequestWorldImportResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("request_world_import", params, (response: RequestWorldImportResponse) => {
            resolve(response)
        });
    });
}

export async function requestWorldCreationFromTemplate(
    socket: Socket,
    params: RequestWorldCreationFromTemplateParams
): Promise<RequestWorldCreationFromTemplateResponse> {
    return new Promise((resolve, reject) => {
        socket.emit("request_world_creation_from_template", params, (response: RequestWorldCreationFromTemplateResponse) => {
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

export function onChatbotServerMessage(
    socket: Socket,
    callback: (event: Message) => void
): void {
    socket.on('chatbot_server_message', callback)
}

export function onWorldCreated(
    socket: Socket,
    callback: (event: WorldCreatedNotification) => void
): void {
    socket.on('world_created', callback)
}

