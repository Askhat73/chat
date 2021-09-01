import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private userName: string = ''

  constructor() { }

  getUserName(): string {
    return this.userName;
  }

  setUserName(name: string) {
    this.userName = name.trim();
  }

  isAuthenticated(): boolean {
    return !!this.userName;
  }
}
