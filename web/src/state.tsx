import { create } from 'zustand'
import type {} from '@redux-devtools/extension' // required for devtools typing
import { io, Socket } from 'socket.io-client'
import { GetMeResponse } from './architextSDK';

const architextBackendUrl = process.env.NEXT_PUBLIC_ARCHITEXT_BACKEND_URL;

if (!architextBackendUrl) {
  throw new Error("❌ NEXT_PUBLIC_ARCHITEXT_BACKEND_URL is not defined");
}

const socket = io(architextBackendUrl);

interface StoreState {
  me: GetMeResponse | null,
  socket: Socket,
  authenticated: boolean,  // true if the socket is authenticated
  markAuthenticated: () => void,
}

export const useStore = create<StoreState>((set, get) => {
  
  const store = {
    me: null,
    socket: socket,
    authenticated: false,
    markAuthenticated: () => set({ authenticated: true }),
  }
  
  return store
});
