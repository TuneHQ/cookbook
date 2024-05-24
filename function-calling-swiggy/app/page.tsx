"use client";

import "chainfury/dist/esm/index.css";
import { Pause, Send, TextArea } from "chainfury";
import { useState, useRef, useEffect } from "react";
import MessageCard from "./components/MessageCard";

const faqs = [
  "Can you suggest me a good restaurant?",
  "What was my last order?",
  "How much I spent on my last 3 orders?",
  "I want to eat something spicy",
];

export interface ChatInterface {
  msg: string;
  attachment_name?: string;
  isSender: boolean;
  sender: string;
  message_id?: string;
}

const safeParse = (str: string) => {
  try {
    return JSON.parse(str);
  } catch (error) {
    return str;
  }
};

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
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [loadingTxt, setLoadingTxt] = useState("");
  const [currentLocation, setCurrentLocation] = useState({
    lat: 12.8400727,
    lon: 80.243273,
  } as {
    lat?: number;
    lon?: number;
  });
  let abortController = useRef(new AbortController());

  const stopGenerating = () => {
    if (abortController?.current?.abort) {
      abortController?.current.abort();
    }
  };

  async function getLocation() {
    if (navigator.geolocation) {
      (await navigator.geolocation.getCurrentPosition((position) => {
        setCurrentLocation({
          lat: position.coords.latitude,
          lon: position.coords.longitude,
        });
      })) as any;
    }
  }

  const handleSearch = async () => {
    try {
      const searchValue = search.trim();
      setSearch("");
      if (loading) return;
      setLoading(true);
      abortController.current = new AbortController();
      abortController.current.signal.addEventListener("abort", () => {
        setLoading(false);
        setAnswer("");
      });
      const url = `/prompt`;

      const response = await fetch(url, {
        method: "POST",
        signal: abortController.current?.signal,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: [
            {
              role: "system",
              content: `You are an very enthsiastic AI bot by TuneHQ. Its important you add information marked as [important].
              Users location is ${currentLocation.lat}, ${currentLocation.lon}.
              Current time is ${new Date().toLocaleTimeString()}.`,
            },
            ...chats?.slice(0, chats.length - 1).map((chat) => {
              return {
                role: chat.isSender ? "user" : "assistant",
                content: chat.msg?.includes("data:image/png;base64")
                  ? "Image Generated"
                  : chat.msg,
              };
            }),
          ],
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

        const { done, value } = chunkReader;
        if (done) {
          break;
        }

        const text = decoder.decode(value);
        const lines = text.trim().split("\n\n\n\n\n\n");

        for (const line of lines) {
          console.log("eventData ->", { line });

          const eventData = safeParse(line);
          if (eventData?.sources) continue;
          if (eventData.error) {
            // if eventData has error
            console.log("error ->", eventData.error);
            setLoading(false);
            // show error
            alert(eventData.error);
            return;
          }
          if (eventData?.type === "text" || eventData?.type === "image") {
            setLoadingTxt("");
            console.log("data ->", eventData.data);
            message = message + eventData.data;
          } else if (eventData?.type !== "bye") {
            setLoadingTxt(eventData.data);
          } else if (eventData?.type === "bye") {
            message = eventData.data;
          } else {
            setLoadingTxt("");
            setLoading(false);
          }

          setAnswer(message);
        }
      }

      setAnswer(message);

      setTimeout(() => {
        setAnswer("");
        setLoading(false);
      }, 700);
    } catch (error) {
      console.log(error);
      setAnswer("");
      setLoading(false);
    }
  };

  useEffect(() => {
    getLocation();
  }, []);

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
    <div className="flex flex-col justify-between max-w-[1100px] mx-auto prose-nbx p-[16px] w-full h-full">
      <div className="chatsHolder w-full flex flex-col gap-[16px] overflow-scroll pb-[32px]">
        {chats?.map((chat, id) => (
          <MessageCard
            chat={chat}
            key={id}
            loading={
              id === chats?.length - 1
                ? !chats?.[chats?.length - 1]?.msg && loading
                : false
            }
            loadingTxt={loadingTxt}
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
                      sender: "Tune",
                    },
                  ]);
                }}
                key={id}
                className="revealCardAnimation medium p-[12px] border cursor-pointer rounded-[8px] border-[#DFE1E6] w-full bg-[#FFFFFF] hover:bg-[#ECEFF3]"
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
              setTimeout(() => {
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
                    sender: "Tune",
                  },
                ]);
              });
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
                sender: "Tune",
              },
            ]);
          }}
        />
        <div className="w-full text-center">
          <span className="text-light-text-base dark:text-dark-text-base mini">
            Powered by <a href="https://studio.tune.app/">TuneStudio</a>
          </span>
        </div>
      </div>
    </div>
  );
}
