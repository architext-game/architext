import { create } from 'zustand'
import type {} from '@redux-devtools/extension' // required for devtools typing
import { io, Socket } from 'socket.io-client'
import { GetMeResponse } from './architextSDK';

const socket = io("http://207.180.194.96:5000");

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
