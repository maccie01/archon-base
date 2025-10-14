import React from "react";
import { cn } from "./styles";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, type, error, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        "w-full rounded-lg py-2 px-3",
        "bg-white/50 dark:bg-black/70",
        "border border-border",
        "text-foreground",
        "placeholder:text-muted-foreground",
        "focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2",
        "transition-all duration-200",
        "disabled:opacity-50 disabled:cursor-not-allowed",
        error && "border-red-pastel focus:ring-red-pastel",
        className,
      )}
      ref={ref}
      {...props}
    />
  );
});

Input.displayName = "Input";

export interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: boolean;
}

export const TextArea = React.forwardRef<HTMLTextAreaElement, TextAreaProps>(({ className, error, ...props }, ref) => {
  return (
    <textarea
      className={cn(
        "w-full rounded-lg py-2 px-3",
        "bg-white/50 dark:bg-black/70",
        "border border-border",
        "text-foreground",
        "placeholder:text-muted-foreground",
        "focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2",
        "transition-all duration-200",
        "disabled:opacity-50 disabled:cursor-not-allowed",
        "resize-y min-h-[80px]",
        error && "border-red-pastel focus:ring-red-pastel",
        className,
      )}
      ref={ref}
      {...props}
    />
  );
});

TextArea.displayName = "TextArea";

// Label component for form fields
export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  required?: boolean;
}

export const Label = React.forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, children, required, ...props }, ref) => {
    return (
      // biome-ignore lint/a11y/noLabelWithoutControl: htmlFor is passed through props spread
      <label
        ref={ref}
        className={cn("block text-sm font-medium", "text-gray-700 dark:text-gray-300", "mb-1", className)}
        {...props}
      >
        {children}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
    );
  },
);

Label.displayName = "Label";

// FormField wrapper for consistent spacing
export interface FormFieldProps {
  children: React.ReactNode;
  className?: string;
}

export const FormField: React.FC<FormFieldProps> = ({ children, className }) => {
  return <div className={cn("space-y-1", className)}>{children}</div>;
};

// FormGrid for two-column layouts
export interface FormGridProps {
  children: React.ReactNode;
  className?: string;
  columns?: 1 | 2 | 3;
}

export const FormGrid: React.FC<FormGridProps> = ({ children, className, columns = 2 }) => {
  const gridCols = {
    1: "grid-cols-1",
    2: "grid-cols-2",
    3: "grid-cols-3",
  };

  return <div className={cn("grid gap-4", gridCols[columns], className)}>{children}</div>;
};
