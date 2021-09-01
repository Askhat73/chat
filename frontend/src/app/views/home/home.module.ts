import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home.component';
import {RouterModule, Routes} from "@angular/router";
import { ChatLobbyComponent } from './chat-lobby/chat-lobby.component';
import {FontAwesomeModule} from "@fortawesome/angular-fontawesome";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {RoomFilterPipe} from "../../core/pipes/room-filter.pipe";

const routes: Routes = [
  {path: '', component: HomeComponent},
]

@NgModule({
  declarations: [
    HomeComponent,
    ChatLobbyComponent,
    RoomFilterPipe
  ],
  imports: [
    CommonModule,
    FontAwesomeModule,
    RouterModule.forChild(routes),
    ReactiveFormsModule,
    FormsModule,
  ]
})
export class HomeModule { }
