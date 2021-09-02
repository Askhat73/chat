import { Injectable } from '@angular/core';
import {environment} from "../../../environments/environment";
import {Observable} from "rxjs";
import {Message} from "../interfaces/message";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class MessageService {

  private messageEndpoint = environment.chatUrl + '/api/v1/messages/'

  constructor(private http: HttpClient) { }

  getMessages(roomName: string): Observable<Message[]> {
    return this.http.get<Message[]>(this.messageEndpoint + `?room__name=${roomName}`);
  }
}
