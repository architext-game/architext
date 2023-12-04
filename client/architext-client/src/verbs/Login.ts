import { Verb } from "./AbstractVerb";

export class Login extends Verb{
  process(message: string): void {
    console.log("patata")
    this.sender.sendToClient("echo of" + message)
  }
}