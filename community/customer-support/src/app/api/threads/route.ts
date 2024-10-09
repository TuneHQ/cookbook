import { Thread } from "@/lib/types";
import { getErrorMessage } from "@/lib/utils";

interface TuneThread {
  id: number;
  object: "thread";
  createdAt: string;
  metadata: object;
  title: string;
  toolResources: object;
}

export async function GET() {
  try {
    const res = await fetch("https://studio.tune.app/v1/threads?limit=1000", {
      headers: {
        "Content-Type": "application/json",
        "x-tune-key": process.env.TUNE_API_KEY!,
      },
    });
    const data = await res.json();
    const threads: Thread[] = data.data
      .map((thread: TuneThread) => ({
        id: thread.id,
        title: thread.title.charAt(0).toUpperCase() + thread.title.slice(1),
        createdAt: new Date(thread.createdAt).toLocaleString(),
      }))
      .reverse();
    return Response.json({
      status: true,
      data: threads,
    });
  } catch (error) {
    return Response.json({
      status: false,
      message: `Error fetching threads: ${getErrorMessage(error)}`,
    });
  }
}

export async function POST(request: Request) {
  try {
    const { title } = await request.json();

    const resp = await fetch(`https://studio.tune.app/v1/threads`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-tune-key": process.env.TUNE_API_KEY!,
      },
      body: JSON.stringify({
        datasetId: "",
        messages: [],
        title: title,
      }),
    });
    const respData = await resp.json();
    return Response.json({
      status: true,
      data: respData.data,
    });
  } catch (error) {
    return Response.json({
      status: false,
      message: `Error creating thread: ${getErrorMessage(error)}`,
    });
  }
}
