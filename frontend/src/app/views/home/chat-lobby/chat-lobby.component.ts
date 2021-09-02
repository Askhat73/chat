import { Component, OnInit } from '@angular/core';
import {faCheck, faSpinner} from '@fortawesome/free-solid-svg-icons';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {Room} from "../../../core/interfaces/room";
import {RoomService} from "../../../core/services/room.service";
import {AuthService} from "../../../core/services/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-chat-lobby',
  templateUrl: './chat-lobby.component.html',
  styleUrls: ['./chat-lobby.component.scss']
})
export class ChatLobbyComponent implements OnInit {

  faSpinner = faSpinner;
  faCheck = faCheck;
  createRoomForm = new FormGroup({
    roomName: new FormControl('', [Validators.required, Validators.pattern('^[A-Za-z0-9_]+$')]),
  });
  userName: string = '';
  roomSearch: string = '';
  rooms: Room[] = [];
  loading = false;
  creatingRoom = false;

  constructor(
    private roomService: RoomService,
    private authService: AuthService,
    private router: Router,
    ) { }

  ngOnInit(): void {
    this.refreshRooms();
  }

  createRoom() {
    const roomName = this.createRoomForm.get('roomName');
    console.log(roomName);
    if(!this.createRoomForm.invalid && roomName?.value.trim()) {
      this.creatingRoom = true;
      this.roomService.createRoom(roomName?.value.trim()).subscribe((room: Room) => {
        this.createRoomForm.reset();
        this.rooms.push(room);
        this.creatingRoom = false;
      }, error => {
        this.creatingRoom = false;
      })
    }
  }

  refreshRooms() {
    this.loading = true;
    this.roomService.getRooms().subscribe((rooms: Room[]) => {
      this.loading = false;
      this.rooms = rooms;
    }, error => {
      this.loading = false;
    })
  }

  enterToRoom(name: string) {
    if(this.userName.trim()) {
      this.authService.setUserName(this.userName.trim());
      this.router.navigate(['/room', name]);
    }
  }
}
