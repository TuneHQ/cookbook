"use client";
import { useEffect, useRef, useState } from "react";
import { Pause, Send, TextArea } from "chainfury";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehype from "rehype-raw";
import Sidebar from "@/components/sidebar";
export interface ChatInterface {
  msg: string;
  attachment_name?: string;
  isSender: boolean;
  sender: string;
  message_id?: string;
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

const faqs = [
  "Question 1?",
  "Question 2?",
  "Question 3?",
  "Question 4?",
  "Question 5?",
  "Question 6?",
];

export default function Home() {
  const [chats, setChats] = useState<ChatInterface[]>([]);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  let abortController = useRef(new AbortController());

  const stopGenerating = () => {
    if (abortController?.current?.abort) {
      abortController?.current.abort();
    }
  };

  const handleSearch = async () => {
    const searchValue = search.trim();
    setSearch("");
    if (loading) return;
    setLoading(true);
    abortController.current = new AbortController();
    abortController.current.signal.addEventListener("abort", () => {
      setLoading(false);
      setAnswer("");
    });
    // const url = `${}`;

    const response = await fetch("", {
      method: "POST",
      signal: abortController.current?.signal,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: "/blitz " + searchValue,
      }),
    });
    if (!response.ok) {
      alert("Something went wrong, please try again later.");
      setLoading(false);
      return;
    }
    if (!response?.headers?.get("content-type")) {
      const text = await response.text();
      setAnswer(text);
      setLoading(false);
      setTimeout(() => {
        setAnswer("");
      }, 10000);
      return;
    }

    const reader = response?.body?.getReader();
    let decoder = new TextDecoder();

    let message = "";
    while (true && reader) {
      const chunkReader = await reader.read();
      console.log({ chunkReader });
      const { done, value } = chunkReader;
      if (done) {
        break;
      }

      const text = decoder.decode(value);
      const lines = text.trim().split("\n\n\n\n\n");

      for (const line of lines) {
        const eventData = JSON.parse(line);
        if (eventData?.sources) continue;
        if (eventData.error) {
          // if eventData has error
          console.log("error ->", eventData.error);
          setLoading(false);
          // show error
          alert(eventData.error);
          return;
        }
        message = message + eventData.value;
        setAnswer(message);
      }
    }
    setAnswer(message);

    setLoading(false);
    setTimeout(() => {
      setAnswer("");
    });
  };

  useEffect(() => {
    if (
      !chats[chats.length - 1]?.isSender &&
      chats[chats.length - 1]?.msg === ""
    )
      handleSearch();
  }, [chats]);

  useEffect(() => {
    scrollToBottom();
    if (answer !== "" && chats.length) {
      let tempChats = [...chats];
      tempChats[tempChats.length - 1].msg = answer;
      setChats(tempChats);
    }
  }, [answer, loading]);
  return (
    <div className="w-screen h-screen flex prose-nbx">
      <div className="fixed top-[0px] border-b-[1px] bg-light-background-interactive dark:bg-dark-background-interactive border-light-border-base dark:border-dark-border-base py-[8px] w-full m-auto ">
        <span className="medium font-[600] text-light-text-onColorr dark:text-dark-text-onColorr text-center flex justify-center items-center">
          headingnwkfjnkjehjkfhgkj
        </span>
      </div>
      <div className=" h-full ">
        <Sidebar />
      </div>
      <div className="w-full h-full flex flex-col pb-[16px] pt-[66px] px-[36px] justify-between  mx-auto">
        <div className="chatsHolder w-full flex flex-col gap-[16px] overflow-scroll pb-[16px]">
          {chats?.map((chat, id) => (
            <MessageCard
              chat={chat}
              key={id}
              loading={
                id === chats?.length - 1
                  ? !chats?.[chats?.length - 1]?.msg && loading
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
                        sender: "TuneStudio",
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
                    sender: "TuneStudio",
                  },
                ]);
              }
            }}
            data-gramm="false"
            data-gramm_editor="false"
            data-enable-grammarly="false"
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Ask anything"
            className="min-h-[40px!important] pb-[8px] max-h-[200px] outline-none"
            endIcon={
              !loading ? (
                <div className="flex gap-[18px] mb-[8px] right-[10px] w-[100px] relative">
                  <div className="w-[16px]">
                    <Send className="fill-light-icon-base dark:fill-dark-icon-base hover:dark:fill-dark-icon-hover hover:fill-light-icon-hover" />
                  </div>
                </div>
              ) : (
                <div
                  onClick={() => stopGenerating()}
                  className="w-[16px] flex mb-[8px] items-center text-light-icon-base dark:text-dark-icon-base hover:dark:text-dark-icon-hover hover:text-light-icon-hover"
                >
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
          className="min-w-[38px] bg-[#FF6A1F] medium-pl h-[38px] w-[38px] scale-[0.67] flex rounded-full"
          style={{ background: "#FF6A1F" }}
        ></div>
      </div>
      <div className="p-[8px] rounded-md w-full bg-light-background-surfaceLow dark:bg-dark-background-surfaceHigh flex flex-col">
        <span className="mini text-light-text-subtle dark:text-dark-text-subtle ">
          {chat?.sender}
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
            {chat.msg}
          </ReactMarkdown>
        ) : (
          <div className="h-[16px] w-[2px] bg-light-text-subtle dark:bg-dark-text-subtle animate-pulse"></div>
        )}
      </div>
    </div>
  );
};
