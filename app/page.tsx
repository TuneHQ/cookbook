"use client";
import { TextArea } from "chainfury";

export default function Home() {
  return (
    <div className="w-screen h-screen">
      <div className="flex flex-col h-full justify-between max-w-[1100px] mx-auto prose-nbx p-[16px]">
        <div className="chatsHolder w-full flex flex-col gap-[16px] overflow-scroll pb-[16px]"></div>

        <div className="relative ">
          <TextArea
            data-gramm="false"
            data-gramm_editor="false"
            data-enable-grammarly="false"
            placeholder="Ask anything"
            className="min-h-[40px!important] pb-[8px] pr-[8px] max-h-[200px] outline-none border-[1px] border-light-text-base "
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
