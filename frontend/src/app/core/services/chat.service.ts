import {Inject, Injectable} from '@angular/core';
import {Subject} from "rxjs";
import {Message} from "../interfaces/message";
import {WebsocketService} from "./websocket.service";
import {map} from "rxjs/operators";
import {AuthService} from "./auth.service";
import {environment} from "../../../environments/environment";

const CHAT_URL = environment.wsUrl + "/ws/chat";

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  public messages$!: Subject<Message>;

  constructor(
    @Inject(String) private roomName: string,
    private websocketService: WebsocketService,
    private authService: AuthService,
    ) {
    if(this.authService.isAuthenticated()) {
      const roomUrl = CHAT_URL + `/${this.roomName}` + `/?user_name=${this.authService.getUserName()}`
      this.messages$ = <Subject<Message>>websocketService.connect(roomUrl).pipe(
        map((response: MessageEvent): Message => {
          const data = JSON.parse(response.data);
          return {
            user_name: data.user_name,
            text: data.text,
            created_at: new Date(data.created_at),
            type: data.type,
          };
        })
      );
    }
  }

  setRoomName(name: string) {
    this.roomName = name;
  }
}
