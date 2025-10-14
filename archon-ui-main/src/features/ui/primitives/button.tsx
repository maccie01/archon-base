import React from "react";
import { cn } from "./styles";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "destructive" | "outline" | "ghost" | "link" | "primary" | "knowledge";
  size?: "default" | "sm" | "lg" | "icon" | "xs";
  loading?: boolean;
  children: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", loading = false, disabled, children, ...props }, ref) => {
    const baseStyles = cn(
      "inline-flex items-center justify-center rounded-xl font-medium",
      "transition-all duration-200",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary",
      "disabled:pointer-events-none disabled:opacity-50",
      loading && "cursor-wait",
    );

    type ButtonVariant = NonNullable<ButtonProps["variant"]>;
    const variants: Record<ButtonVariant, string> = {
      default: cn(
        "bg-primary text-primary-foreground",
        "hover:bg-primary/90",
        "shadow-sm hover:shadow-md",
      ),
      destructive: cn(
        "bg-destructive text-destructive-foreground",
        "hover:bg-destructive/90",
        "shadow-sm hover:shadow-md",
      ),
      outline: cn(
        "border border-border bg-background",
        "hover:bg-muted",
        "text-foreground",
      ),
      ghost: cn(
        "text-foreground",
        "hover:bg-muted",
      ),
      link: cn(
        "text-primary",
        "underline-offset-4 hover:underline",
      ),
      primary: cn(
        "bg-gradient-to-b from-blue-pastel/80 to-blue-pastel/60",
        "dark:from-blue-pastel/20 dark:to-blue-pastel/10",
        "text-blue-700 dark:text-blue-100",
        "border border-blue-pastel/50",
        "hover:from-blue-pastel/90 hover:to-blue-pastel/70",
        "dark:hover:from-blue-pastel/30 dark:hover:to-blue-pastel/20",
        "shadow-sm hover:shadow-md",
      ),
      knowledge: cn(
        "bg-gradient-to-b from-purple-pastel/80 to-purple-pastel/60",
        "dark:from-purple-pastel/20 dark:to-purple-pastel/10",
        "text-purple-700 dark:text-purple-100",
        "border border-purple-pastel/50",
        "hover:from-purple-pastel/90 hover:to-purple-pastel/70",
        "dark:hover:from-purple-pastel/30 dark:hover:to-purple-pastel/20",
        "shadow-sm hover:shadow-md",
        "focus-visible:ring-purple-pastel",
      ),
    };

    type ButtonSize = NonNullable<ButtonProps["size"]>;
    const sizes: Record<ButtonSize, string> = {
      default: "h-10 px-4 py-2",
      sm: "h-9 rounded-md px-3",
      lg: "h-11 rounded-md px-8",
      icon: "h-10 w-10",
      xs: "h-7 px-2 text-xs",
    };

    return (
      <button
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <svg
            className="mr-2 h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-label="Loading"
            role="img"
          >
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {children}
      </button>
    );
  },
);

Button.displayName = "Button";

export interface IconButtonProps extends Omit<ButtonProps, "size" | "children"> {
  icon: React.ReactNode;
  "aria-label": string;
}

export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(({ icon, className, ...props }, ref) => {
  return (
    <Button ref={ref} size="icon" className={cn("relative", className)} {...props}>
      {icon}
    </Button>
  );
});

IconButton.displayName = "IconButton";
