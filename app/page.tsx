"use client";
import { Pause, Send, TextArea } from "chainfury";
import { useState } from "react";

export interface ChatInterface {
  msg: string;
  attachment_name?: string;
  isSender: boolean;
  sender: string;
  message_id?: string;
}

const faqs = [
  "Question 1?",
  "Question 2?",
  "Question 3?",
  "Question 4?",
  "Question 5?",
  "Question 6?",
];

const scrollToBottom = (force = false) => {
  const chatsHolder = document.querySelector(".chatsHolder");
  if (!chatsHolder) return;
  // check if user is already at the bottom of the chatsHolder
  const isAtBottom =
    chatsHolder.scrollHeight - 40 - chatsHolder.scrollTop <=
    chatsHolder.clientHeight;
  if (chatsHolder && (isAtBottom || force)) {
    chatsHolder.scrollTo({
      top: chatsHolder.scrollHeight,
      behavior: "smooth",
    });
  }
};

export default function Home() {
  const [chats, setChats] = useState<ChatInterface[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);

  return (
    <div className="w-screen h-screen">
      <div className="flex flex-col h-full justify-between max-w-[1100px] mx-auto prose-nbx p-[16px]">
        <div className="chatsHolder w-full flex flex-col gap-[16px] overflow-scroll pb-[16px]">
          {/* messagecard */}
        </div>

        <div className="relative">
          {!chats.length ? (
            <div className="w-full grid pb-[16px] gap-[12px] md:grid-cols-2">
              {faqs?.map((val, id) => (
                <div
                  onClick={() => {
                    setChats((prev) => [
                      ...prev,
                      {
                        msg: val,
                        isSender: true,
                        sender: "You",
                      },
                      {
                        msg: "",
                        isSender: false,
                        sender: "BlitzScaling",
                      },
                    ]);
                  }}
                  key={id}
                  className="revealCardAnimation medium p-[12px] border cursor-pointer rounded-[8px] border-light-border-base dark:border-dark-border-base w-full bg-light-background-surface dark:bg-dark-background-surface hover:bg-light-background-surfaceHover dark:hover:bg-dark-background-surfaceHover"
                >
                  {val}
                </div>
              ))}
            </div>
          ) : (
            ""
          )}
          <TextArea
            value={search}
            onKeyDown={(e) => {
              if (search?.trim() === "") return;
              if (e.key === "Enter" && e.shiftKey) return;
              if (e.key === "Enter" && !loading) {
                e.preventDefault();
                scrollToBottom(true);
                setTimeout(() => {
                  scrollToBottom(true);
                }, 100);
                setChats((prev) => [
                  ...prev,
                  {
                    msg: search,
                    isSender: true,
                    sender: "You",
                  },
                  {
                    msg: "",
                    isSender: false,
                    sender: "BlitzScaling",
                  },
                ]);
              }
            }}
            data-gramm="false"
            data-gramm_editor="false"
            data-enable-grammarly="false"
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Ask anything"
            className="min-h-[40px!important] pb-[8px] pr-[8px] max-h-[200px] outline-none"
            endIcon={
              !loading ? (
                <div className="flex gap-[18px] mb-[8px] w-[100px] relative">
                  <div className="w-[16px]">
                    <Send className="fill-light-icon-base dark:fill-dark-icon-base hover:dark:fill-dark-icon-hover hover:fill-light-icon-hover" />
                  </div>
                </div>
              ) : (
                <div className="w-[16px] flex mb-[8px] items-center text-light-icon-base dark:text-dark-icon-base hover:dark:text-dark-icon-hover hover:text-light-icon-hover">
                  <Pause />
                </div>
              )
            }
            onEndClick={() => {
              if (search?.trim() === "") return;
              if (loading) return;
              scrollToBottom(true);
              setTimeout(() => {
                scrollToBottom(true);
              }, 100);
              setChats((prev) => [
                ...prev,
                {
                  msg: search,
                  isSender: true,
                  sender: "You",
                },
                {
                  msg: "",
                  isSender: false,
                  sender: "BlitzScaling",
                },
              ]);
            }}
          />
          <div className="w-full text-center">
            <span className="text-light-text-base dark:text-dark-text-base mini">
              Powered by <a href="https://chat.tune.app/">TuneChat</a>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
