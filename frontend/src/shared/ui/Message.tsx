import type { ReactNode } from "react";

type Props = { title: string; children: ReactNode };

export default function Message({ title, children }: Props) {
  return (
    <div className="grid flex-1 place-items-center p-8 text-center">
      <div className="max-w-md">
        <h2 className="mb-2 text-base font-semibold">{title}</h2>
        <div className="text-sm text-mute">{children}</div>
      </div>
    </div>
  );
}
