import { useState, useEffect, useRef } from 'react'
import './App.css'
import io from 'socket.io-client';
import { DefaultEventsMap } from '@socket.io/component-emitter';
import { Socket } from 'socket.io-client';
import classNames from 'classnames'
import { Message } from './Message';
import _ from 'lodash';

const SOCKET_SERVER_URL = 'http://localhost:5000';

interface Message {
  text: string,
  type: 'user' | 'server',
  visible?: boolean,
  display: 'wrap' | 'box' | 'underline' | 'fit',
  section: boolean
}

interface MessageOptions {
  display: 'wrap' | 'box' | 'underline' | 'fit',
  section: boolean
}

function boxx(string: string): string {
  const fillin: string = '━'.repeat(string.length);
  return `┏━━━━${fillin}━━━━┓\n┃    ${string}    ┃\n┗━━━━${fillin}━━━━┛\n`;
}

function box(text: string, maxWidth: number): string {
  maxWidth = maxWidth - 8
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
  const bottomRef = useRef<HTMLDivElement>(null)
  const scrollRef = useRef<HTMLDivElement>(null)
  const messageListRef = useRef<HTMLDivElement>(null)
  const characterMeasureRef = useRef<HTMLDivElement>(null)

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

  const addServerMessage = (text: string, options: MessageOptions) => {
    const message: Message = {
      text: text.replace(/^\n|\n$/g, ''),
      type: 'server',
      display: options.display,
      section: options.section
    }
    setMessages((prevMessages) => [...prevMessages, message])
  }

  const addUserMessage = () => {
    socket?.emit('message', inputValue)
    const message: Message = { text: inputValue, type: 'user', display: 'wrap', section: false }
    setMessages((prevMessages) => [...prevMessages, message])
    setInputValue('')
  }

  const handleScroll = () => {
    if(!scrollRef.current) return

    const { scrollTop, clientHeight, scrollHeight } = scrollRef.current;

    if (scrollHeight - scrollTop - clientHeight < 10 ) {
      if(!scrolledBottom){
        setScrolledBottom(true)
      }
    } else {
      if(scrolledBottom){
        setScrolledBottom(false)
      }
    }
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      addUserMessage()
    }
  }

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'instant' })
  }, [messages.length])

  useEffect(() => {
    const newSocket = io(SOCKET_SERVER_URL, /*{secure: true} TODO */);
    setSocket(newSocket);

    return () => { newSocket.disconnect() };
  }, []);

  useEffect(() => {
    if (socket) {
      socket.on('message', (message: string, options: MessageOptions) => {
        addServerMessage(message, options)
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

  if(scrolledBottom){
    for (let i = highlightedMessages.length - 1; i >= 0; i--) {
      highlightedMessages[i] = true
      if(messages[i].section){
        highlightedMessages[i] = true
        break
      }
    }
  } else {

  }

  return (
    <div className="bg-bg w-screen h-screen text-white font-console break-words">
      <div className="flex flex-col h-screen justify-end">
        <div
          className="flex-1 overflow-auto p-4 space-y-2 whitespace-pre-wrap"
          ref={scrollRef} onScroll={handleScroll}
        >
          <div className="max-w-3xl mx-auto" ref={messageListRef}>
            {messages.map((message, index, array) => (
              <Message
                charAspectRatio={charAspectRatio}
                key={index}
                className={classNames(
                  "px-2 text-left",
                  { 'text-soft border-t-2 border-muted pb-4 pt-2': message.type == 'user' },
                  { 'pb-2': message.type == 'server' },
                  { 'text-soft': scrolledBottom ? !highlightedMessages[index] : message.visible === false },
                )}
                text={
                  message.display === 'box' ? box(message.text, charsWidth - 2)
                  : message.text
                }
                onIntersectionChange={v => handleIntersectionChange(v, index)}
                intersectionMargin='-0px'
                fit={message.display === 'fit'}
              />
            ))}
          <div ref={bottomRef} />
          <div ref={characterMeasureRef} className="h-0 w-fit overflow-hidden">W</div>
          </div>
        </div>
        <div className="p-4 max-w-3xl mx-auto w-screen">
          <input
            autoFocus
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="p-2 border rounded w-full bg-bg"
            placeholder="Type a message"
          />
        </div>
      </div>
    </div>
  )
}

export default App
