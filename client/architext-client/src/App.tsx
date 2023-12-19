import { useState, useEffect, useRef } from 'react'
import io from 'socket.io-client';
import { DefaultEventsMap } from '@socket.io/component-emitter';
import { Socket } from 'socket.io-client';
import classNames from 'classnames'
import { Message } from './Message';
import _ from 'lodash';

const SOCKET_SERVER_ADDRESS = import.meta.env.VITE_SERVER_ADDRESS;

interface Message {
  text: string,
  type: 'user' | 'server',
  visible?: boolean,
  display: 'wrap' | 'box' | 'underline' | 'fit',
  section: boolean
}

interface ReceivedMessage {
  text: string,
  display: 'wrap' | 'box' | 'underline' | 'fit',
  section: boolean
}

function boxx(string: string): string {
  const fillin: string = '━'.repeat(string.length);
  return `┏━━━━${fillin}━━━━┓\n┃    ${string}    ┃\n┗━━━━${fillin}━━━━┛\n`;
}

// Function to split the text into lines based on the maxWidth
function wrapText(text: string, maxWidth: number): string[] {
  let words = text.split(' ');
  let lines: string[] = [];
  let currentLine = '';

  words.forEach(word => {
    if (word.length > maxWidth) {
      // If the current line is not empty, push it to lines
      if (currentLine) {
        lines.push(currentLine.trim());
        currentLine = '';
      }
      // Split the long word and add it as separate lines
      while (word.length > 0) {
        let part = word.substring(0, maxWidth);
        lines.push(part);
        word = word.substring(maxWidth);
      }
    } else if (currentLine.length + word.length + 1 <= maxWidth) {
      currentLine += (currentLine.length > 0 ? ' ' : '') + word;
    } else {
      lines.push(currentLine.trim());
      currentLine = word;
    }
  });

  if (currentLine) {
    lines.push(currentLine.trim());
  }

  return lines;
}

// Function to center text within the given maxWidth
function centerText(text: string, maxWidth: number): string {
  let space = maxWidth - text.length;
  let paddingStart = Math.floor(space / 2);
  let paddingEnd = space - paddingStart;
  return ' '.repeat(paddingStart) + text + ' '.repeat(paddingEnd);
}

function underline(text: string, maxWidth: number): string {
  let lines = wrapText(text, maxWidth)
  let longestLenght = lines.reduce<number>(((length, line) => (_.max([length, line.length]) ?? length)), 0)
  lines.push('━'.repeat(longestLenght));
  const result = lines.reduce(((str, line) => str += '\n'+line), "").trim()
  return result
}

