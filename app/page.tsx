import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col gap-[16px] items-center justify-between p-24">
      <div className="flex-1 w-full bg-black"></div>{" "}
      <div className="h-[] w-[full] bg-black"></div>
    </main>
  );
}
