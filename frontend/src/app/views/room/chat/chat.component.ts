import {Component, OnDestroy, OnInit} from '@angular/core';
import {faPaperPlane} from "@fortawesome/free-solid-svg-icons";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {AuthService} from "../../../core/services/auth.service";
import {ActivatedRoute, Params} from "@angular/router";
import {WebSocketService} from "../../../core/services/web-socket.service";
import {MessageService} from "../../../core/services/message.service";
import {MessageType} from "../../../core/enums/chat";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
})
export class ChatComponent implements OnInit, OnDestroy {

  faPaperPlane = faPaperPlane
  messageForm = new FormGroup({
    message: new FormControl('', [Validators.required, Validators.nullValidator]),
  })
  public webSocketService?: WebSocketService;

  constructor(
    public authService: AuthService,
    private route: ActivatedRoute,
    private messageService: MessageService,
  ) { }

  ngOnInit(): void {
    this.openWebSocket();
  }

  ngOnDestroy(): void {
    this.webSocketService?.closeWebSocket();
  }

  openWebSocket(): void {
    this.route.params.subscribe((params: Params) => {
      this.webSocketService = new WebSocketService(params.name, this.authService, this.messageService);
      this.webSocketService.openWebSocket();
    });
    console.log(this.webSocketService?.messages)
  }

  sendMessage() {
    const message = this.messageForm.get('message')
    if (!message?.invalid) {
      this.webSocketService?.sendMessage({text: message?.value, user_name: this.authService.getUserName()});
      this.messageForm.reset();
    }
  }

  get messageType(): typeof MessageType {
    return MessageType
  }
}
