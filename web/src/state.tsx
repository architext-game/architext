import { create } from 'zustand'
import type {} from '@redux-devtools/extension' // required for devtools typing
import { io, Socket } from 'socket.io-client'
import { authenticate, AuthenticateResponse, getMe, GetMeResponse, login, LoginResponse } from './architextSDK';

const socket = io("http://207.180.194.96:5000");

interface StoreState {
  me: GetMeResponse | null,
  socket: Socket,
  authChecked: boolean,
  login: (email: string, password: string) => Promise<LoginResponse | GetMeResponse | null>,
  checkAuth: () => Promise<void>
}

export const useStore = create<StoreState>((set, get) => {
  
  const store = {
    me: null,
    socket: socket,
    authChecked: false,
    
    login: async (email: string, password: string) => {
      const loginResponse = await login(socket, { email: email, password: password })
      if(loginResponse.success){
        localStorage.setItem("jwt", loginResponse.data?.jwt_token || "");
        const meResponse = await getMe(socket, {})
        if(meResponse.success){
          set({ me: meResponse })
          return meResponse
        } else {
          set({ me: null })
          return meResponse
        }
      } else {
        set({ me: null })
        return loginResponse
      }
    },

    checkAuth: async () => {
      const token = localStorage.getItem("jwt");
      if (token) {
        const response = await authenticate(socket, { jwt_token: token });
        if (response.success) {
          const meResponse = await getMe(socket, {})
          if(meResponse.success){
            set({ me: meResponse, authChecked: true })
            return
          }
        }
      }
      set({ me: null, authChecked: true })
    },
  }
  store.checkAuth()
  return store
});
