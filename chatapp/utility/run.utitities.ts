import axios from "axios";

const getModelResponse = async (threadID: string) => {
  return await axios
    .post(
      `https://studio.tune.app/v1/threads/${threadID}/runs`,
      {
        model: process.env.TUNE_MODEL,
        threadId: threadID,
      },
      {
        headers: {
          "Content-Type": "application/json",
          "x-tune-key": process.env.TUNE_API_KEY,
        },
      }
    )
    .catch((err: any) => {
      return { success: false };
    })
    .then((res: any) => {
      return { success: true };
    });
};

export { getModelResponse };
