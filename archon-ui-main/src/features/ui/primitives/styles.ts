/**
 * Shared style utilities for Radix primitives
 * Apple-inspired minimalist design with pastel colors
 *
 * Theme Support:
 * - All styles use Tailwind's dark: prefix for automatic theme switching
 * - Theme is managed by ThemeContext (light/dark)
 * - For runtime theme values, use useThemeAware hook
 */

// Base glassmorphism classes with Apple aesthetic - clean glass effect
export const glassmorphism = {
  // Background variations - subtle transparency for glass effect
  background: {
    subtle: "backdrop-blur-xl bg-white/5 dark:bg-white/10",
    strong: "backdrop-blur-xl bg-white/10 dark:bg-white/20",
    card: "backdrop-blur-xl bg-white/5 dark:bg-white/10",
    // Pastel colored backgrounds - soft and minimal
    purple: "backdrop-blur-xl bg-purple-pastel/5 dark:bg-purple-pastel/10",
    blue: "backdrop-blur-xl bg-blue-pastel/5 dark:bg-blue-pastel/10",
    green: "backdrop-blur-xl bg-green-pastel/5 dark:bg-green-pastel/10",
    pink: "backdrop-blur-xl bg-pink-pastel/5 dark:bg-pink-pastel/10",
    orange: "backdrop-blur-xl bg-orange-pastel/5 dark:bg-orange-pastel/10",
    teal: "backdrop-blur-xl bg-teal-pastel/5 dark:bg-teal-pastel/10",
  },

  // Border styles for glass effect - subtle and clean
  border: {
    default: "border border-border",
    primary: "border border-primary/30",
    blue: "border border-blue-pastel/30",
    purple: "border border-purple-pastel/30",
    focus: "focus:border-primary focus:ring-2 focus:ring-primary/20",
    hover: "hover:border-primary/50",
  },

  // Interactive states
  interactive: {
    base: "transition-all duration-200",
    hover: "hover:bg-muted",
    active: "active:bg-muted/80",
    selected:
      "data-[state=checked]:bg-primary/10 data-[state=checked]:text-primary",
    disabled: "disabled:opacity-50 disabled:cursor-not-allowed",
  },

  // Animation presets
  animation: {
    fadeIn:
      "data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
    slideIn: "data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95",
    slideFromTop: "data-[side=bottom]:slide-in-from-top-2",
    slideFromBottom: "data-[side=top]:slide-in-from-bottom-2",
    slideFromLeft: "data-[side=right]:slide-in-from-left-2",
    slideFromRight: "data-[side=left]:slide-in-from-right-2",
  },

  // Shadow effects - subtle and clean
  shadow: {
    sm: "shadow-sm",
    md: "shadow-md",
    lg: "shadow-lg",
    elevated: "shadow-xl",
    // Subtle accent shadows
    accent: {
      purple: "shadow-sm shadow-purple-pastel/10",
      blue: "shadow-sm shadow-blue-pastel/10",
      green: "shadow-sm shadow-green-pastel/10",
      red: "shadow-sm shadow-destructive/10",
      orange: "shadow-sm shadow-orange-pastel/10",
      primary: "shadow-sm shadow-primary/10",
      pink: "shadow-sm shadow-pink-pastel/10",
    },
  },

  // Edge positions for decorative accents
  edgePositions: {
    none: "",
    top: "before:content-[''] before:absolute before:top-0 before:left-0 before:right-0 before:h-[2px]",
    left: "before:content-[''] before:absolute before:top-0 before:left-0 before:bottom-0 before:w-[2px]",
    right: "before:content-[''] before:absolute before:top-0 before:right-0 before:bottom-0 before:w-[2px]",
    bottom: "before:content-[''] before:absolute before:bottom-0 before:left-0 before:right-0 before:h-[2px]",
  },

  // Configurable sizes for cards
  sizes: {
    card: {
      sm: "p-4 max-w-sm",
      md: "p-6 max-w-md",
      lg: "p-8 max-w-lg",
      xl: "p-10 max-w-xl",
    },
  },

  // Priority colors (matching our task system) - pastel variants
  priority: {
    critical: {
      background: "bg-red-100/80 dark:bg-destructive/20",
      text: "text-destructive",
      hover: "hover:bg-red-100 dark:hover:bg-destructive/30",
      shadow: "shadow-sm",
    },
    high: {
      background: "bg-orange-pastel/20 dark:bg-orange-pastel/15",
      text: "text-orange-700 dark:text-orange-300",
      hover: "hover:bg-orange-pastel/30 dark:hover:bg-orange-pastel/20",
      shadow: "shadow-sm",
    },
    medium: {
      background: "bg-blue-pastel/20 dark:bg-blue-pastel/15",
      text: "text-blue-700 dark:text-blue-300",
      hover: "hover:bg-blue-pastel/30 dark:hover:bg-blue-pastel/20",
      shadow: "shadow-sm",
    },
    low: {
      background: "bg-muted",
      text: "text-muted-foreground",
      hover: "hover:bg-muted/80",
      shadow: "shadow-sm",
    },
  },
};

