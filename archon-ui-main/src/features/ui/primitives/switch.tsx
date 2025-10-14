import * as SwitchPrimitives from "@radix-ui/react-switch";
import * as React from "react";
import { cn, glassmorphism } from "./styles";

export type SwitchSize = "sm" | "md" | "lg";
export type SwitchColor = "purple" | "blue" | "green" | "pink" | "orange" | "cyan";

interface SwitchProps extends React.ComponentPropsWithoutRef<typeof SwitchPrimitives.Root> {
  size?: SwitchSize;
  color?: SwitchColor;
  icon?: React.ReactNode;
  iconOn?: React.ReactNode;
  iconOff?: React.ReactNode;
}

const switchVariants = {
  size: {
    sm: {
      root: "h-4 w-8",
      thumb: "h-3 w-3 data-[state=checked]:translate-x-4",
      icon: "",
    },
    md: {
      root: "h-6 w-11",
      thumb: "h-5 w-5 data-[state=checked]:translate-x-5",
      icon: "h-3 w-3",
    },
    lg: {
      root: "h-8 w-14",
      thumb: "h-7 w-7 data-[state=checked]:translate-x-6",
      icon: "h-5 w-5",
    },
  },
  color: {
    purple: {
      checked: "data-[state=checked]:bg-purple-pastel/20 data-[state=checked]:border-purple-pastel/50",
      glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-purple-pastel/40",
      thumb: "data-[state=checked]:border-purple-pastel data-[state=checked]:shadow-sm",
      icon: "text-muted-foreground data-[state=checked]:text-purple-pastel-dark",
      focusRing: "focus-visible:ring-purple-pastel",
    },
    blue: {
      checked: "data-[state=checked]:bg-blue-pastel/20 data-[state=checked]:border-blue-pastel/50",
      glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-blue-pastel/40",
      thumb: "data-[state=checked]:border-blue-pastel data-[state=checked]:shadow-sm",
      icon: "text-muted-foreground data-[state=checked]:text-blue-pastel-dark",
      focusRing: "focus-visible:ring-blue-pastel",
    },
    green: {
      checked: "data-[state=checked]:bg-green-pastel/20 data-[state=checked]:border-green-pastel/50",
      glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-green-pastel/40",
      thumb: "data-[state=checked]:border-green-pastel data-[state=checked]:shadow-sm",
      icon: "text-muted-foreground data-[state=checked]:text-green-pastel-dark",
      focusRing: "focus-visible:ring-green-pastel",
    },
    pink: {
      checked: "data-[state=checked]:bg-pink-pastel/20 data-[state=checked]:border-pink-pastel/50",
      glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-pink-pastel/40",
      thumb: "data-[state=checked]:border-pink-pastel data-[state=checked]:shadow-sm",
      icon: "text-muted-foreground data-[state=checked]:text-pink-pastel-dark",
      focusRing: "focus-visible:ring-pink-pastel",
    },
    orange: {
      checked: "data-[state=checked]:bg-orange-pastel/20 data-[state=checked]:border-orange-pastel/50",
      glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-orange-pastel/40",
      thumb: "data-[state=checked]:border-orange-pastel data-[state=checked]:shadow-sm",
      icon: "text-muted-foreground data-[state=checked]:text-orange-pastel-dark",
      focusRing: "focus-visible:ring-orange-pastel",
    },
    cyan: {
      checked: "data-[state=checked]:bg-teal-pastel/20 data-[state=checked]:border-teal-pastel/50",
      glow: "data-[state=checked]:ring-1 data-[state=checked]:ring-teal-pastel/40",
      thumb: "data-[state=checked]:border-teal-pastel data-[state=checked]:shadow-sm",
      icon: "text-muted-foreground data-[state=checked]:text-teal-pastel-dark",
      focusRing: "focus-visible:ring-teal-pastel",
    },
  },
};

