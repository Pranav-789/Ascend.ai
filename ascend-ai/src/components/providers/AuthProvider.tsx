"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/store/auth.store";
import { userService } from "@/services/user.service";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { setUser, setLoading } = useAuthStore();

  useEffect(() => {
    const initAuth = async () => {
      try {
        const user = await userService.me();
        setUser(user);
      } catch (error) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, [setUser, setLoading]);

  return <>{children}</>;
}
