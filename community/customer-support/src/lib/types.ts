export type Thread = {
  id: number;
  title: string;
  createdAt: string;
};

export type Message = {
  id: number;
  content: string;
  sender: "user" | "assistant";
};
