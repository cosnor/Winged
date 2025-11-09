export const theme: any = {
  colors: {
    // Primary colors from gaming aesthetic
    primary: "#d97706", // amber
    danger: "#dc2626", // red
    background: "#fefce8", // cream

    // Extended color palette
    foreground: "#374151", // dark gray
    card: "#ffffff",
    cardForeground: "#374151",

    // Gaming accent colors
    accent: "#dc2626", // bright red
    accentForeground: "#ffffff",
    secondary: "#dc4e26ff",
    secondaryForeground: "#ffffff",

    // Utility colors
    muted: "#fefce8",
    mutedForeground: "#6b7280",
    border: "#d97706",
    input: "#ffffff",
    ring: "rgba(217, 119, 6, 0.5)",

    // Chart colors for data visualization
    chart: {
      1: "#64b5f6", // blue
      2: "#81c784", // green
      3: "#ffb74d", // orange
      4: "#ba68c8", // purple
      5: "#ff8a65", // coral
    },

    // Rarity colors for collectibles
    rarity: {
      common: "#9ca3af", // gray
      rare: "#3b82f6", // blue
      epic: "#8b5cf6", // purple
      legendary: "#f59e0b", // amber
      mythic: "#ef4444", // red
    },

    // Dark mode variants
    dark: {
      background: "#1f2937",
      foreground: "#f9fafb",
      card: "#374151",
      primary: "#fbbf24",
      secondary: "#ef4444",
      border: "#fbbf24",
    },
  },

  text: {
    // Typography scale
    title: {
      fontSize: 24,
      fontWeight: "bold",
      letterSpacing: "0.05em",
      textTransform: "uppercase" as const,
    },
    subtitle: {
      fontSize: 20,
      fontWeight: "bold",
      letterSpacing: "0.025em",
    },
    body: {
      fontSize: 16,
      fontWeight: "normal",
      lineHeight: 1.5,
    },
    small: {
      fontSize: 14,
      color: "#6b7280",
      lineHeight: 1.4,
    },
    caption: {
      fontSize: 12,
      color: "#9ca3af",
      fontWeight: "medium",
    },

    // Gaming specific text styles
    pixelTitle: {
      fontSize: 28,
      fontWeight: "bold",
      letterSpacing: "0.1em",
      textTransform: "uppercase" as const,
      textShadow: "2px 2px 0 #b45309",
    },
    glowText: {
      fontSize: 18,
      fontWeight: "bold",
      textShadow: "0 0 5px currentColor, 0 0 10px currentColor",
    },
  },

  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
  },

  radius: {
    sm: 4,
    md: 6,
    lg: 8,
    xl: 12,
    pixel: 2, // For pixel art aesthetic
  },

  shadows: {
    pixel: "2px 2px 0 0 #b45309, 4px 4px 0 0 #92400e",
    pixelHover: "1px 1px 0 0 #b45309, 2px 2px 0 0 #92400e",
    card: "4px 4px 0 0 #b45309, 8px 8px 0 0 #92400e",
    glow: "0 0 5px #d97706, 0 0 10px #d97706, 0 0 15px #d97706",
  },

  animations: {
    pixelPulse: "pixelPulse 2s infinite",
    bounce: "bounce 1s infinite",
    fadeIn: "fadeIn 0.3s ease-in-out",
  },

  // Utility functions for easy usage
  utils: {
    getTextStyle: (variant: keyof typeof theme.text) => theme.text[variant],
    getRarityColor: (rarity: keyof typeof theme.colors.rarity) => theme.colors.rarity[rarity],
    getChartColor: (index: keyof typeof theme.colors.chart) => theme.colors.chart[index],
  },
} as const
