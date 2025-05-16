"use client"

import { getMe, GetMeResponse } from "@/architextSDK";
import { useStore } from "@/state";
import { useAuth } from "@clerk/nextjs";
import clsx from "clsx";
import Link from "next/link";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface HeaderProps {
  className?: string;
}

export function Header({ className }: HeaderProps) {
  const auth = useAuth();
  const socket = useStore((state) => state.socket);
  const authenticated = useStore((state) => state.authenticated);

  const [me, setMe] = useState<GetMeResponse>();
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (authenticated) {
      getMe(socket, {}).then(response => {
        setMe(response);
      });
    }
  }, [authenticated]);

  const toggleDropdown = () => setDropdownVisible(!dropdownVisible);
  const toggleMenu = () => setMenuOpen(prev => !prev);

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
    <header className={clsx(className, "w-full pt-4 font-mono relative")}>
      <div className="max-w-screen-lg mx-auto flex flex-col sm:flex-row gap-4 sm:gap-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl sm:text-5xl hover:underline">
            <Link href="/">Architext</Link>
          </h1>
          <button
            onClick={toggleMenu}
            className="sm:hidden text-3xl focus:outline-none"
            aria-label="Toggle menu"
          >
            {menuOpen ? "✕" : "☰"}
          </button>
        </div>

        <AnimatePresence>
          {menuOpen && (
            <motion.nav
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3, ease: "easeInOut" }}
              className="flex flex-col space-y-4 sm:flex-row items-start text-lg sm:hidden"
            >
              <Link href="/worlds" className="hover:underline">
                Play
              </Link>

              {auth.isSignedIn ? (
                <div className="relative" id="user-dropdown">
                  <button onClick={toggleDropdown} className="hover:underline">
                    {me?.data?.name}
                  </button>
                  {dropdownVisible && (
                    <div className="absolute top-full mt-2 left-0 bg-bg border border-gray-200 rounded-md shadow-lg py-2 w-40 z-50">
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
                <div><Link href="/signup" className="hover:underline">
                  Sign up
                </Link>
                </div>
              )}
            </motion.nav>
          )}
        </AnimatePresence>

        {/* Menú siempre visible en escritorio */}
        <nav className="hidden sm:flex sm:gap-6 items-start text-lg">
          <Link href="/worlds" className="hover:underline">
            Play
          </Link>
          {auth.isSignedIn ? (
            <div className="relative" id="user-dropdown">
              <button onClick={toggleDropdown} className="hover:underline">
                {me?.data?.name}
              </button>
              {dropdownVisible && (
                <div className="absolute top-full mt-2 left-0 bg-bg border border-gray-200 rounded-md shadow-lg py-2 w-40 z-50">
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
            <Link href="/login" className="hover:underline">
              Sign in
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}
