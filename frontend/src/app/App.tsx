import { MarketPage, useWatchlist } from "@/features/market";
import TopBar from "./layout/TopBar";

export default function App() {
  const watchlist = useWatchlist();
  return (
    <div className="flex min-h-screen flex-col lg:h-screen lg:overflow-hidden">
      <TopBar sources={watchlist.sources} />
      <MarketPage watchlist={watchlist} />
    </div>
  );
}
