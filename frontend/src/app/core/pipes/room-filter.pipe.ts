import { Pipe, PipeTransform } from '@angular/core';
import {Room} from "../interfaces/room";

@Pipe({
  name: 'roomFilterPipe',
  pure: false,
})
export class RoomFilterPipe implements PipeTransform {

  transform(rooms: Room[], roomName: string= ''): Room[] {
    if (!roomName.trim()) {
      return rooms
    }
    return rooms.filter(room => room.name.toLowerCase().includes(roomName.toLowerCase()));
  }

}
