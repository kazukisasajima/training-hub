import { createContext } from "react";
import * as authApi from "../api/api";

export type AuthContextType = {
  user: authApi.MeResponse | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  refresh: () => Promise<void>;
};

export const AuthContext = createContext<AuthContextType | null>(null);