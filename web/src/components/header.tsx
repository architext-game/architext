"use client"

import { getMe, GetMeResponse } from "@/architextSDK";
import { useStore } from "@/state";
import { useAuth } from "@clerk/nextjs";
import clsx from "clsx";
import Link from "next/link";
import { useEffect, useState } from "react";

interface HeaderProps {
  className?: string
}

export function Header({ className }: HeaderProps) {
  const auth = useAuth();
  const socket = useStore((state) => state.socket);
  const authenticated = useStore((state) => state.authenticated);

  const [me, setMe] = useState<GetMeResponse>();
  const [dropdownVisible, setDropdownVisible] = useState(false);

  useEffect(() => {
    if (authenticated) {
      getMe(socket, {}).then(response => {
        setMe(response);
      });
    }
  }, [authenticated]);

  const toggleDropdown = () => setDropdownVisible(!dropdownVisible);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (!(event.target as HTMLElement).closest("#user-dropdown")) {
        setDropdownVisible(false);
      }
    };
    document.addEventListener("click", handleOutsideClick);
    return () => document.removeEventListener("click", handleOutsideClick);
  }, []);

  return (
    <div className={clsx(className, "flex flex-row font-mono gap-10 justify-start w-full pb-11 pt-9 relative")}>
      <h1 className="font-mono text-5xl hover:underline">
        <Link href="/">Architext</Link>
      </h1>
      <Link href="/worlds" className="text-lg hover:underline">
        Play
      </Link>
      {auth.isSignedIn ? (
        <div className="relative" id="user-dropdown">
          <button
            onClick={toggleDropdown}
            className="text-lg hover:underline"
          >
            {me?.data?.name}
          </button>
          {dropdownVisible && (
            <div className="absolute top-10 left-0 bg-bg border border-gray-200 rounded-md shadow-lg py-2 w-40 z-50">
              <button
                onClick={() => auth.signOut()}
                className="block w-full text-left px-4 py-2 hover:bg-backgroundHighlight"
              >
                Sign out
              </button>
            </div>
          )}
        </div>
      ) : (
        <Link href="/login" className="text-lg hover:underline">
          Sign in
        </Link>
      )}
    </div>
  );
}
