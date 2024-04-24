const axios = require("axios");

// export async function POST(request: Request) {
//   const { threadID } = await request.json();

//   const resp = await axios
//     .post(`https://studio.tune.app/v1/threads/${threadID}/messages`, {
//       headers: {
//         "Content-Type": "application/json",
//         "x-tune-key": process.env.TUNE_API_KEY,
//       },
//     })
//     .catch((err: any) => {
//       return err;
//     })
//     .then((res: any) => {
//       return res?.data;
//     });

//   return Response.json({
//     success: resp?.data ? true : false,
//     data: resp?.data ? resp?.data : [],
//   });
// }

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const threadID = searchParams.get("threadID");
  console.log({ threadID });
  const resp = await axios
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
