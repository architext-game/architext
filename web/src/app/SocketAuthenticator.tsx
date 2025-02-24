"use client"
import { useAuth } from '@clerk/nextjs'
import { useEffect, useState } from "react";
import { useStore } from "@/state";
import { authenticate } from "@/architextSDK";

export function SocketAuthenticator() {
  const auth = useAuth()
  const socket = useStore((state) => state.socket)
  const [token, setToken] = useState<string | null>()
  const markAuthenticated = useStore((state) => state.markAuthenticated)

  useEffect(() => {
    auth.getToken().then(token => {
      setToken(token)
    })
  }, [auth])

  useEffect(() => {
    if (token) {
      authenticate(socket, { jwt_token: token }).then(() => {
        markAuthenticated()
      })
    }
  }, [token, socket])

  return <></>
}