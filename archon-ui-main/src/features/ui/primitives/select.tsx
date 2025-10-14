import * as SelectPrimitive from "@radix-ui/react-select";
import { Check, ChevronDown } from "lucide-react";
import React from "react";
import { cn, glassmorphism } from "./styles";

export type SelectColor = "purple" | "blue" | "green" | "pink" | "orange" | "cyan";

// Select Root - just re-export
export const Select = SelectPrimitive.Root;
export const SelectValue = SelectPrimitive.Value;

const selectColorVariants = {
  purple: {
    trigger:
      "hover:border-purple-pastel/50 hover:ring-1 hover:ring-purple-pastel/30 focus:border-purple-pastel focus:ring-2 focus:ring-purple-pastel/40",
    item: "hover:bg-purple-pastel/20 data-[state=checked]:bg-purple-pastel/30 data-[state=checked]:text-purple-pastel-dark",
  },
  blue: {
    trigger:
      "hover:border-blue-pastel/50 hover:ring-1 hover:ring-blue-pastel/30 focus:border-blue-pastel focus:ring-2 focus:ring-blue-pastel/40",
    item: "hover:bg-blue-pastel/20 data-[state=checked]:bg-blue-pastel/30 data-[state=checked]:text-blue-pastel-dark",
  },
  green: {
    trigger:
      "hover:border-green-pastel/50 hover:ring-1 hover:ring-green-pastel/30 focus:border-green-pastel focus:ring-2 focus:ring-green-pastel/40",
    item: "hover:bg-green-pastel/20 data-[state=checked]:bg-green-pastel/30 data-[state=checked]:text-green-pastel-dark",
  },
  pink: {
    trigger:
      "hover:border-pink-pastel/50 hover:ring-1 hover:ring-pink-pastel/30 focus:border-pink-pastel focus:ring-2 focus:ring-pink-pastel/40",
    item: "hover:bg-pink-pastel/20 data-[state=checked]:bg-pink-pastel/30 data-[state=checked]:text-pink-pastel-dark",
  },
  orange: {
    trigger:
      "hover:border-orange-pastel/50 hover:ring-1 hover:ring-orange-pastel/30 focus:border-orange-pastel focus:ring-2 focus:ring-orange-pastel/40",
    item: "hover:bg-orange-pastel/20 data-[state=checked]:bg-orange-pastel/30 data-[state=checked]:text-orange-pastel-dark",
  },
  cyan: {
    trigger:
      "hover:border-teal-pastel/50 hover:ring-1 hover:ring-teal-pastel/30 focus:border-teal-pastel focus:ring-2 focus:ring-teal-pastel/40",
    item: "hover:bg-teal-pastel/20 data-[state=checked]:bg-teal-pastel/30 data-[state=checked]:text-teal-pastel-dark",
  },
};

/**
 * 🤖 AI CONTEXT: Enhanced Select Trigger
 *
 * GLASSMORPHISM ENHANCEMENTS:
 * 1. TRANSPARENCY - True glass effect with backdrop blur
 * 2. NEON BORDERS - Color-coded focus states
 * 3. GLOW EFFECTS - Box shadows for depth
 * 4. COLOR VARIANTS - Support for theme colors
 */
// Select Trigger with glassmorphism styling
export const SelectTrigger = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger> & {
    showChevron?: boolean;
    color?: SelectColor;
  }
>(({ className = "", children, showChevron = true, color = "cyan", ...props }, ref) => {
  const colorStyles = selectColorVariants[color];

  return (
    <SelectPrimitive.Trigger
      ref={ref}
      className={cn(
        "flex items-center justify-between gap-2 px-3 py-2 rounded-lg",
        "backdrop-blur-xl bg-black/10 dark:bg-white/10",
        "border border-border",
        "transition-all duration-200",
        colorStyles.trigger,
        "disabled:opacity-50 disabled:cursor-not-allowed",
        "data-[placeholder]:text-muted-foreground",
        glassmorphism.interactive.base,
        className,
      )}
      {...props}
    >
      {children}
      {showChevron && (
        <SelectPrimitive.Icon className="ml-auto">
          <ChevronDown className="w-3 h-3 opacity-60 transition-transform duration-300 data-[state=open]:rotate-180" />
        </SelectPrimitive.Icon>
      )}
    </SelectPrimitive.Trigger>
  );
});
SelectTrigger.displayName = SelectPrimitive.Trigger.displayName;

