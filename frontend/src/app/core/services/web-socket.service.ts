import {Inject, Injectable} from '@angular/core';
import {environment} from "../../../environments/environment";
import {Message} from "../interfaces/message";
import {AuthService} from "./auth.service";
import {MessageService} from "./message.service";


const CHAT_URL = environment.wsUrl + "/ws/chat";

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {

  webSocket!: WebSocket;
  messages: Message[] = []

  constructor(
    @Inject(String) private roomName: string,
    private authService: AuthService,
    private messageService: MessageService,
    ) { }

  public openWebSocket(): void {
    const roomUrl = CHAT_URL + `/${this.roomName}` + `/?user_name=${this.authService.getUserName()}`
    this.webSocket = new WebSocket(roomUrl);

    this.webSocket.onopen = (event: Event) => {
      this.messageService.getMessages(this.roomName).subscribe((messages: Message[]) => {
        this.messages = messages;
      });
    }

    this.webSocket.onmessage = (event: MessageEvent) => {
      const chatMessage = <Message>JSON.parse(event.data);
      this.messages.push(chatMessage);
    }

    this.webSocket.onclose = (event: CloseEvent) => {
      console.log('Close ', event);
    }

  }

  public sendMessage(message: Message): void {
    this.webSocket.send(JSON.stringify(message));
  }

  public closeWebSocket(): void {
    this.webSocket.close();
  }
}