// Card-specific glass styles with accent colors - Apple-inspired
export const glassCard = {
  // Base glass card - clean and minimal
  base: "relative rounded-xl overflow-hidden border transition-all duration-200",

  // Blur intensity levels - subtle glass effect
  blur: {
    none: "backdrop-blur-none",
    sm: "backdrop-blur-sm",
    md: "backdrop-blur-md",
    lg: "backdrop-blur-lg",
    xl: "backdrop-blur-xl",
    "2xl": "backdrop-blur-2xl",
    "3xl": "backdrop-blur-3xl",
  },

  // Glass transparency levels - theme-aware
  transparency: {
    clear: "bg-white/[0.02] dark:bg-white/[0.01]",
    light: "bg-white/[0.08] dark:bg-white/[0.05]",
    medium: "bg-white/[0.15] dark:bg-white/[0.08]",
    frosted: "bg-white/[0.40] dark:bg-black/[0.40]",
    solid: "bg-white/[0.90] dark:bg-black/[0.95]",
  },

  // Edge colors for decorative accents - pastel palette
  edgeColors: {
    purple: {
      solid: "bg-purple-pastel",
      gradient: "from-purple-pastel/30",
      border: "border-purple-pastel/30",
      bg: "bg-gradient-to-br from-purple-pastel/5 to-purple-pastel/2",
    },
    blue: {
      solid: "bg-blue-pastel",
      gradient: "from-blue-pastel/30",
      border: "border-blue-pastel/30",
      bg: "bg-gradient-to-br from-blue-pastel/5 to-blue-pastel/2",
    },
    green: {
      solid: "bg-green-pastel",
      gradient: "from-green-pastel/30",
      border: "border-green-pastel/30",
      bg: "bg-gradient-to-br from-green-pastel/5 to-green-pastel/2",
    },
    orange: {
      solid: "bg-orange-pastel",
      gradient: "from-orange-pastel/30",
      border: "border-orange-pastel/30",
      bg: "bg-gradient-to-br from-orange-pastel/5 to-orange-pastel/2",
    },
    pink: {
      solid: "bg-pink-pastel",
      gradient: "from-pink-pastel/30",
      border: "border-pink-pastel/30",
      bg: "bg-gradient-to-br from-pink-pastel/5 to-pink-pastel/2",
    },
    red: {
      solid: "bg-destructive",
      gradient: "from-destructive/30",
      border: "border-destructive/30",
      bg: "bg-gradient-to-br from-destructive/5 to-destructive/2",
    },
    teal: {
      solid: "bg-teal-pastel",
      gradient: "from-teal-pastel/30",
      border: "border-teal-pastel/30",
      bg: "bg-gradient-to-br from-teal-pastel/5 to-teal-pastel/2",
    },
  },

  // Colored glass tints - soft pastel backgrounds
  tints: {
    none: "",
    purple: {
      clear: "bg-purple-pastel/[0.02] dark:bg-purple-pastel/[0.03]",
      light: "bg-purple-pastel/[0.05] dark:bg-purple-pastel/[0.08]",
      medium: "bg-purple-pastel/[0.10] dark:bg-purple-pastel/[0.12]",
      frosted: "bg-purple-pastel/[0.15] dark:bg-purple-pastel/[0.20]",
      solid: "bg-purple-pastel/[0.25] dark:bg-purple-pastel/[0.30]",
    },
    blue: {
      clear: "bg-blue-pastel/[0.02] dark:bg-blue-pastel/[0.03]",
      light: "bg-blue-pastel/[0.05] dark:bg-blue-pastel/[0.08]",
      medium: "bg-blue-pastel/[0.10] dark:bg-blue-pastel/[0.12]",
      frosted: "bg-blue-pastel/[0.15] dark:bg-blue-pastel/[0.20]",
      solid: "bg-blue-pastel/[0.25] dark:bg-blue-pastel/[0.30]",
    },
    green: {
      clear: "bg-green-pastel/[0.02] dark:bg-green-pastel/[0.03]",
      light: "bg-green-pastel/[0.05] dark:bg-green-pastel/[0.08]",
      medium: "bg-green-pastel/[0.10] dark:bg-green-pastel/[0.12]",
      frosted: "bg-green-pastel/[0.15] dark:bg-green-pastel/[0.20]",
      solid: "bg-green-pastel/[0.25] dark:bg-green-pastel/[0.30]",
    },
    orange: {
      clear: "bg-orange-pastel/[0.02] dark:bg-orange-pastel/[0.03]",
      light: "bg-orange-pastel/[0.05] dark:bg-orange-pastel/[0.08]",
      medium: "bg-orange-pastel/[0.10] dark:bg-orange-pastel/[0.12]",
      frosted: "bg-orange-pastel/[0.15] dark:bg-orange-pastel/[0.20]",
      solid: "bg-orange-pastel/[0.25] dark:bg-orange-pastel/[0.30]",
    },
    pink: {
      clear: "bg-pink-pastel/[0.02] dark:bg-pink-pastel/[0.03]",
      light: "bg-pink-pastel/[0.05] dark:bg-pink-pastel/[0.08]",
      medium: "bg-pink-pastel/[0.10] dark:bg-pink-pastel/[0.12]",
      frosted: "bg-pink-pastel/[0.15] dark:bg-pink-pastel/[0.20]",
      solid: "bg-pink-pastel/[0.25] dark:bg-pink-pastel/[0.30]",
    },
    red: {
      clear: "bg-destructive/[0.02] dark:bg-destructive/[0.03]",
      light: "bg-destructive/[0.05] dark:bg-destructive/[0.08]",
      medium: "bg-destructive/[0.10] dark:bg-destructive/[0.12]",
      frosted: "bg-destructive/[0.15] dark:bg-destructive/[0.20]",
      solid: "bg-destructive/[0.25] dark:bg-destructive/[0.30]",
    },
    teal: {
      clear: "bg-teal-pastel/[0.02] dark:bg-teal-pastel/[0.03]",
      light: "bg-teal-pastel/[0.05] dark:bg-teal-pastel/[0.08]",
      medium: "bg-teal-pastel/[0.10] dark:bg-teal-pastel/[0.12]",
      frosted: "bg-teal-pastel/[0.15] dark:bg-teal-pastel/[0.20]",
      solid: "bg-teal-pastel/[0.25] dark:bg-teal-pastel/[0.30]",
    },
  },

  // Card variants with subtle shadows and borders
  variants: {
    none: {
      border: "border-border",
      shadow: "shadow-sm",
      hover: "hover:shadow-md hover:bg-white/[0.04] dark:hover:bg-white/[0.02]",
    },
    purple: {
      border: "border-purple-pastel/30 dark:border-purple-pastel/20",
      shadow: "shadow-sm ring-1 ring-purple-pastel/10",
      hover: "hover:shadow-md hover:ring-purple-pastel/20 hover:bg-purple-pastel/5",
    },
    blue: {
      border: "border-blue-pastel/30 dark:border-blue-pastel/20",
      shadow: "shadow-sm ring-1 ring-blue-pastel/10",
      hover: "hover:shadow-md hover:ring-blue-pastel/20 hover:bg-blue-pastel/5",
    },
    green: {
      border: "border-green-pastel/30 dark:border-green-pastel/20",
      shadow: "shadow-sm ring-1 ring-green-pastel/10",
      hover: "hover:shadow-md hover:ring-green-pastel/20 hover:bg-green-pastel/5",
    },
    orange: {
      border: "border-orange-pastel/30 dark:border-orange-pastel/20",
      shadow: "shadow-sm ring-1 ring-orange-pastel/10",
      hover: "hover:shadow-md hover:ring-orange-pastel/20 hover:bg-orange-pastel/5",
    },
    pink: {
      border: "border-pink-pastel/30 dark:border-pink-pastel/20",
      shadow: "shadow-sm ring-1 ring-pink-pastel/10",
      hover: "hover:shadow-md hover:ring-pink-pastel/20 hover:bg-pink-pastel/5",
    },
    red: {
      border: "border-destructive/30 dark:border-destructive/20",
      shadow: "shadow-sm ring-1 ring-destructive/10",
      hover: "hover:shadow-md hover:ring-destructive/20 hover:bg-destructive/5",
    },
    teal: {
      border: "border-teal-pastel/30 dark:border-teal-pastel/20",
      shadow: "shadow-sm ring-1 ring-teal-pastel/10",
      hover: "hover:shadow-md hover:ring-teal-pastel/20 hover:bg-teal-pastel/5",
    },
  },

  // Shadow size variants - simple, no glow
  shadows: {
    purple: {
      sm: "shadow-sm shadow-purple-pastel/5",
      md: "shadow-md shadow-purple-pastel/10",
      lg: "shadow-lg shadow-purple-pastel/15",
      xl: "shadow-xl shadow-purple-pastel/20",
    },
    blue: {
      sm: "shadow-sm shadow-blue-pastel/5",
      md: "shadow-md shadow-blue-pastel/10",
      lg: "shadow-lg shadow-blue-pastel/15",
      xl: "shadow-xl shadow-blue-pastel/20",
    },
    green: {
      sm: "shadow-sm shadow-green-pastel/5",
      md: "shadow-md shadow-green-pastel/10",
      lg: "shadow-lg shadow-green-pastel/15",
      xl: "shadow-xl shadow-green-pastel/20",
    },
    orange: {
      sm: "shadow-sm shadow-orange-pastel/5",
      md: "shadow-md shadow-orange-pastel/10",
      lg: "shadow-lg shadow-orange-pastel/15",
      xl: "shadow-xl shadow-orange-pastel/20",
    },
    pink: {
      sm: "shadow-sm shadow-pink-pastel/5",
      md: "shadow-md shadow-pink-pastel/10",
      lg: "shadow-lg shadow-pink-pastel/15",
      xl: "shadow-xl shadow-pink-pastel/20",
    },
    red: {
      sm: "shadow-sm shadow-destructive/5",
      md: "shadow-md shadow-destructive/10",
      lg: "shadow-lg shadow-destructive/15",
      xl: "shadow-xl shadow-destructive/20",
    },
    teal: {
      sm: "shadow-sm shadow-teal-pastel/5",
      md: "shadow-md shadow-teal-pastel/10",
      lg: "shadow-lg shadow-teal-pastel/15",
      xl: "shadow-xl shadow-teal-pastel/20",
    },
  },

  // Hover shadow enhancements
  hoverShadows: {
    purple: {
      sm: "hover:shadow-md hover:shadow-purple-pastel/10",
      md: "hover:shadow-lg hover:shadow-purple-pastel/15",
      lg: "hover:shadow-xl hover:shadow-purple-pastel/20",
      xl: "hover:shadow-2xl hover:shadow-purple-pastel/25",
    },
    blue: {
      sm: "hover:shadow-md hover:shadow-blue-pastel/10",
      md: "hover:shadow-lg hover:shadow-blue-pastel/15",
      lg: "hover:shadow-xl hover:shadow-blue-pastel/20",
      xl: "hover:shadow-2xl hover:shadow-blue-pastel/25",
    },
    green: {
      sm: "hover:shadow-md hover:shadow-green-pastel/10",
      md: "hover:shadow-lg hover:shadow-green-pastel/15",
      lg: "hover:shadow-xl hover:shadow-green-pastel/20",
      xl: "hover:shadow-2xl hover:shadow-green-pastel/25",
    },
    orange: {
      sm: "hover:shadow-md hover:shadow-orange-pastel/10",
      md: "hover:shadow-lg hover:shadow-orange-pastel/15",
      lg: "hover:shadow-xl hover:shadow-orange-pastel/20",
      xl: "hover:shadow-2xl hover:shadow-orange-pastel/25",
    },
    pink: {
      sm: "hover:shadow-md hover:shadow-pink-pastel/10",
      md: "hover:shadow-lg hover:shadow-pink-pastel/15",
      lg: "hover:shadow-xl hover:shadow-pink-pastel/20",
      xl: "hover:shadow-2xl hover:shadow-pink-pastel/25",
    },
    red: {
      sm: "hover:shadow-md hover:shadow-destructive/10",
      md: "hover:shadow-lg hover:shadow-destructive/15",
      lg: "hover:shadow-xl hover:shadow-destructive/20",
      xl: "hover:shadow-2xl hover:shadow-destructive/25",
    },
    teal: {
      sm: "hover:shadow-md hover:shadow-teal-pastel/10",
      md: "hover:shadow-lg hover:shadow-teal-pastel/15",
      lg: "hover:shadow-xl hover:shadow-teal-pastel/20",
      xl: "hover:shadow-2xl hover:shadow-teal-pastel/25",
    },
  },

  // Size variants
  sizes: {
    none: "p-0",
    sm: "p-4",
    md: "p-6",
    lg: "p-8",
    xl: "p-10",
  },

  // Edge-lit effects for cards - minimal, no glow
  edgeLit: {
    position: {
      none: "",
      top: "before:content-[''] before:absolute before:top-0 before:left-0 before:right-0 before:h-[2px] before:rounded-t-xl",
      left: "before:content-[''] before:absolute before:top-0 before:left-0 before:bottom-0 before:w-[2px] before:rounded-l-xl",
      right:
        "before:content-[''] before:absolute before:top-0 before:right-0 before:bottom-0 before:w-[2px] before:rounded-r-xl",
      bottom:
        "before:content-[''] before:absolute before:bottom-0 before:left-0 before:right-0 before:h-[2px] before:rounded-b-xl",
    },
    color: {
      purple: {
        line: "before:bg-purple-pastel dark:before:bg-purple-pastel/80",
        gradient: {
          horizontal:
            "before:bg-gradient-to-r before:from-transparent before:via-purple-pastel dark:before:via-purple-pastel/80 before:to-transparent",
          vertical:
            "before:bg-gradient-to-b before:from-transparent before:via-purple-pastel dark:before:via-purple-pastel/80 before:to-transparent",
        },
      },
      blue: {
        line: "before:bg-blue-pastel dark:before:bg-blue-pastel/80",
        gradient: {
          horizontal:
            "before:bg-gradient-to-r before:from-transparent before:via-blue-pastel dark:before:via-blue-pastel/80 before:to-transparent",
          vertical:
            "before:bg-gradient-to-b before:from-transparent before:via-blue-pastel dark:before:via-blue-pastel/80 before:to-transparent",
        },
      },
      green: {
        line: "before:bg-green-pastel dark:before:bg-green-pastel/80",
        gradient: {
          horizontal:
            "before:bg-gradient-to-r before:from-transparent before:via-green-pastel dark:before:via-green-pastel/80 before:to-transparent",
          vertical:
            "before:bg-gradient-to-b before:from-transparent before:via-green-pastel dark:before:via-green-pastel/80 before:to-transparent",
        },
      },
      orange: {
        line: "before:bg-orange-pastel dark:before:bg-orange-pastel/80",
        gradient: {
          horizontal:
            "before:bg-gradient-to-r before:from-transparent before:via-orange-pastel dark:before:via-orange-pastel/80 before:to-transparent",
          vertical:
            "before:bg-gradient-to-b before:from-transparent before:via-orange-pastel dark:before:via-orange-pastel/80 before:to-transparent",
        },
      },
      pink: {
        line: "before:bg-pink-pastel dark:before:bg-pink-pastel/80",
        gradient: {
          horizontal:
            "before:bg-gradient-to-r before:from-transparent before:via-pink-pastel dark:before:via-pink-pastel/80 before:to-transparent",
          vertical:
            "before:bg-gradient-to-b before:from-transparent before:via-pink-pastel dark:before:via-pink-pastel/80 before:to-transparent",
        },
      },
      red: {
        line: "before:bg-destructive dark:before:bg-destructive/80",
        gradient: {
          horizontal:
            "before:bg-gradient-to-r before:from-transparent before:via-destructive dark:before:via-destructive/80 before:to-transparent",
          vertical:
            "before:bg-gradient-to-b before:from-transparent before:via-destructive dark:before:via-destructive/80 before:to-transparent",
        },
      },
      teal: {
        line: "before:bg-teal-pastel dark:before:bg-teal-pastel/80",
        gradient: {
          horizontal:
            "before:bg-gradient-to-r before:from-transparent before:via-teal-pastel dark:before:via-teal-pastel/80 before:to-transparent",
          vertical:
            "before:bg-gradient-to-b before:from-transparent before:via-teal-pastel dark:before:via-teal-pastel/80 before:to-transparent",
        },
      },
    },
  },
};

// Compound styles for common patterns
export const compoundStyles = {
  // Standard interactive element (buttons, menu items, etc.)
  interactiveElement: `
    ${glassmorphism.interactive.base}
    ${glassmorphism.interactive.hover}
    ${glassmorphism.interactive.disabled}
  `,

  // Floating panels (dropdowns, popovers, tooltips)
  floatingPanel: `
    ${glassmorphism.background.strong}
    ${glassmorphism.border.default}
    ${glassmorphism.shadow.lg}
    ${glassmorphism.animation.fadeIn}
    ${glassmorphism.animation.slideIn}
  `,

  // Form controls (inputs, selects, etc.)
  formControl: `
    ${glassmorphism.background.subtle}
    ${glassmorphism.border.default}
    ${glassmorphism.border.hover}
    ${glassmorphism.border.focus}
    ${glassmorphism.interactive.base}
    ${glassmorphism.interactive.disabled}
  `,

  // Cards - use glassCard instead
  card: `
    ${glassmorphism.background.card}
    ${glassmorphism.border.default}
    ${glassmorphism.shadow.md}
  `,
};

// Utility function to combine classes
export function cn(...classes: (string | undefined | false)[]): string {
  return classes.filter(Boolean).join(" ");
}
