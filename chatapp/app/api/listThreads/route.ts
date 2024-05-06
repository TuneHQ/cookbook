const axios = require("axios");

export async function GET() {
  const resp = await axios
    .get("https://studio.tune.app/v1/threads?limit=1000", {
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

  return Response.json({
    success: resp?.data ? true : false,
    data: resp?.data ? resp?.data : [],
  });
}