/**
 * 🤖 AI CONTEXT: Enhanced Select Content
 *
 * GLASS DROPDOWN DESIGN:
 * 1. TRANSPARENCY - Full glass effect on dropdown
 * 2. BACKDROP BLUR - Heavy blur for content behind
 * 3. NEON GLOW - Subtle color-matched glow
 * 4. PORTAL - Ensures z-index above all content
 */
// Select Content with glassmorphism and Portal for z-index solution
export const SelectContent = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Content> & {
    color?: SelectColor;
  }
>(({ className = "", children, position = "popper", color = "cyan", ...props }, ref) => {
  const glowColor = {
    purple: "ring-1 ring-purple-pastel/30",
    blue: "ring-1 ring-blue-pastel/30",
    green: "ring-1 ring-green-pastel/30",
    pink: "ring-1 ring-pink-pastel/30",
    orange: "ring-1 ring-orange-pastel/30",
    cyan: "ring-1 ring-teal-pastel/30",
  }[color];

  return (
    <SelectPrimitive.Portal>
      <SelectPrimitive.Content
        ref={ref}
        className={cn(
          "relative z-[10000] min-w-[8rem] overflow-hidden rounded-lg",
          "backdrop-blur-xl bg-black/20 dark:bg-white/10",
          "border border-border",
          "shadow-lg",
          glowColor,
          "text-foreground",
          "data-[state=open]:animate-in data-[state=closed]:animate-out",
          "data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
          "data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95",
          "data-[side=bottom]:slide-in-from-top-2",
          "data-[side=left]:slide-in-from-right-2",
          "data-[side=right]:slide-in-from-left-2",
          "data-[side=top]:slide-in-from-bottom-2",
          glassmorphism.animation.fadeIn,
          className,
        )}
        position={position}
        sideOffset={5}
        {...props}
      >
        <SelectPrimitive.Viewport className="p-1">{children}</SelectPrimitive.Viewport>
      </SelectPrimitive.Content>
    </SelectPrimitive.Portal>
  );
});
SelectContent.displayName = SelectPrimitive.Content.displayName;

// Select Item with hover effects
export const SelectItem = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Item> & {
    icon?: React.ReactNode;
    color?: SelectColor;
  }
>(({ className = "", children, icon, color = "cyan", ...props }, ref) => {
  const colorStyles = selectColorVariants[color];

  return (
    <SelectPrimitive.Item
      ref={ref}
      className={cn(
        "relative flex items-center text-sm outline-none",
        "transition-all duration-200 cursor-pointer rounded-md",
        "pl-8 pr-3 py-2",
        "text-foreground",
        "hover:text-foreground",
        "focus:text-foreground",
        "data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
        "data-[state=checked]:font-medium",
        colorStyles.item,
        glassmorphism.interactive.base,
        className,
      )}
      {...props}
    >
      <SelectPrimitive.ItemIndicator className="absolute left-2 flex h-4 w-4 items-center justify-center">
        <Check className="h-4 w-4" />
      </SelectPrimitive.ItemIndicator>
      <SelectPrimitive.ItemText className="flex items-center gap-2">
        {icon && <span className="flex-shrink-0">{icon}</span>}
        {children}
      </SelectPrimitive.ItemText>
    </SelectPrimitive.Item>
  );
});
SelectItem.displayName = SelectPrimitive.Item.displayName;

// Export group and label for completeness
export const SelectGroup = SelectPrimitive.Group;
export const SelectLabel = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Label>
>(({ className = "", ...props }, ref) => (
  <SelectPrimitive.Label
    ref={ref}
    className={cn("px-2 py-1.5 text-xs font-semibold text-gray-600 dark:text-gray-400", className)}
    {...props}
  />
));
SelectLabel.displayName = SelectPrimitive.Label.displayName;
