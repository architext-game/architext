import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ClerkProvider } from '@clerk/nextjs'
import { SocketAuthenticator } from "./SocketAuthenticator";
import { dark } from '@clerk/themes'
import { colors } from "../../tailwind.config"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Architext",
  description: "The great text game where YOU ARE THE ARCHITEXT!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider appearance={{
      baseTheme: dark,
      variables: {
        colorBackground: colors.background,
        fontFamily: "mononoki",
        colorInputBackground: colors.background,
        colorNeutral: "#FFFFFF",
      },
      elements: {
        button: 'bg-background hover:bg-backgroundHighlight text-text isolation-auto',
        card: 'border-b border-text isolation-auto overflow-hidden bg-background',
        rootBox: 'border border-text isolation-auto overflow-hidden rounded-lg'
      }
    }}>
      <SocketAuthenticator/>
      <html lang="en" className="">
        <head>
          <link
            rel="icon"
            href="/icon?<generated>"
            type="image/<generated>"
            sizes="<generated>"
          />
        </head>
        <body
          className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
