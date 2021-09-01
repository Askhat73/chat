import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {Observable} from "rxjs";
import {Room} from "../interfaces/room";

@Injectable({
  providedIn: 'root'
})
export class RoomService {

  private roomEndpoint = environment.chatUrl + '/api/v1/rooms/'

  constructor(private http: HttpClient) { }

  getRooms(): Observable<Room[]> {
    return this.http.get<Room[]>(this.roomEndpoint);
  }

  createRoom(name: string): Observable<Room> {
    return this.http.post<Room>(this.roomEndpoint, {name: name});
  }
}
