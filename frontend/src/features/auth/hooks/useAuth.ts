import { useCallback, useEffect, useState } from "react";
import * as authApi from "../api/api";

export function useAuth() {
  const [user, setUser] = useState<authApi.MeResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const u = await authApi.me();
      setUser(u);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const signIn = useCallback(async (email: string, password: string) => {
    await authApi.login(email, password);
    await refresh();
  }, [refresh]);

  const signOut = useCallback(async () => {
    await authApi.logout();
    setUser(null);
  }, []);

  return { user, loading, signIn, signOut, refresh };
}