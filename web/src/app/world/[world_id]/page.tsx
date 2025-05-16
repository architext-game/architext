"use client"

import { useState, useEffect, useRef, use, RefObject } from 'react'
import classNames from 'classnames'
import { Message } from './Message';
import _ from 'lodash';
import { onChatbotServerMessage, chatbotMessage, Message as ReceivedMessage, authenticate, enterWorld, getMe, getWorld, GetWorldResponse, getWorlds, onWorldCreatedNotification } from '@/architextSDK';
import { useStore } from '@/state';
import { useRouter } from 'next/navigation';
import { HamburgerMenu } from './hamburger';
import Link from 'next/link';
import { Overlay } from '@/components/overlay';
import { EditWorldForm } from './edit_world_form';
import { CreateTemplateForm } from './create_template_form';
import useHeartbeat from '../heartbeat';

const usePageScrolledToBottom = () => {
  const [isAtBottom, setIsAtBottom] = useState(false);

  const handleScroll = () => {
    // Comprueba si el usuario ha llegado al final de la página
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 10) {
      setIsAtBottom(true);
    } else {
      setIsAtBottom(false);
    }
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);

    // Comprobación inicial
    handleScroll();

    // Cleanup: elimina el listener al desmontar el componente
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return isAtBottom;
};

const useIsScrolledToBottom = (ref: RefObject<HTMLDivElement | null>) => {
  const [isAtBottom, setIsAtBottom] = useState(false);

  useEffect(() => {
    console.log("USEEFFECT")
    const handleScroll = () => {
      console.log("Scrolling")
      if (!ref.current) return;

      const { scrollTop, scrollHeight, clientHeight } = ref.current;
      if (scrollTop + clientHeight >= scrollHeight - 10) {
        setIsAtBottom(true);
      } else {
        setIsAtBottom(false);
      }
    };

    const element = ref.current;
    if (element) {
      console.log("adding listener")
      element.addEventListener('scroll', handleScroll);
    }

    // Comprobación inicial por si el contenido ya está scrolleado al cargar
    handleScroll();

    // Cleanup: elimina el listener al desmontar el componente
    return () => {
      if (element) {
        element.removeEventListener('scroll', handleScroll);
      }
    };
  }, [ref]);

  return isAtBottom;
};

interface Message {
  text: string,
  type: 'user' | 'server',
  visible?: boolean,
  display: 'wrap' | 'box' | 'underline' | 'fit',
  section: boolean
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

function App({ params, searchParams }: { 
  params: Promise<{ world_id: string }>,
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const [worldId, setWorldId] = useState<string>(use(params).world_id)
  const socket = useStore((state) => state.socket)
  const me = useStore((state) => state.me)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  // const [scrolledBottom, setScrolledBottom] = useState<boolean>(false)
  const scrolledBottom = usePageScrolledToBottom()
  const [charsWidth, setCharsWidth] = useState<number>(0)
  const [charAspectRatio, setCharAspectRatio] = useState<number>(1)
  const [previousLastSection, setPreviousLastSection] = useState<number>(-1)
  const [shouldSelect, setShouldSelect] = useState<boolean>(false)
  const [privateInput, setPrivateInput] = useState<boolean>(false)
  const [showEditWorldOverlay, setShowEditWorldOverlay] = useState(false)
  const [showCreateTemplateOverlay, setShowCreateTemplateOverlay] = useState(false)
  const [world, setWorld] = useState<GetWorldResponse>()
  const bottomRef = useRef<HTMLDivElement>(null)
  const lastSectionRef = useRef<HTMLDivElement>(null)
  const scrollRef = useRef<HTMLDivElement>(null)
  const messageListRef = useRef<HTMLDivElement>(null)
  const characterMeasureRef = useRef<HTMLDivElement>(null)
  const textInputContainerRef = useRef<HTMLDivElement>(null)
  const textAreaRef = useRef<HTMLTextAreaElement>(null)
  const worldIsNew = use(searchParams).future;  // so it may not exist yet
  const shouldEnterWorld = useRef(true);
  const authenticated = useStore((state) => state.authenticated)


  useHeartbeat(socket)

  useEffect(() => {
    if(worldId){
      getWorld(socket, { world_id: worldId }).then(response => {
        setWorld(response)
      })
    }
  }, [worldId])
  
  const privileged = world?.data?.you_authorized


  // TODO: This has not been really tested for cases when the world
  // does not yet exist.
  async function eventuallyEnterWorld(eventualWorlId: string){
    console.log("Entering world", eventualWorlId)
    const current_world_id = (await getMe(socket, {})).data?.current_world_id
    if(current_world_id == eventualWorlId){
      return
    }
    // Enter a world taking into account that it may not exist yet.
    const enterWorldResponse = await enterWorld(socket, { world_id: eventualWorlId })
    console.log(enterWorldResponse)
    if(!enterWorldResponse.success){
      if(worldIsNew){
        console.log("World is new, waiting for creation...")
        addServerMessage({ text: 'Your world is being created... please wait.', options: { asksForPassword: false, display: "wrap", fillInput: null, section: false } })
        onWorldCreatedNotification(socket, async ({ world_id }) => {
          console.log("OnWorldCreated event received, world_id is", world_id)
          if(world_id == eventualWorlId){
            const response = await enterWorld(socket, { world_id: worldId })
            if(!response.success){
              // addServerMessage({ text: 'There was an error entering the world.', options: { asksForPassword: false, display: "wrap", fillInput: null, section: false } })
            } else {
              addServerMessage({ text: 'Your new world is ready!', options: { asksForPassword: false, display: "wrap", fillInput: null, section: false } })
            }
            socket.removeAllListeners('world_created')
          }
        })
      } else {
        // addServerMessage({ text: 'There was an error entering the world.', options: { asksForPassword: false, display: "wrap", fillInput: null, section: false } })
      }
    } else {
      // addServerMessage({ text: 'You are in the world you want to be.', options: { asksForPassword: false, display: "wrap", fillInput: null, section: false } })
    }
  }

  async function gameSetup(worldId: string){
    await eventuallyEnterWorld(worldId)
    chatbotMessage(socket, { message: "look" })
  }

  useEffect(() => {
    if(authenticated && shouldEnterWorld.current == true){
      shouldEnterWorld.current = false
      gameSetup(worldId)
    }
  }, [socket, worldId, worldIsNew])

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
      display: receivedMessage.options.display,
      section: receivedMessage.options.section,
      type: 'server',
      text: receivedMessage.options.display === 'fit' ? receivedMessage.text : receivedMessage.text.trim()
    }
    setMessages((prevMessages) => [...prevMessages, message])
  }

