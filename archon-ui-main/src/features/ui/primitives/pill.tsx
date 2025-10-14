import type React from "react";
import { cn } from "./styles";

export type PillColor = "blue" | "orange" | "cyan" | "purple" | "pink" | "green" | "gray";

export interface StatPillProps extends React.HTMLAttributes<HTMLDivElement> {
  color?: PillColor;
  value: number | string;
  icon?: React.ReactNode;
  size?: "sm" | "md";
}

// Static maps hoisted outside component to avoid re-allocation on each render
const SIZE_MAP = {
  sm: "h-6 px-2 text-[11px] gap-1",
  md: "h-7 px-2.5 text-xs gap-1.5",
} as const;

const COLOR_MAP: Record<PillColor, { bg: string; text: string; border: string; glow: string }> = {
  blue: {
    bg: "from-blue-pastel/30 to-white/60 dark:from-blue-pastel/20 dark:to-black/30",
    text: "text-blue-pastel-dark",
    border: "border-blue-pastel/60",
    glow: "shadow-sm ring-1 ring-blue-pastel/30",
  },
  orange: {
    bg: "from-orange-pastel/30 to-white/60 dark:from-orange-pastel/20 dark:to-black/30",
    text: "text-orange-pastel-dark",
    border: "border-orange-pastel/60",
    glow: "shadow-sm ring-1 ring-orange-pastel/30",
  },
  cyan: {
    bg: "from-teal-pastel/30 to-white/60 dark:from-teal-pastel/20 dark:to-black/30",
    text: "text-teal-pastel-dark",
    border: "border-teal-pastel/60",
    glow: "shadow-sm ring-1 ring-teal-pastel/30",
  },
  purple: {
    bg: "from-purple-pastel/30 to-white/60 dark:from-purple-pastel/20 dark:to-black/30",
    text: "text-purple-pastel-dark",
    border: "border-purple-pastel/60",
    glow: "shadow-sm ring-1 ring-purple-pastel/30",
  },
  pink: {
    bg: "from-pink-pastel/30 to-white/60 dark:from-pink-pastel/20 dark:to-black/30",
    text: "text-pink-pastel-dark",
    border: "border-pink-pastel/60",
    glow: "shadow-sm ring-1 ring-pink-pastel/30",
  },
  green: {
    bg: "from-green-pastel/30 to-white/60 dark:from-green-pastel/20 dark:to-black/30",
    text: "text-green-pastel-dark",
    border: "border-green-pastel/60",
    glow: "shadow-sm ring-1 ring-green-pastel/30",
  },
  gray: {
    bg: "from-gray-100/80 to-white/60 dark:from-gray-500/20 dark:to-gray-500/10",
    text: "text-gray-700 dark:text-gray-200",
    border: "border-gray-300/60 dark:border-gray-500/50",
    glow: "shadow-sm ring-1 ring-gray-300/30",
  },
};

/**
 * StatPill — rounded glass/stat indicator with neon accents.
 * Used for compact counters inside cards (docs, examples, etc.).
 */
export const StatPill: React.FC<StatPillProps> = ({
  color = "blue",
  value,
  icon,
  size = "sm",
  className,
  ...props
}) => {
  const c = COLOR_MAP[color];

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full backdrop-blur-md border",
        "bg-gradient-to-b",
        c.bg,
        c.text,
        c.border,
        c.glow,
        SIZE_MAP[size],
        className,
      )}
      {...props}
    >
      {icon && (
        <span className="inline-flex items-center" aria-hidden="true">
          {icon}
        </span>
      )}
      <span className="font-semibold tabular-nums">{value}</span>
    </div>
  );
};
