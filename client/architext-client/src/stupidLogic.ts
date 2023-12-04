/**
 * This is the starting point for a "smart logic"
 * that handles all it can in the frontend.
 *
 * I stopped this and went on the road for a
 * stupid logic.
 */

import { useState, useEffect, useRef } from 'react'

interface send {
  toClient: (message: string) => void,
}

export const useProcess = (send: send) => {
  return (message: string) => {
    
  }
}

