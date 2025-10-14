import * as TabsPrimitive from "@radix-ui/react-tabs";
import React from "react";
import { cn } from "./styles";

// Root
export const Tabs = TabsPrimitive.Root;

// List - styled like pill navigation
export const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "backdrop-blur-sm bg-white/40 dark:bg-white/5 border border-white/30 dark:border-white/15",
      "rounded-full p-1 shadow-lg inline-flex gap-1",
      className,
    )}
    role="tablist"
    {...props}
  />
));
TabsList.displayName = TabsPrimitive.List.displayName;

// Trigger
type TabColor = "blue" | "purple" | "pink" | "orange" | "cyan" | "green";

export const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger> & {
    color?: TabColor;
  }
>(({ className, color = "blue", ...props }, ref) => {
  const activeClasses = {
    blue: "data-active:bg-blue-pastel/30 data-active:text-blue-pastel-dark data-active:border data-active:border-blue-pastel/50 data-active:shadow-sm",
    purple: "data-active:bg-purple-pastel/30 data-active:text-purple-pastel-dark data-active:border data-active:border-purple-pastel/50 data-active:shadow-sm",
    pink: "data-active:bg-pink-pastel/30 data-active:text-pink-pastel-dark data-active:border data-active:border-pink-pastel/50 data-active:shadow-sm",
    orange: "data-active:bg-orange-pastel/30 data-active:text-orange-pastel-dark data-active:border data-active:border-orange-pastel/50 data-active:shadow-sm",
    cyan: "data-active:bg-teal-pastel/30 data-active:text-teal-pastel-dark data-active:border data-active:border-teal-pastel/50 data-active:shadow-sm",
    green: "data-active:bg-green-pastel/30 data-active:text-green-pastel-dark data-active:border data-active:border-green-pastel/50 data-active:shadow-sm",
  } satisfies Record<TabColor, string>;

  const focusRingClasses = {
    blue: "focus-visible:ring-blue-pastel",
    purple: "focus-visible:ring-purple-pastel",
    pink: "focus-visible:ring-pink-pastel",
    orange: "focus-visible:ring-orange-pastel",
    cyan: "focus-visible:ring-teal-pastel",
    green: "focus-visible:ring-green-pastel",
  } satisfies Record<TabColor, string>;

  return (
    <TabsPrimitive.Trigger
      ref={ref}
      className={cn(
        "flex items-center gap-2 px-5 py-2.5 rounded-full transition-all duration-200",
        "text-sm font-semibold whitespace-nowrap",
        "text-gray-700 dark:text-gray-300 hover:bg-white/10 dark:hover:bg-white/5",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
        focusRingClasses[color],
        activeClasses[color],
        "disabled:pointer-events-none disabled:opacity-50",
        className,
      )}
      {...props}
    >
      {props.children}
    </TabsPrimitive.Trigger>
  );
});
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName;

// Content
export const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2",
      "focus-visible:ring-ring focus-visible:ring-offset-2",
      className,
    )}
    {...props}
  />
));
TabsContent.displayName = TabsPrimitive.Content.displayName;
