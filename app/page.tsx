"use client";
import { useEffect, useRef, useState } from "react";
import { Send, TextArea } from "chainfury";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehype from "rehype-raw";
import Sidebar from "@/components/sidebar";
import axios from "axios";
const {
  uniqueNamesGenerator,
  adjectives,
  colors,
  animals,
} = require("unique-names-generator");

export interface ChatInterface {
  role: string;
  content?: string;
  isSender?: boolean;
  sender?: string;
}

export interface ModelInterface {
  id: number;
  name: string;
  can_modify: boolean;
  is_running: boolean;
  config?: any;
  nbx_key?: string;
  deployment_id?: string;
  model_id?: string;
  is_shared?: boolean;
  provider?: string;
}

const scrollToBottom = (force = false) => {
  const chatsHolder = document.querySelector(".chatsHolder");
  if (!chatsHolder) return;
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

const faqs = [
  "Explore today's top news stories",
  "How to build resume?",
  "What led to the extinction of dinosaurs?",
  "Generate LinkedIn content ideas on financial markets",
];

export default function Home() {
  const [chats, setChats] = useState<ChatInterface[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [threadListLoader, setThreadListLoader] = useState(false);
  const [threadList, setThreadList] = useState([] as any[]);
  const [threadID, setThreadID] = useState("");

  useEffect(() => {
    getThreadList();
  }, []);

  useEffect(() => {
    if (!threadID) return;
    setThreadListLoader(true);
    axios
      .get("/api/chats?threadID=" + threadID)
      .then((res) => {
        if (res?.data?.success === false) return alert(res?.data?.data);
        setChats(res?.data?.data ?? []);
      })
      .catch((err: any) => {
        console.log(err);
      })
      .finally(() => setThreadListLoader(false));
  }, [threadID]);

  function getThreadList() {
    setThreadListLoader(true);
    axios
      .get("/api/listThreads")
      .then((res) => {
        if (res?.data?.success === false)
          return alert("Failed to fetch thread list");
        setThreadList(res?.data?.data ?? []);
      })
      .finally(() => setThreadListLoader(false));
  }

  function createthreadID() {
    if (!threadID) {
      const randomName = uniqueNamesGenerator({
        dictionaries: [adjectives, colors, animals],
        separator: " ",
      });
      axios
        .post("/api/threadID", {
          title: randomName,
        })
        .then((res) => {
          setThreadID(res.data?.data?.id);
          handleSearch(res.data?.data?.id);
          getThreadList();
        })
        .catch((err: any) => {
          console.log(err);
        });
    }
  }

  const handleSearch = async (id: string) => {
    setLoading(true);
    if (id === "" && !threadID) {
      await createthreadID();
      return;
    }
    const searchValue = search.trim();
    setSearch("");

    const response = await axios
      .post(
        "/api/chats",
        {
          threadID: id,
          content: searchValue,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .catch((err: any) => {
        console.log(err);
      })
      .then((res: any) => {
        console.log(res);
        setChats(res?.data?.data ?? []);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="w-screen h-screen flex prose-nbx">
      <div className="fixed top-[0px] border-b-[1px] bg-light-background-interactive dark:bg-dark-background-interactive border-light-border-base dark:border-dark-border-base py-[8px] w-full m-auto ">
        <span className="medium font-[600] text-light-text-onColorr dark:text-dark-text-onColorr text-center flex justify-center items-center">
          {threadList
            ?.find((thread) => thread.id === threadID)
            ?.title.charAt(0)
            .toUpperCase() +
            threadList
              ?.find((thread) => thread.id === threadID)
              ?.title.slice(1) || "ChatApp"}
        </span>
      </div>
      <div className="h-full">
        <Sidebar
          loading={loading}
          threadListLoader={threadListLoader}
          threadList={threadList}
          threadID={threadID}
          setThreadID={setThreadID}
          setChats={setChats}
        />
      </div>
      <div className="w-full h-full flex flex-col pb-[16px] pt-[66px] px-[36px] justify-between  mx-auto">
        <div className="chatsHolder w-full flex flex-col gap-[16px] overflow-scroll pb-[16px]">
          {chats?.map((chat, id) => (
            <MessageCard
              chat={chat}
              key={id}
              loading={
                id === chats?.length - 1
                  ? !chats?.[chats?.length - 1]?.content && loading
                  : false
              }
            />
          ))}
        </div>

        <div className="relative">
          {!chats.length ? (
            <div className="w-full grid pb-[16px] gap-[12px] md:grid-cols-2">
              {faqs?.map((val, id) => (
                <div
                  onClick={() => {
                    setSearch(val);
                    setThreadID("");
                    setChats([]);
                    handleSearch("");
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
                setChats((prev) => [
                  ...prev,
                  {
                    role: "user",
                    content: search,
                    isSender: true,
                    sender: "You",
                  },
                  {
                    role: "assistant",
                    content: "",
                    isSender: false,
                    sender: "TuneStudio",
                  },
                ]);
                scrollToBottom(true);
                handleSearch(threadID);
              }
            }}
            data-gramm="false"
            data-gramm_editor="false"
            data-enable-grammarly="false"
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Ask anything"
            className="min-h-[40px!important] pb-[8px] max-h-[200px] outline-none"
            endIcon={
              <div className="flex gap-[18px] mb-[8px] right-[10px] w-[100px] relative">
                <div
                  className={`w-[16px] ${
                    loading || search?.trim() === ""
                      ? "cursor-not-allowed"
                      : "cursor-pointer"
                  }`}
                  onClick={() => {
                    if (loading || search?.trim() === "") return;
                    setChats((prev) => [...prev]);
                    scrollToBottom(true);
                    handleSearch(threadID);
                  }}
                >
                  <Send className="fill-light-icon-base dark:fill-dark-icon-base hover:dark:fill-dark-icon-hover hover:fill-light-icon-hover" />
                </div>
              </div>
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
                  role: "user",
                  content: search,
                  isSender: true,
                  sender: "You",
                },
                {
                  role: "assistant",
                  content: "",
                  isSender: false,
                  sender: "TuneStudio",
                },
              ]);
            }}
          />
          <div className="w-full text-center">
            <span className="text-light-text-base dark:text-dark-text-base mini">
              Powered by <a href="https://studio.rc.tune.app/">TuneStudio</a>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

const MessageCard = ({
  chat,
  loading,
}: {
  chat: ChatInterface;
  loading: boolean;
}) => {
  return (
    <div className="flex gap-[16px] w-full">
      <div className="h-[30px] w-[30px] flex justify-center items-center rounded-full bg-light-background-surfaceHighHover dark:bg-dark-background-surfaceHighHover">
        <div
          className={`min-w-[38px] ${
            chat?.role === "assistant"
              ? "bg-[#FF6A1F]"
              : "bg-light-background-interactive dark:bg-dark-background-interactive"
          }  medium-pl h-[38px] w-[38px] scale-[0.67] flex rounded-full`}
          style={{ background: "#FF6A1F" }}
        ></div>
      </div>
      <div className="p-[8px] rounded-md w-full bg-light-background-surfaceLow dark:bg-dark-background-surfaceHigh flex flex-col">
        <span className="mini text-light-text-subtle dark:text-dark-text-subtle ">
          {chat?.role}
        </span>
        {!loading ? (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehype]}
            className={`markdownHolder`}
            components={{
              table: (props: any) => (
                <div className="overflow-x-auto w-full">
                  <table {...props} className="table-auto w-full" />
                </div>
              ),
            }}
          >
            {chat.content}
          </ReactMarkdown>
        ) : (
          <div className="h-[16px] w-[2px] bg-light-text-subtle dark:bg-dark-text-subtle animate-pulse"></div>
        )}
      </div>
    </div>
  );
};
