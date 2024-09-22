import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehype from "rehype-raw";
import { ChatInterface } from "../page";

const MessageCard = ({
  chat,
  loading,
  loadingTxt,
}: {
  chat: ChatInterface;
  loading: boolean;
  loadingTxt?: string;
}) => {
  return (
    <div className="flex gap-[16px] w-full prose-nbx">
      <div
        className={`${
          chat?.isSender ? "bg-[#ECEFF3]" : "bg-[#FF6A1F]"
        } h-[30px] w-[30px] flex justify-center items-center rounded-full medium`}
      >
        {chat?.isSender ? chat?.sender?.charAt(0) : ""}
      </div>
      <div className="p-[8px] rounded-md w-full bg-[#f3f3f3] flex flex-col">
        <span className="mini text-[#808897] ">{chat?.sender}</span>
        {loadingTxt && loading ? (
          <div className="bg-[#fff] px-[8px] py-[2px] rounded-md w-fit mini-pl flex gap-[6px] items-center my-[2px]">
            <svg
              height={24}
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 200 200"
            >
              <circle
                cx="100"
                cy="100"
                r="0"
                fill="none"
                stroke="#FF6A1F"
                strokeWidth="0.5"
              >
                <animate
                  attributeName="r"
                  calcMode="spline"
                  dur="2"
                  keySplines="0 .2 .5 1"
                  keyTimes="0;1"
                  repeatCount="indefinite"
                  values="1;80"
                ></animate>
                <animate
                  attributeName="stroke-width"
                  calcMode="spline"
                  dur="2"
                  keySplines="0 .2 .5 1"
                  keyTimes="0;1"
                  repeatCount="indefinite"
                  values="0;25"
                ></animate>
                <animate
                  attributeName="stroke-opacity"
                  calcMode="spline"
                  dur="2"
                  keySplines="0 .2 .5 1"
                  keyTimes="0;1"
                  repeatCount="indefinite"
                  values="1;0"
                ></animate>
              </circle>
            </svg>
            {loadingTxt}
          </div>
        ) : (
          ""
        )}
        {!loading ? (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehype]}
            className={`markdownHolder`}
            urlTransform={(value: string) => value}
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
          <div className="h-[16px] w-[2px] bg-[#808897] animate-pulse"></div>
        )}
      </div>
    </div>
  );
};

export default MessageCard;
