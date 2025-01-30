import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type {} from '@redux-devtools/extension' // required for devtools typing
import { io, Socket } from 'socket.io-client'
import { authenticate } from './architextSDK';
import { useEffect, useState } from 'react';

const socket = io("http://207.180.194.96:5000");

export function useSocket() {
  const [isAuthenticated, setIsAuthenticated] = useState(true)

  useEffect(() => {
    socket.on('connect', async () => {
      console.log(`Socket connected with id ${socket.id}, authenticating with jwt...`)
      const jwt = localStorage.getItem("jwt")
      const response = await authenticate(socket, { jwt_token: jwt || '' })
      console.log("Authentication response: ", response)
      if(response.success){
        setIsAuthenticated(true)
      } else {
        setIsAuthenticated(false)
        console.log('Authentication error. Please go back to the login page')
        console.log(response.error || 'Unknown error')
      }
    })

    return () => {
      socket.removeAllListeners('connect')
    }
  }, [socket])

  return {
    socket: socket,
    isAuthenticated: isAuthenticated,
  }
}

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