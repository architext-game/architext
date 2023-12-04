/**
 * This is the starting point for a "smart logic"
 * that handles all it can in the frontend.
 *
 * I stopped this and went on the road for a
 * stupid logic.
 */

import { useState, useEffect, useRef } from 'react'

export const useProcess = (send: send) => {
  const [context, setContext] = useState<context>(initialContext)
  return (message: string) => {
    const newContext = process(message, context, send)
    setContext(newContext)
  }
}

import cloneDeep from 'lodash/cloneDeep'

class BadMessage extends Error {
  constructor(message: string) {
      super(message);
      this.name = "Message can't be processed";
  }
}

 interface context {
  currentVerb: string | null,
  verbState: {}
}

 const initialContext: context = {
  currentVerb: 'login',
  verbState: {}
}

interface send {
  toClient: (message: string) => void,
}
type verbFunction = (message: string, context: context, send: send) => context
type canProcessFunction = (message: string) => boolean
interface verb {
  process: verbFunction,
  can: canProcessFunction
}

const echo: verb = {
  process: (message: string, context: context, send: send) => {
      send.toClient("echo: " + message)
      context.currentVerb = null
      return context
    },
  can: (message: string) => {
    return true
  }
}


interface loginState {
  name?: string,
  password?: string,
  passwordRepeat?: string,
  email?: string,
}

const login: verb = {
  process: (message: string, context: context, send: send) => {
    const state: loginState = context.verbState
    if(!state.name){
      state.name = message

    }
    context = cloneDeep(context)
    send.toClient("echo: " + message)
    context.currentVerb = null
    return context
  },
  can: (message: string) => {
    return false
  }
}

function findVerb(message: string) {
  for(let [name, { can }] of Object.entries(verbs)){
    if(can(message)){
      return name
    }
  }
  return null
}

const verbs: { [key: string]: verb } = {
  echo: echo,
  login: login,
}

function process(message: string, context: context, send: send){
  context = cloneDeep(context)
  if(!context.currentVerb){
    context.currentVerb = findVerb(message)
  }
  if(context.currentVerb){
    context = verbs[context.currentVerb].process(message, context, send)
  } else {
    throw BadMessage
  }
  return context
}