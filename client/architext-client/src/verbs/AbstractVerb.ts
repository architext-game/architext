abstract class Sender {
  abstract sendToClient(message: string): void;
}

class ChatMessageSender extends Sender {
  private sendFunction: (message: string) => void

  constructor(sendFunction: (message: string) => void){
    super()
    this.sendFunction = sendFunction
  }

  sendToClient(message: string): void {
    this.sendFunction(message)
  }
}

class BadMessage extends Error {
  constructor(message: string) {
      super(message);
      this.name = "Message can't be processed";
  }
}

class MessageHandler{
  private verbs: {
    canProcess: (message: string, inWorld: boolean) => boolean,
    constructor: new (sender: Sender) => Verb
  }[] = [
    { canProcess: Login.canProcess, constructor: Login }
  ]

  private finished = false
  private sender: Sender
  private currentVerb: Verb | null

  constructor(sender: Sender) {
    this.finished = false;
    this.sender = sender;
    this.currentVerb = new Login(sender)
  }

  processMessage(message: string){
    if(this.currentVerb === null){
      const verb = this.verbs.find(v => v.canProcess(message, true))
      if(verb){
        this.currentVerb = new verb.constructor(this.sender)
      }
    }
    if(this.currentVerb !== null){
      try {
        this.currentVerb.process(message)
      } catch(error) {
        console.log(error)
      }
      if(this.currentVerb.commandFinished()){
        this.currentVerb = null
      }
    } else {
      throw BadMessage
    }
  }
}

const FREE = 'free';
const PRIVILEGED = 'privileged';
const CREATOR = 'creator';
const NOBOT = 'nobot';

const LOBBYVERB = 'lobbyverb';
const WORLDVERB = 'worldverb';
const VERSATILE = 'versatile';


export abstract class Verb {
  // This is the template for creating new verbs. Every verb should have Verb as a parent.
  // This is an abstract class, with some methods not implemented.
  //
  // A verb is every action that a user can take in the world. Each verb object processes
  // a fixed set of user messages, and takes all the actions relative to them.
  //
  // Each verb has its own criteria that determines if it can process a given message. This
  // criteria is defined in its canProcess method. The session calls the canProcess method
  // of each verb in its verb list until it finds a verb that can process the message.
  //
  // Then, the session creates a new instance of the verb and lets it process all user messages
  // (via the process method) until the verb instance returns true for its method commandFinished.

  static command = 'verb ';
  static permissions = FREE; // Possible values: FREE, PRIVILEGED, NOBOT, CREATOR.
  static verbtype = WORLDVERB;
  static regexCommand = false; // False: can process if message starts with command. True: command is a regex and can process if message matches the regex.

  private finished: boolean;
  protected sender: Sender;

  constructor(sender: Sender) {
    this.finished = false;
    this.sender = sender;
  }

  static inTheRightContext(inWorld: boolean): boolean {
    if (this.verbtype === WORLDVERB && !inWorld) {
      return false;
    }

    if (this.verbtype === LOBBYVERB && inWorld) {
      return false;
    }

    return true;
  }

  static messageMatchesCommand(message: string): boolean {
    console.log("message", message, "command", this.command)
    if (this.regexCommand) {
      // return util.match(this.command, message) != null;
      return false
    } else {
      if (Array.isArray(this.command)) {
        return this.command.some(command => message.startsWith(command));
      } else {
        return message.startsWith(this.command);
      };
    }
  }

  static canProcess(message: string, inWorld: boolean): boolean {
    console.log("can?")
    return this.inTheRightContext(inWorld) && this.messageMatchesCommand(message);
  }

  abstract process(message: string): void;

  commandFinished(): boolean {
    return this.finished;
  }

  protected finishInteraction(): void {
    // This method must be called from within the Verb when the interaction is finished,
    // so the session can pass command to other verbs
    this.finished = true;
  }
}


export class Login extends Verb{
  process(message: string): void {
    console.log("patata")
    this.sender.sendToClient("echo of" + message)
  }
}
