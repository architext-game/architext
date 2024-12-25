import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type {} from '@redux-devtools/extension' // required for devtools typing
import { io, Socket } from 'socket.io-client'

const socket = io("http://207.180.194.96:5000");

interface StoreState {
  socket: Socket;
  jwt: string | null;
  setSocket: (socket: Socket) => void;
  setJWT: (jwt: string) => void;
}

export const useStore = create<StoreState>()(
  (set) => ({
    socket: socket,
    jwt: null,
    setSocket: (socket: Socket) => set((state) => ({ socket: socket })),
    setJWT: (jwt: string) => set((state) => ({ jwt: jwt }))
  })
)