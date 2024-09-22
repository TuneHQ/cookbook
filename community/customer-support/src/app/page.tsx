"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  Headphones,
  Settings,
  BookOpen,
  MessageSquare,
  Send,
  Menu,
  Plus,
} from "lucide-react";
import { GitHubLogoIcon } from "@radix-ui/react-icons";

type Chat = {
  id: number;
  name: string;
};

type Message = {
  id: number;
  content: string;
  sender: "user" | "assistant";
};

export default function Dashboard() {
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, content: "Hello! How can I help you today?", sender: "assistant" },
    { id: 2, content: "I have a question about your product.", sender: "user" },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [chats, setChats] = useState<Chat[]>([
    { id: 1, name: "Chat 1" },
    { id: 2, name: "Chat 2" },
    { id: 3, name: "Chat 3" },
  ]);
  const [selectedChat, setSelectedChat] = useState(1);

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      setMessages([
        ...messages,
        { id: messages.length + 1, content: inputMessage, sender: "user" },
      ]);
      setInputMessage("");
    }
  };

  const handleCreateNewChat = () => {
    const newChat = { id: chats.length + 1, name: `Chat ${chats.length + 1}` };
    setChats([...chats, newChat]);
    setSelectedChat(newChat.id);
    setMessages([]);
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="bg-primary text-primary-foreground p-4 flex items-center justify-between">
        <div className="flex items-center">
          <Headphones className="h-6 w-6 mr-2" />
          <span className="text-xl font-bold">Customer Support</span>
        </div>
        <Button variant="secondary" size="sm">
          <GitHubLogoIcon className="mr-2 h-4 w-4" />
          Star on GitHub
        </Button>
      </header>

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - hidden on mobile */}
        <aside className="w-64 bg-muted/40 text-secondary-foreground p-4 hidden lg:block">
          <Sidebar
            chats={chats}
            selectedChat={selectedChat}
            setSelectedChat={setSelectedChat}
            handleCreateNewChat={handleCreateNewChat}
          />
        </aside>

        {/* Main container */}
        <main className="flex-1 flex flex-col">
          <div className="bg-background p-4 flex items-center lg:hidden">
            <Sheet open={isSidebarOpen} onOpenChange={setIsSidebarOpen}>
              <SheetTrigger asChild>
                <Button variant="outline" size="icon">
                  <Menu className="h-4 w-4" />
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="w-64">
                <Sidebar
                  chats={chats}
                  selectedChat={selectedChat}
                  setSelectedChat={setSelectedChat}
                  handleCreateNewChat={handleCreateNewChat}
                />
              </SheetContent>
            </Sheet>
          </div>
          <ChatMessages
            messages={messages}
            inputMessage={inputMessage}
            setInputMessage={setInputMessage}
            handleSendMessage={handleSendMessage}
          />
        </main>
      </div>
    </div>
  );
}

function Sidebar({
  chats,
  selectedChat,
  setSelectedChat,
  handleCreateNewChat,
}: Readonly<{
  chats: Chat[];
  selectedChat: number;
  setSelectedChat: (id: number) => void;
  handleCreateNewChat: () => void;
}>) {
  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 mb-2 text-lg font-semibold">Settings</div>
      <Button
        variant="ghost"
        className="justify-start mb-2 text-muted-foreground transition-all hover:text-primary"
      >
        <Settings className="mr-2 h-4 w-4" /> Manage Assistant
      </Button>
      <Button
        variant="ghost"
        className="justify-start mb-2 text-muted-foreground transition-all hover:text-primary"
      >
        <BookOpen className="mr-2 h-4 w-4" /> Manage Knowledge Base
      </Button>
      <div className="px-4 py-2 mb-2 text-lg font-semibold">Manage Chats</div>
      <ScrollArea className="flex-1 px-4">
        {chats.map((chat) => (
          <Button
            key={chat.id}
            variant={selectedChat === chat.id ? "secondary" : "ghost"}
            className="w-full justify-start mb-2 text-muted-foreground transition-all hover:text-primary"
            onClick={() => setSelectedChat(chat.id)}
          >
            <MessageSquare className="mr-2 h-4 w-4" /> {chat.name}
          </Button>
        ))}
      </ScrollArea>
      <Button onClick={handleCreateNewChat} className="m-4">
        <Plus className="mr-2 h-4 w-4" /> Create New Chat
      </Button>
    </div>
  );
}

function ChatMessages({
  messages,
  inputMessage,
  setInputMessage,
  handleSendMessage,
}: Readonly<{
  messages: Message[];
  inputMessage: string;
  setInputMessage: (value: string) => void;
  handleSendMessage: () => void;
}>) {
  return (
    <Card className="flex-1 m-4 p-4 overflow-hidden flex flex-col">
      <ScrollArea className="flex-1 mb-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-4 ${
              message.sender === "user" ? "text-right" : "text-left"
            }`}
          >
            <span
              className={`inline-block p-2 rounded-lg ${
                message.sender === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-secondary text-secondary-foreground"
              }`}
            >
              {message.content}
            </span>
          </div>
        ))}
      </ScrollArea>
      <div className="flex items-center">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 p-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-primary"
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSendMessage();
            }
          }}
        />
        <Button onClick={handleSendMessage} className="rounded-l-none">
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </Card>
  );
}
