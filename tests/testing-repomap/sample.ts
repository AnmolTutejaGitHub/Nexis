import { Request, Response } from "express";

interface User {
  id: number;
  name: string;
  email: string;
}

class AuthService {
  private secret: string;

  constructor(secret: string) {
    this.secret = secret;
  }

  login(email: string, password: string): string {
    return "token";
  }

  logout(token: string): void {}
}

function validateEmail(email: string): boolean {
  return email.includes("@");
}

const formatDate = (date: Date): string => {
  return date.toISOString();
};
