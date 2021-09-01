import { NgModule } from '@angular/core';
import {CommonModule} from '@angular/common';
import { RoomComponent } from './room.component';
import {RouterModule, Routes} from "@angular/router";
import {FontAwesomeModule} from "@fortawesome/angular-fontawesome";
import { ChatComponent } from './chat/chat.component';
import {ReactiveFormsModule} from "@angular/forms";
import {AuthGuard} from "../../core/services/auth.guard";


const routes: Routes = [
  {path: ':name', component: RoomComponent, canActivate: [AuthGuard]},
]

@NgModule({
  declarations: [
    RoomComponent,
    ChatComponent,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FontAwesomeModule,
    ReactiveFormsModule,
  ]
})
export class RoomModule { }