function box(text: string, maxWidth: number): string {
  maxWidth = maxWidth - 8

  // Split and center the text
  let lines = wrapText(text, maxWidth)
  let longestLenght = lines.reduce<number>(((length, line) => (_.max([length, line.length]) ?? length)), 0)
  lines = lines.map(line => centerText(line, longestLenght));

  // Create the top and bottom borders based on maxWidth
  const fillin = '━'.repeat(longestLenght);
  let result = `┏━━━${fillin}━━━┓\n`;

  // Add each line of text
  lines.forEach(line => {
    result += `┃   ${line}   ┃\n`;
  });

  // Add the bottom border
  result += `┗━━━${fillin}━━━┛\n`;
  return result;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [socket, setSocket] = useState<Socket<DefaultEventsMap, DefaultEventsMap> | null>(null);
  const [scrolledBottom, setScrolledBottom] = useState<boolean>(false)
  const [charsWidth, setCharsWidth] = useState<number>(0)
  const [charAspectRatio, setCharAspectRatio] = useState<number>(1)
  const [previousLastSection, setPreviousLastSection] = useState<number>(-1)
  const bottomRef = useRef<HTMLDivElement>(null)
  const lastSectionRef = useRef<HTMLDivElement>(null)
  const scrollRef = useRef<HTMLDivElement>(null)
  const messageListRef = useRef<HTMLDivElement>(null)
  const characterMeasureRef = useRef<HTMLDivElement>(null)
  const textInputContainerRef = useRef<HTMLDivElement>(null)

  const updateCharWidth = () => {
    if(messageListRef.current && characterMeasureRef.current){
      let width = messageListRef.current.clientWidth ?? 0
      const style = window.getComputedStyle(messageListRef.current);
      width -= parseInt(style.getPropertyValue('padding-left'));
      width -= parseInt(style.getPropertyValue('padding-right'));
      const charWidth = characterMeasureRef.current?.clientWidth ?? 1
      const widthInChars = Math.floor(width/charWidth)
      setCharsWidth(widthInChars)
      const ar = charWidth / parseFloat(style.fontSize)
      setCharAspectRatio(ar)
    }
  }

  useEffect(() => {
    const observer = new ResizeObserver(entries => {
      updateCharWidth();
    });

    if (messageListRef.current && characterMeasureRef.current) {
      observer.observe(messageListRef.current);
      observer.observe(characterMeasureRef.current);
    }

    return () => {
      observer.disconnect();
    };
  }, [messageListRef.current, characterMeasureRef.current, updateCharWidth]);

  const addServerMessage = (receivedMessage: ReceivedMessage) => {
    const message: Message = {
      ...receivedMessage,
      type: 'server',
      text: receivedMessage.display === 'fit' ? receivedMessage.text : receivedMessage.text.trim()
    }
    setMessages((prevMessages) => [...prevMessages, message])
  }

  const addUserMessage = () => {
    socket?.emit('message', inputValue)
    const message: Message = { text: inputValue, type: 'user', display: 'wrap', section: false }
    setMessages((prevMessages) => [...prevMessages, message])
    setInputValue('')
  }

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setScrolledBottom(entry.isIntersecting);
      },
    );
    if(bottomRef.current){
      observer.observe(bottomRef.current)
      const frozenRef = bottomRef.current
      return () => {
        if(bottomRef.current){
          observer.unobserve(frozenRef)
        }
      }
    }
  }, [bottomRef.current]);

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      addUserMessage()
    }
  }

  useEffect(() => {
    if(!messages.some(m => m.type == 'user')){
      bottomRef.current?.scrollIntoView({ behavior: 'instant' })
    }else if(previousLastSection !== lastSectionIndex){
      lastSectionRef.current?.scrollIntoView({ behavior: 'instant' })
    }else if(scrolledBottom){
      bottomRef.current?.scrollIntoView({ behavior: 'instant' })
    }
    setPreviousLastSection(lastSectionIndex)
  }, [messages.length, lastSectionRef, bottomRef])

  useEffect(() => {
    const newSocket = io(SOCKET_SERVER_ADDRESS, /*{secure: true} TODO */);
    setSocket(newSocket);

    return () => { newSocket.disconnect() };
  }, []);

  useEffect(() => {
    if (socket) {
      socket.on('message', (receivedMessage: ReceivedMessage) => {
        addServerMessage(receivedMessage)
      });

      socket.on('connect', () => {
        console.log("connected")
      });
    }
  }, [socket]);

  const handleIntersectionChange = (visible: boolean, index: number) => {

    setMessages((messages) => {
      const updatedMessages = [ ...messages ]
      updatedMessages[index] = { ...updatedMessages[index], visible }
      return updatedMessages
    })
  }

  const highlightedMessages: boolean[] = new Array(messages.length).fill(false);

  let lastSectionIndex = -1

  for (let i = messages.length - 1; i >= 0; i--) {
    if(messages[i].section){
      lastSectionIndex = i
      break
    }
  }

  if(scrolledBottom){
    for (let i = highlightedMessages.length - 1; i >= 0; i--) {
      highlightedMessages[i] = true
      if(messages[i].section){
        lastSectionIndex = i
        break
      }
    }
  } else {

  }

  useEffect(() => {
    window.visualViewport?.addEventListener('resize', (ev) => {
      console.log("adasd", ev);
    })
  }, [])

  return (
    <div className="bg-bg min-h-screen w-screen flex flex-col justify-end text-white font-console break-words text-sm sm:text-base">
        <div
          className="flex-1 px-3 sm:px-6 whitespace-pre-wrap overflow-auto flex flex-col"
          ref={scrollRef}
        >
          <div className="grow shrink-0 basis-auto mx-auto max-w-3xl flex flex-col justify-end" ref={messageListRef}>
            {messages.map((message, index, array) => {
              return (
                <Message
                  charAspectRatio={charAspectRatio}
                  key={index}
                  className={classNames(
                    "text-left",
                    { 'text-soft border-muted pb-4 pt-2': message.type == 'user' },
                    { 'pb-2': message.type === 'server' && message.display !== 'underline' && message.display !== 'box' },
                    { 'text-soft': scrolledBottom ? !highlightedMessages[index] : false && message.visible === false },
                  )}
                  text={
                    message.display === 'box' ? box(message.text, charsWidth - 2)
                    : message.display === 'underline' ? underline(message.text, charsWidth - 2)
                    : message.text
                  }
                  onIntersectionChange={v => handleIntersectionChange(v, index)}
                  intersectionMargin='-0px'
                  fit={message.display === 'fit'}
                  ref={
                    lastSectionIndex === index ? lastSectionRef : null
                  }
                />
              )
              })}
            <div ref={bottomRef}/>
            <div style={{height: textInputContainerRef.current?.clientHeight}}/> {/* Fill height blocked by textInput */}
            <div ref={characterMeasureRef} className="h-0 w-fit overflow-hidden">W</div>
          </div>
        </div>
        <div className="bg-bg fixed bottom-0 w-screen p-4f flex justify-center py-4 px-2" ref={textInputContainerRef}>
          <input
            autoFocus
            autoCapitalize="none"
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="p-2 border rounded w-full bg-bg max-w-3xl"
            placeholder="Type a message"
          />
          {
            !scrolledBottom &&
            <div className='absolute mx-auto -top-4 left-0 right-0 text-center flex justify-center'>
              <div className='bg-bg px-3 py-2 rounded-sm border border-white'>↓ 👁️ ↓</div>
            </div>
          }
        </div>
    </div>
  )
}

export default App
