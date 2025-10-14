import * as CheckboxPrimitives from "@radix-ui/react-checkbox";
import { Check, Minus } from "lucide-react";
import * as React from "react";
import { cn, glassmorphism } from "./styles";

export type CheckboxColor = "purple" | "blue" | "green" | "pink" | "orange" | "cyan";

interface CheckboxProps extends React.ComponentPropsWithoutRef<typeof CheckboxPrimitives.Root> {
  color?: CheckboxColor;
  indeterminate?: boolean;
}

const checkboxVariants = {
  purple: {
    checked: "data-[state=checked]:bg-purple-pastel/20 data-[state=checked]:border-purple-pastel",
    glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-purple-pastel/40",
    indicator: "text-purple-pastel-dark",
    focusRing: "focus-visible:ring-purple-pastel",
  },
  blue: {
    checked: "data-[state=checked]:bg-blue-pastel/20 data-[state=checked]:border-blue-pastel",
    glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-blue-pastel/40",
    indicator: "text-blue-pastel-dark",
    focusRing: "focus-visible:ring-blue-pastel",
  },
  green: {
    checked: "data-[state=checked]:bg-green-pastel/20 data-[state=checked]:border-green-pastel",
    glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-green-pastel/40",
    indicator: "text-green-pastel-dark",
    focusRing: "focus-visible:ring-green-pastel",
  },
  pink: {
    checked: "data-[state=checked]:bg-pink-pastel/20 data-[state=checked]:border-pink-pastel",
    glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-pink-pastel/40",
    indicator: "text-pink-pastel-dark",
    focusRing: "focus-visible:ring-pink-pastel",
  },
  orange: {
    checked: "data-[state=checked]:bg-orange-pastel/20 data-[state=checked]:border-orange-pastel",
    glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-orange-pastel/40",
    indicator: "text-orange-pastel-dark",
    focusRing: "focus-visible:ring-orange-pastel",
  },
  cyan: {
    checked: "data-[state=checked]:bg-teal-pastel/20 data-[state=checked]:border-teal-pastel",
    glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-teal-pastel/40",
    indicator: "text-teal-pastel-dark",
    focusRing: "focus-visible:ring-teal-pastel",
  },
};

/**
 * 🤖 AI CONTEXT: Glassmorphic Checkbox Component
 *
 * DESIGN DECISIONS:
 * 1. TRANSPARENCY - Glass effect with subtle background
 *    - Unchecked: Almost invisible (bg-white/10)
 *    - Checked: Color tinted glass (color-500/20)
 *
 * 2. NEON GLOW - Tron-style accent on activation
 *    - Box shadow creates outer glow
 *    - Drop shadow on check icon for depth
 *
 * 3. ANIMATION - Smooth state transitions
 *    - Scale animation on check/uncheck
 *    - Fade in/out for indicator
 *    - 300ms transitions for smoothness
 *
 * 4. STATES - Support for three states
 *    - Unchecked: Empty box
 *    - Checked: Check icon with glow
 *    - Indeterminate: Minus icon (partial selection)
 */
const Checkbox = React.forwardRef<React.ElementRef<typeof CheckboxPrimitives.Root>, CheckboxProps>(
  ({ className, color = "cyan", indeterminate, checked, ...props }, ref) => {
    const colorStyles = checkboxVariants[color];

    return (
      <CheckboxPrimitives.Root
        className={cn(
          "peer h-5 w-5 shrink-0 rounded-md",
          "bg-black/10 dark:bg-white/10 backdrop-blur-xl",
          "border-2 border-border",
          "transition-all duration-200",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
          colorStyles.focusRing,
          "disabled:cursor-not-allowed disabled:opacity-50",
          "hover:border-accent/50",
          colorStyles.checked,
          colorStyles.glow,
          "data-[state=indeterminate]:bg-opacity-50",
          glassmorphism.interactive.base,
          className,
        )}
        checked={indeterminate ? "indeterminate" : checked}
        {...props}
        ref={ref}
      >
        <CheckboxPrimitives.Indicator
          className={cn(
            "flex items-center justify-center",
            "data-[state=checked]:animate-in data-[state=checked]:zoom-in-0",
            "data-[state=unchecked]:animate-out data-[state=unchecked]:zoom-out-0",
            "data-[state=indeterminate]:animate-in data-[state=indeterminate]:zoom-in-0",
          )}
        >
          {indeterminate ? (
            <Minus className={cn("h-3.5 w-3.5", colorStyles.indicator)} />
          ) : (
            <Check className={cn("h-4 w-4", colorStyles.indicator)} />
          )}
        </CheckboxPrimitives.Indicator>
      </CheckboxPrimitives.Root>
    );
  },
);

Checkbox.displayName = CheckboxPrimitives.Root.displayName;

export { Checkbox, checkboxVariants };
