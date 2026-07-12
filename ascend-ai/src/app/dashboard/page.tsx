"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth.store";
import { authService } from "@/services/auth.service";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function DashboardPage() {
  const { user, authenticated, loading, logout } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !authenticated) {
      router.push("/login");
    }
  }, [loading, authenticated, router]);

  const handleLogout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error("Logout failed", error);
    } finally {
      logout();
      router.push("/login");
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-lg">Loading...</p>
      </div>
    );
  }

  if (!authenticated) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="min-h-screen p-8 max-w-4xl mx-auto space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Button variant="outline" onClick={handleLogout}>
          Sign out
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Welcome, {user?.username}!</CardTitle>
          <CardDescription>Your personal dashboard</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <span className="font-semibold">Email: </span>
            {user?.email}
          </div>
          <div>
            <span className="font-semibold">Role: </span>
            <span className="capitalize">{user?.role || "User"}</span>
          </div>
          <div>
            <span className="font-semibold">User ID: </span>
            <span className="text-sm text-gray-500">{user?.id}</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
