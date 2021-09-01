import { Component, OnInit } from '@angular/core';
import {faPaperPlane} from "@fortawesome/free-solid-svg-icons";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {ChatService} from "../../../core/services/chat.service";
import {Message} from "../../../core/interfaces/message";
import {AuthService} from "../../../core/services/auth.service";
import {ActivatedRoute, Params} from "@angular/router";
import {WebsocketService} from "../../../core/services/websocket.service";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit {

  messages: Message[] = []
  faPaperPlane = faPaperPlane
  messageForm = new FormGroup({
    message: new FormControl('', [Validators.required, Validators.nullValidator]),
  })
  private chatService?: ChatService;

  constructor(
    public authService: AuthService,
    private websocketService: WebsocketService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe((params: Params) => {
      this.chatService = new ChatService(params.name, this.websocketService, this.authService)
      this.chatService.messages$.subscribe((message: Message) => {
        this.messages.push(message);
        console.log(message);
      }, error => {
        console.log(error);
      });
    })
  }

  sendMessage() {
    const message = this.messageForm.get('message')
    if (!message?.invalid) {
      this.chatService?.messages$.next({text: message?.value, user_name: this.authService.getUserName()});
      this.messageForm.reset();
    }
  }
}
