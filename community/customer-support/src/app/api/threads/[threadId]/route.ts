import { getErrorMessage } from "@/lib/utils";

export async function POST(request: Request) {
  try {
    const { threadId, content } = await request.json();

    const first = await fetch(
      `https://studio.tune.app/v1/threads/${threadId}/messages`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-tune-key": process.env.TUNE_API_KEY!,
        },
        body: JSON.stringify({
          assistantId: "",
          content,
          fileIds: [],
          role: "user",
          runId: "",
          threadId: threadId,
        }),
      }
    );
    console.log("first", first);

    const second = await fetch(
      `https://studio.tune.app/v1/threads/${threadId}/runs`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-tune-key": process.env.TUNE_API_KEY!,
        },
        body: JSON.stringify({
          model: process.env.TUNE_MODEL,
          threadId: threadId,
        }),
      }
    );
    console.log("second", second);

    const messagesData = await getMessages(threadId);
    const messages = filterMessages(messagesData.data);

    return Response.json({
      success: true,
      data: messages,
    });
  } catch (error) {
    return Response.json({
      status: false,
      message: `Error posting message: ${getErrorMessage(error)}`,
    });
  }
}

export async function GET(
  request: Request,
  { params: { threadId } }: { params: { threadId: string } }
) {
  try {
    if (!threadId) throw "Thread ID is missing";

    const resp = await getMessages(threadId);

    return Response.json({
      success: resp?.data ? true : false,
      data: filterMessages(resp.data),
    });
  } catch (error) {
    return Response.json({
      status: false,
      message: `Error getting messages: ${getErrorMessage(error)}`,
    });
  }
}

async function getMessages(threadId: string) {
  return fetch(`https://studio.tune.app/v1/threads/${threadId}/messages`, {
    headers: {
      "Content-Type": "application/json",
      "x-tune-key": process.env.TUNE_API_KEY!,
    },
  }).then((res) => res.json());
}

interface TuneMessage {
  role: string;
  content: { text: { value: string } }[];
}

function filterMessages(messages: TuneMessage[]) {
  return messages
    .map((message: TuneMessage) => {
      if (message?.role !== "system")
        return {
          role: message?.role,
          content:
            typeof message?.content?.[0]?.text === "string"
              ? message?.content?.[0]?.text
              : message?.content?.[0]?.text?.value,
        };
    })
    .filter((message) => message);
}