/**
 * 🤖 AI CONTEXT: Enhanced Switch Component
 *
 * GLASS PROPERTIES for true glassmorphism:
 * 1. TRANSPARENCY - Subtle background opacity
 *    - unchecked: Almost invisible (bg-white/10)
 *    - checked: Color tinted glass (color-500/20)
 *
 * 2. SIZE VARIANTS - Three sizes for different use cases
 *    - sm: 16px height, no icons
 *    - md: 24px height, smaller icons (12x12px)
 *    - lg: 32px height, full icons (20x20px)
 *
 * 3. GLOW EFFECTS - Neon accents that animate
 *    - Box shadow for outer glow
 *    - Drop shadow for icon glow
 *    - Transition animations for smooth state changes
 *
 * 4. ICON SUPPORT - Dynamic icon switching
 *    - iconOn: Displayed when checked
 *    - iconOff: Displayed when unchecked
 *    - icon: Same icon for both states
 *
 * 5. CONTROLLED/UNCONTROLLED MODE SUPPORT
 *    - Controlled: Pass checked prop + onCheckedChange handler
 *    - Uncontrolled: Pass defaultChecked, component manages own state
 */
const Switch = React.forwardRef<React.ElementRef<typeof SwitchPrimitives.Root>, SwitchProps>(
  (
    {
      className,
      size = "md",
      color = "cyan",
      icon,
      iconOn,
      iconOff,
      checked,
      defaultChecked,
      onCheckedChange,
      ...props
    },
    ref,
  ) => {
    const sizeStyles = switchVariants.size[size];
    const colorStyles = switchVariants.color[color];

    // Detect controlled vs uncontrolled mode
    const isControlled = checked !== undefined;

    // Internal state for uncontrolled mode
    const [internalChecked, setInternalChecked] = React.useState(defaultChecked ?? false);

    // Get the actual checked state (controlled or uncontrolled)
    const actualChecked = isControlled ? checked : internalChecked;

    // Handle state changes for both controlled and uncontrolled modes
    const handleCheckedChange = React.useCallback(
      (newChecked: boolean) => {
        // Update internal state for uncontrolled mode
        if (!isControlled) {
          setInternalChecked(newChecked);
        }
        // Call parent's handler if provided
        onCheckedChange?.(newChecked);
      },
      [isControlled, onCheckedChange],
    );

    const displayIcon = React.useMemo(() => {
      if (size === "sm") return null;
      return actualChecked ? iconOn || icon : iconOff || icon;
    }, [size, actualChecked, icon, iconOn, iconOff]);

    return (
      <SwitchPrimitives.Root
        className={cn(
          "relative inline-flex shrink-0 cursor-pointer items-center rounded-full",
          "bg-black/10 dark:bg-white/10 backdrop-blur-xl",
          "border border-border",
          "transition-all duration-200",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
          colorStyles.focusRing,
          "disabled:cursor-not-allowed disabled:opacity-50",
          colorStyles.checked,
          colorStyles.glow,
          sizeStyles.root,
          glassmorphism.interactive.base,
          className,
        )}
        checked={actualChecked}
        onCheckedChange={handleCheckedChange}
        {...props}
        ref={ref}
      >
        <SwitchPrimitives.Thumb
          className={cn(
            "pointer-events-none relative flex items-center justify-center rounded-full",
            "bg-gradient-to-br from-gray-100/80 to-white/60 dark:from-gray-700/80 dark:to-gray-800/60",
            "backdrop-blur-sm border-2",
            "border-border",
            "shadow-sm ring-0 transition-all duration-200",
            "data-[state=unchecked]:translate-x-0",
            "data-[state=checked]:from-white/90 data-[state=checked]:to-white/70 dark:data-[state=checked]:from-gray-100/20 dark:data-[state=checked]:to-gray-200/10",
            colorStyles.thumb,
            sizeStyles.thumb,
          )}
        >
          {displayIcon && (
            <div
              className={cn(
                "flex items-center justify-center transition-all duration-200",
                colorStyles.icon,
                sizeStyles.icon,
              )}
            >
              {displayIcon}
            </div>
          )}
        </SwitchPrimitives.Thumb>
      </SwitchPrimitives.Root>
    );
  },
);

Switch.displayName = SwitchPrimitives.Root.displayName;

export { Switch, switchVariants };
