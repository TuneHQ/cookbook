import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehype from "rehype-raw";

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
        {chat?.sender?.charAt(0)}
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

export default MessageCard;
