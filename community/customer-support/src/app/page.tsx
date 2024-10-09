"use client";

import { useEffect, useState } from "react";
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
  Loader,
} from "lucide-react";
import { GitHubLogoIcon } from "@radix-ui/react-icons";
import { Message, Thread } from "@/lib/types";

export default function Dashboard() {
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, content: "Hello! How can I help you today?", sender: "assistant" },
    { id: 2, content: "I have a question about your product.", sender: "user" },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [threads, setThreads] = useState<Thread[]>([]);
  const [selectedThread, setSelectedThread] = useState(1);
  const [threadListLoader, setThreadListLoader] = useState(false);

  useEffect(() => {
    setThreadListLoader(true);
    // Fetch threads
    fetch("/api/threads")
      .then((res) => res.json())
      .then((data) => {
        if (data.status) {
          setThreads(data.data);
        } else {
          alert(data.message);
        }
      })
      .finally(() => setThreadListLoader(false));
  }, []);

  useEffect(() => {
    if (!selectedThread) return;
    setThreadListLoader(true);
    fetch(`/api/threads/${selectedThread}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.status) {
          setMessages(data.data.messages);
        } else {
          alert(data.message);
        }
      })
      .finally(() => setThreadListLoader(false));
  }, [selectedThread]);

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
    const newThread = {
      id: threads.length + 1,
      title: `Chat ${threads.length + 1}`,
      createdAt: new Date().toLocaleString(),
    };
    setThreads([...threads, newThread]);
    setSelectedThread(newThread.id);
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
            threads={threads}
            selectedThread={selectedThread}
            setSelectedThread={setSelectedThread}
            handleCreateNewChat={handleCreateNewChat}
            threadListLoader={threadListLoader}
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
                  threads={threads}
                  selectedThread={selectedThread}
                  setSelectedThread={setSelectedThread}
                  handleCreateNewChat={handleCreateNewChat}
                  threadListLoader={threadListLoader}
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
  threads,
  selectedThread,
  setSelectedThread,
  handleCreateNewChat,
  threadListLoader,
}: Readonly<{
  threads: Thread[];
  selectedThread: number;
  setSelectedThread: (id: number) => void;
  handleCreateNewChat: () => void;
  threadListLoader: boolean;
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
      <div className="px-4 py-2 mb-2 text-lg font-semibold">Manage threads</div>
      {threadListLoader ? (
        <div className="flex-1 flex items-center justify-center">
          <Loader className="animate-spin h-8 w-8 text-primary" />
        </div>
      ) : (
        <ScrollArea className="flex-1 px-4">
          {threads.map((thread) => (
            <Button
              key={thread.id}
              variant={selectedThread === thread.id ? "secondary" : "ghost"}
              className="w-full justify-start mb-2 text-muted-foreground transition-all hover:text-primary"
              onClick={() => setSelectedThread(thread.id)}
            >
              <MessageSquare className="mr-2 h-4 w-4" /> {thread.title}
            </Button>
          ))}
        </ScrollArea>
      )}
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
