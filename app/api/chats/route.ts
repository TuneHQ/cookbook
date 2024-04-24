import { getMessages } from "@/utility/chats.utilities";
import { getModelResponse } from "@/utility/run.utitities";

const axios = require("axios");

export async function POST(request: Request) {
  const requestBody = await request.json();
  const threadID = requestBody.threadID;
  const content = requestBody.content;

  const resp = await axios
    .post(
      `https://studio.tune.app/v1/threads/${threadID}/messages`,
      {
        assistantId: "",
        content,
        fileIds: [],
        role: "user",
        runId: "",
        threadId: threadID,
      },
      {
        headers: {
          "Content-Type": "application/json",
          "x-tune-key": process.env.TUNE_API_KEY,
        },
      }
    )
    .catch(() => {
      return {
        success: false,
      };
    })
    .then(() => {
      return {
        success: true,
      };
    });

  if (resp?.success) {
    const response = await getModelResponse(threadID);
    if (response?.success) {
      const respdata = await getMessages(threadID);
      return Response.json({
        success: respdata?.data ? true : false,
        data: respdata?.data
          ? respdata?.data
              ?.map(
                (val: { role: any; content: { text: { value: any } }[] }) => {
                  console.log({ resp: val?.content });

                  if (val?.role !== "system")
                    return {
                      role: val?.role,
                      content: val?.content?.[0]?.text?.value || "",
                    };
                }
              )
              ?.filter((val: any) => val)
          : [],
      });
    }
    return Response.json({
      success: false,
      data: [],
    });
  }

  return Response.json({
    success: resp?.success,
    data: [],
  });
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const threadID = searchParams.get("threadID");
  if (!threadID) return Response.json({ success: false, data: [] });

  const resp = await getMessages(threadID);

  return Response.json({
    success: resp?.data ? true : false,
    data: resp?.data
      ? resp?.data
          ?.map((val: { role: any; content: { text: { value: any } }[] }) => {
            console.log({ resp: val?.content });

            if (val?.role !== "system")
              return {
                role: val?.role,
                content: val?.content?.[0]?.text?.value || "",
              };
          })
          ?.filter((val: any) => val)
      : [],
  });
}
