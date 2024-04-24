import axios from "axios";

const getMessages = async (threadID: string) => {
  return await axios
    .get(`https://studio.tune.app/v1/threads/${threadID}/messages`, {
      headers: {
        "Content-Type": "application/json",
        "x-tune-key": process.env.TUNE_API_KEY,
      },
    })
    .catch((err: any) => {
      return err;
    })
    .then((res: any) => {
      return res?.data;
    });
};

export { getMessages };
