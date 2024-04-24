const axios = require("axios");

export async function POST(request: Request) {
  const requestBody = await request.json();
  const title = requestBody.title;

  const resp = await axios
    .post(
      `https://studio.tune.app/v1/threads`,
      {
        datasetId: "",
        messages: [],
        title: title,
      },
      {
        headers: {
          "Content-Type": "application/json",
          "x-tune-key": process.env.TUNE_API_KEY,
        },
      }
    )
    .catch((err: any) => {
      return err;
    })
    .then((res: any) => {
      return res?.data;
    });

  return Response.json({
    success: resp ? true : false,
    data: resp ? resp : {},
  });
}
