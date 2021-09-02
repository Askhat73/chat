import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {ErrorPageComponent} from "./components/error-page/error-page.component";

const routes: Routes = [
  {path: 'room', loadChildren: () => import('./views/room/room.module').then(m => m.RoomModule)},
  {path: '', loadChildren: () => import('./views/home/home.module').then(m => m.HomeModule), pathMatch: 'full'},
  {path: '**', component: ErrorPageComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
