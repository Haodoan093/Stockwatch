import {
  CandlestickSeries,
  ColorType,
  CrosshairMode,
  HistogramSeries,
  LineSeries,
  createChart,
  type CandlestickData,
  type IChartApi,
  type ISeriesApi,
  type LineData,
  type MouseEventParams,
  type Time,
} from "lightweight-charts";
import { useEffect, useMemo, useRef, useState } from "react";
import { fmtPrice, fmtVol, tone } from "@/shared/lib/format";
import { MA_COLORS } from "../constants";
import type { Candle } from "../types";

const UP = "#0ecb81";
const DOWN = "#f6465d";
const MA20 = MA_COLORS.ma20;
const MA50 = MA_COLORS.ma50;

type Props = { candles: Candle[] };

export default function PriceChart({ candles }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleSeries = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const volumeSeries = useRef<ISeriesApi<"Histogram"> | null>(null);
  const ma20Series = useRef<ISeriesApi<"Line"> | null>(null);
  const ma50Series = useRef<ISeriesApi<"Line"> | null>(null);
  const byDate = useRef<Map<string, Candle>>(new Map());
  const [hover, setHover] = useState<Candle | null>(null);

  // Tạo biểu đồ một lần
  useEffect(() => {
    const el = host.current;
    if (!el) return;
    const chart = createChart(el, {
      autoSize: true,
      layout: {
        background: { type: ColorType.Solid, color: "transparent" },
        textColor: "#848e9c",
        fontSize: 12,
      },
      grid: { vertLines: { color: "#1a2029" }, horzLines: { color: "#1a2029" } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: "#232a34", scaleMargins: { top: 0.06, bottom: 0.25 } },
      timeScale: { borderColor: "#232a34", rightOffset: 4 },
      localization: { priceFormatter: (p: number) => fmtPrice(p) },
    });
    candleSeries.current = chart.addSeries(CandlestickSeries, {
      upColor: UP,
      downColor: DOWN,
      wickUpColor: UP,
      wickDownColor: DOWN,
      borderVisible: false,
    });
    ma20Series.current = chart.addSeries(LineSeries, {
      color: MA20,
      lineWidth: 1,
      priceLineVisible: false,
      lastValueVisible: false,
      crosshairMarkerVisible: false,
    });
    ma50Series.current = chart.addSeries(LineSeries, {
      color: MA50,
      lineWidth: 1,
      priceLineVisible: false,
      lastValueVisible: false,
      crosshairMarkerVisible: false,
    });
    const volume = chart.addSeries(HistogramSeries, {
      priceFormat: { type: "volume" },
      priceScaleId: "",
      priceLineVisible: false,
      lastValueVisible: false,
    });
    volume.priceScale().applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
    volumeSeries.current = volume;
    chartRef.current = chart;

    const onMove = (param: MouseEventParams<Time>) => {
      const key = typeof param.time === "string" ? param.time : null;
      setHover(key ? (byDate.current.get(key) ?? null) : null);
    };
    chart.subscribeCrosshairMove(onMove);

    return () => {
      chart.unsubscribeCrosshairMove(onMove);
      chart.remove();
      chartRef.current = null;
    };
  }, []);

  // Cập nhật dữ liệu khi đổi mã / khoảng thời gian
  useEffect(() => {
    if (!chartRef.current) return;
    byDate.current = new Map(candles.map((c) => [c.date, c]));
    const ohlc: CandlestickData<Time>[] = candles.map((c) => ({
      time: c.date as Time,
      open: c.open,
      high: c.high,
      low: c.low,
      close: c.close,
    }));
    const line = (pick: (c: Candle) => number | null): LineData<Time>[] =>
      candles.flatMap((c) => {
        const v = pick(c);
        return v == null ? [] : [{ time: c.date as Time, value: v }];
      });
    candleSeries.current?.setData(ohlc);
    ma20Series.current?.setData(line((c) => c.ma20));
    ma50Series.current?.setData(line((c) => c.ma50));
    volumeSeries.current?.setData(
      candles.map((c) => ({
        time: c.date as Time,
        value: c.volume,
        color: c.close >= c.open ? "rgba(14,203,129,0.35)" : "rgba(246,70,93,0.35)",
      })),
    );
    chartRef.current.timeScale().fitContent();
    setHover(null);
  }, [candles]);

  const shown = hover ?? candles[candles.length - 1] ?? null;
  const prev = useMemo(() => {
    if (!shown) return null;
    const i = candles.findIndex((c) => c.date === shown.date);
    return i > 0 ? candles[i - 1] : null;
  }, [candles, shown]);
  const delta = shown && prev ? shown.close - prev.close : null;

  return (
    <div className="relative min-h-[320px] flex-1 lg:min-h-0">
      {shown && (
        <div className="pointer-events-none absolute top-2 left-3 z-10 flex flex-wrap gap-x-3 gap-y-0.5 text-xs">
          <span className="text-mute">{shown.date}</span>
          <span className="num">
            <span className="text-mute">M </span>
            <span className={tone(delta)}>{fmtPrice(shown.open)}</span>
          </span>
          <span className="num">
            <span className="text-mute">C </span>
            <span className={tone(delta)}>{fmtPrice(shown.high)}</span>
          </span>
          <span className="num">
            <span className="text-mute">T </span>
            <span className={tone(delta)}>{fmtPrice(shown.low)}</span>
          </span>
          <span className="num">
            <span className="text-mute">Đ </span>
            <span className={tone(delta)}>{fmtPrice(shown.close)}</span>
          </span>
          <span className="num">
            <span className="text-mute">KL </span>
            {fmtVol(shown.volume)}
          </span>
          {shown.ma20 != null && (
            <span className="num" style={{ color: MA20 }}>
              MA20 {fmtPrice(shown.ma20)}
            </span>
          )}
          {shown.ma50 != null && (
            <span className="num" style={{ color: MA50 }}>
              MA50 {fmtPrice(shown.ma50)}
            </span>
          )}
        </div>
      )}
      <div ref={host} className="absolute inset-0" role="img" aria-label="Biểu đồ nến giá cổ phiếu" />
    </div>
  );
}
