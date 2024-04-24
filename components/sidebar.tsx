import SvgPlus from "chainfury/dist/esm/Icons/Plus";

import ChatList from "@/app/Svgcomps/ChatList";
import { useRouter } from "next/navigation";

const Sidebar = ({
  threadList,
  threadListLoader,
  threadID,
  setThreadID,
  setChats,
}: {
  threadList: any[];
  threadListLoader: boolean;
  threadID: string;
  setThreadID: (threadID: string) => void;
  setChats: (chats: any[]) => void;
}) => {
  const router = useRouter();
  return (
    <div className="w-[240px] min-w-[240px] h-full border-r border-light-border-base dark:border-dark-border-base pb-[16px] pt-[66px] px-[14px] flex flex-col gap-[8px] ">
      <button
        className="flex items-center primaryBtn p-[8px] text-left w-full rounded-md small font-[600]"
        onClick={() => {
          setThreadID("");
          setChats([]);
        }}
      >
        <SvgPlus className="w-[16px] h-[16px] mr-[8px] fill-light-icon-onColor dark:fill-dark-icon-onColor" />
        New Chat
      </button>
      <div className="w-full flex xmini-pl items-center gap-[12px] text-light-text-subtle dark:text-dark-text-subtle whitespace-nowrap mt-[24px] mb-[8px]">
        RECENT CHATS
        <div className="h-px w-full bg-light-neutral-700 dark:bg-dark-neutral-700"></div>
      </div>
      <div className="w-full h-full overflow-scroll flex flex-col gap-[8px]">
        {threadList.map((thread, index) => (
          <div
            key={index}
            className="flex items-center gap-[4px] cursor-pointer hover:bg-light-background-appHover hover:dark:bg-dark-background-appHover w-full px-[10px] py-[4px] rounded-md overflow-hidden text-ellipsis whitespace-nowrap"
            onClick={() => setThreadID(thread.id)}
          >
            <ChatList
              className={`iconBase min-w-[16px] ${
                threadListLoader ? "cursor-not-allowed" : "cursor-pointer"
              }`}
            />
            <span className="medium textMuted">
              {thread?.title.charAt(0).toUpperCase()}
              {thread?.title.slice(1)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