  const addUserMessage = () => {
    chatbotMessage(socket, { message: inputValue })
    const message: Message = { text: inputValue, type: 'user', display: 'wrap', section: false }
    setMessages((prevMessages) => [...prevMessages, message])
    setInputValue('')
    setPrivateInput(false)
  }

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        // setScrolledBottom(entry.isIntersecting);
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

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      addUserMessage()
    }
  }

  const handleKeyDownInput = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
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
    if(shouldSelect && textAreaRef.current){
      textAreaRef.current.select()
      setShouldSelect(false)
    }
  }, [shouldSelect])

  useEffect(() => {
    if (socket) {
      onChatbotServerMessage(socket, (receivedMessage) => {
        addServerMessage(receivedMessage)
        if(receivedMessage.options.fillInput){
          setInputValue(receivedMessage.options.fillInput)
          setShouldSelect(true)
        }
        if(receivedMessage.options.asksForPassword){
          setPrivateInput(true)
        }
      })

      socket.on('connect_error', () => {
        const message: Message = {
          display: 'wrap',
          section: true,
          type: 'server',
          text: `Error connecting to server. Check your connection. Contact oliverlsanz@gmail.com if the issue persists.`
        }
        setMessages((prevMessages) => [...prevMessages, message])
      });

      return () => { socket.removeAllListeners() }
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
    if (textAreaRef?.current) {
      textAreaRef.current.style.height = 'auto'; // Reset height to shrink if needed
      textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`; // Set to scroll height
    }
  }, [textAreaRef, inputValue]);
  
  return (
    <div className="bg-bg min-h-screen w-screen max-w-full overflow-x-hidden flex flex-col justify-end text-white font-mono break-words text-sm md:text-lg">
        <HamburgerMenu>
          <Link href="/worlds" className="py-3 px-6 rounded-lg hover:bg-backgroundHighlight">
            Go to world selection
          </Link>
          { privileged && 
            <>
            <div onClick={() => setShowEditWorldOverlay(true)} className="py-3 px-6 rounded-lg hover:bg-backgroundHighlight cursor-pointer">
              Edit World Details
            </div>
            <div onClick={() => setShowCreateTemplateOverlay(true)} className="py-3 px-6 rounded-lg hover:bg-backgroundHighlight cursor-pointer">
              Create Template from this World
            </div>
            </>
          }
        </HamburgerMenu>
        {
          showEditWorldOverlay &&
          <Overlay onClose={() => setShowEditWorldOverlay(false)}>
            <EditWorldForm id={worldId} onClose={() => setShowEditWorldOverlay(false)} />
          </Overlay>
        }
        {
          showCreateTemplateOverlay &&
          <Overlay onClose={() => setShowCreateTemplateOverlay(false)}>
            <CreateTemplateForm id={worldId} onClose={() => setShowCreateTemplateOverlay(false)} />
          </Overlay>
        }
        <div
          className="flex-1 px-3 sm:px-6 whitespace-pre-wrap overflow-auto flex"
          ref={scrollRef}
        >
          <div className="grow shrink-0 basis-auto mx-auto w-full max-w-screen-md flex flex-col justify-end" ref={messageListRef}>
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
            <div id="bottom" ref={bottomRef} className="h-2 w-2 bg-pink"></div>
            <div style={{height: textInputContainerRef.current?.clientHeight}}/> {/* Fill height blocked by textInput */}
            <div ref={characterMeasureRef} className="h-0 w-fit overflow-hidden">W</div>
          </div>
        </div>
        <div className="bg-bg fixed bottom-0 w-full p-4f flex justify-center py-4 px-2 text-base" ref={textInputContainerRef}>
          {
            privateInput ? 
            <input 
            type="password"
            style={{resize: "none"}}
            autoFocus
            autoCapitalize="none"
            value={inputValue}
            onChange={(e) => { setInputValue(e.target.value) }}
            className="p-2 border rounded w-full bg-bg max-w-screen-md h-fit max-h-32 sm:max-h-48 md:max-h-96 focus:outline-none"
            // placeholder="Type a message"
            onKeyDown={handleKeyDownInput}
            />
            :
            <textarea 
            rows={1} 
            wrap="on"
            style={{resize: "none"}}
            autoFocus
            autoCapitalize="none"
            value={inputValue}
            onChange={(e) => { setInputValue(e.target.value) }}
            className="p-2 border rounded w-full bg-bg max-w-screen-md h-fit max-h-32 sm:max-h-48 md:max-h-96 overflow-hidden focus:outline-none"
            // placeholder="Type a message"
            onKeyDown={handleKeyDown}
            ref={textAreaRef}
          ></textarea>}

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
