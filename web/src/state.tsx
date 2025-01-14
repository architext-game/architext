import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type {} from '@redux-devtools/extension' // required for devtools typing
import { io, Socket } from 'socket.io-client'

const socket = io("http://207.180.194.96:5000");

interface StoreState {
  socket: Socket;
  setSocket: (socket: Socket) => void;
}

export const useStore = create<StoreState>()(
  (set) => ({
    socket: socket,
    setSocket: (socket: Socket) => set((state) => ({ socket: socket })),
  })
)